# Phase 1: トリアージ + JIN通知 実装計画書

> **For agentic workers:** このプランは bite-sized タスクで構成。各タスクは独立して完了できる。既存テストフレームワークなしのため、TDD は「期待動作の明示 + 手動検証 + ログ確認」で代用する。commit は実装単位でまとめてよい。

**Goal:** AIKA が回答を生成する前に、事故りやすい問い合わせを検知して JIN にエスカレーションする3層トリアージ機構を実装する。

**Architecture:** 既存 line_webhook.py の webhook() 内に triage.classify() を1点フックし、approval なら notify_jin() を呼んで manual モード化 + 待機メッセージを返す。auto なら既存パスを完全維持。

**Tech Stack:** Python 3.12 / Flask（既存）/ jpholiday（既存）/ requests（既存）/ json 標準ライブラリ / OpenRouter API（既存）/ LINE Messaging API Push（新規利用）

**Source spec:** `6_システム/PHASE1_DESIGN.md`

---

## Phase 0: Documentation / Code Discovery

実装前に確認済みの実コード情報。推測で差し込まないため、この節を根拠にする。

### 本番コードの確認元

- VPS: `/root/line_webhook.py`
- 確認日: 2026-05-12
- 本番サービス: `flatup-aika.service`
- 触らないサービス: `linebot.service`, `flatup-bot.service`

### 使用してよい既存API / 関数

| 既存名 | 場所 | 用途 |
|---|---:|---|
| `call_aika(uid, msg)` | 235行目付近 | AIKA応答生成 |
| `reply_line(token, msg, quick_items)` | 265行目付近 | LINE返信 |
| `save_log(user_id, q, a)` | 206行目付近 | 会話ログ保存、PIIマスク込み |
| `save_error(user_id, q, a, detail)` | 216行目付近 | エラーログ保存、PIIマスク込み |
| `add_to_history(uid, role, content)` | 187行目付近 | インメモリ会話履歴追加 |
| `mask_pii(text)` | 195行目付近 | 電話・メール・生年月日のマスク |
| `QR_TOP` | 既存定数 | 待機メッセージのQuick Reply |
| `user_state` | 既存グローバル | `"active"` / `"manual"` |
| `HANDOVER_PHRASE` | 既存定数 | 事後manual化の検出 |

### 実際のフック位置

`webhook()` 内の順序は以下。Phase 1 は「担当者に相談したい」固定返答の直後、「★ AI応答」の直前に入れる。

```text
1. /reset
2. manual状態チェック
3. 担当者相談ボタン専用の固定返答
4. ★ Phase 1 triage
5. ★ AI応答（既存）
```

### Anti-pattern Guards

- `call_aika()` の中身は変更しない。
- `reply_line()` の仕様を増やさない。
- `HANDOVER_PHRASE` による既存の事後manual化を消さない。
- `linebot.service` / `flatup-bot.service` は停止・再起動・編集しない。
- approval実機テストでは、manual状態に入るため、同じユーザーで連続テストする場合は `/reset` を挟む。

---

## File Structure

### 新規作成
| パス | 責務 | 行数目安 |
|---|---|---:|
| `6_システム/code/lib/__init__.py` | パッケージ宣言（空ファイル） | 1 |
| `6_システム/code/lib/triage.py` | 分類エンジン（3層判定）| ~100 |
| `6_システム/code/lib/notify.py` | LINE Push + 10分抑制 | ~60 |
| `6_システム/code/config/triage_rules.json` | 危険語・安全語の辞書 | JSON |
| `6_システム/code/config/triage_prompt.txt` | Layer 3 用LLMプロンプト | ~10 |

### 修正
| パス | 修正箇所 |
|---|---|
| `6_システム/code/line_webhook.py` | 1) import追加 2) webhook内でtriage呼び出し 3) approval経路ブロック |

### VPS配置先
| Vault | VPS |
|---|---|
| `6_システム/code/line_webhook.py` | `/root/line_webhook.py` |
| `6_システム/code/lib/*` | `/root/lib/*` |
| `6_システム/code/config/*` | `/root/config/*` |

---

## Task 1: triage_rules.json 作成

**Files:**
- Create: `6_システム/code/config/triage_rules.json`

- [ ] **Step 1: ファイルを作成**

内容（JSONとして妥当である必要あり）:

```json
{
  "danger_words": {
    "contract": [
      "確定", "キャンセル", "返金", "休会", "退会",
      "キャンペーン", "値引き", "割引", "変更"
    ],
    "complaint": [
      "ひどい", "不満", "困った", "怖い", "迷惑",
      "失礼", "ハラスメント", "セクハラ", "弁護士", "クレーム"
    ],
    "unknown": [
      "駐車場", "見学", "持ち物", "シャワー", "更衣室"
    ]
  },
  "safe_phrases": [
    "こんにちは", "ありがとう", "料金", "場所", "アクセス",
    "クラス", "体験", "予約", "キックボクシング", "ボクシング", "寝技",
    "何時から", "営業時間"
  ]
}
```

注意: 「料金」「予約」単独は danger_words に入れない（Q1反映: 体験申込みフローが誤検知される）。「キャンセル」「変更」など意図が明確な語のみ。`体験予約したい` は auto 候補にする。

- [ ] **Step 2: JSON 妥当性をローカル検証**

Run:
```bash
python3 -c "import json; print(json.load(open('6_システム/code/config/triage_rules.json'))['danger_words']['contract'])"
```
Expected: `['確定', 'キャンセル', '返金', '休会', '退会', 'キャンペーン', '値引き', '割引', '変更']`

- [ ] **Step 3: Commit**

```bash
cd "/Users/jin/Documents/Obsidian Vault"
git add 6_システム/code/config/triage_rules.json
git commit -m "feat(phase1): add triage_rules.json with danger/safe word dictionary"
```

---

## Task 2: triage_prompt.txt 作成

**Files:**
- Create: `6_システム/code/config/triage_prompt.txt`

- [ ] **Step 1: ファイルを作成**

内容:

```
あなたは FLATUP GYM の問い合わせを「auto」または「approval」に分類する補助 AI。

approval の基準:
- 数字・日付・契約に関わる（予約確定、料金例外、休会、退会、返金）
- クレーム・トラブル・不快表明
- データに無い質問（駐車場、見学、持ち物、個別事情）

それ以外（料金一般・場所・クラス紹介・雑談・挨拶）は auto。

迷ったら approval を選ぶ（事故防止優先）。
回答は1単語のみ: auto または approval
```

- [ ] **Step 2: 行数確認**

Run:
```bash
wc -l 6_システム/code/config/triage_prompt.txt
```
Expected: 10〜13行

- [ ] **Step 3: Commit**

```bash
git add 6_システム/code/config/triage_prompt.txt
git commit -m "feat(phase1): add triage_prompt.txt for Layer 3 LLM classifier"
```

---

## Task 3: lib/__init__.py 作成（空のパッケージ宣言）

**Files:**
- Create: `6_システム/code/lib/__init__.py`

- [ ] **Step 1: 空ファイル作成**

内容: 空（0 バイト）または以下の1行:

```python
# FLATUP AIKA Phase 1 lib package
```

- [ ] **Step 2: 確認**

Run:
```bash
ls -la 6_システム/code/lib/__init__.py
```
Expected: ファイル存在、サイズ 0 or 数十バイト

- [ ] **Step 3: Commit**

```bash
git add 6_システム/code/lib/__init__.py
git commit -m "feat(phase1): add lib/__init__.py package marker"
```

---

## Task 4: triage.py 実装

**Files:**
- Create: `6_システム/code/lib/triage.py`

- [ ] **Step 1: 完全コードを書く**

```python
"""Triage engine: 3層判定で auto/approval を分類する。

設計:
  Layer 0: 空文字 → approval (empty_message)
  Layer 1: danger_words ヒット → approval (reason key)
  Layer 2: safe_phrases のみで構成 → auto (safe)
  Layer 3: OpenRouter 軽量 LLM 判定
  失敗時: approval (fallback_error) ← fail-safe
"""

import json
import logging
import os
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

# 設定ファイルパス
RULES_PATH = Path("/root/config/triage_rules.json")
PROMPT_PATH = Path("/root/config/triage_prompt.txt")

# 起動時の最小デフォルト辞書（JSON 破損対策）
DEFAULT_DANGER = {
    "contract": ["確定", "キャンセル", "返金", "退会", "休会"],
    "complaint": ["ひどい", "苦情", "弁護士"],
    "unknown": ["駐車場", "見学"],
}
DEFAULT_SAFE = ["こんにちは", "ありがとう", "料金", "場所", "クラス", "体験", "予約"]
AMBIGUOUS_TIME_WORDS = ["今日", "明日", "今から", "このあと", "今夜", "すぐ"]

# 設定をロード（起動時1回）
def _load_rules():
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("danger_words", DEFAULT_DANGER), data.get("safe_phrases", DEFAULT_SAFE)
    except Exception as e:
        logger.error(f"triage_rules.json load failed, using defaults: {e}")
        return DEFAULT_DANGER, DEFAULT_SAFE

def _load_prompt():
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"triage_prompt.txt load failed: {e}")
        return None

DANGER_WORDS, SAFE_PHRASES = _load_rules()
TRIAGE_PROMPT = _load_prompt()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TRIAGE_MODEL = "anthropic/claude-haiku-4-5"
TRIAGE_TIMEOUT = 10  # 秒


def classify(msg: str) -> tuple[str, str]:
    """メッセージを (decision, reason) に分類。
    
    Returns:
        ("auto"|"approval", reason: str)
    """
    # Layer 0: 空文字
    if msg is None or msg.strip() == "":
        return ("approval", "empty_message")
    
    msg_norm = msg.strip()
    
    # Layer 1: danger_words ヒット
    for category, words in DANGER_WORDS.items():
        for w in words:
            if w in msg_norm:
                return ("approval", category)
    
    # Layer 2: safe_phrases のみで構成
    if _is_safe_query(msg_norm):
        return ("auto", "safe")
    
    # Layer 3: LLM 分類
    if TRIAGE_PROMPT is None:
        # プロンプトロード失敗時は安全側に
        return ("approval", "fallback_error")
    
    try:
        decision = _llm_classify(msg_norm)
        if decision == "auto":
            return ("auto", "llm_auto")
        elif decision == "approval":
            return ("approval", "llm_approval")
        else:
            return ("approval", "fallback_error")
    except Exception as e:
        logger.error(f"triage Layer 3 failed: {e}")
        return ("approval", "fallback_error")


def _is_safe_query(msg: str) -> bool:
    """明確に安全な短い問い合わせだけ auto にする。

    danger_words は先に判定済み。ここでは「料金教えて」「場所はどこ」
    のような定型質問を即autoにし、長い個別事情はLLMへ回す。
    """
    compact = msg.replace(" ", "").replace("　", "")
    if any(w in compact for w in AMBIGUOUS_TIME_WORDS):
        return False
    if len(compact) > 30:
        return False
    return any(p in compact for p in SAFE_PHRASES)


def _llm_classify(msg: str) -> str:
    """OpenRouter で軽量分類。戻り値は "auto" or "approval" or ""。"""
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    
    r = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://line.flatupnarita.jp",
            "X-Title": "FLATUP AIKA Triage",
        },
        json={
            "model": TRIAGE_MODEL,
            "messages": [
                {"role": "system", "content": TRIAGE_PROMPT},
                {"role": "user", "content": msg},
            ],
            "max_tokens": 5,
            "temperature": 0,
        },
        timeout=TRIAGE_TIMEOUT,
    )
    r.raise_for_status()
    resp = r.json()["choices"][0]["message"]["content"].strip().lower()
    if "approval" in resp:
        return "approval"
    elif "auto" in resp:
        return "auto"
    return ""
```

- [ ] **Step 2: 構文チェック**

Run:
```bash
python3 -m py_compile 6_システム/code/lib/triage.py && echo OK
```
Expected: `OK`

- [ ] **Step 3: 期待動作の手動検証（テスト用ローカルスクリプト、コミットしない）**

`/tmp/test_triage.py` を作成:

```python
# /tmp/test_triage.py（VPS配置後に動作確認用）
import sys
sys.path.insert(0, "/root")
from lib import triage

tests = [
    ("", "approval"),
    ("こんにちは", "auto"),
    ("料金教えて", "auto"),
    ("料金プラン教えて", "auto"),
    ("体験予約したい", "auto"),
    ("キャンセルしたいです", "approval"),
    ("ひどい対応", "approval"),
    ("駐車場ありますか", "approval"),
]
for msg, exp_dec in tests:
    dec, reason = triage.classify(msg)
    status = "OK" if dec == exp_dec else "FAIL"
    print(f"[{status}] msg={msg!r} expected={exp_dec} got=({dec}, {reason})")
```

このスクリプトは **VPS 配置後の Task 8 で実行** する。Mac 側ではimportパス都合で動かない。

- [ ] **Step 4: Commit**

```bash
git add 6_システム/code/lib/triage.py
git commit -m "feat(phase1): add triage.py with 3-layer classifier and fail-safe fallback"
```

---

## Task 5: notify.py 実装

**Files:**
- Create: `6_システム/code/lib/notify.py`

- [ ] **Step 1: 完全コードを書く**

```python
"""JIN への LINE Push 通知。10分ストーム抑制付き。

設計:
  - 同 uid に10分以内に通知済 → throttled
  - LINE Push 成功 → sent
  - 失敗 → failed (manual化と待機メッセージは続行)
"""

import logging
import os
from datetime import datetime, timezone, timedelta
from typing import Dict
import requests

logger = logging.getLogger(__name__)

LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
OWNER_USER_ID = "U521cd38b7f048be84eaa880ccabdc7f9"  # JIN
THROTTLE_MINUTES = 10
JST = timezone(timedelta(hours=9))

# インメモリで「最後に通知した時刻」を uid 単位で記録
# 再起動で消えるが、その場合は最初の検出が通知される（許容）
_last_notify_at: Dict[str, datetime] = {}


def _mask_uid(uid: str) -> str:
    """uid を先頭 8 文字 + *** にマスク。"""
    if not uid or len(uid) < 8:
        return "***"
    return uid[:8] + "***"


def _mask_pii(text: str) -> str:
    """PII を簡易マスク（line_webhook.py の mask_pii と同等の処理）。
    
    既存の mask_pii を import するのが理想だが、循環依存を避けるため
    notify 内では最小実装にする。詳細マスクは save_log 側で行う。
    """
    import re
    if not text:
        return text
    # 電話番号
    text = re.sub(r'(\d{3})[-\s]?(\d{3,4})[-\s]?(\d{4})', r'\1-****-\3', text)
    return text


def notify_jin(uid: str, msg: str, reason: str) -> dict:
    """JIN に LINE Push 通知。
    
    Returns:
        {"sent": bool, "throttled": bool, "error": str|None, "status": "sent"|"throttled"|"failed"}
    """
    now = datetime.now(JST)
    
    # ストーム抑制チェック
    last = _last_notify_at.get(uid)
    if last and (now - last).total_seconds() < THROTTLE_MINUTES * 60:
        logger.info(f"notify_jin throttled for uid={_mask_uid(uid)}")
        return {"sent": False, "throttled": True, "error": None, "status": "throttled"}
    
    # メッセージ組み立て
    ts_str = now.strftime("%Y-%m-%d %H:%M JST")
    body = (
        "【AIKA確認依頼】\n"
        f"理由: {reason}\n"
        f"User: {_mask_uid(uid)}\n"
        f"受信: {_mask_pii(msg)[:100]}\n"
        f"時刻: {ts_str}"
    )
    
    # LINE Push 送信
    access_token = os.environ.get("LINE_ACCESS_TOKEN", "")
    if not access_token:
        logger.error("notify_jin failed: LINE_ACCESS_TOKEN not set")
        return {"sent": False, "throttled": False, "error": "no_token", "status": "failed"}
    
    try:
        r = requests.post(
            LINE_PUSH_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            json={
                "to": OWNER_USER_ID,
                "messages": [{"type": "text", "text": body}],
            },
            timeout=10,
        )
        r.raise_for_status()
        _last_notify_at[uid] = now
        logger.info(f"notify_jin sent for uid={_mask_uid(uid)} reason={reason}")
        return {"sent": True, "throttled": False, "error": None, "status": "sent"}
    except Exception as e:
        logger.error(f"notify_jin LINE Push failed: {e}")
        return {"sent": False, "throttled": False, "error": str(e), "status": "failed"}
```

- [ ] **Step 2: 構文チェック**

Run:
```bash
python3 -m py_compile 6_システム/code/lib/notify.py && echo OK
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add 6_システム/code/lib/notify.py
git commit -m "feat(phase1): add notify.py with LINE Push and 10min throttle"
```

---

## Task 6: line_webhook.py 差分パッチ

**Files:**
- Modify: `6_システム/code/line_webhook.py`（既存の v5 をベースに）

⚠️ 前提: 現在 VPS 稼働中の `/root/line_webhook.py` をベースにする。SCP で取得 → Mac で編集 → Vault に保存 → 後で VPS に scp 戻し。

- [ ] **Step 1: 現行 line_webhook.py を Vault に取得**

Run:
```bash
scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  root@162.43.90.71:/root/line_webhook.py \
  "/Users/jin/Documents/Obsidian Vault/6_システム/code/line_webhook.py"
```
Expected: 転送成功、ファイル存在

- [ ] **Step 2: 差分パッチ1 - import 追加（ファイル先頭）**

修正前（既存のimport群、おおよそ7〜14行目あたり）:
```python
import os, hmac, re, hashlib, base64, json, logging, requests, jpholiday
from datetime import datetime, timezone, timedelta
from pathlib import Path
from flask import Flask, request, jsonify, abort
```

修正後（**最後の行** `from flask import ...` の **後** に1行追加）:
```python
import os, hmac, re, hashlib, base64, json, logging, requests, jpholiday
from datetime import datetime, timezone, timedelta
from pathlib import Path
from flask import Flask, request, jsonify, abort

from lib import triage, notify  # Phase 1
```

- [ ] **Step 3: 差分パッチ2 - webhook() 内に triage フック追加**

既存の webhook() 関数内、「★ 担当者相談ボタン専用の固定返答」ブロック の **直後**、「★ AI応答」ブロックの **直前** に、新規ブロックを挿入する。

挿入する内容:

```python
        # ★ Phase 1: 事前トリアージ
        try:
            decision, reason = triage.classify(msg)
        except Exception as e:
            logger.error(f"triage exception: {e}")
            decision, reason = "approval", "fallback_error"

        if decision == "approval":
            # JIN 通知
            try:
                notify_result = notify.notify_jin(uid, msg, reason)
                notify_status = notify_result.get("status", "failed")
            except Exception as e:
                logger.error(f"notify exception: {e}")
                notify_status = "failed"

            # manual モード化
            user_state[uid] = "manual"
            logger.info(f"approval triage: uid={uid[:8]}*** reason={reason} notify={notify_status}")

            # 履歴に短いマーカー（文脈保持）
            add_to_history(uid, "user", msg)
            add_to_history(uid, "assistant", "[担当者確認に切り替え済み]")

            # 待機メッセージ
            wait_msg = "確認が必要な内容のため、担当者より折り返しご連絡いたします😊"
            try:
                reply_line(token, wait_msg, QR_TOP)
            except Exception as e:
                logger.error(f"LINE返信エラー: {e}")

            # ログ保存
            save_log(uid, msg, f"[APPROVAL] reason={reason} notify={notify_status}")
            continue
```

`continue` で auto 経路（既存の AI 応答ブロック）をスキップ。auto 時はこの新規ブロック全体を素通りして既存パスへ。

- [ ] **Step 4: 差分パッチ3 - 確認（既存パスは変更なし）**

`★ AI応答` ブロック以降は **1 行も変更しない**。auto 経路は完全に既存挙動を維持する。

- [ ] **Step 5: 構文チェック**

Run:
```bash
python3 -m py_compile "/Users/jin/Documents/Obsidian Vault/6_システム/code/line_webhook.py" && echo OK
```
Expected: `OK`

- [ ] **Step 6: 行数比較**

Run:
```bash
wc -l "/Users/jin/Documents/Obsidian Vault/6_システム/code/line_webhook.py"
```
Expected: 元 386 行 + 約 28 行 = **約 414 行**

- [ ] **Step 7: Commit**

```bash
git add "6_システム/code/line_webhook.py"
git commit -m "feat(phase1): wire triage hook into webhook() with approval path"
```

---

## Task 7: VPS デプロイ前の最終ローカル検証

**Files:** なし（検証のみ）

- [ ] **Step 1: 全 Python ファイル構文チェック**

Run:
```bash
cd "/Users/jin/Documents/Obsidian Vault/6_システム/code"
PYTHONPYCACHEPREFIX=/private/tmp/pycache python3 -m py_compile lib/triage.py lib/notify.py line_webhook.py && echo ALL_SYNTAX_OK
```
Expected: `ALL_SYNTAX_OK`

- [ ] **Step 2: JSON 妥当性**

Run:
```bash
python3 -c "import json; json.load(open('config/triage_rules.json')); print('json ok')"
```
Expected: `json ok`

- [ ] **Step 3: import 構造の簡易確認（ローカルでは完全 import は不可）**

Run:
```bash
grep -E '^(from lib|import)' line_webhook.py | head -10
```
Expected: 既存の import + `from lib import triage, notify` が含まれる

---

## Task 8: VPS デプロイ

**Files:** VPS 側のみ操作

- [ ] **Step 1: 現行 VPS を最新バックアップ（cmpチェック付き）**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cp /root/line_webhook.py /root/line_webhook.py.bak_$(date +%Y%m%d)_phase1 && echo BACKUP_OK"
```
Expected: `BACKUP_OK`

```bash
TODAY=$(date +%Y%m%d)
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cmp -s /root/line_webhook.py /root/line_webhook.py.bak_${TODAY}_phase1 && echo BACKUP_MATCHES_CURRENT"
```
Expected: `BACKUP_MATCHES_CURRENT`

- [ ] **Step 2: VPS にディレクトリ作成**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "mkdir -p /root/lib /root/config && echo DIRS_OK"
```
Expected: `DIRS_OK`

- [ ] **Step 3: ファイル群を scp で配置**

```bash
cd "/Users/jin/Documents/Obsidian Vault/6_システム/code"

scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  lib/__init__.py lib/triage.py lib/notify.py \
  root@162.43.90.71:/root/lib/

scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  config/triage_rules.json config/triage_prompt.txt \
  root@162.43.90.71:/root/config/

scp -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes \
  line_webhook.py \
  root@162.43.90.71:/root/line_webhook.py
```
Expected: 全て転送成功（エラーなし）

- [ ] **Step 4: VPS 上で構文チェック・import 確認・JSON 妥当性（3つ）**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "/root/aika_env/bin/python3 -m py_compile /root/line_webhook.py /root/lib/triage.py /root/lib/notify.py && echo SYNTAX_OK"
```
Expected: `SYNTAX_OK`

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "cd /root && /root/aika_env/bin/python3 -c 'from lib import triage, notify; print(\"import ok\")'"
```
Expected: `import ok`

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "/root/aika_env/bin/python3 -c 'import json; json.load(open(\"/root/config/triage_rules.json\")); print(\"json ok\")'"
```
Expected: `json ok`

→ いずれか失敗の場合は Task 11 ロールバック手順へ。

- [ ] **Step 5: サービス再起動**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "systemctl restart flatup-aika && sleep 3 && systemctl is-active flatup-aika"
```
Expected: `active`

- [ ] **Step 6: smoke test（health + ログ確認）**

```bash
curl -fsS https://line.flatupnarita.jp/health
```
Expected: `{"aika":"v5","status":"ok"}`

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "journalctl -u flatup-aika -n 30 --no-pager | grep -iE 'error|exception|traceback' || true"
```
Expected: 出力なし、または既知の警告のみ

- [ ] **Step 7: トリアージ動作の単体確認（VPS 上で /tmp スクリプト実行）**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 << 'EOF'
cat > /tmp/test_triage.py << 'PYEOF'
import sys
sys.path.insert(0, "/root")
from lib import triage

tests = [
    ("", "approval"),
    ("こんにちは", "auto"),
    ("料金教えて", "auto"),
    ("料金プラン教えて", "auto"),
    ("体験予約したい", "auto"),
    ("キャンセルしたいです", "approval"),
    ("ひどい対応", "approval"),
    ("駐車場ありますか", "approval"),
]
for msg, exp in tests:
    dec, reason = triage.classify(msg)
    status = "OK" if dec == exp else "FAIL"
    print(f"[{status}] msg={msg!r} expected={exp} got=({dec}, {reason})")
PYEOF
/root/aika_env/bin/python3 /tmp/test_triage.py
rm -f /tmp/test_triage.py
EOF
```
Expected: 全 8 行が `[OK]`

注意: この単体確認はルール判定だけを通す。OpenRouterキーを読み込む必要はない。

---

## Task 9: 実機テスト 7 ケース（LINE から JIN が手動送信）

**Files:** なし（LINE で送信のみ）

- [ ] **Step 1: 手動モード解除（念のため）**

LINE で AIKA に送信:
```
/reset
```
Expected: `AIモードを再起動しました✅`

- [ ] **Step 2: ケース1 - auto 経路（挨拶）**

送信: `こんにちは`
Expected: AIKA 通常応答、JIN のスマホに通知なし

- [ ] **Step 3: ケース2 - auto 経路（料金）**

送信: `料金教えて`
Expected: 料金プラン回答、JIN 通知なし

- [ ] **Step 4: ケース3 - auto 経路（誤検知防止確認）**

送信: `料金プラン教えて`
Expected: 料金プラン回答、JIN 通知なし（「料金」が danger word に入っていないことの確認）

- [ ] **Step 5: ケース4 - approval 経路（contract）**

まず `/reset` を送ってAIモードへ戻す。

送信: `キャンセルしたいです`
Expected:
- JIN のスマホに LINE Push 通知 1 件（「【AIKA確認依頼】 理由: contract」）
- LINE トーク画面に `確認が必要な内容のため、担当者より折り返しご連絡いたします😊`

- [ ] **Step 6: ケース5 - approval 経路（complaint）**

まず `/reset` を送ってAIモードへ戻す。

送信: `ひどい対応されました`
Expected: JIN に通知 2 件目、トークに待機メッセージ

- [ ] **Step 7: ケース6 - approval 経路（unknown）**

まず `/reset` を送ってAIモードへ戻す。

送信: `駐車場ありますか`
Expected: JIN に通知 3 件目、トークに待機メッセージ

- [ ] **Step 8: ケース7 - throttled（10分以内に再度 approval 検出）**

まず `/reset` を送ってAIモードへ戻す。`/reset` はmanual状態を解除するが、`notify.py` の10分通知履歴は消さないため、同じuidのthrottled確認に使える。

送信: `退会したい`
Expected:
- トークに待機メッセージは届く
- JIN のスマホには通知 **来ない**（10 分以内の throttled）

- [ ] **Step 9: ログ確認**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 \
  "tail -50 /root/flatup_brain/LOGS/conversation_U521cd38b7f048be84eaa880ccabdc7f9.md | grep -E 'APPROVAL|notify' || echo NO_APPROVAL_LOG"
```
Expected: 4 件の `[APPROVAL] reason=X notify=Y` が記録されている（sent×3, throttled×1）

---

## Task 10: 仕様書・CLAUDE.md 更新

**Files:**
- Modify: `LINE_BOT_仕様.md`（「実装済み機能」セクションに Phase 1 追加）
- Modify: `CLAUDE.md`（「実装済み機能」セクションに Phase 1 追加）
- Create: `4_日記/2026-05-XX.md`（実装記録）

- [ ] **Step 1: 仕様書に Phase 1 完了を追記**

JIN が Obsidian で `LINE_BOT_仕様.md` の「実装済み機能」セクションに以下を追加:
```
- Phase 1 事前トリアージ + JIN 通知（lib/triage.py / lib/notify.py）
  - 3層判定（危険語 / 安全語 / 軽量LLM）
  - LINE Push で JIN にエスカレーション
  - 10分ストーム抑制
  - fail-safe（曖昧時は approval）
```

- [ ] **Step 2: CLAUDE.md にも同様の1行追加**

- [ ] **Step 3: 日記ファイル作成（実装日）**

`4_日記/2026-05-XX.md` に：
- 実装日時
- デプロイ手順サマリ
- 実機テスト結果
- 残った気付き

- [ ] **Step 4: Commit + push**

```bash
cd "/Users/jin/Documents/Obsidian Vault"
git add LINE_BOT_仕様.md CLAUDE.md "4_日記/2026-05-XX.md" "6_システム/code/"
git commit -m "feat(phase1): triage + notify deployed and verified in production"
git push origin main
```

---

## Task 11: ロールバック手順（緊急時のみ）

**Files:** VPS のみ

⚠️ 以下は Phase 1 デプロイで問題が起きた場合のみ実行。通常は使わない。

- [ ] **Step 1: 1コマンドロールバック**

```bash
ssh -i ~/.ssh/flatup_vps -o IdentitiesOnly=yes root@162.43.90.71 << 'EOF'
set -e
TODAY=$(date +%Y%m%d)
systemctl stop flatup-aika
cp /root/line_webhook.py.bak_${TODAY}_phase1 /root/line_webhook.py
ts="$(date +%Y%m%d-%H%M%S)"
mkdir -p "/root/phase1_disabled_$ts"
mv /root/lib/triage.py /root/lib/notify.py /root/lib/__init__.py "/root/phase1_disabled_$ts/" 2>/dev/null || true
mv /root/config/triage_rules.json /root/config/triage_prompt.txt "/root/phase1_disabled_$ts/" 2>/dev/null || true
systemctl start flatup-aika
sleep 2
systemctl is-active flatup-aika
EOF
```
Expected: `active`

- [ ] **Step 2: 外形確認**

```bash
curl -fsS https://line.flatupnarita.jp/health
```
Expected: `{"aika":"v5","status":"ok"}`

→ これで Phase 1 配置前の状態に完全復帰。所要 30 秒。

---

## ロードマップサマリ

```
Task 1-3  設定ファイル + パッケージ宣言    (15 分)
Task 4    triage.py 実装                     (30 分)
Task 5    notify.py 実装                     (20 分)
Task 6    line_webhook.py 差分               (15 分)
Task 7    ローカル検証                       (5 分)
Task 8    VPS デプロイ + smoke test          (10 分)
Task 9    実機テスト 7 ケース                (15 分)
Task 10   仕様書更新 + commit               (10 分)
─────────────────────────────────────
合計                                          約 2 時間
```

## デプロイ時間帯の推奨

- ✅ **日曜日（定休日）** ⭐⭐⭐
- ✅ 平日 22 時以降
- ❌ 平日 10-20 時（会員さんとの干渉）

## 成功定義

1. 全 9 Task が完了
2. 実機テスト 7 ケース全て期待通り
3. health endpoint が 200 OK
4. journalctl にエラーなし
5. JIN のスマホに approval 通知が 3 件届く + throttled 1 件届かない

## 完了後のスコア予測

```
現在:           83 / 100
Phase 1 完了:   86〜87 / 100  (+3〜4)
  - 機能完成度: 16/16 へ拡張（事前トリアージ）
  - 自動化:     +1（JIN 通知の自動化）
  - 運用性:     +1（事故防止層追加）
```
