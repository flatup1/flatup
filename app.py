import streamlit as st
import anthropic
import json
import os
import io
import csv
import calendar as cal_module
from pathlib import Path
from datetime import datetime, date

st.set_page_config(
    page_title="FLATUP GYM 集客マシン",
    page_icon="☀️",
    layout="wide"
)

# ── ファイルパス ──────────────────────────────────────────
BASE = Path(__file__).parent
KB_PATH      = BASE / "knowledge.json"
STATS_PATH   = BASE / "stats.json"
CALENDAR_PATH= BASE / "calendar_data.json"
TAGS_PATH    = BASE / "material_tags.json"

# ── データ読み書き ────────────────────────────────────────
with open(KB_PATH, encoding="utf-8") as f:
    KB = json.load(f)

def load_stats():
    if STATS_PATH.exists():
        return json.loads(STATS_PATH.read_text(encoding="utf-8"))
    return {"members":70,"monthly_revenue":600000,"google_reviews":7,
            "tiktok_followers":0,"instagram_followers":0,"youtube_subscribers":0,
            "trial_bookings_month":0,"history":[]}

def save_stats(data):
    STATS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_calendar():
    if CALENDAR_PATH.exists():
        return json.loads(CALENDAR_PATH.read_text(encoding="utf-8"))
    return []

def save_calendar(data):
    CALENDAR_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_tags():
    if TAGS_PATH.exists():
        return json.loads(TAGS_PATH.read_text(encoding="utf-8"))
    return {"files":[], "tags":{}}

def save_tags(data):
    TAGS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ── ナレッジテキスト ──────────────────────────────────────
def kb_text():
    g = KB["gym"]; f = KB["fees"]; s = KB["staff"]; u = KB["uizin"]
    return f"""
【FLATUP GYM 公式ナレッジ】
- ジム名：{g['name']}
- コンセプト：{g['concept']}
- 住所：{g['address']}
- 電話：{g['phone']}
- 哲学：{' / '.join(g['philosophy'])}
- 強み：{' / '.join(g['strengths'])}
- 会費：男性{f['male']}円 / 女性{f['female']}円 / キッズ{f['kids']}円 / 体験{f['trial']}円
- AIKA代表：{s['aika']['story']}
- 松元仁志会長：{s['hitoshi']['story']}
- キッズクラス：{KB['classes']['kids']['target']}、週3回（火木土）、月{KB['classes']['kids']['monthly_fee']}円
- UIZINイベント：{u['concept']} / ワンマッチ{u['fees']['one_match']}円 / トーナメント{u['fees']['tournament']}円
- スタイル：{KB['classes']['style']}
"""

# ── システムプロンプト ────────────────────────────────────
SYSTEM_PROMPT = f"""あなたは「FLATUP GYM 最強AI動画工場マシン」です。
TikTok ShopとInstagram Shopping（Reels）の両方に対応し、キッズ集客と自宅トレグッズ販売を同時に推進するFLATUP GYM専属AIです。
最短・最速・最低工数・最低価格でSNS拡散されやすく視聴維持率の高いショート動画を量産します。

{kb_text()}

---
### 【対応プラットフォーム】
- **TikTok Shop**：商品タグによる即時購入導線。テンポ重視・フック強め
- **Instagram Reels + Instagram Shopping**：ビジュアル重視・信頼感ある商品タグ付け
- **YouTube Shorts**：SEO重視・説明文に住所・電話

---
### 【動画構成テンプレート（全プラットフォーム共通・厳守）】
- 0〜3秒：強烈フック（「これ出来る子10%だけ」「顔に当たる瞬間が面白い」「プロが選んだ1位はコレ」）
- 3〜10秒：共感（失敗シーン・悩み映像・コミカル）
- 10〜20秒：解決（成功パンチ・キッズ笑顔・AIKA指導シーン）
- 20〜25秒：行動（商品タグ誘導 or 体験CTA）
- 最後5秒：**AIKA代表の実写笑顔を必ず挿入**（ハイブリッド人間AI・信頼感担保）

---
### 【CapCut 2026 高度編集テクニック（edit_tips・capcut_promptに必ず反映）】
- **Speed Ramp（最重要）**：パンチが当たる瞬間に必ず使用
  → 高速1.8倍 → スロー0.5倍 → 高速（Curveタブ → Bullet or Custom）
- **Keyframe**：当たる瞬間にScale 100%→115%ズームイン
- **Color Correction**：太陽のような明るい暖色（オレンジ・イエロー強調）
  → TikTok：鮮やかビビッド系 / Instagram：Dreamy・フィルム感
- **AI Auto Captions**：キーワード太字・オレンジ色・アニメーション・絵文字
  → TikTok：大胆・大きく / Instagram：控えめ・上品
- **Text Behind Subject**：被写体後ろにテロップ
- **Beat Sync**：Beat DetectionでBGMにリズム同期
- **AI Ultra HD / Sharpen**：画質向上（Pro推奨）
- 1カット1〜1.5秒。BGM：エネルギッシュ＋パンチ効果音（ボリューム40%）

---
### 【毎日3本ローテーション】
① キッズ部門（スピードボールチャレンジ・笑顔・保護者向け）
② 女性部門（産後ダイエット・AIKAストーリー・体型変化）
③ ジム連携部門（技・成長・体験500円・UIZIN大会）

---
### 【プラットフォーム別出力仕様】

**TikTok / TikTok Shop（デフォルト）：**
- ハッシュタグ8〜15個、15〜60秒、縦型9:16
- キャプション：簡潔＋コメント誘導（「コメントで○○→送ります」）
- Shop台本にはshop_tag_textフィールド追加（商品タグに表示するテキスト）
- platform："TikTok"

**Instagram Reels + Instagram Shopping（「IG:」で起動）：**
- ハッシュタグ5〜10個（厳選）、15〜90秒
- キャプション：感情に訴える文章・改行多用・最後に質問
- edit_tips：テロップ控えめ・上品・Dreamy/Vivid系カラー
- capcut_prompt：フィルム感あるカラーグレーディング
- instagram_shopping_tagフィールド追加（商品名・誘導文）
- platform："Instagram"

**YouTube Shorts（「YT:」で起動）：**
- titleにSEOキーワード必須（成田 キックボクシング / 格闘技 初心者 / キッズ 習い事 成田）
- descriptionフィールド：住所・電話・体験500円・URL
- thumbnail_textフィールド：サムネイルテキスト案
- ハッシュタグ3〜5個（#Shorts必須）
- platform："YouTube"

**全プラットフォーム同時（「ALL:」で起動）：**
- TikTok / Instagram / YouTube の3バージョンを同時生成
- 出力：JSON配列（platformフィールドで区別）

---
### 【投稿カレンダー生成（「カレンダー:」で起動）】
JSON配列（date/platform/time/category/title/hook/caption/hashtags/status:"pending" 全フィールド必須）
- TikTok毎日1本・Instagram週3本（月水金）・YouTube週2本（火土）で月30本以上
- カテゴリ比率：キッズ40%・女性30%・技成長15%・Shop10%・UIZIN5%
- 最適投稿時間：平日16〜19時、土日10〜12時

---
### 【出力ルール（厳守）】
- LP → 完全HTMLファイル（モバイルファースト・オレンジ×黄色・インラインCSS）
- 動画台本 → JSON配列（title/hook/script/visual_suggestions/caption/cta/edit_tips/capcut_prompt/platform 全フィールド必須）
- SNS投稿 → JSON配列（id/caption/hashtags/platform）
- LINEシナリオ → JSON（welcome/choices配列/cta）
- LINEメッセージ → JSON配列（type/message）
- CapCutプロンプト → そのままCapCutにコピペできる完全テキスト
- 今日の3本 → キッズ・女性・ジム連携 の3本セット（JSON）
- 動画ネタN個 → タイトル＋フック＋一言説明のJSON配列
- カレンダー → JSON配列

JSONのみ出力（コードブロック・説明文不要）。HTMLのみ出力（説明文不要）。

---
### 【TikTok Shop / Instagram Shopping アフィリエイトモード（「Shop:」で起動）】
- FLATUP GYMブランドの信頼性を活かした商品紹介台本を生成
- Speed Ramp・ビフォーアフター・AIKA実写を必ず含める
- TikTok用とInstagram用の両キャプションを出力
- 出力フィールド：title/hook/script/visual_suggestions/caption_tiktok/caption_instagram/cta/edit_tips/capcut_prompt/commission_note/shop_tag_text/instagram_shopping_tag/platform
- commission_note：報酬率目安・狙いどころ・選定理由

---
### 【戦略分析モード（「分析:」で起動）】
4人チームとして構造的に分析：
① リスクコンサルタント ② マーケティング戦略家 ③ 経営コンサルタント ④ 現場コーチ

分析ステップ：①リスク → ②顧客心理 → ③ビジネス構造 → ④改善戦略3つ
→ ⑤メリデメリスク → ⑥最適戦略1選 → ⑦最小コスト実行プラン → ⑧SNS拡散
→ ⑨紹介自然発生の仕組み → ⑩半年/1年/3年の長期成長戦略 → 成功確率★評価

Markdown形式で出力。全提案で「最短・最速・最低工数・最低コスト」を重視。"""

# ── Claude呼び出し ────────────────────────────────────────
def ask_claude(client, user_msg, history, use_sonnet=False):
    messages = history + [{"role": "user", "content": user_msg}]
    # 分析モードのみSonnet、それ以外はHaikuで節約
    is_analysis = user_msg.strip().startswith("分析:")  or "戦略分析" in user_msg
    model = "claude-sonnet-4-6" if (use_sonnet or is_analysis) else "claude-haiku-4-5-20251001"
    resp = client.messages.create(
        model=model,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return resp.content[0].text.strip()

def detect_output_type(text):
    t = text.strip()
    if t.startswith("<!DOCTYPE") or t.startswith("<html"):
        return "html"
    if t.startswith("[") or t.startswith("{"):
        try:
            json.loads(t)
            return "json"
        except:
            pass
    return "text"

def parse_json_safe(raw):
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("[") or part.startswith("{"):
                raw = part
                break
    return json.loads(raw.strip())

# ── 台本をknowledge.jsonに保存 ────────────────────────────
def save_scripts_to_kb(scripts):
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    saved = kb.setdefault("saved_scripts", [])
    for s in scripts:
        entry = {
            "id": len(saved) + 1,
            "title": s.get("title",""),
            "hook": s.get("hook",""),
            "category": s.get("category",""),
            "platform": s.get("platform","TikTok"),
            "saved_at": datetime.now().strftime("%Y-%m-%d"),
        }
        saved.append(entry)
    KB_PATH.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(scripts)

# ── 台本レンダリング ──────────────────────────────────────
PLATFORM_ICON = {"TikTok":"🎵","Instagram":"📸","YouTube":"▶️"}

def render_scripts(data, key_prefix):
    for i, s in enumerate(data):
        plat = s.get("platform","TikTok")
        icon = PLATFORM_ICON.get(plat,"📱")
        with st.expander(f"{icon} #{s.get('id','?')} {s.get('title','')}"):
            st.info(f"**フック:** {s.get('hook','')}")
            if s.get("thumbnail_text"):
                st.warning(f"🖼 サムネイル: {s.get('thumbnail_text','')}")
            st.text_area("台本", s.get("script",""), height=120,
                         key=f"sc_{key_prefix}_{i}", label_visibility="collapsed")
            if s.get("capcut_prompt"):
                with st.expander("CapCutプロンプト"):
                    st.text_area("", s.get("capcut_prompt",""), height=80,
                                 key=f"cp_{key_prefix}_{i}", label_visibility="collapsed")
            if s.get("commission_note"):
                st.warning(f"💰 {s.get('commission_note','')}")
            if s.get("shop_tag_text"):
                st.info(f"🛒 TikTok Shopタグ: {s.get('shop_tag_text','')}")
            if s.get("instagram_shopping_tag"):
                st.info(f"🛍 Instagram Shoppingタグ: {s.get('instagram_shopping_tag','')}")
            if s.get("caption_tiktok"):
                with st.expander("🎵 TikTokキャプション"):
                    st.text_area("", s.get("caption_tiktok",""), height=80,
                                 key=f"ctk_{key_prefix}_{i}", label_visibility="collapsed")
            if s.get("caption_instagram"):
                with st.expander("📸 Instagramキャプション"):
                    st.text_area("", s.get("caption_instagram",""), height=80,
                                 key=f"cig_{key_prefix}_{i}", label_visibility="collapsed")
            if s.get("description"):
                with st.expander("YouTube説明文"):
                    st.text_area("", s.get("description",""), height=80,
                                 key=f"desc_{key_prefix}_{i}", label_visibility="collapsed")
            st.caption(f"CTA: {s.get('cta','')}  |  {s.get('edit_tips','')}")
            st.write(s.get("caption",""))

def render_json_output(data, key_prefix):
    if isinstance(data, list) and data:
        first = data[0]
        if "hook" in first:
            col_a, col_b = st.columns([3,1])
            with col_a:
                st.download_button("⬇️ 台本JSONをダウンロード",
                                   data=json.dumps(data, ensure_ascii=False, indent=2),
                                   file_name="scripts.json", mime="application/json",
                                   key=f"dl_{key_prefix}")
            with col_b:
                if st.button("💾 ナレッジに保存", key=f"kb_{key_prefix}"):
                    n = save_scripts_to_kb(data)
                    st.success(f"{n}件保存しました")
            render_scripts(data, key_prefix)
        elif "date" in first:
            render_calendar_data(data, key_prefix)
        elif "caption" in first and "hashtags" in first:
            for p in data:
                plat = p.get("platform","")
                icon = PLATFORM_ICON.get(plat,"📱")
                with st.expander(f"{icon} 投稿 #{p.get('id','?')}"):
                    st.text_area("", p.get("caption",""), height=100,
                                 key=f"sns_{key_prefix}_{p.get('id','')}", label_visibility="collapsed")
                    hashtags = p.get("hashtags",[])
                    if isinstance(hashtags, list):
                        st.write("  ".join(hashtags))
                    else:
                        st.write(hashtags)
        elif "message" in first:
            for j, m in enumerate(data):
                st.markdown(f"**{m.get('type','')}**")
                st.text_area("", m.get("message",""), height=80,
                             key=f"lm_{key_prefix}_{j}", label_visibility="collapsed")
                st.markdown("---")
        else:
            st.json(data)
    elif isinstance(data, dict):
        if "welcome" in data:
            st.markdown("**ウェルカムメッセージ**")
            st.info(data.get("welcome",""))
            for c in data.get("choices",[]):
                with st.expander(f"▶ {c.get('label','')}"):
                    st.write(c.get("reply",""))
            st.success(f"**CTA:** {data.get('cta','')}")
        else:
            st.json(data)

def render_calendar_data(data, key_prefix):
    platforms = sorted({d.get("platform","TikTok") for d in data})
    selected_plat = st.multiselect(
        "プラットフォーム", platforms, default=platforms,
        key=f"cal_filter_{key_prefix}"
    )
    filtered = [d for d in data if d.get("platform","TikTok") in selected_plat]
    if not filtered:
        return

    # サマリー
    c1, c2, c3 = st.columns(3)
    c1.metric("合計", f"{len(filtered)}本")
    c2.metric("完成済み", len([d for d in filtered if d.get("status") == "done"]))
    c3.metric("投稿済み", len([d for d in filtered if d.get("status") == "posted"]))

    # テーブル表示
    rows = [{"日付": d.get("date",""), "時間": d.get("time",""),
             "媒体": d.get("platform",""), "カテゴリ": d.get("category",""),
             "タイトル": d.get("title",""), "ステータス": d.get("status","pending")}
            for d in filtered]
    st.dataframe(rows, use_container_width=True)

    # CSVエクスポート
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["date","platform","time","category","title","hook","caption","hashtags","status"])
    writer.writeheader()
    writer.writerows(filtered)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇️ CSVダウンロード", buf.getvalue(),
                           file_name="posting_calendar.csv", mime="text/csv",
                           key=f"csv_{key_prefix}")
    with col2:
        if st.button("💾 カレンダーに保存", key=f"save_cal_{key_prefix}"):
            existing = load_calendar()
            keys = {(e["date"], e.get("platform","")) for e in existing}
            new_items = [d for d in filtered if (d.get("date",""), d.get("platform","")) not in keys]
            save_calendar(existing + new_items)
            st.success(f"{len(new_items)}件保存しました")

# ════════════════════════════════════════════════════════
# サイドバー
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Claude API Key", type="password",
                             value=os.environ.get("ANTHROPIC_API_KEY",""))
    st.markdown("---")
    st.markdown("**🎯 プラットフォーム**")
    platform_mode = st.radio("", ["TikTok", "Instagram", "YouTube", "全部(ALL)"],
                              label_visibility="collapsed")
    PLATFORM_PREFIX = {"Instagram":"IG: ", "YouTube":"YT: ", "全部(ALL)":"ALL: "}

    st.markdown("---")
    st.markdown("**📝 クイック入力**")
    examples = [
        "今日の3本", "産後ママ向けLP", "UIZINキッズ台本10本",
        "カレンダー: 4月分", "動画ネタ20個", "CapCutプロンプト キッズ",
        "Shop: スピードボール 台本3本", "Shop: リフレックスボール 台本3本",
        "Shop: キッズ運動グッズ 台本3本",
        "分析: AI動画量産集客システム全体",
        "分析: UIZINキッズ集客企画",
    ]
    for e in examples:
        if st.button(e, key=f"ex_{e}", use_container_width=True):
            st.session_state["input_text"] = e
    st.markdown("---")
    if st.button("🗑 会話リセット", use_container_width=True):
        st.session_state["history"] = []
        st.session_state["messages_display"] = []
        st.rerun()

# ════════════════════════════════════════════════════════
# タブ
# ════════════════════════════════════════════════════════
tab_ai, tab_cal, tab_dash, tab_material = st.tabs([
    "🤖 AI工場", "📅 投稿カレンダー", "📊 ダッシュボード", "🎬 素材マッチング"
])

# ────────────────────────────────────────────────────────
# Tab 1: AI工場
# ────────────────────────────────────────────────────────
with tab_ai:
    st.title("☀️ FLATUP GYM 集客マシン")

    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "messages_display" not in st.session_state:
        st.session_state["messages_display"] = []

    for msg in st.session_state["messages_display"]:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "html":
                st.download_button("⬇️ LP HTMLをダウンロード", data=msg["content"],
                                   file_name="flatup_lp.html", mime="text/html",
                                   key=f"dl_html_h_{msg['id']}")
                st.components.v1.html(msg["content"], height=500, scrolling=True)
            elif msg.get("type") == "json":
                render_json_output(msg["parsed"], f"h_{msg['id']}")
            else:
                st.markdown(msg["content"])

    if not api_key:
        st.info("👈 サイドバーにClaude APIキーを入力してください")
    else:
        user_input = st.chat_input("何を作りますか？（例：今日の3本、IG: キッズ台本5本、カレンダー: 4月分）")
        if st.session_state.get("input_text"):
            user_input = st.session_state.pop("input_text")

        # プラットフォームプレフィックス自動付与
        if user_input and platform_mode in PLATFORM_PREFIX:
            pref = PLATFORM_PREFIX[platform_mode]
            skip = any(user_input.startswith(p) for p in ["IG:","YT:","ALL:","Shop:","分析:","カレンダー:","LP"])
            if not skip:
                user_input = pref + user_input

        if user_input:
            msg_id = len(st.session_state["messages_display"])
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state["messages_display"].append(
                {"role":"user","content":user_input,"type":"text","id":msg_id}
            )

            with st.chat_message("assistant"):
                with st.spinner("生成中..."):
                    client = anthropic.Anthropic(api_key=api_key)
                    try:
                        response = ask_claude(client, user_input, st.session_state["history"])
                        output_type = detect_output_type(response)
                        msg_id2 = len(st.session_state["messages_display"])

                        if output_type == "html":
                            st.download_button("⬇️ LP HTMLをダウンロード", data=response,
                                               file_name="flatup_lp.html", mime="text/html",
                                               key="dl_html_new")
                            st.components.v1.html(response, height=500, scrolling=True)
                            st.session_state["messages_display"].append(
                                {"role":"assistant","content":response,"type":"html","id":msg_id2}
                            )
                        elif output_type == "json":
                            data = parse_json_safe(response)
                            render_json_output(data, f"n_{msg_id2}")
                            st.session_state["messages_display"].append(
                                {"role":"assistant","content":response,"type":"json",
                                 "parsed":data,"id":msg_id2}
                            )
                        else:
                            st.markdown(response)
                            st.session_state["messages_display"].append(
                                {"role":"assistant","content":response,"type":"text","id":msg_id2}
                            )

                        st.session_state["history"].append({"role":"user","content":user_input})
                        st.session_state["history"].append({"role":"assistant","content":response})
                        if len(st.session_state["history"]) > 20:
                            st.session_state["history"] = st.session_state["history"][-20:]

                    except anthropic.AuthenticationError:
                        st.error("APIキーが無効です")
                    except Exception as e:
                        st.error(f"エラー: {e}")

# ────────────────────────────────────────────────────────
# Tab 2: 投稿カレンダー
# ────────────────────────────────────────────────────────
with tab_cal:
    st.header("📅 投稿カレンダー")

    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        cal_year = st.number_input("年", value=date.today().year, min_value=2024, max_value=2030)
    with col2:
        cal_month = st.number_input("月", value=date.today().month, min_value=1, max_value=12)
    with col3:
        cal_platforms = st.multiselect("対象媒体", ["TikTok","Instagram","YouTube"],
                                        default=["TikTok","Instagram","YouTube"])

    if not api_key:
        st.info("👈 サイドバーにAPIキーを入力してください")
    elif st.button("🗓 カレンダー生成", type="primary"):
        days = cal_module.monthrange(int(cal_year), int(cal_month))[1]
        plat_str = "・".join(cal_platforms)
        prompt = f"""カレンダー: {cal_year}年{cal_month}月の投稿カレンダーを生成してください。
対象プラットフォーム：{plat_str}
期間：{cal_year}-{cal_month:02d}-01 〜 {cal_year}-{cal_month:02d}-{days:02d}
条件：TikTok毎日1本、Instagram週3本（月水金）、YouTube週2本（火土）
カテゴリバランス：キッズ40%・女性30%・技成長15%・Shop10%・UIZIN5%"""
        with st.spinner("30本分生成中..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                response = ask_claude(client, prompt, [])
                data = parse_json_safe(response)
                st.session_state["cal_data"] = data
                st.success(f"✅ {len(data)}件生成しました")
            except Exception as e:
                st.error(f"エラー: {e}")

    if "cal_data" not in st.session_state:
        saved = load_calendar()
        if saved:
            st.session_state["cal_data"] = saved

    if st.session_state.get("cal_data"):
        render_calendar_data(st.session_state["cal_data"], "tab_cal")

    st.markdown("---")
    st.subheader("💾 保存済みカレンダー")
    saved_cal = load_calendar()
    if saved_cal:
        pending = len([c for c in saved_cal if c.get("status","pending") == "pending"])
        done    = len([c for c in saved_cal if c.get("status") == "done"])
        posted  = len([c for c in saved_cal if c.get("status") == "posted"])
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("合計保存", len(saved_cal))
        c2.metric("未着手", pending)
        c3.metric("完成済み", done)
        c4.metric("投稿済み", posted)
        if st.button("🗑 カレンダーをリセット"):
            save_calendar([])
            st.rerun()
    else:
        st.caption("まだカレンダーデータがありません")

# ────────────────────────────────────────────────────────
# Tab 3: ダッシュボード
# ────────────────────────────────────────────────────────
with tab_dash:
    st.header("📊 実績ダッシュボード")
    stats = load_stats()

    TARGETS = {
        "members": 150, "monthly_revenue": 1500000,
        "google_reviews": 100, "tiktok_followers": 10000,
        "instagram_followers": 3000, "youtube_subscribers": 1000,
    }

    # KPI更新フォーム
    with st.expander("📝 実績を更新", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            new_members  = st.number_input("会員数", value=stats.get("members",70), min_value=0)
            new_revenue  = st.number_input("月売上（円）", value=stats.get("monthly_revenue",600000), step=10000)
            new_reviews  = st.number_input("Google口コミ数", value=stats.get("google_reviews",7), min_value=0)
            new_trials   = st.number_input("今月の体験予約数", value=stats.get("trial_bookings_month",0), min_value=0)
        with col2:
            new_tiktok   = st.number_input("TikTokフォロワー", value=stats.get("tiktok_followers",0), min_value=0)
            new_ig       = st.number_input("Instagramフォロワー", value=stats.get("instagram_followers",0), min_value=0)
            new_yt       = st.number_input("YouTubeチャンネル登録", value=stats.get("youtube_subscribers",0), min_value=0)

        if st.button("💾 実績を保存", type="primary"):
            stats.update({
                "members": new_members, "monthly_revenue": new_revenue,
                "google_reviews": new_reviews, "trial_bookings_month": new_trials,
                "tiktok_followers": new_tiktok, "instagram_followers": new_ig,
                "youtube_subscribers": new_yt,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            stats.setdefault("history",[]).append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "members": new_members, "monthly_revenue": new_revenue,
                "google_reviews": new_reviews, "tiktok_followers": new_tiktok,
                "instagram_followers": new_ig, "youtube_subscribers": new_yt,
            })
            if len(stats["history"]) > 90:
                stats["history"] = stats["history"][-90:]
            save_stats(stats)
            st.success("✅ 保存しました")
            st.rerun()

    # KPIカード
    st.markdown("---")
    st.subheader("🎯 現状 vs 目標")
    stats = load_stats()

    c1, c2, c3 = st.columns(3)
    kpis = [
        ("c1", "👥 会員数", "members", f"人", f"目標{TARGETS['members']}人"),
        ("c1", "💰 月売上", "monthly_revenue", "¥", f"目標¥{TARGETS['monthly_revenue']:,}"),
        ("c2", "⭐ Google口コミ", "google_reviews", "件", f"目標{TARGETS['google_reviews']}件"),
        ("c2", "📋 体験予約(今月)", "trial_bookings_month", "件", "目標20件/月"),
        ("c3", "🎵 TikTok", "tiktok_followers", "人", f"目標{TARGETS['tiktok_followers']:,}人"),
        ("c3", "📸 Instagram", "instagram_followers", "人", f"目標{TARGETS['instagram_followers']:,}人"),
        ("c3", "▶️ YouTube", "youtube_subscribers", "人", f"目標{TARGETS['youtube_subscribers']:,}人"),
    ]
    col_map = {"c1": c1, "c2": c2, "c3": c3}
    for col_key, label, key, unit, delta in kpis:
        val = stats.get(key, 0)
        target = TARGETS.get(key, 20)
        display = f"¥{val:,}" if unit == "¥" else f"{val:,}{unit}"
        with col_map[col_key]:
            st.metric(label, display, delta=delta)
            st.progress(min(val / target, 1.0))

    if stats.get("last_updated"):
        st.caption(f"最終更新: {stats['last_updated']}")

    # 推移グラフ
    history = stats.get("history", [])
    if len(history) > 1:
        st.markdown("---")
        st.subheader("📈 推移グラフ")
        try:
            import pandas as pd
            df = pd.DataFrame(history).set_index("date")
            t1, t2, t3, t4 = st.tabs(["会員数","口コミ","TikTok","Instagram"])
            with t1: st.line_chart(df[["members"]])
            with t2: st.line_chart(df[["google_reviews"]])
            with t3: st.line_chart(df[["tiktok_followers"]])
            with t4: st.line_chart(df[["instagram_followers"]])
        except ImportError:
            st.info("グラフ表示には pandas が必要です: `pip install pandas`")

# ────────────────────────────────────────────────────────
# Tab 4: 素材マッチング
# ────────────────────────────────────────────────────────
with tab_material:
    st.header("🎬 動画素材マッチング")
    st.caption("撮影済み動画と台本シーンを自動マッチング")

    SCENE_TAGS = [
        "AIKA実写・笑顔","AIKA実写・指導","松元会長","キッズ笑顔・ハイタッチ",
        "ミット打ち正面","ミット打ち横","スピードボール","リフレックスボール",
        "ジム入口・外観","ジム内・雰囲気","女性クラス","産後ママ",
        "UIZIN大会","キッズ入場曲","集合写真","ランキングボード"
    ]

    # スキャン
    col1, col2 = st.columns([4,1])
    with col1:
        folder_path = st.text_input("素材フォルダ", value=str(Path.home() / "Desktop"),
                                     placeholder="/Users/jin/Desktop/FLATUP素材")
    with col2:
        scan = st.button("🔍 スキャン", use_container_width=True)

    if scan:
        folder = Path(folder_path)
        if folder.exists():
            files = sorted(
                list(folder.rglob("*.mp4")) + list(folder.rglob("*.mov")) +
                list(folder.rglob("*.MP4")) + list(folder.rglob("*.MOV")),
                key=lambda p: p.stat().st_mtime, reverse=True
            )[:50]
            st.session_state["material_files"] = [str(f) for f in files]
            st.success(f"✅ {len(files)}本の動画を検出")
        else:
            st.error("フォルダが見つかりません")

    material_files = st.session_state.get("material_files", [])
    tag_store = load_tags()

    if material_files:
        st.subheader("🏷 素材タグ付け")
        tag_data = tag_store.get("tags", {})
        for i, f in enumerate(material_files[:30]):
            fname = Path(f).name
            c1, c2 = st.columns([3,2])
            with c1:
                st.caption(f"📹 {fname}")
            with c2:
                selected = st.multiselect("", SCENE_TAGS, default=tag_data.get(fname,[]),
                                          key=f"tag_{i}", label_visibility="collapsed")
                tag_data[fname] = selected

        if st.button("💾 タグを保存"):
            save_tags({"files": material_files, "tags": tag_data})
            st.success("✅ 保存しました")
            st.rerun()

        # マッチング
        st.markdown("---")
        st.subheader("🔗 台本×素材マッチング")
        script_input = st.text_area("台本JSON（AI工場で生成したものを貼り付け）",
                                     height=120, placeholder='[{"id":1,"title":"..."}]')

        if script_input and api_key:
            if st.button("🎯 マッチング実行", type="primary"):
                tagged = {fname: tags for fname, tags in tag_data.items() if tags}
                if not tagged:
                    st.warning("まず素材にタグをつけてください")
                else:
                    try:
                        scripts = json.loads(script_input)
                        client = anthropic.Anthropic(api_key=api_key)
                        prompt = f"""以下の動画台本に対して、撮影済み素材の中から最適なファイルを推薦してください。

台本：
{json.dumps(scripts, ensure_ascii=False, indent=2)}

撮影済み素材（ファイル名: タグ一覧）：
{json.dumps(tagged, ensure_ascii=False, indent=2)}

出力：JSON配列
[{{"scene_id":1,"title":"","recommended_files":["ファイル名"],"scene_timing":"0-3秒フック","reason":"推薦理由"}}]"""
                        with st.spinner("マッチング中..."):
                            resp = client.messages.create(
                                model="claude-sonnet-4-6", max_tokens=2000,
                                messages=[{"role":"user","content":prompt}]
                            )
                            result = parse_json_safe(resp.content[0].text.strip())
                        for r in result:
                            with st.expander(f"#{r.get('scene_id')} {r.get('title','')} — {r.get('scene_timing','')}"):
                                for fname in r.get("recommended_files",[]):
                                    st.success(f"✅ {fname}")
                                st.caption(r.get("reason",""))
                    except Exception as e:
                        st.error(f"エラー: {e}")
    else:
        st.info("👆 素材フォルダのパスを入力してスキャンしてください")

    # 撮影推奨リスト
    st.markdown("---")
    st.subheader("📋 撮影推奨リスト")
    rec = {
        "🔴 最優先（すぐ撮る）": [
            "AIKA笑顔クローズアップ 5秒 × 3パターン（屋内・明るい）",
            "キッズ笑顔・ハイタッチシーン（保護者同意済み）",
            "ミット打ち正面スロー撮影（Speed Ramp用・60fps推奨）",
        ],
        "🟡 あると強い": [
            "松元会長の一言コメント動画（10〜15秒）",
            "産後ママ会員のビフォーアフターコメント（任意）",
            "ジム全体ウォークスルー（入口→フロア→練習シーン）",
        ],
        "🟢 あれば使える": [
            "スピードボール/リフレックスボール練習シーン",
            "UIZIN大会ハイライト（入場曲・試合・表彰）",
            "キッズランキングボードを指差すシーン",
            "体験者が笑顔で帰るシーン",
        ]
    }
    for cat, items in rec.items():
        with st.expander(cat):
            for item in items:
                st.markdown(f"- {item}")
