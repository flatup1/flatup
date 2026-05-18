export type RiskLevel = "低" | "中" | "高";

export interface ManualCompetitorInput {
  name?: string;
  url: string;
  area?: string;
  category?: string;
}

export interface SearchTask {
  keyword: string;
  area: string;
  status: "manual_review_required";
  note: string;
}

export interface FetchedPage {
  url: string;
  title: string;
  text: string;
  fetchedAt: string;
  error?: string;
}

export interface CompetitorAnalysis {
  name: string;
  area: string;
  url: string;
  category: string;
  price: string;
  trial_price: string;
  campaign: string;
  kids_offer: string;
  women_offer: string;
  beginner_offer: string;
  opening_hours: string;
  google_review_count: string;
  google_review_summary: string;
  sns_activity: string;
  strengths: string[];
  weaknesses: string[];
  flatup_opportunity: string;
  risk_level: RiskLevel;
  source_urls: string[];
}

export interface ReelScript {
  hook: string;
  body: string;
  captions: string;
  cta: string;
}

export interface MarketingIdeas {
  conclusions: string[];
  parentNeeds: string[];
  parentCopies: string[];
  womenNeeds: string[];
  womenCopies: string[];
  beginnerNeeds: string[];
  beginnerCopies: string[];
  lineMessages: {
    kids: string;
    women: string;
    beginner: string;
  };
  reels: {
    kids: ReelScript;
    women: ReelScript;
    beginner: ReelScript;
  };
  adCopies: {
    kids: string[];
    women: string[];
    beginner: string[];
  };
  actions: string[];
  humanReviewNotes: string[];
}
