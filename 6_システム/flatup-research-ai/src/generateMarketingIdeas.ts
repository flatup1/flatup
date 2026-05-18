import { HUMAN_CONFIRMATION_TEXT } from "./safety.js";
import type { CompetitorAnalysis, MarketingIdeas } from "./types.js";

export function generateMarketingIdeas(competitors: CompetitorAnalysis[]): MarketingIdeas {
  const hasKidsGap = competitors.some((competitor) => competitor.kids_offer === "不明");
  const hasWomenGap = competitors.some((competitor) => competitor.women_offer === "不明");
  const hasBeginnerGap = competitors.some((competitor) => competitor.beginner_offer === "不明");

  return {
    conclusions: [
      hasBeginnerGap ? "初心者の不安を減らす訴求を前面に出す" : "初心者歓迎の具体例を継続発信する",
      hasKidsGap ? "キッズは強さより自己肯定感を訴求する" : "キッズの成長ストーリーを投稿化する",
      hasWomenGap ? "女性が安心できる雰囲気を写真・動画で見せる" : "女性向けの安心導線をLINE文にも反映する"
    ],
    parentNeeds: ["子どもが怖がらず始められること", "先生が安全に見てくれること", "運動が苦手でも続けられること"],
    parentCopies: [
      "運動が苦手な子の、はじめの一歩に。",
      "最初から強い子なんていない。",
      "勝ち負けより、挑戦できた自分を好きになる。"
    ],
    womenNeeds: ["怖くない雰囲気", "初心者でも浮かないこと", "押し売りされない安心感"],
    womenCopies: [
      "怖くない格闘技、成田にあります。",
      "強さより、やさしさから始める。",
      "運動が久しぶりの方でも、最初の一歩から。"
    ],
    beginnerNeeds: ["何を準備すればいいか知りたい", "ついていけるか不安", "ガチ勢ばかりではないと知りたい"],
    beginnerCopies: [
      "初心者のための格闘技ジム。",
      "殴り合う場所じゃない。自分を好きになる場所。",
      "できた！を増やす、やさしい格闘技。"
    ],
    lineMessages: {
      kids: "お子さまの運動不足や自信づくりに、キックボクシングを始めてみませんか？😊\nFLATUP GYMは、初心者のお子さまでも安心して通えるやさしい格闘技ジムです。\n強くなる前に、まず「できた！」を増やすことを大切にしています。\n体験をご希望の方は、ご希望の曜日と時間帯をお送りください。",
      women: "運動が久しぶりの方でも、FLATUP GYMなら安心して始められます。\n怖い雰囲気や押し売りではなく、やさしく続けられる格闘技フィットネスです。\n体験をご希望の方は、ご希望の曜日と時間帯をお送りください。",
      beginner: "格闘技が初めてでも大丈夫です。\nFLATUP GYMは、最初の一歩をやさしくサポートする成田市の格闘技ジムです。\nまずは体験で、雰囲気だけ見に来てください。"
    },
    reels: {
      kids: {
        hook: "運動が苦手な子ほど、FLATUPに来てほしい",
        body: "子どもがミットを打つ。先生が笑顔で褒める。最後に親子で笑う。",
        captions: "最初から強い子なんていない。\nできた！を増やす格闘技ジム。",
        cta: "体験受付中。成田市 FLATUP GYM"
      },
      women: {
        hook: "怖くない格闘技、成田にあります",
        body: "女性がゆっくり基本練習。ミット打ち後に笑顔。無理なく汗をかく。",
        captions: "強さより、やさしさから始める。\n初心者・女性歓迎。",
        cta: "体験受付中。FLATUP GYM"
      },
      beginner: {
        hook: "最初から強い人はいません",
        body: "構え方から丁寧に説明。初めてのミット。小さくガッツポーズ。",
        captions: "できた！を増やす格闘技。\n初心者の一歩を応援します。",
        cta: "成田市で体験受付中"
      }
    },
    adCopies: {
      kids: ["最初から強い子なんていない。", "運動が苦手な子の、はじめの一歩に。", "できた！を増やす格闘技ジム。"],
      women: ["怖くない格闘技、成田にあります。", "女性が安心して通える格闘技ジム。", "強さより、やさしさから始める。"],
      beginner: ["初心者のための格闘技ジム。", "殴り合う場所じゃない。自分を好きになる場所。", "まずは体験で、雰囲気だけ見に来てください。"]
    },
    actions: [
      "手動で競合URLを data/competitors.manual.json に3件追加する",
      "キッズ向けLINE文を人間が確認する",
      "女性向けリールを1本撮る",
      "初心者向け広告コピーを1案だけテストする",
      "反応が良かった表現を次週のレポートに残す"
    ],
    humanReviewNotes: [
      "LINE配信文・広告コピー・投稿文は送信前に必ず人間が確認する",
      "料金・体験条件は最新情報と照合してから使う",
      HUMAN_CONFIRMATION_TEXT
    ]
  };
}
