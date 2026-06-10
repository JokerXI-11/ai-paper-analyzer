"""
核心分析引擎：将 PDF 解析和大模型调用组合成完整的论文分析流程
"""

import os
from pdf_parser import extract_text_from_pdf, get_pdf_metadata, chunk_text
from llm_client import LLMClient
from prompts import (
    SYSTEM_PROMPT,
    SUMMARY_PROMPT,
    METHOD_PROMPT,
    INNOVATION_PROMPT,
    KEYWORDS_PROMPT,
    FULL_PAPER_PROMPT,
)


class PaperAnalyzer:
    """论文分析器：封装完整的分析流水线"""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.llm = LLMClient(model_name)
        self.metadata = {}
        self.full_text = ""
        self.chunks = []

    def load_paper(self, pdf_path: str):
        """加载论文 PDF"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"文件不存在: {pdf_path}")

        print(f"[加载] 正在解析 PDF: {pdf_path}")
        self.metadata = get_pdf_metadata(pdf_path)
        self.full_text = extract_text_from_pdf(pdf_path)

        print(f"  - 标题: {self.metadata.get('title', '未知')}")
        print(f"  - 作者: {self.metadata.get('author', '未知')}")
        print(f"  - 页数: {self.metadata['total_pages']}")
        print(f"  - 总字符数: {len(self.full_text)}")

    def _analyze_long_text(self, prompt_template: str, label: str) -> str:
        """处理长文本：分块分析后汇总"""
        if not self.chunks:
            self.chunks = chunk_text(self.full_text)

        # 如果只有一块，直接分析
        if len(self.chunks) == 1:
            return self.llm.chat(SYSTEM_PROMPT, prompt_template.format(text=self.chunks[0]))

        # 多块分析
        partial_results = []
        for i, chunk in enumerate(self.chunks):
            print(f"  [{label}] 分析第 {i+1}/{len(self.chunks)} 块...")
            result = self.llm.chat(SYSTEM_PROMPT, prompt_template.format(text=chunk))
            partial_results.append(result)

        # 汇总合并
        merge_prompt = f"""以下是对一篇论文各部分的{label}分析结果，请将它们整合为一份连贯、去重的完整报告：

{'='.join(partial_results)}

请整合为一份完整的{label}报告："""
        return self.llm.chat(SYSTEM_PROMPT, merge_prompt)

    def generate_summary(self) -> str:
        """生成论文摘要"""
        print("\n[分析] 生成论文摘要...")
        return self._analyze_long_text(SUMMARY_PROMPT, "摘要")

    def extract_methods(self) -> str:
        """提取研究方法"""
        print("\n[分析] 提取研究方法...")
        return self._analyze_long_text(METHOD_PROMPT, "方法")

    def extract_innovations(self) -> str:
        """提取创新点"""
        print("\n[分析] 提取创新点...")
        return self._analyze_long_text(INNOVATION_PROMPT, "创新点")

    def extract_keywords(self) -> str:
        """提取关键词"""
        print("\n[分析] 提取关键词...")
        # 关键词提取用前两个分块就够了
        text = self.chunks[0] if self.chunks else self.full_text[:8000]
        if len(self.chunks) > 1:
            text += "\n" + self.chunks[-1][:2000]
        return self.llm.chat(SYSTEM_PROMPT, KEYWORDS_PROMPT.format(text=text))

    def full_analysis(self) -> str:
        """完整分析：一次性输出结构化报告"""
        print("\n[分析] 执行完整论文分析...")

        if len(self.full_text) <= 12000:
            # 短论文直接分析
            return self.llm.chat(SYSTEM_PROMPT, FULL_PAPER_PROMPT.format(text=self.full_text))

        # 长论文：逐项分析后组合
        summary = self.generate_summary()
        methods = self.extract_methods()
        innovations = self.extract_innovations()
        keywords = self.extract_keywords()

        return self._compose_report(summary, methods, innovations, keywords)

    def _compose_report(self, summary: str, methods: str, innovations: str, keywords: str) -> str:
        """将各项分析结果组合为统一报告"""
        report = f"""# 论文分析报告

## 基本信息
- **标题**: {self.metadata.get('title', '未知')}
- **作者**: {self.metadata.get('author', '未知')}
- **页数**: {self.metadata['total_pages']}
- **分析模型**: {self.model_name}

---

## 摘要

{summary}

---

## 研究方法

{methods}

---

## 创新点与贡献

{innovations}

---

## 关键词

{keywords}

---

*本报告由 AI 论文分析助手自动生成*
"""
        return report

    def run_pipeline(self, pdf_path: str, mode: str = "full") -> str:
        """
        运行完整分析流水线

        Args:
            pdf_path: PDF 文件路径
            mode: 分析模式 - "full"(完整), "summary"(仅摘要),
                  "methods"(仅方法), "innovations"(仅创新点), "keywords"(仅关键词)

        Returns:
            分析报告文本
        """
        self.load_paper(pdf_path)

        mode_handlers = {
            "full": self.full_analysis,
            "summary": self.generate_summary,
            "methods": self.extract_methods,
            "innovations": self.extract_innovations,
            "keywords": self.extract_keywords,
        }

        if mode not in mode_handlers:
            raise ValueError(f"不支持的分析模式: {mode}。可选: {list(mode_handlers.keys())}")

        result = mode_handlers[mode]()
        print(f"\n[完成] 分析结束！")
        return result
