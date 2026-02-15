import fitz
from agents import function_tool


@function_tool
def get_pdf_info(file_path: str) -> str:
    """PDFの基本情報（ページ数、メタデータ、各ページのサイズ・テキストプレビュー）を取得します。
    最初にこのツールを呼んで対象PDFの内容を把握してください。

    Args:
        file_path: PDFファイルのパス
    """
    doc = fitz.open(file_path)
    info_lines = [
        f"ファイル: {file_path}",
        f"ページ数: {len(doc)}",
        f"メタデータ: {doc.metadata}",
        "",
    ]
    for i, page in enumerate(doc):
        preview = page.get_text()[:150].replace("\n", " ")
        info_lines.append(
            f"  Page {i + 1}: {page.rect.width:.0f}x{page.rect.height:.0f}pt | "
            f"テキスト冒頭: {preview}..."
        )
    doc.close()
    return "\n".join(info_lines)


@function_tool
def extract_text(file_path: str, page_number: int | None = None) -> str:
    """PDFからテキストを抽出します。

    Args:
        file_path: PDFファイルのパス
        page_number: 抽出するページ番号（1始まり）。省略時は全ページ。
    """
    doc = fitz.open(file_path)
    result = []
    if page_number:
        page = doc[page_number - 1]
        result.append(f"--- Page {page_number} ---\n{page.get_text()}")
    else:
        for i, page in enumerate(doc):
            result.append(f"--- Page {i + 1} ---\n{page.get_text()}")
    doc.close()
    return "\n".join(result)


@function_tool
def search_text(file_path: str, query: str) -> str:
    """PDF内のテキストを検索し、見つかった位置を返します。

    Args:
        file_path: PDFファイルのパス
        query: 検索するテキスト
    """
    doc = fitz.open(file_path)
    results = []
    for i, page in enumerate(doc):
        instances = page.search_for(query)
        for rect in instances:
            results.append(
                f"  Page {i + 1}: ({rect.x0:.1f}, {rect.y0:.1f}) - "
                f"({rect.x1:.1f}, {rect.y1:.1f})"
            )
    doc.close()
    if not results:
        return f"'{query}' は見つかりませんでした。"
    return f"'{query}' が {len(results)} 箇所で見つかりました:\n" + "\n".join(results)
