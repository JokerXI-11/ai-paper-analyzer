"""
AI 论文分析助手 - Streamlit Web 界面

启动方式:
    streamlit run app.py
"""

import streamlit as st
import os
import tempfile
from analyzer import PaperAnalyzer
from config import MODEL_CONFIGS
from pdf_parser import get_pdf_metadata

st.set_page_config(
    page_title="AI 论文分析助手",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI 论文分析助手")
st.markdown("基于 GPT / Claude / DeepSeek 大语言模型的学术论文智能分析工具")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")

    # 模型选择
    available_models = [m for m in MODEL_CONFIGS if MODEL_CONFIGS[m].get("api_key")]
    if not available_models:
        available_models = list(MODEL_CONFIGS.keys())

    model = st.selectbox(
        "选择模型",
        options=list(MODEL_CONFIGS.keys()),
        index=0,
        help="选择用于分析的 AI 模型",
    )

    st.divider()

    # 分析模式
    mode = st.radio(
        "分析模式",
        options=["完整分析", "仅摘要", "仅方法", "仅创新点", "仅关键词"],
        index=0,
    )

    mode_map = {
        "完整分析": "full",
        "仅摘要": "summary",
        "仅方法": "methods",
        "仅创新点": "innovations",
        "仅关键词": "keywords",
    }

    st.divider()

    # 使用说明
    st.markdown("""
    ### 使用说明
    1. 上传论文 PDF 文件
    2. 选择分析模式和模型
    3. 点击「开始分析」
    4. 查看结构化分析报告

    ### 支持功能
    - 📝 论文摘要生成
    - 🔬 研究方法提取
    - 💡 创新点识别
    - 🏷️ 关键词提取
    """)

# 文件上传区域
uploaded_file = st.file_uploader(
    "上传论文 PDF",
    type=["pdf"],
    help="支持中英文 PDF 论文",
)

if uploaded_file:
    # 保存上传文件到临时目录
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # 显示文件信息
    try:
        metadata = get_pdf_metadata(tmp_path)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("页数", metadata["total_pages"])
        with col2:
            st.metric("标题", metadata.get("title", "未知")[:30] + "..." if len(metadata.get("title", "")) > 30 else metadata.get("title", "未知"))
        with col3:
            st.metric("作者", metadata.get("author", "未知"))
    except Exception:
        st.info("已上传文件，点击下方按钮开始分析")

    # 分析按钮
    if st.button("🚀 开始分析", type="primary", use_container_width=True):
        api_mode = mode_map[mode]

        with st.spinner(f"正在使用 {model} 进行分析..."):
            try:
                analyzer = PaperAnalyzer(model_name=model)
                report = analyzer.run_pipeline(tmp_path, mode=api_mode)

                # 显示结果
                st.success("✅ 分析完成！")

                # 使用 markdown 展示报告
                with st.expander("📊 查看完整分析报告", expanded=True):
                    st.markdown(report)

                # 下载按钮
                st.download_button(
                    label="📥 下载分析报告 (Markdown)",
                    data=report,
                    file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_分析报告.md",
                    mime="text/markdown",
                )

            except Exception as e:
                st.error(f"分析过程中出现错误: {str(e)}")
                st.info("请确认: 1) API Key 已正确配置  2) PDF 包含可提取的文字内容")

    # 清理临时文件
    os.unlink(tmp_path)

else:
    # 未上传文件时显示示例
    st.info("👆 请上传一篇论文 PDF 文件开始分析")

    st.markdown("""
    ### 支持的分析功能

    | 功能 | 说明 | 适用场景 |
    |------|------|----------|
    | 📝 摘要生成 | 200-300字论文概要 | 快速了解论文核心内容 |
    | 🔬 方法提取 | 识别研究方法与工具 | 文献调研、方法对比 |
    | 💡 创新点识别 | 区分方法/应用/理论创新 | 论文评审、研究方向判断 |
    | 🏷️ 关键词提取 | 中英文关键词列表 | 文献分类、检索优化 |
    | 📊 完整报告 | 结构化六维度分析 | 深度论文解读 |

    ### 技术架构

    本项目结合 **PDF 解析** 与 **大语言模型 API**，自动完成学术论文的结构化分析。
    支持 GPT-4o、Claude Sonnet、DeepSeek 等主流模型，通过智能分块策略处理长篇论文。
    """)

# Footer
st.divider()
st.caption("AI 论文分析助手 | 基于大语言模型的学术论文智能分析工具")
