# MASTER IMPLEMENTATION ROADMAP & BACKLOG
## Facts-Only Mutual Fund RAG Assistant (INDMoney)

**Document Version:** 2.1.0  
**Author:** Lead Software Architect & Sprint Master  
**Architecture Pattern:** Unified Next.js (App Router) + Neon Serverless PostgreSQL (Option B)  
**Scope:** Exhaustive Engineering Backlog & Component Contracts (100% Master Prompt Alignment)  

---

## 1. Unified Application Structure (Option B: Next.js on Vercel)

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
└── package.json                        # Next.js 14/15, React, Lucide-React
```

---

## 2. Detailed Task-by-Task Engineering Backlog

```text
[EPIC 1: Database Migration & Corpus Seeding]
  ├── TASK-101: Execute PostgreSQL schema migration on Neon HTTP API (/sql) [P0]
  ├── TASK-102: Ingest 18 official public documents (Mirae Asset, SEBI, AMFI) [P0]
  ├── TASK-103: Parse HTML tables and statutory KIM/SID text into clean Markdown [P0]
  ├── TASK-104: Implement chunker with context header injection (450 tokens, 80 overlap) [P0]
  ├── TASK-105: Embed all chunks via Google text-embedding-004 in batches [P0]
  └── TASK-106: Insert chunks and sources into Neon database with SHA-256 hashes [P0]

[EPIC 2: Next.js Serverless Edge Core (Option B)]
  ├── TASK-201: Implement lib/guardrails.js (PAN, Aadhaar, Phone, OTP, Advice filter) [P0]
  ├── TASK-202: Implement lib/embeddings.js (Google text-embedding-004 REST) [P0]
  ├── TASK-203: Implement lib/neonClient.js (Cosine distance vector search over /sql) [P0]
  ├── TASK-204: Implement lib/geminiFailover.js (4-tier cascade: 2.5-flash -> 1.5-pro) [P0]
  └── TASK-205: Implement app/api/chat/route.js (Unified serverless API endpoint) [P0]

[EPIC 3: Executive Gloss Frontend UI]
  ├── TASK-301: Initialize Next.js project with scoped Executive Gloss CSS variables [P0]
  ├── TASK-302: Build Header with INDMoney branding and active model status pill [P1]
  ├── TASK-303: Build WelcomeCard with facts-only scope explanation [P1]
  ├── TASK-304: Build ExamplePills for one-click factual inquiry triggers [P1]
  ├── TASK-305: Build ChatStream with user/assistant bubbles, citations, and dates [P0]
  ├── TASK-306: Build InputBar with keyboard handlers and loading states [P0]
  └── TASK-307: Build DisclaimerFooter with persistent compliance warning [P0]

[EPIC 4: Automated Testing & Vercel Packaging]
  ├── TASK-401: Implement automated test runner for factual queries [P0]
  ├── TASK-402: Implement automated test runner for advice and PII guardrails [P0]
  ├── TASK-403: Implement model failover simulation test [P1]
  ├── TASK-404: Author sources.md with complete 18-source metadata table [P0]
  ├── TASK-405: Author sample-qa.md with realistic citation-backed examples [P0]
  └── TASK-406: Author master README.md with setup and Vercel deployment guide [P0]
```
