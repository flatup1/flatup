#!/bin/bash
set -u

SERVICE="flatup-aika.service"
HEALTH_URL="https://line.flatupnarita.jp/health"
ERROR_DIR="/root/flatup_brain/ERRORS"
MONITOR_LOG="/var/log/flatup_aika_monitor.log"
ENV_FILE="/root/flatup_config.env"
APP_LOG="/var/log/flatup_aika.log"

umask 077
mkdir -p "$ERROR_DIR"
touch "$MONITOR_LOG"
chmod 600 "$MONITOR_LOG" 2>/dev/null || true

now() {
  date "+%Y-%m-%d %H:%M:%S"
}

record_issue() {
  local message="$1"
  local ts
  ts="$(now)"
  echo "[$ts] $message" >> "$MONITOR_LOG"
  echo "- [$ts] $message" >> "$ERROR_DIR/monitor_$(date '+%Y-%m-%d').md"
}

fix_permissions() {
  chmod 600 "$ENV_FILE" 2>/dev/null || record_issue "権限修復失敗: $ENV_FILE"
  chmod 600 "$APP_LOG" 2>/dev/null || record_issue "権限修復失敗: $APP_LOG"
  chmod 700 /root/flatup_brain/LOGS 2>/dev/null || true
  chmod 700 /root/flatup_brain/ERRORS 2>/dev/null || true
}

fix_permissions

if ! systemctl is-active --quiet "$SERVICE"; then
  record_issue "サービス停止を検知: $SERVICE。再起動します。"
  if systemctl restart "$SERVICE"; then
    record_issue "サービス再起動成功: $SERVICE"
  else
    record_issue "サービス再起動失敗: $SERVICE"
    exit 1
  fi
fi

if ! curl -fsS --max-time 10 "$HEALTH_URL" >/dev/null; then
  record_issue "ヘルスチェック失敗: $HEALTH_URL。サービス再起動を試行します。"
  if systemctl restart "$SERVICE"; then
    sleep 3
    if curl -fsS --max-time 10 "$HEALTH_URL" >/dev/null; then
      record_issue "ヘルスチェック復旧: $HEALTH_URL"
    else
      record_issue "ヘルスチェック未復旧: $HEALTH_URL"
      exit 1
    fi
  else
    record_issue "ヘルスチェック失敗後の再起動失敗: $SERVICE"
    exit 1
  fi
fi

exit 0
