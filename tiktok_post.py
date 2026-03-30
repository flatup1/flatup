"""
FLATUP GYM TikTok自動投稿ツール
Streamlit UI + tiktok-uploader（Playwrightベース）

⚠️ 注意：
- cookies認証を使用。TikTokが仕様変更すると壊れる可能性あり
- 1日の投稿上限に注意（スパム判定リスク）
- 最初にcookiesを取得する必要あり（1回だけ）
"""

import streamlit as st
import subprocess
import json
import os
import sys
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="TikTok自動投稿", page_icon="🎵", layout="centered")
st.title("🎵 TikTok自動投稿ツール")
st.caption("動画ファイルを選んでワンクリック投稿")

# ── 警告 ──────────────────────────────────────────────────
st.warning("""
⚠️ **注意事項**
- cookies認証を使用します（1回セットアップが必要）
- TikTokの仕様変更で動かなくなる場合があります
- 1日3〜5本以内に抑えてください（スパム判定防止）
- 動画は事前にCapCutで完成させてから投稿してください
""")

# ── セットアップ確認 ──────────────────────────────────────
with st.expander("🔧 初回セットアップ（1回だけ）"):
    st.markdown("""
**Step 1: ライブラリインストール**
```bash
pip3 install tiktok-uploader playwright
playwright install chromium
```

**Step 2: cookies取得**
```bash
tiktok-uploader auth --browser chrome
```
→ ブラウザが開くのでTikTokにログイン → 自動でcookies保存

**Step 3: cookies.jsonのパスを確認**
```bash
ls ~/.tiktok-uploader/
```
""")

# ── 投稿設定 ──────────────────────────────────────────────
st.markdown("---")

video_path = st.text_input(
    "動画ファイルのパス",
    placeholder="/Users/jin/Desktop/動画/flatup_kids_01.mp4"
)

# CapCutからエクスポートした動画を自動検出
desktop_path = Path.home() / "Desktop"
mp4_files = list(desktop_path.rglob("*.mp4"))[:20]
if mp4_files:
    selected = st.selectbox(
        "またはDesktopから選択",
        ["（手動入力）"] + [str(p) for p in sorted(mp4_files, key=os.path.getmtime, reverse=True)]
    )
    if selected != "（手動入力）":
        video_path = selected

# ハッシュタグプリセット
HASHTAG_PRESETS = {
    "キッズ格闘技": "#FLATUPGYM #キッズ格闘技 #スピードボールチャレンジ #反射神経 #子供の習い事 #世界一優しい格闘技ジム #UIZIN #初陣",
    "女性・ダイエット": "#FLATUPGYM #世界一優しい格闘技ジム #キックボクシング女子 #ダイエット #ストレス発散 #産後ダイエット #初心者歓迎 #成田格闘技",
    "UIZIN大会": "#FLATUPGYM #UIZIN #初陣 #キッズ格闘技 #初心者大会 #勇気の一歩 #世界一優しい格闘技ジム #子供の成長",
    "スピードボール商品": "#スピードボール #パンチングボール #自宅トレ #反射神経 #FLATUPGYM #キッズ習い事 #ボクシングトレーニング #TikTokShop",
    "カスタム": ""
}

caption_text = st.text_area(
    "キャプション（投稿文）",
    placeholder="動画の説明文を入力...",
    height=100
)

hashtag_preset = st.selectbox("ハッシュタグ", list(HASHTAG_PRESETS.keys()))
if hashtag_preset == "カスタム":
    hashtags = st.text_input("ハッシュタグを入力", placeholder="#FLATUPGYM #キッズ格闘技")
else:
    hashtags = HASHTAG_PRESETS[hashtag_preset]
    st.code(hashtags)

full_caption = f"{caption_text}\n\n{hashtags}".strip()

# スケジュール投稿（オプション）
schedule_post = st.checkbox("スケジュール投稿")
if schedule_post:
    col1, col2 = st.columns(2)
    with col1:
        post_date = st.date_input("投稿日")
    with col2:
        post_time = st.time_input("投稿時刻")

# ── プレビュー ────────────────────────────────────────────
if caption_text or hashtags:
    with st.expander("📱 投稿プレビュー"):
        st.markdown(f"```\n{full_caption}\n```")
        st.caption(f"文字数: {len(full_caption)}")

# ── 投稿実行 ──────────────────────────────────────────────
st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    if st.button("🚀 今すぐ投稿", type="primary",
                  disabled=not (video_path and caption_text)):
        if not Path(video_path).exists():
            st.error(f"動画ファイルが見つかりません: {video_path}")
        else:
            # tiktok-uploaderコマンド構築
            cmd = [
                sys.executable, "-m", "tiktok_uploader",
                "--video", video_path,
                "--description", full_caption,
            ]

            with st.spinner("TikTokに投稿中...（1〜2分かかります）"):
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True, text=True, timeout=180
                    )
                    if result.returncode == 0:
                        st.success("✅ 投稿完了！")
                        # 投稿ログに記録
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "video": video_path,
                            "caption": full_caption[:50] + "...",
                            "status": "success"
                        }
                        log_path = Path(__file__).parent / "post_log.json"
                        logs = json.loads(log_path.read_text()) if log_path.exists() else []
                        logs.append(log_entry)
                        log_path.write_text(json.dumps(logs, ensure_ascii=False, indent=2))
                    else:
                        st.error(f"投稿失敗:\n{result.stderr}")
                        st.code(result.stdout)
                except subprocess.TimeoutExpired:
                    st.error("タイムアウト。cookiesが有効か確認してください。")
                except FileNotFoundError:
                    st.error("tiktok-uploaderがインストールされていません。\n`pip3 install tiktok-uploader` を実行してください。")

with col_b:
    if st.button("📋 キャプションだけコピー用に表示"):
        st.code(full_caption)

# ── 投稿ログ ──────────────────────────────────────────────
st.markdown("---")
st.subheader("📊 投稿履歴")
log_path = Path(__file__).parent / "post_log.json"
if log_path.exists():
    logs = json.loads(log_path.read_text())
    if logs:
        for log in reversed(logs[-10:]):
            status_icon = "✅" if log.get("status") == "success" else "❌"
            st.markdown(f"{status_icon} `{log['timestamp'][:16]}` — {log['caption']}")
    else:
        st.caption("まだ投稿履歴がありません")
else:
    st.caption("まだ投稿履歴がありません")

# ── GitHub Actions スケジュール設定 ──────────────────────
st.markdown("---")
with st.expander("⏰ GitHub Actionsで毎日自動実行する方法"):
    st.markdown("""
**毎日17時に自動投稿する設定例：**

`.github/workflows/tiktok_post.yml`
```yaml
name: TikTok Auto Post
on:
  schedule:
    - cron: '0 8 * * *'  # 毎日17時JST (UTC+9)
  workflow_dispatch:

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install tiktok-uploader playwright
      - run: playwright install chromium
      - run: python tiktok_post_cli.py
        env:
          TIKTOK_COOKIES: ${{ secrets.TIKTOK_COOKIES }}
```

⚠️ GitHub ActionsでのTikTok投稿はcookiesの維持が難しいため、
**手動またはMacのcronで動かす方が安定します。**
""")
