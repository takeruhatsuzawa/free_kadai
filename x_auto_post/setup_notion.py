#!/usr/bin/env python3
"""Notionデータベースをセットアップするスクリプト

事前準備:
  1. https://www.notion.so/my-integrations でIntegrationを作成
  2. 作成したIntegrationのTokenを .env の NOTION_TOKEN に設定
  3. NotionでIntegrationを共有したい親ページを開き、URLからページIDを取得
     例: https://www.notion.so/MyPage-abc123def456 → abc123def456

実行方法:
  python setup_notion.py
"""
import os
from pathlib import Path

from notion_client import Client
from notion_client.errors import APIResponseError
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


def create_database(notion: Client, parent_page_id: str) -> str:
    response = notion.databases.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        title=[{"type": "text", "text": {"content": "X投稿管理"}}],
        properties={
            "投稿内容": {"title": {}},
            "ステータス": {
                "select": {
                    "options": [
                        {"name": "下書き", "color": "gray"},
                        {"name": "承認済み", "color": "green"},
                        {"name": "投稿済み", "color": "blue"},
                        {"name": "スキップ", "color": "red"},
                    ]
                }
            },
            "生成日時": {"date": {}},
            "投稿日時": {"date": {}},
            "文字数": {"number": {"format": "number"}},
            "ツイートID": {"rich_text": {}},
        },
    )
    return response["id"].replace("-", "")


def format_database_id(raw_id: str) -> str:
    d = raw_id.replace("-", "")
    return f"{d[:8]}-{d[8:12]}-{d[12:16]}-{d[16:20]}-{d[20:]}"


def main():
    token = os.environ.get("NOTION_TOKEN", "")
    if not token or token == "your_notion_token_here":
        print("エラー: .env に NOTION_TOKEN が設定されていません")
        print("  1. https://www.notion.so/my-integrations でIntegrationを作成")
        print("  2. .env に NOTION_TOKEN=ntn_xxxx を追加")
        return

    print("Notion X投稿管理データベース セットアップ")
    print("=" * 45)
    print()
    print("【手順】")
    print("  1. Notionでデータベースを配置したいページを開く")
    print("  2. そのページの「...」メニュー → 「接続」→ 作成したIntegrationを追加")
    print("  3. ページURLの末尾のIDを入力する")
    print()
    print("  URL例: https://www.notion.so/MyPage-8a9b1c2d3e4f5a6b7c8d9e0f1a2b3c4d")
    print("  ページID:                              8a9b1c2d3e4f5a6b7c8d9e0f1a2b3c4d")
    print()

    raw_input = input("親ページID（またはURL）: ").strip()
    if not raw_input:
        print("キャンセルしました")
        return

    # URLから末尾のIDを抽出
    if "notion.so" in raw_input:
        parts = raw_input.rstrip("/").split("/")
        last = parts[-1]
        # "ページ名-ID" 形式の場合
        page_id = last.split("-")[-1] if "-" in last else last
    else:
        page_id = raw_input.replace("-", "")

    notion = Client(auth=token)

    print("\nデータベースを作成中...")
    try:
        db_id_raw = create_database(notion, page_id)
        db_id = format_database_id(db_id_raw)
    except APIResponseError as e:
        print(f"\nエラー: {e.message}")
        print("ページにIntegrationが共有されているか確認してください")
        return

    print(f"\n✓ データベース「X投稿管理」を作成しました！")
    print()
    print("【次の手順】.env に以下を追加してください:")
    print(f"  NOTION_DATABASE_ID={db_id}")
    print()

    env_path = BASE_DIR / ".env"
    if env_path.exists():
        with open(env_path, "a", encoding="utf-8") as f:
            f.write(f"\nNOTION_DATABASE_ID={db_id}\n")
        print(f"✓ .env に自動追記しました")


if __name__ == "__main__":
    main()
