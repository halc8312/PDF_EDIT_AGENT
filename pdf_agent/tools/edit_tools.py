from pathlib import Path

import fitz
import pypdf
from agents import function_tool


def _output_path(original: str, suffix: str = "_edited") -> str:
    """元ファイルを上書きしない出力パスを生成"""
    p = Path(original)
    return str(p.with_stem(p.stem + suffix))


@function_tool
def delete_pages(file_path: str, page_numbers: list[int]) -> str:
    """PDFから指定ページを削除します。

    Args:
        file_path: 入力PDFファイルのパス
        page_numbers: 削除するページ番号のリスト（1始まり）。例: [2, 5]
    """
    doc = fitz.open(file_path)
    for pn in sorted(page_numbers, reverse=True):
        doc.delete_page(pn - 1)
    out = _output_path(file_path, "_deleted")
    doc.save(out)
    doc.close()
    out_doc = fitz.open(out)
    page_count = len(out_doc)
    out_doc.close()
    return f"ページ {page_numbers} を削除しました。残り{page_count}ページ。保存先: {out}"


@function_tool
def rotate_pages(file_path: str, page_numbers: list[int], degrees: int) -> str:
    """指定ページを回転させます。

    Args:
        file_path: 入力PDFファイルのパス
        page_numbers: 回転するページ番号のリスト（1始まり）
        degrees: 回転角度（90, 180, 270 のいずれか）
    """
    doc = fitz.open(file_path)
    for pn in page_numbers:
        doc[pn - 1].set_rotation(degrees)
    out = _output_path(file_path, "_rotated")
    doc.save(out)
    doc.close()
    return f"ページ {page_numbers} を {degrees}° 回転しました。保存先: {out}"


@function_tool
def merge_pdfs(file_paths: list[str], output_path: str) -> str:
    """複数のPDFファイルを1つに結合します。

    Args:
        file_paths: 結合するPDFファイルパスのリスト（結合順）
        output_path: 出力ファイルのパス
    """
    merger = pypdf.PdfMerger()
    for fp in file_paths:
        merger.append(fp)
    merger.write(output_path)
    merger.close()
    total = len(pypdf.PdfReader(output_path).pages)
    return f"{len(file_paths)} ファイルを結合しました（全{total}ページ）。保存先: {output_path}"


@function_tool
def split_pdf(file_path: str, start_page: int, end_page: int) -> str:
    """PDFの指定範囲を別ファイルに分割します。

    Args:
        file_path: 入力PDFファイルのパス
        start_page: 開始ページ番号（1始まり、含む）
        end_page: 終了ページ番号（1始まり、含む）
    """
    reader = pypdf.PdfReader(file_path)
    writer = pypdf.PdfWriter()
    for pn in range(start_page - 1, end_page):
        writer.add_page(reader.pages[pn])
    out = _output_path(file_path, f"_p{start_page}-{end_page}")
    with open(out, "wb") as f:
        writer.write(f)
    return f"ページ {start_page}〜{end_page} を抽出しました。保存先: {out}"


@function_tool
def replace_text(file_path: str, search_text: str, replace_with: str) -> str:
    """PDF内のテキストを検索して置換します。
    注意: フォントの制約により完全な見た目の一致は保証されません。

    Args:
        file_path: 入力PDFファイルのパス
        search_text: 検索するテキスト
        replace_with: 置換後のテキスト
    """
    doc = fitz.open(file_path)
    count = 0
    for page in doc:
        instances = page.search_for(search_text)
        for inst in instances:
            page.add_redact_annot(inst, fill=(1, 1, 1))
        page.apply_redactions()
        for inst in instances:
            page.insert_text(inst.tl, replace_with, fontsize=11, color=(0, 0, 0))
            count += 1
    out = _output_path(file_path, "_replaced")
    doc.save(out)
    doc.close()
    return f"'{search_text}' → '{replace_with}': {count}箇所を置換しました。保存先: {out}"


@function_tool
def insert_image(
    file_path: str,
    page_number: int,
    image_path: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> str:
    """指定ページの指定位置に画像を挿入します。

    Args:
        file_path: 入力PDFファイルのパス
        page_number: 挿入先のページ番号（1始まり）
        image_path: 挿入する画像ファイルのパス
        x: 左上のX座標（pt）
        y: 左上のY座標（pt）
        width: 画像の表示幅（pt）
        height: 画像の表示高さ（pt）
    """
    doc = fitz.open(file_path)
    page = doc[page_number - 1]
    rect = fitz.Rect(x, y, x + width, y + height)
    page.insert_image(rect, filename=image_path)
    out = _output_path(file_path, "_with_image")
    doc.save(out)
    doc.close()
    return f"画像を Page {page_number} の ({x},{y}) に挿入しました。保存先: {out}"


@function_tool
def encrypt_pdf(file_path: str, password: str) -> str:
    """PDFにパスワードを設定して暗号化（AES-256）します。

    Args:
        file_path: 入力PDFファイルのパス
        password: 設定するパスワード
    """
    doc = fitz.open(file_path)
    out = _output_path(file_path, "_encrypted")
    doc.save(out, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=password)
    doc.close()
    return f"PDFを暗号化しました。保存先: {out}"
