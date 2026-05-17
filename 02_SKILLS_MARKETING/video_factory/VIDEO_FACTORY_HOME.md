---
type: video_factory_home
updated: 2026-04-29
---

# Video Factory Home

目的: 既存素材から、最低工数・低コストで高品質なショート動画を量産する。

## 基本方針

- 素材がある場合、Sora/Veoなどの動画生成は主軸にしない。
- まずは Claude Code + FFmpeg + Whisper/faster-whisper + Remotion で回す。
- Premiere Pro / After Effects は必要なときだけ使う。
- 1本ごとの職人編集ではなく、テンプレートを育てて量産する。

## 現在の標準フロー

```text
素材フォルダ
  -> Claude Codeで素材確認
  -> Whisper系で文字起こし
  -> FFmpeg/video-useで粗編集
  -> Remotionテンプレで字幕・演出
  -> output/final.mp4
  -> このVaultにログ保存
```

## Active Templates

- [[templates/talking-head]]
- [[templates/list-short]]
- [[templates/story-short]]
- [[templates/promo-proof]]

## Master Briefs

- [[CODEX_REMOTION_X_MASTER_BRIEF]]

## Next Improvements

- 最初の勝ちテンプレを1つ作る
- 字幕デザインを固定する
- 10本作って修正パターンをログ化する
