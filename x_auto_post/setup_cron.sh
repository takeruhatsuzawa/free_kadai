#!/bin/bash
# cronジョブを設定するスクリプト（承認フロー版）
#
# 登録されるジョブ:
#   毎日 generate_hour 時: 投稿候補を生成してNotionに保存
#   毎日 post_hour 時    : Notionで承認済みの投稿をXに投稿

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON=$(command -v python3 || command -v python)

if [ -z "$PYTHON" ]; then
  echo "エラー: python3 が見つかりません"
  exit 1
fi

GENERATE_HOUR=$(python3 -c "import json; c=json.load(open('$SCRIPT_DIR/config.json')); print(c.get('generate_hour', 8))" 2>/dev/null || echo "8")
POST_HOUR=$(python3 -c "import json; c=json.load(open('$SCRIPT_DIR/config.json')); print(c.get('post_hour', 12))" 2>/dev/null || echo "12")

GENERATE_JOB="0 ${GENERATE_HOUR} * * * cd \"$SCRIPT_DIR\" && $PYTHON generate_candidates.py >> logs/cron.log 2>&1"
POST_JOB="0 ${POST_HOUR} * * * cd \"$SCRIPT_DIR\" && $PYTHON post_approved.py >> logs/cron.log 2>&1"

echo "以下のcronジョブを追加します:"
echo ""
echo "  [1] 毎日 ${GENERATE_HOUR}:00 → 投稿候補を生成してNotionに保存"
echo "      $GENERATE_JOB"
echo ""
echo "  [2] 毎日 ${POST_HOUR}:00 → Notionで承認済みの投稿をXに投稿"
echo "      $POST_JOB"
echo ""
read -p "続行しますか？ (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
  (crontab -l 2>/dev/null; echo "$GENERATE_JOB"; echo "$POST_JOB") | crontab -
  echo ""
  echo "✓ cronジョブを設定しました"
  echo ""
  echo "確認: crontab -l"
  echo "削除: crontab -e で該当行を削除"
  echo ""
  echo "【運用フロー】"
  echo "  毎朝 ${GENERATE_HOUR}時: 投稿候補3件がNotionに「下書き」で追加される"
  echo "  あなた: Notionで内容を確認・編集し、投稿したいものを「承認済み」に変更"
  echo "  毎日 ${POST_HOUR}時: 承認済みの投稿が自動でXに投稿される"
else
  echo "キャンセルしました"
fi
