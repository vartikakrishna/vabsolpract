# SPRINT & MILESTONE PLAN
## Facts-Only Mutual Fund RAG Assistant (INDMoney)

**Document Version:** 2.1.0  
**Author:** Lead Product Manager & Engineering Lead  
**Architecture Pattern:** Unified Next.js (App Router) + Neon Serverless PostgreSQL (Option B)  
**Cycle:** 5-Phase Rapid Delivery Plan (100% Master Prompt Alignment)  

---

## 1. Phase-by-Phase Roadmap Breakdown

```text
Phase 0: Environment Audit & Credential Verification [COMPLETED]
 ├── Neon Database Connection & Vector Extension Verification [COMPLETED]
 ├── Gemini AI Key Validation & Model Listing [COMPLETED]
 └── Pre-Development Architecture & Compliance Specs [COMPLETED]
       │
       ▼
Phase 1: Database Migration & Official Corpus Ingestion [IMMEDIATE NEXT STEP]
 ├── Execute PostgreSQL DDL Schema (sources, chunks, ingestion_runs, HNSW index)
 ├── Ingest 18 Official Public Documents (Mirae Asset, SEBI, AMFI)
 └── Generate 768-dim Embeddings via text-embedding-004 & Store in Neon
       │
       ▼
Phase 2: Next.js Serverless Core & Multi-Model Failover (Option B)
 ├── Scaffold Unified Next.js (App Router) Project
 ├── Implement app/api/chat/route.js (Serverless Edge Handler)
 ├── Implement Neon Serverless HTTP Vector Retrieval (/sql)
 ├── Build 4-Tier Gemini Cascade Failover Orchestrator (2.5-flash -> 1.5-pro)
 └── Implement In-Memory PII & Investment Advice Refusal Gates
       │
       ▼
Phase 3: Executive Gloss Frontend Components
 ├── Build app/page.jsx with Executive Gloss Tokens (Obsidian #07090E, Cyan #00D4AA)
 ├── Build Header with INDMoney branding and active model status pill
 ├── Build WelcomeCard and 3 One-Click Example Query Pills
 ├── Build ChatStream with verified source links and last_verified_at date badges
 └── Embed Persistent Compliance Disclaimer ("Facts-only. No investment advice.")
       │
       ▼
Phase 4: Automated Testing, Evaluation & Vercel Packaging
 ├── Execute 16-Scenario Automated QA Battery (5 Factual, 3 Advice, 2 Unverified, 3 PII, 3 Failover)
 ├── Generate sources.md (18 Official Source URLs Table)
 ├── Generate sample-qa.md (8-10 Realistic Q&A Pairs with Citations)
 ├── Generate master README.md with Local & Vercel Deployment Instructions
 └── Final Production Verification on localhost:3000
```

---

## 2. Milestone Deliverables & Timeframes

| Milestone | Deliverables | Estimated Completion | Critical Dependencies |
| :--- | :--- | :--- | :--- |
| **M0: Project Setup & Specs** | Complete documentation suite in `project-documents/` and `doc/`. | Day 1 (Completed) | User approval of architecture. |
| **M1: Data Pipeline & Neon DB** | Migrated Neon schema, HNSW index, 18 seeded official documents in `sources` and `chunks`. | Day 1 | Verified Neon DB URL. |
| **M2: Next.js Serverless Core** | `/api/chat` route handler, Neon HTTP vector search, PII & advice guardrails, 4-tier Gemini cascade failover. | Day 2 | Verified Gemini API Key. |
| **M3: Executive Gloss UI** | Working Next.js UI with Executive Gloss styling, responsive chat stream, citations, and model indicator. | Day 2 | M2 core services. |
| **M4: Automated QA & Compliance** | 100% pass across all 16 test cases (W1, W2, W3 evaluation). | Day 3 | Complete prototype. |
| **M5: Vercel Production Release** | Vercel deployment guide, `sources.md`, `sample-qa.md`, `README.md`. | Day 3 | Successful M4 QA pass. |
