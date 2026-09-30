# FACTS-ONLY MF ASSISTANT — MASTER IMPLEMENTATION PLAN (OPTION B: NEXT.JS ON VERCEL)

## 1. Executive Summary

The **Facts-Only Mutual Fund RAG Assistant** is a compliance-first, citation-backed conversational agent designed for **INDMoney** retail investors, customer support, and content teams.

The product's governing principle is absolute:
> **"Facts only. Verified sources. No investment advice."**

Following our architectural deep dive, the project is structured as **Option B: A Unified Next.js (App Router) Application deployed natively to the Vercel Web Portal**. This architecture provides the exact simplicity of having a single frontend project to manage, while leveraging lightweight Vercel Serverless Functions (`app/api/chat/route.js`) to guarantee that **database passwords and Gemini API keys are never exposed in browser network responses** (strictly satisfying Master Prompt Negative Rules #11 & #12).

---

## 2. Verified Infrastructure & Credentials Audit

| Infrastructure Item | Verification Status | Architectural Implementation in Option B |
| :--- | :--- | :--- |
| **Neon PostgreSQL** | `postgresql://neondb_owner:npg_b1cyE8oAPfCs@ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require` (Postgres 18.6) | Accessed over Neon Serverless HTTP API (`/sql`) from Vercel Serverless Route Handler using `DATABASE_URL` stored in `.env.local` / Vercel Environment Variables. `vector` extension verified active. |
| **Gemini AI API** | `AQ.Ab8RN6JXmbSM0kd88Dh7RTwqouoBhgyEM9-vsVxD3y5t6Fn4Tg` (Google GenAI REST) | Stored as `GEMINI_API_KEY` on serverless edge. Drives `text-embedding-004` and the 4-tier model failover cascade (`gemini-2.5-flash` → `2.0-flash` → `1.5-flash` → `1.5-pro`). |
| **Hosting Platform** | Vercel Web Portal | Single Git repository deploy. Zero server maintenance, instant preview builds, automatic HTTPS. |

---

## 3. High-Level Architecture (Option B)

```text
+-----------------------------------------------------------------------------------------------+
|                                    USER BROWSER / CLIENT                                      |
|                             Next.js Client Components (React 19)                              |
|   - "Executive Gloss" Dark Slate Theme (#07090E)      - 3 One-Click Factual Quick Pills        |
|   - Welcome Banner (Strict Facts-Only Scope)          - Verified Citation Hyperlink Badges    |
|   - Responsive Chat Stream (<= 3 Sentences)           - Persistent Footer Disclaimer          |
+-----------------------------------------------------------------------------------------------+
                                                │
                                                │ HTTPS POST /api/chat (query)
                                                ▼
+-----------------------------------------------------------------------------------------------+
|                      VERCEL SERVERLESS EDGE LAYER: app/api/chat/route.js                      |
|                                                                                               |
|  1. In-Memory PII Gate (Regex: PAN, Aadhaar, Phone, OTP, Email)                               |
|     -> Immediate rejection with security disclaimer (Zero storage, zero logging)              |
|                                                                                               |
|  2. Investment Advice & Return Projection Gate                                                |
|     -> Immediate polite compliance refusal: "Facts-only. No investment advice."               |
|                                                                                               |
|  3. Query Vector Embedding via Google GenAI REST: text-embedding-004                          |
|     -> Produces 768-dimensional normalized dense vector                                       |
|                                                                                               |
|  4. Neon Vector Similarity Search via Serverless HTTP SQL API (/sql):                         |
|     SELECT c.chunk_text, s.url, s.title, s.last_verified_at,                                  |
|            1 - (c.embedding <=> $1::vector) AS similarity                                     |
|     FROM chunks c JOIN sources s ON c.source_id = s.id                                        |
|     WHERE 1 - (c.embedding <=> $1::vector) >= 0.65                                            |
|     ORDER BY similarity DESC LIMIT 4;                                                         |
|                                                                                               |
|  5. Multi-Model Gemini Failover Cascade Engine:                                               |
|     Primary:    gemini-2.5-flash  (SOTA speed & grounding fidelity)                           |
|        │ (on HTTP 429 rate limit, 503, or timeout)                                            |
|        ▼                                                                                      |
|     Tier 1:     gemini-2.0-flash  (Next-generation stable fallback)                          |
|        │ (on error)                                                                           |
|        ▼                                                                                      |
|     Tier 2:     gemini-1.5-flash  (High-availability workhorse)                               |
|        │ (on error)                                                                           |
|        ▼                                                                                      |
|     Tier 3:     gemini-1.5-pro    (Deep statutory reasoning fallback)                       |
|                                                                                               |
|  6. Grounding Validation & Truncation:                                                        |
|     - Answer strictly derived from retrieved text; if missing: "I couldn't verify..."         |
|     - Post-generation programmatic clamp to <= 3 sentences                                    |
|     - Exact official URL and last_verified_at injected from database metadata                 |
+-----------------------------------------------------------------------------------------------+
                             │                                           │
              HTTPS /sql API │ (Neon-Connection-String)   HTTPS REST API │ (GEMINI_API_KEY)
                             ▼                                           ▼
             +-------------------------------+           +-------------------------------+
             |       Neon PostgreSQL         |           |       Google Generative AI    |
             |   (Project b5vklo5s)          |           |   (Account vabsoldigital...)  |
             | - pgvector HNSW Index         |           | - text-embedding-004          |
             | - 18 Official Sources Seeded  |           | - Gemini Model Cascade        |
             | - Auto-scaling & pooled conn  |           | - Sub-second latency          |
             +-------------------------------+           +-------------------------------+
```

---

## 4. Official Source Corpus (18 Verified Public Sources)

| # | Organization | AMC | Scheme / Subject | Document / Page Title | Verified Official URL | Fact Types Extracted |
|---|---|---|---|---|---|---|
| 1 | AMC | Mirae Asset | Large Cap Fund | Scheme Overview & Performance Page | `https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-large-cap-fund` | Expense ratio, AUM, Benchmark, Riskometer |
| 2 | AMC | Mirae Asset | Large Cap Fund | Scheme Information Document (SID) / KIM | `https://www.miraeassetmf.co.in/downloads/regulatory/scheme-information-documents` | Min SIP, Min Lumpsum, Exit Load, Objective |
| 3 | AMC | Mirae Asset | Flexi Cap Fund | Scheme Overview Page | `https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund` | Benchmark (Nifty 500 TRI), Riskometer, Plan types |
| 4 | AMC | Mirae Asset | Flexi Cap Fund | Key Information Memorandum (KIM) | `https://www.miraeassetmf.co.in/downloads/regulatory/key-information-memorandum` | Exit load tiers, Min initial investment, Allotment date |
| 5 | AMC | Mirae Asset | ELSS Tax Saver Fund | Scheme Overview Page | `https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund` | Statutory 3-year lock-in, Benchmark, Riskometer |
| 6 | AMC | Mirae Asset | ELSS Tax Saver Fund | Statutory Details & KIM | `https://www.miraeassetmf.co.in/downloads/regulatory/scheme-information-documents` | Section 80C tax deduction, Min investment (₹500), Exit load (Nil) |
| 7 | AMC | Mirae Asset | Midcap Fund | Scheme Overview Page | `https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-midcap-fund` | Benchmark (Nifty Midcap 150 TRI), Expense ratio |
| 8 | AMC | Mirae Asset | Midcap Fund | Key Information Memorandum (KIM) | `https://www.miraeassetmf.co.in/downloads/regulatory/key-information-memorandum` | Min SIP, Exit load (1% within 1 year), Fund managers |
| 9 | AMC | Mirae Asset | General / All Schemes | Investor Service: Account Statement | `https://www.miraeassetmf.co.in/investor-services/account-statement` | Account statement download process, CAS generation |
| 10 | AMC | Mirae Asset | General / All Schemes | Investor Service: Capital Gains | `https://www.miraeassetmf.co.in/investor-services/capital-gains-statement` | Capital gains statement download steps, tax filing guidance |
| 11 | AMC | Mirae Asset | General / All Schemes | General FAQs on KYC & Folio Operations | `https://www.miraeassetmf.co.in/faqs/general-faqs` | Folio lookup, KYC status check, nominee registration |
| 12 | AMC | Mirae Asset | General / All Schemes | Monthly Factsheet Bulletin | `https://www.miraeassetmf.co.in/downloads/factsheet` | Total Expense Ratios (Regular vs Direct), portfolio turnover |
| 13 | AMFI | AMFI | General / All Schemes | AMFI Riskometer Guidelines | `https://www.amfiindia.com/investor-corner/knowledge-center/riskometer.html` | Riskometer 6-tier classification (Low to Very High), review norms |
| 14 | AMFI | AMFI | General / All Schemes | AMFI Minimum SIP Rules & Mechanics | `https://www.amfiindia.com/investor-corner/knowledge-center/sip.html` | SIP frequency, mandates, ECS/NACH procedure, pauses |
| 15 | AMFI | AMFI | General / All Schemes | AMFI Total Expense Ratio (TER) Rules | `https://www.amfiindia.com/research-information/ter-data` | Statutory TER caps under SEBI Regulation 52, Direct vs Regular |
| 16 | SEBI | SEBI | General / Mutual Funds | SEBI Categorization Circular (Oct 2017) | `https://www.sebi.gov.in/legal/circulars/oct-2017/categorization-and-rationalization-of-mutual-fund-schemes_36199.html` | Large Cap (Top 100), Mid Cap (101-250), Flexi Cap investment mandate |
| 17 | SEBI | SEBI | General / Protection | SEBI SCORES 2.0 Grievance Redressal | `https://scores.sebi.gov.in/` | Investor grievance redressal mechanism, dispute escalation steps |
| 18 | SEBI | SEBI | ELSS Guidelines | SEBI Master Circular on Mutual Funds | `https://www.sebi.gov.in/legal/master-circulars/jun-2023/master-circular-for-mutual-funds_73236.html` | ELSS statutory lock-in, repurchase restrictions, disclosure norms |

---

## 5. Complete Database Schema (Neon DDL)

```sql
-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. sources table: Verified official documents catalog
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url TEXT UNIQUE NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    organization VARCHAR(100) NOT NULL,
    amc_name VARCHAR(100),
    scheme_name VARCHAR(150),
    document_type VARCHAR(50),
    content_hash VARCHAR(64) NOT NULL,
    published_at DATE,
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. chunks table: Chunked segments with 768-dim embeddings
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    token_count INTEGER,
    embedding vector(768) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. HNSW Vector Index for fast cosine search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw 
ON chunks USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 5. ingestion_runs: Freshness and audit logs
CREATE TABLE IF NOT EXISTS ingestion_runs (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    chunks_created INTEGER DEFAULT 0,
    error_message TEXT,
    content_hash VARCHAR(64)
);

-- 6. Relational indexes
CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(url);
CREATE INDEX IF NOT EXISTS idx_chunks_source_id ON chunks(source_id);
```

---

## 6. Project Directory Structure (Option B: Unified Next.js)

```text
vabsolpract/
├── app/
│   ├── layout.jsx                      # Global root layout with Inter font
│   ├── page.jsx                        # Executive Gloss Chat UI (Client Component)
│   ├── globals.css                     # Executive Gloss design tokens & glassmorphism
│   └── api/
│       └── chat/
│           └── route.js                # Serverless Edge RAG Route Handler
├── lib/
│   ├── guardrails.js                   # In-memory PII regex & advice intent classifier
│   ├── embeddings.js                   # Google text-embedding-004 REST client
│   ├── neonClient.js                   # Neon Serverless HTTP API vector query (/sql)
│   └── geminiFailover.js               # 4-Tier Gemini Failover Cascade (2.5 -> 1.5)
├── components/
│   ├── Header.jsx                      # INDMoney branding + active model pill
│   ├── WelcomeCard.jsx                 # Strict facts-only scope explanation
│   ├── ExamplePills.jsx                # 3 one-click factual inquiry triggers
│   ├── ChatStream.jsx                  # User/Assistant bubbles with citations
│   ├── InputBar.jsx                    # Floating glass input with keyboard handlers
│   └── DisclaimerFooter.jsx            # Persistent compliance disclaimer
├── scripts/
│   ├── ingest_sources.py               # Official 18-source scraper, chunker & seeder
│   └── raw_data/                       # 18 cached official public documents
├── project-documents/                  # Complete 8 pre-development specifications
├── doc/
│   └── implementation_plan.md          # Master Implementation Plan (Option B)
├── sources.md                          # 18 Verified Official Sources Table
├── sample-qa.md                        # 8-10 Sample Q&A Pairs with Citations
├── README.md                           # Master Setup & Vercel Deployment Guide
├── .env.example                        # Sanitized configuration template
├── .env.local                          # Active credentials (DATABASE_URL & GEMINI_API_KEY)
└── package.json                        # Next.js, React, Lucide-React
```

---

## 7. Automated Testing Plan (16 Scenarios)

* **Suite A: Factual Questions (5 Scenarios):** Large Cap Min SIP (₹500), ELSS 3-Year Lock-in, Midcap Exit Load (1% within 1 year), Flexi Cap Benchmark (Nifty 500 TRI), Statement download instructions.
* **Suite B: Investment Advice Refusals (3 Scenarios):** Buy/sell advice, fund comparison for selection, and future return predictions refused with standard compliance disclaimer.
* **Suite C: Unsupported Facts (2 Scenarios):** Un-indexed schemes or non-public questions trigger the honest fallback: *"I couldn't verify that fact from the official sources available to me."*
* **Suite D: PII Protection (3 Scenarios):** PAN card, Aadhaar + OTP, and phone/email queries intercepted and discarded before DB/LLM calls.
* **Suite E: Failover & Citation Validation (3 Scenarios):** 429 rate limit cascade verified, official domains verified (`miraeassetmf.co.in`, `sebi.gov.in`, `amfiindia.com`), and `last_verified_at` verified.

---

## 8. REQUIRED USER INPUT

All necessary database credentials and Gemini API keys have been provided and verified.

```text
No additional user input is required to begin implementation.
```
