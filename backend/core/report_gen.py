# core/report_gen.py
def build_evidence_report(sym_v, sym_h, sym_r, fractal_D, img_meta:dict):
    evidence_list = []
    if sym_v > 80:
        evidence_list.append({
            "feature":"垂直轴对称",
            "score": sym_v,
            "evidence":"图像左右像素相似度高于80分",
            "culture_note":"白族甲马版画、扎染边框纹样常出现垂直轴对称"
        })
    if sym_h >80:
        evidence_list.append({
            "feature":"水平轴对称",
            "score": sym_h,
            "evidence":"图像上下像素相似度高于80分",
            "culture_note":"剑川木雕、白族照壁彩绘大量使用水平轴对称"
        })
    if sym_r >80:
        evidence_list.append({
            "feature":"180°旋转对称",
            "score": sym_r,
            "evidence":"图像旋转180°后和原图高度相似",
            "culture_note":"部分银器、甲马纹样具备旋转对称特征"
        })
    if 1.3 < fractal_D <1.8:
        evidence_list.append({
            "feature":"类分形纹理",
            "score": fractal_D,
            "evidence":"盒计数分形维处于1.3‑1.8区间",
            "culture_note":"典型白族扎染冰裂纹，手工工艺自然形成自相似纹理"
        })
    report = {
        "image_meta": img_meta,
        "evidence_chain": evidence_list
    }
    return report
