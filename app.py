import streamlit as st
import requests
import base64
from PIL import Image
import io
import os

# 页面基础配置
st.set_page_config(
    page_title="大理非遗文化数学挖掘平台",
    layout="wide",
    page_icon="🏔️"
)

# 读取本地背景图 tp.png，与app.py放在同一文件夹
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(CUR_DIR, "tp.jpg")

# 打印路径到终端，调试用！看程序找的是哪个位置
print(f"正在寻找背景图片路径：{bg_path}")
print(f"该路径是否存在：{os.path.exists(bg_path)}")

try:
    hero_img = Image.open(bg_path)
    # 修改参数 use_container_width
    st.image(hero_img, use_container_width=True, caption="大理｜非遗文化数字化探究平台")
except FileNotFoundError:
    st.warning(f"⚠️未找到背景图片 tp.png，查找路径：{bg_path}。请把tp.png放到frontend文件夹，和app.py放在一起")

# 标题与简介
st.title("🏔️ 基于AI的大理非遗文化数学元素挖掘与探究")
st.markdown("""
<div style="color:#444; font-size:16px;">
智慧教育演示平台｜前后端分离架构｜AI图像识别，提取纹样对称、分形等数学特征，输出可解释证据链报告
</div>
""", unsafe_allow_html=True)
st.divider()

# 侧边栏
with st.sidebar:
    st.header("⚙️ 参数配置")
    upload_file = st.file_uploader("上传非遗纹样图片", type=["jpg","png","jpeg"])
    category = st.selectbox("非遗类别",["白族扎染","甲马版画","剑川木雕","银器","其他"])
    source_text = st.text_input("图片来源(调研/网络/博物馆)","")
    use_sam = st.checkbox("启用SAM AI抠图（需模型文件）",False)
    st.divider()
    st.info("后端接口地址：http://127.0.0.1:8000，请确保后端服务已启动")

API_URL = "http://127.0.0.1:8000"

if upload_file is not None:
    with st.spinner("🔍后端AI分析中，请稍候……"):
        resp = requests.post(
            f"{API_URL}/api/v1/pattern/analyze",
            files={"file":upload_file},
            params={"use_sam":use_sam,"category":category,"source":source_text}
        )
    result = resp.json()
    if result["code"]!=200:
        st.error("❌接口调用失败！请检查后端是否启动")
    else:
        data = result["data"]
        def b64_to_img(b64_str):
            return Image.open(io.BytesIO(base64.b64decode(b64_str)))
        img_ori = b64_to_img(data["img_original_b64"])
        img_clean = b64_to_img(data["img_clean_b64"])
        img_edge = b64_to_img(data["img_edge_b64"])
        st.subheader("🖼️ 图像预处理结果")
        c1,c2,c3 = st.columns(3)
        with c1:
            st.image(img_ori,caption="原图", use_container_width=True)
        with c2:
            st.image(img_clean,caption="纹样抠图处理图", use_container_width=True)
        with c3:
            st.image(img_edge,caption="边缘提取图", use_container_width=True)
        st.divider()
        st.subheader("📐数学量化指标")
        mf = data["math_feature"]
        cc1,cc2,cc3,cc4 = st.columns(4)
        cc1.metric("垂直对称",f'{mf["vertical_sym"]}/100')
        cc2.metric("水平对称",f'{mf["horizontal_sym"]}/100')
        cc3.metric("180°旋转对称",f'{mf["rotate180_sym"]}/100')
        cc4.metric("分形维D",round(mf["fractal_D"],3))
        st.divider()
        st.subheader("🔍证据链可解释报告（项目创新点）")
        ev_list = data["evidence_chain"]
        if len(ev_list)==0:
            st.info("未检测到显著数学特征，可能为自然随机纹理，例如扎染冰裂纹。")
        for ev in ev_list:
            st.markdown(f"""
> **特征：{ev['feature']}｜得分：{ev['score']}**
> - 判断依据：{ev['evidence']}
> - 文化解读：{ev['culture_note']}
""")
        st.divider()
        st.download_button(
            label="📥导出文本报告",
            data=str(data),
            file_name="analysis_report.txt"
        )
else:
    st.info("👈 请在左侧侧边栏上传非遗纹样图片开始分析")
