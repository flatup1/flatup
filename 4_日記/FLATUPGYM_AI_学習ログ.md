# FLATUPGYM AI 学習ログ

このファイルは、FLATUPGYM AIが「次回もっと賢く動く」ための学習ログです。

AIが勝手に本番を変えるのではなく、JIN承認済みの改善・判断・失敗学習をここに残します。

## 書き方

```text
## YYYY-MM-DD タイトル

### 起きたこと
- 

### 学んだこと
- 

### 次からのルール
- 

### 反映先
- 
```

## 2026-05-17 Typefully連携はAPIキー本体を書かずに管理する

### 起きたこと

- Typefully APIはローカルPCから疎通確認できた。
- `flatupgym` の social set ID は `307036`。
- APIキーは `/Users/jin/.config/typefully/config.json` に保存する。
- Obsidian、README、GitHubにはAPIキー本体を書かない。

### 学んだこと

- 投稿自動化は便利だが、公開までAIに任せると危険。
- X投稿はTypefullyで下書き保存し、人間が確認してから公開・予約するのが安全。
- 1日5投稿、オリジナル比率70%以上、自動リプライ禁止を明文化する必要がある。

### 次からのルール

- Typefully関連の説明にはキー本体を書かない。
- AIは `--immediate` や即時公開操作を勝手に使わない。
- 参考ポストを使う場合も、FLATUPの経験と言葉に置き換える。

### 反映先

- `02_SKILLS_MARKETING/SNS/Typefully_X運用メモ_FLATUP.md`
- `6_システム/FLATUP_AI_OS_オーナー用コマンド早見表.md`
- `6_システム/FLATUPGYM_AI_機能一覧.md`

## 2026-05-17 FLATUPGYM AIはObsidianを脳、GitHubを成長履歴にする

### 起きたこと

- JINから「私の分身をObsidianで作り、GitHubで管理し、修正を繰り返し学習しながら賢くなるFLATUPGYM AIを作りたい」という方針が出た。
- 既存のAIOS、LINE Bot、SNS、Typefully、JIN Copilot、研究AIを一箇所で管理する必要が出た。

### 学んだこと

- 「賢くなる」は、AIが勝手に本番を変更することではない。
- Obsidianに判断と学びを残し、GitHubに履歴を残し、次回のAIがそれを読むことで賢くなる。
- 入口ファイルがないと、AIもJINも毎回どこから見ればいいか迷う。

### 次からのルール

- 新しいAI作業は `00_CORE/FLATUPGYM_AI_HOME.md` を入口にする。
- 機能追加・運用変更・重要な判断は、この学習ログへ追記する。
- GitHub push前に秘密情報が入っていないか確認する。

### 反映先

- `00_CORE/FLATUPGYM_AI_HOME.md`
- `6_システム/FLATUPGYM_AI_使い方.md`
- `6_システム/FLATUPGYM_AI_機能一覧.md`
- `6_システム/FLATUPGYM_AI_GitHub運用.md`
