"""
AI 论文分析助手 - 命令行入口

用法:
    python main.py paper.pdf                        # 完整分析
    python main.py paper.pdf --mode summary          # 仅摘要
    python main.py paper.pdf --mode methods          # 仅方法提取
    python main.py paper.pdf --model gpt-4o          # 指定模型
    python main.py paper.pdf --output report.md      # 指定输出文件
"""

import argparse
import os
import sys
from analyzer import PaperAnalyzer
from config import MODEL_CONFIGS, OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="AI 论文分析助手 - 基于大语言模型的学术论文智能分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py paper.pdf
  python main.py paper.pdf --mode summary --model claude-sonnet
  python main.py paper.pdf --output my_report.md
        """,
    )

    parser.add_argument("pdf_path", help="论文 PDF 文件路径")
    parser.add_argument(
        "--mode",
        choices=["full", "summary", "methods", "innovations", "keywords"],
        default="full",
        help="分析模式 (默认: full)",
    )
    parser.add_argument(
        "--model",
        choices=list(MODEL_CONFIGS.keys()),
        default="gpt-4o-mini",
        help="使用的模型 (默认: gpt-4o-mini)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="输出文件路径 (默认: output/<论文名>_分析报告.md)",
    )

    args = parser.parse_args()

    # 验证输入文件
    if not os.path.exists(args.pdf_path):
        print(f"错误: 文件不存在 - {args.pdf_path}")
        sys.exit(1)

    if not args.pdf_path.lower().endswith(".pdf"):
        print("警告: 输入文件不是 .pdf 格式，可能无法正常解析")

    # 检查 API Key
    config = MODEL_CONFIGS[args.model]
    if not config.get("api_key"):
        print(f"错误: 模型 {args.model} 的 API Key 未设置")
        print(f"请在 .env 文件中设置对应的 API Key")
        print(f"需要的环境变量: {config.get('provider', '').upper()}_API_KEY")
        sys.exit(1)

    # 运行分析
    print(f"{'='*50}")
    print(f"  AI 论文分析助手")
    print(f"  模型: {args.model} | 模式: {args.mode}")
    print(f"{'='*50}")

    analyzer = PaperAnalyzer(model_name=args.model)
    report = analyzer.run_pipeline(args.pdf_path, mode=args.mode)

    # 输出结果
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_basename = os.path.splitext(os.path.basename(args.pdf_path))[0]
    output_path = args.output or os.path.join(OUTPUT_DIR, f"{pdf_basename}_分析报告.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[输出] 分析报告已保存到: {output_path}")
    print(f"\n{report[:500]}...")
    print(f"\n完整报告请查看: {output_path}")


if __name__ == "__main__":
    main()
