"""
PDF 解析模块：提取学术论文的文本内容
支持普通文本型 PDF 和扫描版 PDF
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """从 PDF 文件中提取全部文本内容"""
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if text.strip():
            full_text.append(f"[第 {page_num + 1} 页]\n{text}")

    doc.close()

    if not full_text:
        raise ValueError(
            f"未能从 PDF 中提取到文字内容。"
            f"文件可能是扫描版 PDF，建议先用 OCR 工具处理。"
        )

    return "\n\n".join(full_text)


def extract_text_by_pages(pdf_path: str) -> list[dict]:
    """按页提取文本，返回每页的页码和内容"""
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({
            "page": page_num + 1,
            "text": text.strip(),
            "char_count": len(text),
        })

    doc.close()
    return pages


def get_pdf_metadata(pdf_path: str) -> dict:
    """获取 PDF 文件的元数据"""
    doc = fitz.open(pdf_path)
    metadata = {
        "total_pages": len(doc),
        "title": doc.metadata.get("title", "未知"),
        "author": doc.metadata.get("author", "未知"),
        "subject": doc.metadata.get("subject", ""),
        "creator": doc.metadata.get("creator", ""),
    }
    doc.close()
    return metadata


def chunk_text(text: str, max_chars: int = 8000, overlap: int = 200) -> list[str]:
    """
    将长文本分块，每块不超过 max_chars 字符
    块之间有 overlap 字符的重叠，保持上下文连贯
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars

        # 尝试在句子边界处截断
        if end < len(text):
            # 寻找最近的句号、换行或段落分隔符
            for sep in ["\n\n", "\n", "。", ". "]:
                pos = text.rfind(sep, start, end)
                if pos > start + max_chars // 2:
                    end = pos + len(sep)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap if end < len(text) else len(text)

    return chunks
