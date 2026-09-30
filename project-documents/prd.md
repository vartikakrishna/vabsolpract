# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## Facts-Only Mutual Fund RAG Assistant (INDMoney)

**Document Version:** 3.0.0  
**Author:** Principal Software Architect & Lead Product Manager  
**Architecture Pattern:** Unified Next.js (App Router) + Neon Serverless PostgreSQL + Google GenAI (Option B)  
**Target Launch Platform:** INDMoney Web Portal / Vercel Edge  
**Corpus Scope:** HDFC Mutual Fund (Primary AMC) + Mirae Asset Mutual Fund + SEBI + AMFI  
**Status:** Approved & Live (100% Ingestion & Safety Verification Passed)  

---

## 1. Executive Summary & Problem Statement

### 1.1 Executive Summary
The **Facts-Only Mutual Fund RAG Assistant** is an enterprise-grade, citation-backed, source-grounded conversational agent purpose-built for the **INDMoney** ecosystem. It provides instantaneous, 100% verified factual information regarding mutual fund schemes using exclusively official documentation from **HDFC Mutual Fund**, **Mirae Asset Mutual Fund**, **SEBI**, and **AMFI**.

### 1.2 Core Product Principle
> **"Facts only. Verified sources. No investment advice."**  
> Under no circumstances may the ingestion or retrieval engine synthesize investment recommendations, fund ratings, return predictions, buy/sell/hold suggestions, or personalized financial planning.

### 1.3 Scope of Primary Authoritative AMC Sources
1. **HDFC Mutual Fund AMC Root:** `https://www.hdfcfund.com/`
2. **HDFC Large Cap Fund (Direct Plan):** `https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct`
3. **HDFC Flexi Cap Fund (Direct Plan):** `https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct`
4. **HDFC ELSS Tax Saver Fund (Direct Plan):** `https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct`
5. **HDFC Large and Mid Cap Fund (Direct Plan):** `https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct`
6. **Mirae Asset Flagship Schemes & Regulatory Guidelines:** (Large Cap, Flexi Cap, ELSS, Midcap, SEBI Master Circulars, AMFI).

### 1.4 Technical Architecture Context (Option B)
To comply strictly with **Master Prompt Negative Rules #11 & #12** (prohibiting API key or database credential exposure in frontend bundles), the product is structured as a **unified Next.js (App Router) web application deployed to Vercel**. A lightweight serverless function (`app/api/chat/route.js`) securely handles PII filtering, query vector embedding via `gemini-embedding-001` (768 dimensions), Neon pgvector HNSW retrieval, and Multi-Model Gemini failover (`gemini-3.6-flash` cascade), while presenting an ultra-fast, responsive "Executive Gloss" interface to the investor.

---

## 2. Target Personas & User Journeys

### 2.1 Target Personas

| Persona | Demographics / Role | Motivations & Goals | Pain Points |
| :--- | :--- | :--- | :--- |
| **P1: Pragmatic Retail Investor** | 24–45 yrs old; active INDMoney user investing in SIPs/ELSS. | Needs exact, factual verification of scheme attributes (TER, exit load window, 80C eligibility). | Skeptical of AI hallucinations; frustrated by navigating 80-page Scheme Information Documents (SIDs). |
| **P2: First-Line Support Executive** | INDMoney Customer Experience Team. | Rapidly resolve customer scheme inquiries with official AMC backing. | High ticket volumes during tax-filing season regarding capital gains statements and redemption cutoffs. |
| **P3: Compliance & Risk Officer** | Internal Auditing & Legal. | Ensure automated tools never provide unauthorized portfolio or financial advice. | Legal liability from unauthorized financial recommendations or storage of customer PII. |

### 2.2 Five-Tier Query Classification & Decision Logic

Every user query is routed through a deterministic 5-category decision engine:

```text
                                  User Query
                                      │
                                      ▼
             ┌───────────────────────────────────────────────────┐
             │       Category E: PII Submission Interceptor      │
             └───────────────────────────────────────────────────┘
                                      │
                         [ Contains PAN/Aadhaar/OTP? ]
                                 ├── YES ──► REJECT IMMEDIATELY (Zero persistence)
                                 └── NO ───┐
                                           ▼
             ┌───────────────────────────────────────────────────┐
             │    Category C & D: Advice & Performance Gate      │
             └───────────────────────────────────────────────────┘
                                      │
                      [ Asks "Should I buy?", CAGR, etc.? ]
                                 ├── YES ──► POLITE FACTS-ONLY REFUSAL
                                 └── NO ───┐
                                           ▼
             ┌───────────────────────────────────────────────────┐
             │    Vector Similarity Search in Neon pgvector      │
             └───────────────────────────────────────────────────┘
                                      │
                       [ Top Chunk Similarity >= 0.65? ]
                                 ├── NO ───► Category B: UNVERIFIED FALLBACK
                                 └── YES ──► Category A: FACTUAL GROUNDED ANSWER
```

| Category | Definition | System Action & Response Rule |
| :--- | :--- | :--- |
| **Category A: Factual & In Scope** | Questions regarding factual scheme parameters documented in the verified corpus (TER, exit load, min SIP, lock-in, benchmark). | Retrieve top-K official chunks → Grounded Gemini answer (≤ 3 sentences) + 1 official URL citation + `Last updated from sources: [DATE]`. |
| **Category B: Factual but Unsupported** | Legitimate factual query whose exact answer is not present in the indexed official corpus. | Transparent refusal without hallucination: *"I couldn't verify that fact from the official sources available to me."* |
| **Category C: Investment Advice** | Queries seeking buy/sell/hold decisions, fund rankings, or personalized portfolio allocation. | Refuse politely. Explain assistant provides factual data only and does not provide investment advice. Provide official educational link where appropriate. |
| **Category D: Performance & Return Analysis** | Queries asking for return predictions, CAGR calculations, or comparison of past/future performance. | Refuse calculation/prediction. Link to official factsheet if available. |
| **Category E: PII Submission Attempt** | Queries containing or asking to store sensitive personal information (PAN, Aadhaar, OTP, account/folio numbers, phone, email). | Intercept before database or LLM transmission. Refuse storage. Instruct user never to share sensitive PII in chat. |

---

## 3. Grounding & Response Generation Rules

Every successful factual answer must satisfy the following constraints:
1. **Strictly Factual & Grounded:** Derived exclusively from retrieved official source chunks. General model knowledge is prohibited.
2. **Length Limit:** Maximum 3 clear, factual sentences.
3. **Mandatory Single Official Citation:** Exactly one verified official source hyperlink derived from retrieved chunk metadata.
4. **Freshness Indicator:** Displays `Last updated from sources: [DATE]` matching the source's verified timestamp.
5. **No Hallucinations:** Zero tolerance for invented numbers or scheme parameters.
6. **No Investment Recommendations:** Zero advisory language.

---

## 4. Evaluation Framework (W1, W2, W3 Skills)

* **W1 — Thinking Like a Model:** Rigorously discriminates between **Answer (Cat A)** vs. **Refuse (Cat C, D, E)** vs. **Unable to verify (Cat B)**.
* **W2 — LLMs & Prompting:** Grounding system prompts, concise sentence limits, anti-hallucination guardrails, and citation attachments.
* **W3 — RAG:** High-precision semantic retrieval, cosine similarity filtering (≥ 0.65), chunk contextual headers, and source freshness tracking.
