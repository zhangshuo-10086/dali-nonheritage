from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os
import csv
import json
import uuid
import logging

from core.symmetry import calc_vertical_symmetry, calc_horizontal_symmetry, calc_rotate180_symmetry
from core.fractal import box_counting_fractal_dim
from core.report_gen import build_evidence_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="大理非遗文化数学元素挖掘后端")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw_images")
DATA_PROC = os.path.join(BASE_DIR, "data", "processed")
META_CSV = os.path.join(BASE_DIR, "data", "meta.csv")
RULE_PATH = os.path.join(BASE_DIR, "knowledge", "rule_base.json")

os.makedirs(DATA_RAW, exist_ok=True)
os.makedirs(DATA_PROC, exist_ok=True)

if not os.path.exists(META_CSV):
    with open(META_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["img_id", "filename", "category", "source", "authorize", "save_path"])

try:
    with open(RULE_PATH, "r", encoding="utf-8") as f:
        RULES = json.load(f)
except Exception as e:
    logger.error(f"加载rule_base.json失败:{e}")
    RULES = {}

SAM_AVAILABLE = False
try:
    from segment_anything import sam_model_registry, SamPredictor
    SAM_AVAILABLE = True
except Exception:
    logger.warning("segment‑anything未安装，SAM抠图功能不可用")


def img2base64_jpeg(img_np, quality=70):
    img_pil = Image.fromarray(img_np)
    buf = io.BytesIO()
    img_pil.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def img2base64_png(img_np):
    img_pil = Image.fromarray(img_np)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def limit_image_max_edge(pil_img: Image.Image, max_edge=1200) -> Image.Image:
    """限制图片最大长边，保护内存，防止Replit OOM"""
    w, h = pil_img.size
    if max(w, h) <= max_edge:
        return pil_img
    scale = max_edge / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": exc.detail, "data": None}
    )


@app.post("/api/v1/image/upload")
async def upload_image(
    file: UploadFile = File(...),
    category: str = "未知类别",
    source: str = "",
    authorize: str = "未授权"
):
    max_size = 10 * 1024 * 1024
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail="文件不能超过10MB")

    img_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[-1]
    save_name = img_id + ext
    save_path = os.path.join(DATA_RAW, save_name)

    try:
        with open(save_path, "wb") as fw:
            fw.write(content)
        with open(META_CSV, "a", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow([img_id, file.filename, category, source, authorize, save_path])
        logger.info(f"upload成功 img_id={img_id}, filename={file.filename}")
    except Exception as e:
        logger.exception("图片保存失败")
        raise HTTPException(status_code=500, detail="图片存储失败")
    return {"code": 200, "msg": "ok", "data": {"img_id": img_id, "save_name": save_name}}


@app.post("/api/v1/pattern/analyze")
async def analyze_pattern(
    file: UploadFile = File(...),
    use_sam: bool = False,
    category: str = "未知类别",
    source: str = ""
):
    logger.info(f"analyze_pattern 请求, category={category}, use_sam={use_sam}")
    max_size = 10 * 1024 * 1024
    img_bytes = await file.read()
    if len(img_bytes) > max_size:
        raise HTTPException(status_code=413, detail="文件不能超过10MB")

    try:
        img_pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_pil = limit_image_max_edge(img_pil, max_edge=1200)
    except Exception as e:
        logger.exception("图片解析失败")
        raise HTTPException(status_code=400, detail="不是合法图片文件")

    img_rgb = np.array(img_pil)
    img_rgb_clean = img_rgb

    sam_weight_path = os.path.join(BASE_DIR, "sam_vit_b_01ec64.pth")
    if use_sam and SAM_AVAILABLE and os.path.exists(sam_weight_path):
        try:
            sam = sam_model_registry["vit_b"](checkpoint=sam_weight_path)
            predictor = SamPredictor(sam)
            h, w = img_rgb.shape[:2]
            predictor.set_image(img_rgb)
            pts = np.array([[w // 2, h // 2]])
            lab = np.array([1])
            masks, _, _ = predictor.predict(point_coords=pts, point_labels=lab, multimask_output=False)
            mask = masks[0].astype(np.uint8) * 255
            img_rgb_clean = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)
        except Exception as e:
            logger.warning(f"SAM抠图执行失败:{e}")
    elif use_sam:
        logger.info("use_sam=True，但缺少模型权重，跳过SAM抠图")

    img_gray = cv2.cvtColor(img_rgb_clean, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    edge = cv2.Canny(blur, 50, 150)
    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)

    sym_v = calc_vertical_symmetry(img_gray)
    sym_h = calc_horizontal_symmetry(img_gray)
    sym_r = calc_rotate180_symmetry(img_gray)
    fractal_D = box_counting_fractal_dim(binary)

    meta_info = {"category": category, "source": source}
    evidence_report = build_evidence_report(sym_v, sym_h, sym_r, fractal_D, meta_info)

    res_data = {
        "math_feature": {
            "vertical_sym": sym_v,
            "horizontal_sym": sym_h,
            "rotate180_sym": sym_r,
            "fractal_D": fractal_D
        },
        "evidence_chain": evidence_report["evidence_chain"],
        "img_original_b64": img2base64_jpeg(img_rgb),
        "img_clean_b64": img2base64_jpeg(img_rgb_clean),
        "img_edge_b64": img2base64_png(edge)
    }
    logger.info(f"分析完成, v={sym_v},h={sym_h},r={sym_r},D={fractal_D}")
    return {"code": 200, "msg": "ok", "data": res_data}


@app.get("/api/v1/rule/culture")
def get_culture_rule():
    return {"code": 200, "msg": "ok", "data": RULES}


@app.get("/")
def index():
    return {"code": 200, "msg": "大理非遗数学挖掘后端服务，访问 /docs 调试接口", "data": None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
