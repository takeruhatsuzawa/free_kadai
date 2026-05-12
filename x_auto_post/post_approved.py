#!/usr/bin/env python3
"""Notionで「承認済み」になった投稿をXに投稿するスクリプト

cronで定期実行する想定。承認済みが1件あれば投稿し、Notionを「投稿済み」に更新する。
実行方法:
  python post_approved.py           # 通常実行
  python post_approved.py --dry-run # 投稿せずに確認のみ
"""
import argparse
import logging
import os
from datetime import datetime
from pathlib import Path

import tweepy
from notion_client import Client
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "post.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def get_approved_posts(notion: Client, database_id: str) -> list[dict]:
    response = notion.databases.query(
        database_id=database_id,
        filter={"property": "ステータス", "select": {"equals": "承認済み"}},
        sorts=[{"property": "生成日時", "direction": "ascending"}],
        page_size=1,
    )
    return response.get("results", [])


def extract_text(page: dict) -> str:
    title_parts = page["properties"]["投稿内容"]["title"]
    return "".join(part["text"]["content"] for part in title_parts)


def update_to_posted(notion: Client, page_id: str, tweet_id: str) -> None:
    notion.pages.update(
        page_id=page_id,
        properties={
            "ステータス": {"select": {"name": "投稿済み"}},
            "投稿日時": {"date": {"start": datetime.now().isoformat()}},
            "ツイートID": {"rich_text": [{"text": {"content": tweet_id}}]},
        },
    )


def post_to_x(text: str) -> dict:
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=text)
    return response.data


def main():
    parser = argparse.ArgumentParser(description="承認済みX投稿スクリプト")
    parser.add_argument("--dry-run", action="store_true", help="投稿せずに確認のみ")
    args = parser.parse_args()

    load_dotenv(BASE_DIR / ".env")
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    database_id = os.environ["NOTION_DATABASE_ID"]

    log.info("=== 承認済み投稿チェック 開始 ===")
    approved = get_approved_posts(notion, database_id)

    if not approved:
        log.info("承認済みの投稿はありません")
        return

    page = approved[0]
    page_id = page["id"]
    tweet_text = extract_text(page)

    if not tweet_text:
        log.warning(f"投稿内容が空のページをスキップ: {page_id}")
        return

    log.info(f"投稿対象 ({len(tweet_text)}文字):\n{tweet_text}")

    if args.dry_run:
        log.info("[DRY RUN] 投稿をスキップしました")
        return

    result = post_to_x(tweet_text)
    tweet_id = str(result["id"])
    log.info(f"投稿成功 ✓ tweet_id={tweet_id}")

    update_to_posted(notion, page_id, tweet_id)
    log.info("Notionステータスを「投稿済み」に更新しました")


if __name__ == "__main__":
    main()
