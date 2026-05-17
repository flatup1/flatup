# FLATUPGYM AI GitHub運用

最終更新: 2026-05-17

このVaultはGitHub `flatup1/flatup` で管理します。

目的は、FLATUPGYM AIの記憶・仕様・改善履歴を失わないことです。

## 基本方針

- Obsidian VaultがAIの脳。
- GitHubが変更履歴。
- commitは「何を学んだか」「何を改善したか」がわかる単位で行う。
- APIキー、個人情報、認証情報は絶対にcommitしない。

## いつcommitするか

| タイミング | commitする |
|---|---|
| 新しい運用ルールを決めた | はい |
| 使い方メモを更新した | はい |
| AIKA人格・LINE Bot仕様を変更した | JIN承認後にcommit |
| SNS/Typefully運用を更新した | はい |
| 学習ログを追記した | はい |
| APIキーを設定した | いいえ |
| 個人情報を含むメモ | 原則commitしない |

## 安全なpush手順

```bash
cd "/Users/jin/Documents/Obsidian Vault"
git status --short
```

秘密情報チェック:

```bash
rg -n "api[_-]?key|secret|token|password|Bearer|tf_[A-Za-z0-9]|sk-[A-Za-z0-9]" .
```

必要なファイルだけ追加:

```bash
git add "00_CORE/FLATUPGYM_AI_HOME.md"
git add "6_システム/FLATUPGYM_AI_使い方.md"
git add "6_システム/FLATUPGYM_AI_機能一覧.md"
git add "6_システム/FLATUPGYM_AI_GitHub運用.md"
git add "4_日記/FLATUPGYM_AI_学習ログ.md"
```

commit:

```bash
git commit -m "docs: integrate flatup ai knowledge base"
```

push:

```bash
git push origin main
```

## AIに頼む時の言い方

```text
今回の変更を秘密情報チェックして、必要なファイルだけgit addして、commit/pushして。
```

```text
FLATUPGYM AIの学習ログを更新して、GitHubに残して。
```

```text
この変更は本番LINE Botに影響するか確認してからcommitして。
```

## commitメッセージ例

| 内容 | メッセージ |
|---|---|
| 使い方更新 | `docs: update flatup ai usage guide` |
| 学習ログ追加 | `docs: add flatup ai learning log entry` |
| Typefully運用 | `docs: document typefully x workflow` |
| LINE Bot仕様 | `docs: update aika line bot spec` |
| コード修正 | `fix: update line bot closed day handling` |

## AIの自動学習ループ

FLATUPGYM AIの学習は、次の流れで回します。

1. 実運用で起きたことをObsidianに書く。
2. AIが原因・判断・改善案に分ける。
3. JINが承認する。
4. 関連ファイルを更新する。
5. テストや確認をする。
6. GitHubにpushする。
7. 次回AIが `FLATUPGYM_AI_HOME.md` と学習ログを読んで再開する。

## 禁止

- `git reset --hard`
- force push
- APIキーや.envのcommit
- 会員個人情報のcommit
- JIN承認なしの本番仕様変更
- JIN承認なしのAIKA人格変更
