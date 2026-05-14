# 緊急休業モード設計

作成日: 2026-05-14

## 目的

インストラクター不在などで急遽レッスンを休みにする場合、AIKA が通常営業案内を返して来店事故を起こさないようにする。

## コマンド

オーナーのみ実行可能。

```text
/closed today
/closed YYYY-MM-DD
/closed list
/closed off
/open today
```

## 状態ファイル

本番:

```text
/root/config/closed_dates.json
```

Vault ミラー:

```text
6_システム/code/config/closed_dates.json
```

形式:

```json
{
  "closed_dates": []
}
```

## 判定ルール

- リクエストごとに JSON を読み込む。
- 今日の日付が `closed_dates` に含まれる場合、AI 応答より前に休業メッセージを返す。
- 過去日は自動無視する。cron は使わない。
- JSON が存在しない、または破損している場合は「休業なし」として扱う。

## 休業時メッセージ

```text
申し訳ございません🙇‍♀️
本日は急遽インストラクター不在のため、
レッスンをお休みさせていただきます。

ご来店前に必ずご確認のお願いを申し上げます。
次回以降のご質問はお気軽にお寄せください😊
```

Quick Reply は既存の `QR_TOP` を流用する。

## webhook フック位置

1. `/reset`
2. `/closed`, `/open`
3. 休業日判定
4. 手動モード中チェック
5. 担当者相談ボタン
6. Phase 1 トリアージ
7. AI 応答

休業判定は Phase 1 より前のグローバルフラグとして扱う。
