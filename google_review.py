"""
FLATUP GYM Google口コミ依頼自動化
- メッセージ生成（コピペ用）
- LINE Messaging API経由で自動送信（オプション）
"""

import streamlit as st
import anthropic
import requests
import json
import os
from datetime import datetime

# ── 設定 ──────────────────────────────────────────────────
GOOGLE_REVIEW_URL = os.environ.get(
    "GOOGLE_REVIEW_URL",
    "https://search.google.com/local/writereview?placeid=ChIJ_S9fcrKLYjARsbc1sJ4Lq2s="
)
# バックアップURL（上が動かない場合はこちら）
GOOGLE_MAPS_URL = "https://maps.app.goo.gl/fR9V3Dn1BnWmtsJQ9"
LINE_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
GYM_PHONE = "07085484190"

# ── メッセージテンプレート ────────────────────────────────
TEMPLATES = {
    "キッズクラス（保護者向け）": """{name}さん、本日もお子様のご参加ありがとうございました！☀️
元気いっぱいに頑張っていましたよ🥊

もしよろしければ、Googleに口コミを書いていただけると
とても励みになります✨
（30秒で書けます！）
👇
{url}

また次回もお待ちしています！
FLATUP GYM AIKA""",

    "レディースクラス": """{name}さん、本日もご参加ありがとうございました！☀️
今日も全力で頑張りましたね🥊✨

お時間あればGoogleに感想を書いていただけると嬉しいです。
（星だけでも大歓迎です！）
👇
{url}

次回もお待ちしています😊
FLATUP GYM AIKA""",

    "体験レッスン後": """{name}さん、本日は体験レッスンにお越しいただき
ありがとうございました！☀️

ご感想をGoogleに書いていただけると
これから来てくださる方の参考になります🙏
（1〜2行でOKです！）
👇
{url}

ご入会・ご質問はいつでもどうぞ✨
FLATUP GYM {phone}""",

    "UIZIN大会参加後": """{name}さん（保護者様）、
本日のUIZIN大会、お疲れ様でした！🥊

お子様の勇気ある姿、本当に素晴らしかったです✨
もしよろしければ大会・ジムの感想をGoogleに書いていただけますか？
👇
{url}

次回のUIZINでもお待ちしています！
FLATUP GYM AIKA""",

    "カスタム（AIが生成）": None
}

# ── LINE送信 ──────────────────────────────────────────────
def send_line_message(user_id: str, message: str, token: str) -> bool:
    resp = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json={
            "to": user_id,
            "messages": [{"type": "text", "text": message}]
        }
    )
    return resp.status_code == 200

# ── UI ───────────────────────────────────────────────────
st.set_page_config(page_title="口コミ依頼ツール", page_icon="⭐", layout="centered")
st.title("⭐ Google口コミ依頼ツール")
st.caption("体験・レッスン後に送る口コミ依頼メッセージを自動生成")

with st.sidebar:
    st.header("設定")
    review_url = st.text_input(
        "Google口コミURL",
        value=GOOGLE_REVIEW_URL,
        help="Google マップ → 口コミ → 口コミを書く → URLをコピー"
    )
    api_key = st.text_input("Claude API Key（カスタム生成用）", type="password",
                             value=os.environ.get("ANTHROPIC_API_KEY", ""))
    line_token = st.text_input("LINE Token（自動送信用・任意）", type="password",
                                value=LINE_TOKEN)
    st.markdown("---")
    st.markdown("**現在の口コミ数**")
    current = st.number_input("件数", value=7, min_value=0)
    target = st.number_input("目標", value=100, min_value=1)
    progress = current / target
    st.progress(progress)
    st.caption(f"{current}件 / 目標{target}件（あと{target - current}件）")

# ── 入力 ──────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    member_name = st.text_input("会員名（さん付けなし）", placeholder="例：田中花子")
with col2:
    template_key = st.selectbox("テンプレート", list(TEMPLATES.keys()))

# カスタム生成の追加入力
custom_note = ""
if template_key == "カスタム（AIが生成）":
    custom_note = st.text_area("今日のエピソード・特記事項",
                                placeholder="例：初めてミット打ちができた、大会前最後の練習だった")

# ── メッセージ生成 ────────────────────────────────────────
if st.button("📝 メッセージ生成", type="primary", disabled=not member_name):
    if template_key == "カスタム（AIが生成）" and api_key:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""FLATUP GYM（成田市・世界一優しい格闘技ジム）のAIKA代表として、
会員{member_name}さんへのGoogle口コミ依頼LINEメッセージを作成してください。

今日のエピソード：{custom_note if custom_note else '通常レッスン'}
口コミURL：{review_url}
電話番号：{GYM_PHONE}

条件：
- 150文字以内
- 温かく自然なAIKAの口調
- 押しつけがましくない
- 口コミURLを必ず含める
- 「FLATUP GYM AIKA」で締める

メッセージ本文のみ出力。"""
        with st.spinner("生成中..."):
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
        message = msg.content[0].text.strip()
    elif template_key != "カスタム（AIが生成）":
        message = TEMPLATES[template_key].format(
            name=member_name,
            url=review_url,
            phone=GYM_PHONE
        )
    else:
        st.warning("カスタム生成にはClaude APIキーが必要です")
        st.stop()

    st.session_state["generated_message"] = message

# ── 結果表示 ──────────────────────────────────────────────
if "generated_message" in st.session_state:
    msg = st.session_state["generated_message"]

    st.markdown("---")
    st.markdown("**生成されたメッセージ**")
    st.text_area("", msg, height=200, label_visibility="collapsed")

    char_count = len(msg)
    st.caption(f"文字数: {char_count}文字")

    # コピー用
    st.code(msg, language=None)

    # LINE自動送信
    if line_token:
        st.markdown("---")
        st.markdown("**LINE自動送信**")
        line_user_id = st.text_input("送信先LINEユーザーID",
                                      placeholder="Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        if st.button("📱 LINEで送信", disabled=not line_user_id):
            if send_line_message(line_user_id, msg, line_token):
                st.success("✅ 送信しました！")
            else:
                st.error("送信失敗。ユーザーIDまたはトークンを確認してください。")
    else:
        st.info("LINE自動送信を使うには、サイドバーでLINE Tokenを設定してください")

# ── 一括生成 ──────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 一括生成（複数会員に送る）")
st.caption("CSVで名前リストを貼り付けると全員分まとめて生成")

names_input = st.text_area("会員名（1行1人）",
                             placeholder="田中花子\n佐藤太郎\n鈴木一郎",
                             height=100)
bulk_template = st.selectbox("テンプレート（一括）",
                               [k for k in TEMPLATES.keys() if k != "カスタム（AIが生成）"],
                               key="bulk_template")

if st.button("📋 一括生成", disabled=not names_input):
    names = [n.strip() for n in names_input.strip().split("\n") if n.strip()]
    results = []
    for name in names:
        msg = TEMPLATES[bulk_template].format(
            name=name, url=review_url, phone=GYM_PHONE
        )
        results.append({"name": name, "message": msg})

    for r in results:
        with st.expander(f"📩 {r['name']}さん"):
            st.text_area("", r["message"], height=150,
                         key=f"bulk_{r['name']}", label_visibility="collapsed")
            st.code(r["message"], language=None)

    st.download_button(
        "⬇️ JSONでダウンロード",
        data=json.dumps(results, ensure_ascii=False, indent=2),
        file_name=f"review_requests_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
