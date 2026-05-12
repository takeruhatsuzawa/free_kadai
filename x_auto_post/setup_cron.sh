#!/bin/bash
# cronジョブを設定するスクリプト
# 実行前に config.json の post_hour を確認してください

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON=$(command -v python3 || command -v python)
POST_HOUR=$(python3 -c "import json; c=json.load(open('$SCRIPT_DIR/config.json')); print(c.get('post_hour', 7))" 2>/dev/null || echo "7")

if [ -z "$PYTHON" ]; then
  echo "エラー: python3 が見つかりません"
  exit 1
fi

CRON_JOB="0 ${POST_HOUR} * * * cd \"$SCRIPT_DIR\" && $PYTHON post.py >> logs/cron.log 2>&1"

echo "以下のcronジョブを追加します:"
echo "  $CRON_JOB"
echo ""
read -p "続行しますか？ (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
  echo "✓ cronジョブを設定しました（毎日 ${POST_HOUR}時 に投稿）"
  echo ""
  echo "確認コマンド: crontab -l"
  echo "削除コマンド: crontab -e で該当行を削除"
else
  echo "キャンセルしました"
fi
