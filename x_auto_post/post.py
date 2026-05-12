#!/usr/bin/env python3
"""X自動投稿スクリプト - Claude APIで文章生成してXに投稿する"""
import argparse
import json
import logging
import os
import random
from pathlib import Path

import anthropic
import tweepy
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


def load_config() -> dict:
    with open(BASE_DIR / "config.json", encoding="utf-8") as f:
        return json.load(f)


def load_past_posts(count: int = 10) -> list[str]:
    path = BASE_DIR / "past_posts.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    texts = [p.get("text", "").strip() for p in data if p.get("text", "").strip()]
    return texts[:count]


def generate_tweet(config: dict, past_posts: list[str]) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    topic = config["topic"]
    style = config.get("style", "親しみやすい文体")
    max_chars = config.get("max_chars", 120)
    hashtags = " ".join(config.get("hashtags", []))

    past_examples = ""
    if past_posts:
        sampled = random.sample(past_posts, min(5, len(past_posts)))
        past_examples = "\n\n【過去の投稿例（文体・雰囲気の参考にしてください）】\n" + "\n---\n".join(sampled)

    prompt = f"""あなたはXで登山アカウントを運営するSNS担当者です。
以下の条件でX投稿文を1つ作成してください。

テーマ: {topic}
文体・トーン: {style}
本文の文字数目安: {max_chars}文字以内
末尾のハッシュタグ: {hashtags}
{past_examples}

【ルール】
- 投稿文のみ出力（説明・前置きは一切不要）
- 絵文字を自然に使用する
- ハッシュタグを含む全体が280文字以内に収まること
- 毎回異なる切り口で（山の絶景、装備レビュー、安全注意、季節の山、達成感、ルート紹介など）
- 読者が思わず「いいね」したくなる、共感・発見・感動のある内容にする"""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


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
    parser = argparse.ArgumentParser(description="X自動投稿スクリプト（登山アカウント）")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="投稿せずに生成内容だけ確認する（テスト用）",
    )
    args = parser.parse_args()

    load_dotenv(BASE_DIR / ".env")
    log.info("=== X自動投稿 開始 ===")

    config = load_config()
    past_posts = load_past_posts(config.get("past_posts_count", 10))
    log.info(f"過去投稿データ: {len(past_posts)}件 読み込み済み")

    tweet_text = generate_tweet(config, past_posts)
    char_count = len(tweet_text)
    log.info(f"生成された投稿文 ({char_count}文字):\n{tweet_text}")

    if args.dry_run:
        log.info("[DRY RUN] 投稿をスキップしました。--dry-run を外すと実際に投稿されます。")
        return

    result = post_to_x(tweet_text)
    log.info(f"投稿成功 ✓ tweet_id={result['id']}")


if __name__ == "__main__":
    main()
