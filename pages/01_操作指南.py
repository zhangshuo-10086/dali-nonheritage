import streamlit as st
from PIL import Image
import os
import requests

st.set_page_config(
    page_title="纹样分析｜大理非遗文化数学挖掘平台",
    layout="wide",
    page_icon="🔍"
)

# ============后端还没部署，这里先占位 =================
RENDER_API_BASE_URL = ""
API_ANALYZE = f"{RENDER_API_BASE_URL}/api/analyze"
# =====================================================

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
img_nv3 = os.path.join(os.path.dirname(CUR_DIR), "nv3.png")
img_nv4 = os.path.join(os.path.dirname(CUR_DIR), "nv4.png")
img_nv5 = os.path.join(os.path.dirname(CUR_DIR), "nv5.png")


st.title("🔍 进入挖掘与探究 — 纹样AI分析")
st.divider()

st.subheader("📝 操作示意参考图")
col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists(img_nv3):
        st.image(Image.open(img_nv3), caption="① 上传非遗纹样图片", use_container_width=True)
    else:
        st.warning("⚠️ 未找到 nv3.png")

with col2:
    if os.path.exists(img_nv4):
        st.image(Image.open(img_nv4), caption="② 选择非遗类别", use_container_width=True)
    else:
        st.warning("⚠️ 未找到 nv4.png")

with col3:
    if os.path.exists(img_nv5):
        st.image(Image.open(img_nv5), caption="③ SAM抠图可选设置", use_container_width=True)
    else:
        st.warning("⚠️ 未找到 nv5.png")


st.divider()
st.subheader("📤 上传非遗纹样图片")
uploaded_file = st.file_uploader("请上传图片", type=["png", "jpg", "jpeg"], help="单张最大200MB")

category = st.selectbox(
    "选择非遗类别",
    ["白族扎染", "甲马版画", "剑川木雕", "银器", "其他"]
)

source_text = st.text_input("标注图片来源", placeholder="实地调研 / 网络素材 / 博物馆馆藏")
use_sam = st.checkbox("【可选】启用SAM AI抠图（后端未部署，暂不可用）", value=False, disabled=True)

st.divider()

result_data = None
if uploaded_file is not None:
    st.info("✅ 文件已接收（后端尚未部署，暂无法执行分析）")
    st.image(uploaded_file, caption="待分析图片", use_container_width=True)

    if st.button("🚀 提交分析（后端未部署，暂不可用）", type="primary", disabled=True):
        st.warning("后端API还未部署到Render，完成后端部署后填入API地址才可使用！")


st.divider()
st.subheader("🔙 页面跳转")
st.page_link("pages/00_主页介绍.py", label="📷 返回非遗素材首页", icon="🏔️")
st.page_link("pages/01_操作指南.py", label="📖 查看完整操作指南", icon="📋")
