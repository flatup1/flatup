---
type: master_brief
updated: 2026-05-16
topic: codex_remotion_x_growth
---

# Codex + Remotion + X成長システム Master Brief

## Q: あなたは何を達成したいですか？

## A:

私は、Codex（OpenAI）＋Remotionを中心とした最新AIワークフローを活用して、X（旧Twitter）でバズり・成長するための高品質動画コンテンツを効率的に量産・運用したい。

具体的には、これまで深掘りした以下の要素をすべて統合して実践レベルで活用したい。

## 1. Codex + Remotion動画生成ワークフロー

- 月額約3000円（ChatGPT Plus相当）で、自然言語プロンプトだけでReactベースの高品質モーショングラフィックス動画を生成・編集・レンダリングしたい。
- 初心者でも「白背景にHello World」から始め、テキストアニメーション、画像・ロゴ挿入、BGM追加、視覚修正（スクショ貼り付け対応）、複数シーン構成までCodex内で一貫して完結。
- 1時間に複数本の長尺・ショート動画を自動生成できるレベルを目指す。
- Remotionの詳細な機能（アニメーション、画像処理、Ken Burns効果、Video Composition、オーディオ処理）を深く理解し、活用したい。

## 2. 2026年現在のXアルゴリズム最適化

- xAIのPhoenix Transformer（Grokベース）採用による新アルゴリズムを理解・対応。
- Dwell Time（滞在時間）の最大化、動画（特にモーショングラフィックス）の活用、Reply/Quoteを誘発する議論喚起、Author Diversity（連投回避）、スパム臭・煽り回避、初速重視（投稿タイミング）などを意識。
- Remotionで作った動画をXアルゴリズムに最適化した仕様（縦型1080x1920、Dwell Time重視、CTA明確など）で投稿・運用したい。

## 3. 先進AIエージェント構築

- Taiyo氏（@taiyo_ai_gakuse）の `/goal` プロンプトを使って、ブラウザ操作・Firecrawl検索・Prompt Caching付きのGenspark風フル機能AIエージェントWebアプリをCodex/Claude Codeで構築したい。
- 技術スタック：Vercel chatbotテンプレート起点、Convex DB、WorkOS Auth、Vercel AI SDK v6、Browserbaseなど最新ベストプラクティスを厳密に使用。
- このエージェントを基盤に、動画生成・X運用フロー全体をさらに自動化・拡張したい。

## Remotionに関する詳細設定

- デフォルト動画仕様：1080×1920、30fps、縦型、Modern Flat / High Contrastスタイル
- アニメーション：`useCurrentFrame` + `interpolate` + `spring` を厳密使用
- 画像：必ず `staticFile()` を使う
- オーディオ：Remotion公式の音声機能、必要に応じて `@remotion/media` 系を使う
- Ken Burns効果、`Sequence` によるシーン構成を使う
- これらをデフォルト設定（Master Prompt）として保存し、最短最速で高品質動画を生成できるようにする

## Q: 最終的な統合ビジョンは？

## A:

「Codex + Remotionで高品質動画を爆速量産 → Xアルゴリズムに最適化した投稿戦略で成長 → 自作AIエージェントで全プロセスを自動化」という一貫したAI駆動型コンテンツクリエイター/SNS運用システムを構築する。

## 重視してほしい点

- 実践的で即実行可能な手順・プロンプト例
- 初心者でも再現できる丁寧さ
- コスト最適化とスケーラビリティ
- 上記すべての要素を組み合わせた統合ワークフロー提案
- Remotionのデフォルト設定を適用した最短最速での動画生成

## AIに渡すときの使い方

この文書は、Codex / Claude Code / Claude / Gemini にそのまま貼り付けてよい。

依頼するときは、最後に以下を足す。

```md
上記を前提に、まず今日から動く最小ワークフローを作ってください。
大きな自動化より先に、Remotionテンプレ1つ、X投稿フォーマット1つ、制作ログ1つを作ってください。
```
