import test from "node:test";
import assert from "node:assert/strict";
import { generateReportMarkdown } from "../src/generateReport.js";
import type { CompetitorAnalysis, MarketingIdeas } from "../src/types.js";

test("generateReportMarkdown renders required sections and competitor table", () => {
  const competitors: CompetitorAnalysis[] = [
    {
      name: "サンプルジム",
      area: "成田市",
      url: "https://example.com",
      category: "キックボクシング",
      price: "不明",
      trial_price: "不明",
      campaign: "不明",
      kids_offer: "あり",
      women_offer: "不明",
      beginner_offer: "あり",
      opening_hours: "不明",
      google_review_count: "不明",
      google_review_summary: "不明",
      sns_activity: "不明",
      strengths: ["初心者訴求がある"],
      weaknesses: ["料金が見つけにくい"],
      flatup_opportunity: "初心者と親御さん向けに安心感を明確化する",
      risk_level: "低",
      source_urls: ["https://example.com"]
    }
  ];
  const ideas: MarketingIdeas = {
    conclusions: ["初心者向け訴求を前面に出す"],
    parentNeeds: ["安心できる運動教室"],
    parentCopies: ["運動が苦手な子の、はじめの一歩に。"],
    womenNeeds: ["怖くない雰囲気"],
    womenCopies: ["強さより、やさしさから始める。"],
    beginnerNeeds: ["最初の不安を減らしたい"],
    beginnerCopies: ["怖くない格闘技、成田にあります。"],
    lineMessages: {
      kids: "お子さまの運動不足や自信づくりに、やさしい格闘技を始めてみませんか？",
      women: "運動が久しぶりの方でも安心して始められます。",
      beginner: "最初は誰でも初心者です。体験から気軽にどうぞ。"
    },
    reels: {
      kids: { hook: "運動が苦手な子ほど、FLATUPに来てほしい", body: "先生が笑顔で褒める", captions: "できた！を増やす格闘技ジム", cta: "体験受付中。成田市 FLATUP GYM" },
      women: { hook: "怖くない格闘技、あります", body: "女性がミットを打つ", captions: "強さより、やさしさから始める", cta: "体験受付中" },
      beginner: { hook: "最初から強い人はいません", body: "基本からゆっくり練習", captions: "初心者歓迎", cta: "体験受付中" }
    },
    adCopies: {
      kids: ["最初から強い子なんていない。", "できた！を増やす格闘技。", "運動が苦手な子の、はじめの一歩に。"],
      women: ["怖くない格闘技、成田にあります。", "強さより、やさしさから始める。", "女性が安心して通えるジム。"],
      beginner: ["初心者のための格闘技ジム。", "怖くない。押し売りしない。", "最初の一歩をFLATUPで。"]
    },
    actions: ["LINE配信案を人間が確認する"],
    humanReviewNotes: ["この内容で実行・送信してよろしいですか？"]
  };

  const markdown = generateReportMarkdown("2026-05-17", competitors, ideas);

  assert.match(markdown, /# FLATUP GYM 競合・広告リサーチレポート/);
  assert.match(markdown, /## 2\. 競合調査まとめ/);
  assert.match(markdown, /\| サンプルジム \| 成田市 \| キックボクシング \| 不明 \| 不明 \| あり \| 不明 \| あり \|/);
  assert.match(markdown, /## 11\. 注意点・人間確認が必要なこと/);
});
