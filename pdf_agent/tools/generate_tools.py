import fitz
from agents import function_tool
from tools.edit_tools import _output_path


@function_tool
def add_watermark(file_path: str, text: str, font_size: float = 50) -> str:
    """全ページに斜めの透かし（ウォーターマーク）を追加します。

    Args:
        file_path: 入力PDFファイルのパス
        text: 透かしテキスト（例: 「社外秘」「DRAFT」）
        font_size: フォントサイズ（デフォルト: 50）
    """
    doc = fitz.open(file_path)
    for page in doc:
        r = page.rect
        center = fitz.Point(r.width / 2, r.height / 2)
        page.insert_text(
            fitz.Point(r.width / 2 - len(text) * font_size / 4, r.height / 2),
            text,
            fontsize=font_size,
            color=(0.75, 0.75, 0.75),
            morph=(center, fitz.Matrix(45)),
            overlay=True,
        )
    out = _output_path(file_path, "_watermarked")
    doc.save(out)
    doc.close()
    return f"透かし「{text}」を全ページに追加しました。保存先: {out}"


@function_tool
def add_page_numbers(
    file_path: str,
    position: str = "bottom-center",
    font_size: float = 10,
) -> str:
    """全ページにページ番号を追加します。

    Args:
        file_path: 入力PDFファイルのパス
        position: 配置位置。「bottom-left」「bottom-center」「bottom-right」のいずれか
        font_size: フォントサイズ（デフォルト: 10）
    """
    doc = fitz.open(file_path)
    for i, page in enumerate(doc):
        r = page.rect
        if position == "bottom-right":
            pt = fitz.Point(r.width - 50, r.height - 30)
        elif position == "bottom-left":
            pt = fitz.Point(30, r.height - 30)
        else:
            pt = fitz.Point(r.width / 2 - 10, r.height - 30)
        page.insert_text(pt, str(i + 1), fontsize=font_size, color=(0, 0, 0))

    out = _output_path(file_path, "_numbered")
    doc.save(out)
    doc.close()
    return f"ページ番号を追加しました（{position}）。保存先: {out}"


@function_tool
def add_header_footer(
    file_path: str,
    header_text: str = "",
    footer_text: str = "",
    font_size: float = 9,
) -> str:
    """全ページにヘッダー・フッターテキストを追加します。

    Args:
        file_path: 入力PDFファイルのパス
        header_text: ヘッダーに表示するテキスト（空文字なら追加しない）
        footer_text: フッターに表示するテキスト（空文字なら追加しない）
        font_size: フォントサイズ（デフォルト: 9）
    """
    doc = fitz.open(file_path)
    for page in doc:
        r = page.rect
        if header_text:
            page.insert_text(
                fitz.Point(r.width / 2 - len(header_text) * 3, 25),
                header_text, fontsize=font_size, color=(0.3, 0.3, 0.3),
            )
        if footer_text:
            page.insert_text(
                fitz.Point(r.width / 2 - len(footer_text) * 3, r.height - 20),
                footer_text, fontsize=font_size, color=(0.3, 0.3, 0.3),
            )
    out = _output_path(file_path, "_headfoot")
    doc.save(out)
    doc.close()
    return f"ヘッダー/フッターを追加しました。保存先: {out}"


@function_tool
def add_text_at_position(
    file_path: str,
    page_number: int,
    x: float,
    y: float,
    text: str,
    font_size: float = 12,
) -> str:
    """指定ページの指定座標にテキストを挿入します。

    Args:
        file_path: 入力PDFファイルのパス
        page_number: ページ番号（1始まり）
        x: X座標（pt、左端が0）
        y: Y座標（pt、上端が0）
        text: 挿入するテキスト
        font_size: フォントサイズ（デフォルト: 12）
    """
    doc = fitz.open(file_path)
    page = doc[page_number - 1]
    page.insert_text(fitz.Point(x, y), text, fontsize=font_size, color=(0, 0, 0))
    out = _output_path(file_path, "_annotated")
    doc.save(out)
    doc.close()
    return f"テキスト「{text}」を Page {page_number} の ({x},{y}) に挿入しました。保存先: {out}"
