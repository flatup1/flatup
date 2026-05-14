#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FLATUP AI OS - AIKA LINE Bot v5
- 会話履歴保持（同じことを聞き直さない）
- 「折り返しご連絡」→ AI自動停止（手動モード）
- /reset → AIを再起動（オーナーのみ）
"""

import os, hmac, re, hashlib, base64, json, logging, requests, jpholiday
from datetime import datetime, timezone, timedelta
from pathlib import Path
from flask import Flask, request, jsonify, abort
from lib import closed_mode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/log/flatup_aika.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
app = Flask(__name__)

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
LINE_ACCESS_TOKEN   = os.environ.get("LINE_ACCESS_TOKEN", "")
OPENROUTER_API_KEY  = os.environ.get("OPENROUTER_API_KEY", "")
OBSIDIAN_PATH       = os.environ.get("OBSIDIAN_PATH", "/root/flatup_brain")
MODEL               = "anthropic/claude-haiku-4-5"
LINE_REPLY_URL      = "https://api.line.me/v2/bot/message/reply"
OPENROUTER_URL      = "https://openrouter.ai/api/v1/chat/completions"

# ★ オーナーのLINEユーザーIDを設定（VPSログの「受信: Uxxxxx」の部分）
OWNER_USER_ID = "U521cd38b7f048be84eaa880ccabdc7f9"

# ユーザー状態管理（インメモリ）
# user_state[uid] = "active" or "manual"
user_state = {}

# 会話履歴管理（インメモリ、最大10ターン）
# conversation_history[uid] = [{"role": "user", "content": "..."}, ...]
conversation_history = {}
MAX_HISTORY = 10

MAPS_URL = "https://maps.google.com/?q=千葉県成田市土屋516-4+青柳ビル2F"
HANDOVER_PHRASE = "担当者より折り返しご連絡"

# ── SYSTEM_PROMPTを外部ファイルから読み込み（Obsidian連携） ──────────────────────────────────
def load_system_prompt():
    aika_path = os.getenv("AIKA_PROMPT_PATH", f"{OBSIDIAN_PATH}/1_AIKA人格_本番.md")
    try:
        with open(aika_path, "r", encoding="utf-8") as f:
            prompt = f.read()
            logger.info(f"✅ AIKA人格ファイルをロード: {aika_path}")
            return prompt
    except FileNotFoundError:
        logger.warning(f"⚠️  AIKA人格ファイルが見つかりません: {aika_path} (フォールバック中)")
        return """あなたは千葉県成田市のFLATUP GYM（世界一やさしい格闘技ジム）の受付AI「AIKA」です。

# 人格
クールで知的、女性・子供・初心者に優しい。温かいが冷静。丁寧な敬語を使う。

# ジム情報
【料金】体験: 500円 / 女性月額: 8,800円 / キッズ: 7,700円 / 男性: 9,900円
【場所】成田市土屋516-4 2F 百香亭の上
【クラス】ボクシング、キックボクシング、寝技、レスリング、総合格闘技、ブラジリアン柔術、キッズ、レディース

# 厳守ルール
- 1回の返答は200文字以内、絵文字は1〜2個、マークダウン禁止
- データにないことは「担当者より折り返しご連絡いたします」と返す
"""

SYSTEM_PROMPT = load_system_prompt()

def build_runtime_context():
    """AIKAに現在日時を推測させないため、毎回JSTの日時を渡す。"""
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    weekdays_jp = ["月", "火", "水", "木", "金", "土", "日"]
    weekday = now.weekday()
    minutes = now.hour * 60 + now.minute
    today = now.date()

    is_holiday_today = jpholiday.is_holiday(today)
    holiday_name = jpholiday.is_holiday_name(today) if is_holiday_today else None

    next_open = today + timedelta(days=1)
    while next_open.weekday() == 6 or jpholiday.is_holiday(next_open):
        next_open += timedelta(days=1)
    next_open_str = (
        f"次回営業日: {next_open.month}月{next_open.day}日"
        f"（{weekdays_jp[next_open.weekday()]}）"
    )

    if weekday == 6:
        today_status = f"本日は日曜日のため定休日。通常クラスは行っていない。{next_open_str}。"
    elif is_holiday_today:
        today_status = f"本日は祝日（{holiday_name}）のため定休日。通常クラスは行っていない。{next_open_str}。"
    elif weekday < 5:
        if minutes < 10 * 60:
            today_status = "本日は平日営業日。クラス時間は10:00〜12:00と18:00〜20:00。現在は開始前。"
        elif minutes < 12 * 60:
            today_status = "本日は平日営業日。現在は10:00〜12:00の時間帯。"
        elif minutes < 18 * 60:
            today_status = "本日は平日営業日。午前の時間帯は終了済みで、次は18:00〜20:00。"
        elif minutes < 20 * 60:
            today_status = "本日は平日営業日。現在は18:00〜20:00の時間帯。"
        else:
            today_status = "本日は平日営業日だが、20:00を過ぎているため本日のクラスは終了済み。"
    elif weekday == 5:
        if minutes < 10 * 60:
            today_status = "本日は土曜営業日。10:00キックボクシング、11:00寝技、13:00キッズ、14:00レディース。現在は開始前。"
        elif minutes < 11 * 60:
            today_status = "本日は土曜営業日。現在は10:00キックボクシングの時間帯。以降は11:00寝技、13:00キッズ、14:00レディース。"
        elif minutes < 12 * 60:
            today_status = "本日は土曜営業日。10:00キックボクシングは終了済み。現在は11:00寝技の時間帯。以降は13:00キッズ、14:00レディース。"
        elif minutes < 13 * 60:
            today_status = "本日は土曜営業日。10:00キックボクシングと11:00寝技は終了済み。次は13:00キッズ、14:00レディース。"
        elif minutes < 14 * 60:
            today_status = "本日は土曜営業日。現在は13:00キッズの時間帯。以降は14:00レディース。"
        elif minutes < 15 * 60:
            today_status = "本日は土曜営業日。10:00キックボクシング、11:00寝技、13:00キッズは終了済み。現在は14:00レディースの時間帯。"
        else:
            today_status = "本日は土曜営業日だが、14:00レディースまで全クラス終了済み。夜のクラスはない。"
    return (
        "# 現在日時（自動注入）\n"
        f"- 現在: {now.year}年{now.month}月{now.day}日"
        f"（{weekdays_jp[weekday]}）{now.strftime('%H:%M')} JST\n"
        f"- 今日の営業状況: {today_status}\n"
        "- 日曜日・日本の祝日は定休日（通常クラスなし）。\n"
        "- 「今日」「明日」「今から」などの相対表現は、この現在日時を基準に答える。\n"
        "- 今日のレッスン有無を聞かれたら、今日の営業状況を優先して答える。\n"
        "- 現在日時が必要な質問では推測せず、この情報を使う。"
    )

# Quick Reply ボタン定義
QR_TOP = [
    {"type": "action", "action": {"type": "message", "label": "体験入会したい🥊", "text": "体験入会について教えてください"}},
    {"type": "action", "action": {"type": "message", "label": "料金プラン💰",     "text": "料金プランを教えてください"}},
    {"type": "action", "action": {"type": "message", "label": "クラス情報📋",     "text": "クラスの種類を教えてください"}},
    {"type": "action", "action": {"type": "message", "label": "場所・アクセス📍", "text": "場所・アクセス方法を教えてください"}},
    {"type": "action", "action": {"type": "message", "label": "担当者に相談📞",   "text": "担当者に相談したい"}},
]

QR_MAP = [
    {"type": "action", "action": {"type": "uri",     "label": "Googleマップで開く🗺️", "uri": MAPS_URL}},
    {"type": "action", "action": {"type": "message", "label": "体験入会したい🥊",      "text": "体験入会について教えてください"}},
    {"type": "action", "action": {"type": "message", "label": "担当者に相談📞",        "text": "担当者に相談したい"}},
]

QR_DAY = [
    {"type": "action", "action": {"type": "message", "label": "平日に体験したい",  "text": "平日に体験したいです"}},
    {"type": "action", "action": {"type": "message", "label": "土曜日に体験したい", "text": "土曜日に体験したいです"}},
    {"type": "action", "action": {"type": "message", "label": "日程を相談したい",   "text": "日程について相談したいです"}},
]

QR_WEEKDAY_TIME = [
    {"type": "action", "action": {"type": "message", "label": "10〜12時", "text": "平日10時〜12時で希望します"}},
    {"type": "action", "action": {"type": "message", "label": "18〜20時", "text": "平日18時〜20時で希望します"}},
]

QR_SATURDAY_TIME = [
    {"type": "action", "action": {"type": "message", "label": "10時 キックボクシング", "text": "土曜10時のキックボクシングで希望します"}},
    {"type": "action", "action": {"type": "message", "label": "11時 寝技",            "text": "土曜11時の寝技クラスで希望します"}},
    {"type": "action", "action": {"type": "message", "label": "13時 キッズ",          "text": "土曜13時のキッズクラスで希望します"}},
    {"type": "action", "action": {"type": "message", "label": "14時 レディース",      "text": "土曜14時のレディースクラスで希望します"}},
]

def choose_quick_reply(msg, reply):
    if "場所" in msg or "アクセス" in msg or "どこ" in msg or "住所" in msg:
        return QR_MAP
    if "曜日" in reply or "いつ" in reply:
        return QR_DAY
    if ("平日" in msg or "平日" in reply) and ("時間" in reply or "帯" in reply):
        return QR_WEEKDAY_TIME
    if ("土曜" in msg or "土曜" in reply) and ("時間" in reply or "帯" in reply or "クラス" in reply):
        return QR_SATURDAY_TIME
    if "平日" in msg and ("体験" in msg or "希望" in msg):
        return QR_WEEKDAY_TIME
    if "土曜" in msg and ("体験" in msg or "希望" in msg):
        return QR_SATURDAY_TIME
    return QR_TOP

def get_history(uid):
    return conversation_history.get(uid, [])

def add_to_history(uid, role, content):
    if uid not in conversation_history:
        conversation_history[uid] = []
    conversation_history[uid].append({"role": role, "content": content})
    # 最大ターン数を超えたら古いものを削除
    if len(conversation_history[uid]) > MAX_HISTORY * 2:
        conversation_history[uid] = conversation_history[uid][-MAX_HISTORY * 2:]

def mask_pii(text):
    """個人情報をログ保存前にマスクする。"""
    if not text:
        return text
    text = str(text)
    text = re.sub(r"(\d{3})[-\s]?(\d{3,4})[-\s]?(\d{4})", r"\1-****-\3", text)
    text = re.sub(r"\b([A-Za-z0-9])[A-Za-z0-9._%+-]*(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", r"\1****\2", text)
    text = re.sub(r"(\d{4}年)\d{1,2}(月)\d{1,2}(日)", r"\1**\2**\3", text)
    return text


def save_log(user_id, q, a):
    try:
        d = Path(OBSIDIAN_PATH) / "LOGS"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(d / f"conversation_{user_id}.md", "a", encoding="utf-8") as f:
            f.write(f"\n## [{ts}]\n\n**質問:** {mask_pii(q)}\n\n**AIKA:** {mask_pii(a)}\n\n---\n")
    except Exception as e:
        logger.error(f"ログ保存エラー: {e}")

def save_error(user_id, q, a, detail):
    try:
        d = Path(OBSIDIAN_PATH) / "ERRORS"
        d.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(d / "error_log.md", "a", encoding="utf-8") as f:
            f.write(f"\n### [{ts}] {detail}\n**User:** {user_id}\n**質問:** {mask_pii(q)}\n**応答:** {mask_pii(a)}\n\n---\n")
    except:
        pass

def build_reply_instruction(msg):
    """質問の範囲を超えて営業案内を足しすぎないための短い制御。"""
    compact = re.sub(r"\s+", "", msg)
    if re.fullmatch(r"(今日は)?何曜日[？?]?", compact):
        return "このユーザー質問は曜日確認のみ。曜日だけを1文で答え、営業案内や予約誘導は足さない。"
    if re.fullmatch(r"(今|現在)?何時[？?]?", compact):
        return "このユーザー質問は現在時刻確認のみ。現在時刻だけを1文で答え、営業案内や予約誘導は足さない。"
    return "ユーザーが聞いた範囲にだけ答える。不要な営業案内や予約誘導は足しすぎない。"

def sanitize_ai_reply(text):
    """LINE返信前に、LLMが混ぜたMarkdown記号を取り除く。"""
    if not text:
        return text
    text = str(text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s{0,3}>\s?", "", text)
    text = re.sub(r"(?m)^\s*[-*]\s+", "", text)
    return text.strip()

def call_aika(uid, msg):
    history = get_history(uid)
    system_content = f"{SYSTEM_PROMPT}\n\n{build_runtime_context()}\n\n# 返信範囲\n{build_reply_instruction(msg)}"
    messages = [{"role": "system", "content": system_content}]
    messages.extend(history)
    messages.append({"role": "user", "content": msg})

    r = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://line.flatupnarita.jp",
            "X-Title": "FLATUP AI OS",
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": 250,
            "temperature": 0.4,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def verify_sig(body, sig):
    h = hmac.new(LINE_CHANNEL_SECRET.encode(), body, hashlib.sha256).digest()
    return hmac.compare_digest(base64.b64encode(h).decode(), sig)

def reply_line(token, msg, quick_items):
    # Strip Unicode line separators that break HTTP encoding
    msg = msg.replace("\u2028", "\n").replace("\u2029", "\n")
    payload = {
        "replyToken": token,
        "messages": [{
            "type": "text",
            "text": msg,
            "quickReply": {"items": quick_items}
        }]
    }
    requests.post(
        LINE_REPLY_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        },
        json=payload,
        timeout=10,
    ).raise_for_status()

@app.route("/webhook", methods=["POST"])
def webhook():
    sig  = request.headers.get("X-Line-Signature", "")
    body = request.get_data()
    if not verify_sig(body, sig):
        abort(400)
    try:
        events = json.loads(body)["events"]
    except:
        abort(400)

    for event in events:
        if event.get("type") != "message":
            continue
        if event.get("message", {}).get("type") != "text":
            continue

        uid   = event.get("source", {}).get("userId", "unknown")
        msg   = event["message"]["text"].strip()
        token = event["replyToken"]
        logger.info(f"受信: {uid[:8]}*** ({len(msg)}文字)")

        # ★ /reset コマンド（オーナーのみ or 未設定時は全員可）
        if msg == "/reset":
            if uid == OWNER_USER_ID:
                user_state[uid] = "active"
                conversation_history[uid] = []
                try:
                    reply_line(token, "AIモードを再起動しました✅", QR_TOP)
                except Exception as e:
                    logger.error(f"LINE返信エラー: {e}")
            continue

        # ★ 緊急休業モードのオーナーコマンド
        closed_command_reply = closed_mode.handle_command(msg, uid, OWNER_USER_ID)
        if closed_command_reply is not None:
            try:
                reply_line(token, closed_command_reply, QR_TOP)
            except Exception as e:
                logger.error(f"休業モードコマンド返信エラー: {e}")
            continue

        # ★ 休業日はAI応答より前に固定メッセージを返す
        if closed_mode.is_closed_today():
            try:
                reply_line(token, closed_mode.CLOSED_MESSAGE, QR_TOP)
            except Exception as e:
                logger.error(f"休業メッセージ返信エラー: {e}")
            save_log(uid, msg, closed_mode.CLOSED_MESSAGE)
            continue

        # ★ 手動モード中はAIを動かさない
        if user_state.get(uid) == "manual":
            logger.info(f"手動モード中のため無視: {uid[:8]}***")
            logger.info(f"メッセージ受信（手動モード中）: {uid[:8]}*** - {msg[:30]}")
            # ユーザーに確認メッセージを返信
            confirm_msg = "只今担当者が対応中です。少々お待ちください😊"
            try:
                reply_line(token, confirm_msg, QR_TOP)
                logger.info(f"確認メッセージを送信: {uid[:8]}***")
            except Exception as e:
                logger.error(f"確認メッセージ送信エラー: {e}")
            save_log(uid, msg, confirm_msg)
            continue

        # ★ 担当者相談ボタン専用の固定返答
        if msg == "担当者に相談したい":
            consult_reply = "確認いたしました。後ほどAIKAよりLINEをお送りします😊\nご質問があればお気軽にどうぞ。"
            try:
                reply_line(token, consult_reply, QR_TOP)
            except Exception as e:
                logger.error(f"LINE返信エラー: {e}")
            save_log(uid, msg, consult_reply)
            continue

        # ★ AI応答
        fallback = "少し調子が悪いみたいです💦\nもう一度送っていただけますか？"
        resp, err = fallback, False
        try:
            resp = sanitize_ai_reply(call_aika(uid, msg))
            # 会話履歴に追加
            add_to_history(uid, "user", msg)
            add_to_history(uid, "assistant", resp)
        except requests.exceptions.Timeout:
            save_error(uid, msg, "", "APIタイムアウト"); err = True
        except Exception as e:
            save_error(uid, msg, "", f"エラー: {e}"); err = True

        reply_text = fallback if err else resp
        qr = QR_TOP if err else choose_quick_reply(msg, resp)

        reply_sent = False
        try:
            reply_line(token, reply_text, qr)
            reply_sent = True
        except Exception as e:
            logger.error(f"LINE返信エラー: {e}")

        # ★ 引き継ぎフレーズを検出したら手動モードへ（送信成功時のみ）
        if not err and reply_sent and HANDOVER_PHRASE in resp:
            user_state[uid] = "manual"
            logger.info(f"手動モードへ切替: {uid[:8]}***")

        save_log(uid, msg, resp)

    return jsonify({"status": "ok"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "aika": "v5"})

if __name__ == "__main__":
    missing = [k for k in ["LINE_CHANNEL_SECRET", "LINE_ACCESS_TOKEN", "OPENROUTER_API_KEY"]
               if not os.environ.get(k)]
    if missing:
        logger.error(f"環境変数未設定: {', '.join(missing)}")
        exit(1)
    logger.info("FLATUP AIKA v5 起動中...")
    app.run(host="0.0.0.0", port=5000, debug=False)
