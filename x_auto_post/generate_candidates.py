#!/usr/bin/env python3
"""投稿候補をN件生成してNotionデータベースに「下書き」として保存するスクリプト

実行方法:
  python generate_candidates.py        # 3件生成（デフォルト）
  python generate_candidates.py -n 5   # 5件生成
"""
import argparse
import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path

import anthropic
from notion_client import Client
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "generate.log", encoding="utf-8"),
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


def generate_candidates(config: dict, past_posts: list[str], n: int) -> list[str]:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    topic = config["topic"]
    style = config.get("style", "親しみやすい文体")
    max_chars = config.get("max_chars", 120)
    hashtags = " ".join(config.get("hashtags", []))

    past_examples = ""
    if past_posts:
        sampled = random.sample(past_posts, min(5, len(past_posts)))
        past_examples = "\n\n【過去の投稿例（文体・雰囲気の参考）】\n" + "\n---\n".join(sampled)

    prompt = f"""あなたはXで登山アカウントを運営するSNS担当者です。
以下の条件でX投稿文を{n}件作成してください。

テーマ: {topic}
文体・トーン: {style}
本文の文字数目安: {max_chars}文字以内
末尾のハッシュタグ: {hashtags}
{past_examples}

【ルール】
- 投稿文のみ出力（説明・前置きは一切不要）
- 絵文字を自然に使用する
- ハッシュタグを含む全体が280文字以内
- {n}件はそれぞれ必ず異なる切り口で（山の絶景、装備レビュー、安全注意、季節の山、達成感、ルート紹介など）
- 各投稿の区切りは「---」のみ（番号・ラベル不要）"""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()
    candidates = [c.strip() for c in raw.split("---") if c.strip()]
    return candidates[:n]


def save_to_notion(notion: Client, database_id: str, candidates: list[str]) -> None:
    now = datetime.now().isoformat()
    for text in candidates:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "投稿内容": {"title": [{"text": {"content": text}}]},
                "ステータス": {"select": {"name": "下書き"}},
                "生成日時": {"date": {"start": now}},
                "文字数": {"number": len(text)},
            },
        )


def main():
    parser = argparse.ArgumentParser(description="X投稿候補生成スクリプト")
    parser.add_argument("-n", type=int, default=None, help="生成する候補数（未指定時はconfig.jsonのgenerate_countを使用）")
    args = parser.parse_args()

    load_dotenv(BASE_DIR / ".env")
    config = load_config()
    n = args.n or config.get("generate_count", 3)

    past_posts = load_past_posts(config.get("past_posts_count", 10))
    log.info(f"過去投稿データ: {len(past_posts)}件 読み込み済み")

    log.info(f"{n}件の投稿候補を生成中...")
    candidates = generate_candidates(config, past_posts, n)

    log.info(f"\n{'='*40}")
    for i, c in enumerate(candidates, 1):
        log.info(f"[候補{i}] ({len(c)}文字)\n{c}\n")
    log.info("="*40)

    notion = Client(auth=os.environ["NOTION_TOKEN"])
    database_id = os.environ["NOTION_DATABASE_ID"]
    save_to_notion(notion, database_id, candidates)
    log.info(f"✓ {len(candidates)}件の候補をNotionに保存しました（ステータス: 下書き）")
    log.info("Notionでステータスを「承認済み」に変更すると、次回の定期実行時に投稿されます")


if __name__ == "__main__":
    main()
