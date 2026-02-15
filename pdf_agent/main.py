import asyncio

from agents import Agent, Runner

from tools.edit_tools import (
    delete_pages,
    encrypt_pdf,
    insert_image,
    merge_pdfs,
    replace_text,
    rotate_pages,
    split_pdf,
)
from tools.generate_tools import (
    add_header_footer,
    add_page_numbers,
    add_text_at_position,
    add_watermark,
)
from tools.read_tools import extract_text, get_pdf_info, search_text


pdf_agent = Agent(
    name="PDF編集エージェント",
    model="gpt-4.1",
    instructions="""あなたはPDF編集のエキスパートです。
ユーザーの指示に従い、ツールを使ってPDFを編集してください。

【行動ルール】
1. 操作の前に必ず get_pdf_info で対象PDFの情報を確認する
2. ユーザーの指示が曖昧な場合は質問して確認する
3. 複数ステップが必要な場合は計画を立ててから順番に実行する
4. 元ファイルは上書きしない（各ツールが自動で別名保存する）
5. 操作完了後、何を行ったか・保存先を日本語で報告する
6. 連続操作では前のツールの出力ファイルを次の入力にする

【座標系の補足】
- PDF座標は左上が原点 (0,0)、単位はpt（1pt ≈ 0.353mm）
- A4サイズは約 595 x 842 pt
""",
    tools=[
        get_pdf_info,
        extract_text,
        search_text,
        delete_pages,
        rotate_pages,
        merge_pdfs,
        split_pdf,
        replace_text,
        insert_image,
        encrypt_pdf,
        add_watermark,
        add_page_numbers,
        add_header_footer,
        add_text_at_position,
    ],
)


async def main() -> None:
    print("=" * 50)
    print("  PDF編集エージェント")
    print("  終了するには 'quit' と入力してください")
    print("=" * 50)

    while True:
        user_input = input("\n📝 指示: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("終了します。")
            break

        result = await Runner.run(pdf_agent, user_input)
        print(f"\n🤖 結果:\n{result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
