# PDF編集エージェント（OpenAI Agents SDK）

OpenAI が提供する [Agents SDK](https://github.com/openai/openai-agents-python) を使った PDF 編集エージェントです。Python 関数に `@function_tool` デコレーターを付けるだけで、ツールループやスキーマ生成を自動化します。

## 1. インストール

```bash
pip install openai-agents pymupdf pypdf reportlab
```

```bash
export OPENAI_API_KEY=sk-...
```

## 2. プロジェクト構成

```
pdf_agent/
├── main.py              # エントリーポイント
├── tools/
│   ├── __init__.py
│   ├── read_tools.py    # 読み取り系ツール
│   ├── edit_tools.py    # 編集系ツール
│   └── generate_tools.py # 生成系ツール
└── requirements.txt
```

## 3. ツール一覧

### 読み取り系（`tools/read_tools.py`）

| ツール | 説明 |
|---|---|
| `get_pdf_info` | PDF の基本情報（ページ数、メタデータ、各ページのサイズ・テキストプレビュー）を取得 |
| `extract_text` | PDF からテキストを抽出（全ページまたは指定ページ） |
| `search_text` | PDF 内のテキストを検索し、見つかった位置を返す |

### 編集系（`tools/edit_tools.py`）

| ツール | 説明 |
|---|---|
| `delete_pages` | 指定ページを削除 |
| `rotate_pages` | 指定ページを回転（90/180/270°） |
| `merge_pdfs` | 複数の PDF を結合 |
| `split_pdf` | 指定範囲のページを抽出 |
| `replace_text` | テキストを検索して置換 |
| `insert_image` | 指定位置に画像を挿入 |
| `encrypt_pdf` | パスワード暗号化（AES-256） |

### 生成系（`tools/generate_tools.py`）

| ツール | 説明 |
|---|---|
| `add_watermark` | 全ページに透かし（ウォーターマーク）を追加 |
| `add_page_numbers` | 全ページにページ番号を追加 |
| `add_header_footer` | 全ページにヘッダー・フッターを追加 |
| `add_text_at_position` | 指定座標にテキストを挿入 |

## 4. 使い方

```bash
cd pdf_agent
python main.py
```

```
==================================================
  PDF編集エージェント
  終了するには 'quit' と入力してください
==================================================

📝 指示: report.pdf の3ページ目と5ページ目を削除して

🤖 結果:
report.pdf（全8ページ）から3ページ目と5ページ目を削除しました。
残り6ページのファイルが report_deleted.pdf に保存されています。

📝 指示: report_deleted.pdf に「社外秘」の透かしを入れて、ページ番号も右下に付けて

🤖 結果:
2つの操作を実行しました:
1. 全ページに「社外秘」の透かしを追加 → report_deleted_watermarked.pdf
2. そのファイルにページ番号（右下）を追加 → report_deleted_watermarked_numbered.pdf
最終ファイルは report_deleted_watermarked_numbered.pdf です。
```

## 5. モデル選択ガイド

`main.py` の `model=` を変えるだけで切り替えられます。

| モデル | 用途 | Input / 1M | Output / 1M |
|---|---|---|---|
| `gpt-4.1` | バランス型。推奨デフォルト | $2.00 | $8.00 |
| `gpt-4o` | マルチモーダル対応が必要な場合 | $2.50 | $10.00 |
| `gpt-4o-mini` | 大量バッチ処理・コスト最優先 | $0.15 | $0.60 |
| `o3` | 複雑な推論（条件分岐の多い編集指示） | $2.00 | $8.00 |

PDF 編集エージェントの場合、ほとんどのケースで `gpt-4.1` で十分な精度が出ます。日常的な操作（ページ削除、結合、透かし追加など）なら `gpt-4o-mini` でも問題なく動作し、コストが約 1/15 になります。