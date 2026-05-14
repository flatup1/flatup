#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emergency closed-day mode for AIKA."""

import json
import logging
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(os.environ.get("CLOSED_DATES_PATH", "/root/config/closed_dates.json"))
JST = timezone(timedelta(hours=9))
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CLOSED_MESSAGE = (
    "申し訳ございません🙇‍♀️\n"
    "本日は急遽インストラクター不在のため、\n"
    "レッスンをお休みさせていただきます。\n\n"
    "ご来店前に必ずご確認のお願いを申し上げます。\n"
    "次回以降のご質問はお気軽にお寄せください😊"
)


def _today_str():
    return datetime.now(JST).date().isoformat()


def _load_closed_dates():
    try:
        if not CONFIG_PATH.exists():
            return set()
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        dates = data.get("closed_dates", [])
        if not isinstance(dates, list):
            logger.error("closed_dates.json の closed_dates が配列ではありません")
            return set()
        return {d for d in dates if isinstance(d, str) and DATE_RE.fullmatch(d)}
    except Exception as e:
        logger.error(f"休業日ファイル読み込みエラー: {e}")
        return set()


def _save_closed_dates(dates):
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"closed_dates": sorted(dates)}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return True
    except Exception as e:
        logger.error(f"休業日ファイル保存エラー: {e}")
        return False


def _normalize_date(value):
    if value == "today":
        return _today_str()
    if DATE_RE.fullmatch(value or ""):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            return None
    return None


def is_closed_today():
    return _today_str() in _load_closed_dates()


def handle_command(msg, uid, owner_user_id):
    """Handle owner-only closed/open commands.

    Returns a reply string when the command was handled, otherwise None.
    Non-owner commands are ignored and continue through the normal AIKA path.
    """
    if not (msg.startswith("/closed") or msg.startswith("/open")):
        return None
    if uid != owner_user_id:
        return None

    parts = msg.split()
    cmd = parts[0]
    arg = parts[1] if len(parts) >= 2 else ""
    dates = _load_closed_dates()

    if cmd == "/closed":
        if arg == "list":
            future_dates = sorted(d for d in dates if d >= _today_str())
            if not future_dates:
                return "現在、休業日は設定されていません。"
            return "現在の休業日:\n" + "\n".join(future_dates)
        if arg == "off":
            if not _save_closed_dates(set()):
                return "休業日の一括解除を保存できませんでした。サーバー設定を確認してください。"
            return "すべての休業日を解除しました✅"

        target = _normalize_date(arg)
        if not target:
            return "形式が違います。/closed today または /closed YYYY-MM-DD を使ってください。"
        dates.add(target)
        if not _save_closed_dates(dates):
            return "休業日の保存に失敗しました。サーバー設定を確認してください。"
        if target == _today_str():
            return "本日を休業日に設定しました✅"
        return f"{target} を休業日に設定しました✅"

    if cmd == "/open":
        target = _normalize_date(arg)
        if not target:
            return "形式が違います。/open today を使ってください。"
        dates.discard(target)
        if not _save_closed_dates(dates):
            return "営業日への復帰を保存できませんでした。サーバー設定を確認してください。"
        if target == _today_str():
            return "本日を営業日に戻しました✅"
        return f"{target} を営業日に戻しました✅"

    return None
