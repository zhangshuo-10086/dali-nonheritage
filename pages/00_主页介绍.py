import streamlit as st
import base64
from PIL import Image
import os
import io

# =========❗❗删掉 st.set_page_config！子页面禁止写这个=========

# 获取仓库根目录路径（pages子页面专用写法）
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 图片都放在仓库【根目录】，从root_dir拼接
img_tie_path = os.path.join(root_dir, "nv (1).png")    #扎染
img_costume_path = os.path.join(root_dir, "nv (2).png") #白族服饰

# 图片转base64函数
def img_to_base64(img_path):
    img = Image.open(img_path)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"

img_tie = img_to_base64(img_tie_path)
img_costume = img_to_base64(img_costume_path)

html_code = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>大理非遗文化欢迎你</title>
<script src="https://modao.cc/agent-py/static/source/js/tailwindcss.js"></script>
<script src="https://modao.cc/agent-py/static/source/js/iconify-icon.min.js"></script>
<style>
    html {{
      scroll-behavior: smooth;
    }}
    body {{
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans SC", system-ui, sans-serif;
    }}
    .dye-pattern {{
      background-image:
        radial-gradient(circle at 14% 24%, rgba(255, 255, 255, 0.18), transparent 40%),
        radial-gradient(circle at 78% 16%, rgba(130, 195, 255, 0.24), transparent 44%),
        radial-gradient(circle at 52% 88%, rgba(255, 255, 255, 0.12), transparent 42%),
        radial-gradient(circle at 94% 70%, rgba(130, 195, 255, 0.18), transparent 38%);
    }}
    .dye-stripe {{
      background-image: repeating-linear-gradient(135deg,
          rgba(37, 99, 168, 0.9) 0 8px,
          rgba(18, 48, 92, 0.9) 8px 16px,
          rgba(201, 162, 39, 0.85) 16px 20px,
          rgba(192, 54, 44, 0.85) 20px 28px);
    }}
    .btn-wrap{{
        display:flex;
        gap:1rem;
        flex-wrap:wrap;
        margin-top:1.5rem;
    }}
    .page-btn{{
        padding:0.8rem 1.6rem;
        border-radius:0.6rem;
        text-decoration:none;
        font-weight:600;
        font-size:1rem;
        display:inline-flex;
        align-items:center;
        gap:0.4rem;
    }}
    .btn-primary{{
        background-color:#ffffff;
        color:#12305c;
    }}
    .btn-ghost{{
        border:1px solid rgba(255,255,255,0.35);
        background-color:rgba(255,255,255,0.1);
        color:#ffffff;
    }}
    /*图片容器，固定高度，渐变背景，图片完整显示，左右卡片等高平齐 */
    .img-box{{
        height:440px;
        background:linear-gradient(to bottom right,#12305c,#2563a8,#8ab8e0);
        border-radius:12px;
        overflow:hidden;
        position:relative;
    }}
    .img-box img{{
        width:100%;
        height:100%;
        object-fit:contain;
        object-position:center;
        display:block;
    }}
    @media(max-width:768px){{
        .img-box{{
            height:320px;
        }}
    }}
    @media (prefers-reduced-motion: reduce) {{
    html {{
        scroll-behavior: auto;
    }}
    }}
  </style>
</head>
<body class="min-h-screen bg-[#edf3fa] text-slate-800 antialiased">
<!-- 顶部标题区 -->
<header class="relative overflow-hidden bg-[#12305c] text-white">
<div class="absolute inset-0 dye-pattern"></div>
<div class="absolute -right-16 -top-20 h-64 w-64 rounded-full border border-white/10"></div>
<div class="absolute -right-4 top-6 h-40 w-40 rounded-full border border-white/10"></div>
<div class="relative mx-auto max-w-7xl px-6 py-9 md:py-12">
<div class="flex flex-wrap items-center gap-2 text-xs text-sky-100/90">
<span class="inline-flex items-center gap-1 rounded-full bg-white/12 px-3 py-1 ring-1 ring-white/20">
<iconify-icon class="text-sm" icon="mdi:map-marker-outline"></iconify-icon>
            云南 · 大理
        </span>
<span class="inline-flex items-center gap-1 rounded-full bg-white/12 px-3 py-1 ring-1 ring-white/20">
<iconify-icon class="text-sm" icon="mdi:school-outline"></iconify-icon>
            综合实践活动 · 非遗主题课程
        </span>
</div>
<h1 class="mt-5 text-3xl font-bold leading-tight tracking-wide md:text-[2.75rem]">
        🏔️ 基于AI的大理非遗文化数学元素挖掘与探究
      </h1>
<p class="mt-3 max-w-3xl text-sm leading-relaxed text-sky-100/90 md:text-base">
        苍山十九峰下、洱海岸边，白族人把一朵山茶花扎进布里，把一段记忆绣在衣上。
        本页展示白族扎染纹样与传统服饰，纹样中藏着对称、分形等丰富数学规律，让我们一起探究！
      </p>
<div class="btn-wrap">
<!-- ⚠️html内部a标签跳转streamlit页面无效，这里把按钮只做样式，去掉href -->
<button class="page-btn btn-primary" onclick="window.parent.postMessage('goto_analyze','*')">
<iconify-icon icon="mdi:magnify"></iconify-icon>
进入挖掘与探究
</button>
<button class="page-btn btn-ghost" onclick="window.parent.postMessage('goto_guide','*')">
<iconify-icon icon="mdi:book-open-page-variant-outline"></iconify-icon>
查看操作方法
</button>
</div>
<div class="mt-4 flex flex-wrap items-center gap-3">
<span class="inline-flex items-center gap-2 rounded-lg bg-white/12 px-4 py-2 text-xs font-medium text-sky-50 ring-1 ring-white/20">
<iconify-icon class="text-base" icon="mdi:image-multiple-outline"></iconify-icon>
            观察素材 · 2 张
        </span>
<span class="text-xs text-sky-100/70">先观察，再分析纹样中的数学特征</span>
</div>
</div>
<div class="dye-stripe relative h-1.5 w-full"></div>
</header>
<!-- 主体：观察素材展示 -->
<main class="mx-auto max-w-7xl px-6 py-8 md:py-10">
<section class="mx-auto w-full max-w-5xl">
<div class="flex items-center justify-between">
<h2 class="flex items-center gap-2 text-base font-semibold text-[#12305c]">
<iconify-icon class="text-lg" icon="mdi:image-multiple-outline"></iconify-icon>
            非遗观察素材
        </h2>
<span class="text-xs text-slate-500">共 2 张 · 白族扎染 & 白族传统服饰</span>
</div>
<div class="mt-5 grid grid-cols-1 gap-6 md:grid-cols-2">
<!-- 图1：白族扎染 -->
<figure class="rounded-2xl bg-white p-3 ring-1 ring-slate-200/80 shadow-[0_14px_34px_-24px_rgba(18,48,92,0.7)] border-2 border-[#d7e4f3]">
<div class="img-box relative">
<img alt="白族扎染纹样" src="{img_tie}" title="白族扎染纹样"/>
<span class="absolute left-3 top-3 inline-flex items-center gap-1 rounded-full bg-white/92 px-2.5 py-1 text-[11px] font-semibold text-[#12305c] shadow-sm">
<iconify-icon class="text-sm" icon="mdi:numeric-1-circle"></iconify-icon>
                    图 1
                  </span>
<span class="absolute bottom-3 left-3 rounded-md bg-[#12305c]/80 px-2 py-1 text-[11px] font-medium text-white backdrop-blur-sm">
                    白族扎染 · 蓝白对称纹样
                  </span>
</div>
<figcaption class="px-1 pb-1 pt-3">
<h3 class="text-sm font-semibold text-slate-900 md:text-base">板蓝根染制 · 扎染团花</h3>
<p class="mt-1.5 text-[13px] leading-relaxed text-slate-600">
                    中心团花呈现高度中心旋转对称，层层花瓣重复排列，冰裂纹是扎染特有的分形纹理。
                    思考：这个纹样有几条对称轴？冰裂纹为什么具有自相似的分形特点？
                  </p>
<div class="mt-3 flex flex-wrap gap-1.5 text-[11px] text-[#12305c]">
<span class="rounded-full bg-sky-50 px-2 py-0.5 ring-1 ring-sky-100">中心对称</span>
<span class="rounded-full bg-sky-50 px-2 py-0.5 ring-1 ring-sky-100">旋转对称</span>
<span class="rounded-full bg-slate-100 px-2 py-0.5 ring-1 ring-slate-200">靛蓝冰裂纹</span>
<span class="rounded-full bg-slate-100 px-2 py-0.5 ring-1 ring-slate-200">分形纹样</span>
</div>
</figcaption>
</figure>
<!-- 图2：白族服饰 -->
<figure class="rounded-2xl bg-white p-3 ring-1 ring-slate-200/80 shadow-[0_14px_34px_-24px_rgba(18,48,92,0.7)] border-2 border-[#d7e4f3]">
<div class="img-box relative">
<img alt="白族传统服饰" src="{img_costume}" title="白族传统服饰"/>
<span class="absolute left-3 top-3 inline-flex items-center gap-1 rounded-full bg-white/92 px-2.5 py-1 text-[11px] font-semibold text-[#12305c] shadow-sm">
<iconify-icon class="text-sm" icon="mdi:numeric-2-circle"></iconify-icon>
                    图 2
                  </span>
<span class="absolute bottom-3 left-3 rounded-md bg-[#12305c]/80 px-2 py-1 text-[11px] font-medium text-white backdrop-blur-sm">
                    白族服饰 · 头饰与刺绣
                  </span>
</div>
<figcaption class="px-1 pb-1 pt-3">
<h3 class="text-sm font-semibold text-slate-900 md:text-base">洱海之畔的白族盛装</h3>
<p class="mt-1.5 text-[13px] leading-relaxed text-slate-600">
                    白色长衫搭配黑色坎肩，衣身、袖口、头饰布满连续重复的刺绣纹样，大量运用轴对称设计。
                    思考：服饰刺绣纹样存在哪些重复单元？刺绣花边属于平移对称吗？
                  </p>
<div class="mt-3 flex flex-wrap gap-1.5 text-[11px] text-[#12305c]">
<span class="rounded-full bg-sky-50 px-2 py-0.5 ring-1 ring-sky-100">轴对称</span>
<span class="rounded-full bg-red-50 px-2 py-0.5 text-[#c0362c] ring-1 ring-red-100">刺绣纹样</span>
<span class="rounded-full bg-slate-100 px-2 py-0.5 ring-1 ring-slate-200">银饰头箍</span>
<span class="rounded-full bg-amber-50 px-2 py-0.5 text-amber-700 ring-1 ring-amber-100">平移重复</span>
</div>
</figcaption>
</figure>
</div>
</section>
</main>
<footer class="mt-4 border-t border-slate-200 bg-white/70">
<div class="mx-auto flex max-w-7xl flex-col gap-2 px-6 py-6 text-xs text-slate-500 md:flex-row md:items-center md:justify-between">
<p class="flex items-center gap-1.5">
<iconify-icon class="text-base text-[#2563a8]" icon="mdi:feather"></iconify-icon>
        大理非遗文化探究平台 · 白族扎染与服饰主题
      </p>
<p>图片来源：白族扎染纹样、白族传统服饰｜整理时间：2026 年 10 月</p>
</div>
</footer>
<script>
    document.addEventListener("DOMContentLoaded", function () {{
    }});
</script>
</body>
</html>
'''

st.components.v1.html(html_code, height=1480, scrolling=True)

# ✅页面跳转，Streamlit原生页面链接（iframe按钮不能跳转，页面下方补充原生跳转按钮）
st.divider()
st.subheader("页面跳转")
st.page_link("app.py", label="🔍 进入纹样AI分析页面", icon="🔍")
st.page_link("pages/01_操作指南.py", label="📖 查看操作指南", icon="📋")
