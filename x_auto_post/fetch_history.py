#!/usr/bin/env python3
"""過去のX投稿を取得してpast_posts.jsonに保存するスクリプト

実行方法:
  python fetch_history.py           # 最新100件を取得
  python fetch_history.py --max 50  # 取得件数を指定
"""
import argparse
import json
import os
from pathlib import Path

import tweepy
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")


def fetch_my_tweets(max_results: int = 100) -> list[dict]:
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )

    me = client.get_me()
    user_id = me.data.id
    print(f"ユーザーID: {user_id} (@{me.data.username})")

    tweets = []
    # 100件ずつページネーションして取得
    paginator = tweepy.Paginator(
        client.get_users_tweets,
        id=user_id,
        max_results=min(max_results, 100),
        tweet_fields=["created_at", "text", "public_metrics"],
        exclude=["retweets", "replies"],
    ).flatten(limit=max_results)

    for tweet in paginator:
        tweets.append({
            "id": str(tweet.id),
            "text": tweet.text,
            "created_at": str(tweet.created_at) if tweet.created_at else "",
        })

    return tweets


def main():
    parser = argparse.ArgumentParser(description="X過去投稿取得スクリプト")
    parser.add_argument("--max", type=int, default=100, help="取得する最大件数（デフォルト: 100）")
    args = parser.parse_args()

    print(f"過去の投稿を最大{args.max}件取得中...")
    tweets = fetch_my_tweets(args.max)

    out_path = BASE_DIR / "past_posts.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {len(tweets)}件の投稿を {out_path.name} に保存しました")
    if tweets:
        print("\n--- 直近3件のプレビュー ---")
        for t in tweets[:3]:
            preview = t["text"][:60].replace("\n", " ")
            print(f"  [{t['created_at'][:10]}] {preview}...")


if __name__ == "__main__":
    main()
