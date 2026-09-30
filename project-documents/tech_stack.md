# TECHNOLOGY STACK SPECIFICATION
## Facts-Only Mutual Fund RAG Assistant (INDMoney)

**Document Version:** 2.1.0  
**Author:** Principal Software Architect  
**Architecture Pattern:** Unified Next.js (App Router) + Neon Serverless PostgreSQL (Option B)  
**Target Platform:** Vercel Web Portal / Vercel Edge Serverless  

---

## 1. Complete Architecture Overview (Option B: Unified Next.js on Vercel)

The system is architected as a **unified, single-repository Next.js (App Router) application** deployed natively on **Vercel**. It combines an "Executive Gloss" React frontend with secure, zero-maintenance Vercel Serverless Functions (`/api/chat`), connecting directly over HTTPS to **Neon Serverless PostgreSQL (with `pgvector`)** and **Google Generative AI (Multi-Model Gemini Failover Cascade)**.

This architecture completely eliminates the need for separate backend servers (no Python containers, no independent Express servers, no Docker maintenance), while guaranteeing **100% security of API keys and database credentials** away from public browser network tabs.

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

## 2. Technology Layer Breakdown & Justifications

### 2.1 Full-Stack Application Framework: Next.js (App Router)

| Attribute | Specification | Rationale & Architectural Justification |
| :--- | :--- | :--- |
| **Framework** | Next.js (App Router) | Native Vercel deployment, unified single-repository codebase. Combines React UI and Serverless API routes without a standalone backend server. |
| **Runtime Version** | Node.js `v24.15.0` (Active Environment) | Modern, secure, high-performance runtime with native fetch and Web Streams. |
| **API Architecture**| Serverless Route Handler (`app/api/chat/route.js`) | Replaces dedicated backend containers (FastAPI/Express). Automatically scales down to zero when idle, eliminating hosting costs. |
| **Security Boundary**| Server-Side Execution | `DATABASE_URL` and `GEMINI_API_KEY` are kept strictly in serverless environment variables (`.env.local`), completely satisfying Master Prompt Rules #11 & #12. |

### 2.2 Frontend & UI Design System

| Attribute | Specification | Rationale & Architectural Justification |
| :--- | :--- | :--- |
| **UI Library** | React 19 / 18 (Client Components) | Declarative state management for message stream, instant response rendering, full accessibility. |
| **Styling** | Vanilla CSS (Scoped Design Tokens) | "Executive Gloss" theme. Zero CSS-in-JS runtime overhead. Full control over INDMoney dark slate surfaces and specular glassmorphism. |
| **Typography** | Inter / System Sans-Serif | Clean financial tabular numerical clarity and legible statutory disclosures. |
| **Icons** | Lucide React | High-performance, lightweight SVG icons (ShieldCheck, ExternalLink, RefreshCw, Send). |

### 2.3 Database & Vector Store

| Attribute | Specification | Rationale & Architectural Justification |
| :--- | :--- | :--- |
| **Database** | Neon Serverless PostgreSQL 18.6 | Managed serverless Postgres with native connection pooling and instant scaling. Project ID: `br-dawn-waterfall-b5vklo5s`. |
| **Vector Extension**| `pgvector` (`vector(768)`) | In-database cosine distance operations (`<=>`). Directly couples relational source metadata with high-dimensional embeddings. |
| **Vector Index** | HNSW (`vector_cosine_ops`) | Sub-millisecond approximate nearest neighbor retrieval (`m=16, ef_construction=64`). |
| **Query Protocol** | Neon Serverless HTTP API (`/sql`) | Direct SQL queries executed over HTTPS via `Neon-Connection-String` header. Bypasses TCP connection exhaustion on Vercel. |

### 2.4 Embeddings & Multi-Model Gemini Cascade

| Model / Endpoint | Role | Dimensions / Speed | Justification |
| :--- | :--- | :--- | :--- |
| **text-embedding-004** | Document & Query Embeddings | 768 dimensions | SOTA semantic retrieval, cost-efficient, native to Google GenAI REST. |
| **gemini-2.5-flash** | **Primary Generator** | Sub-second latency | Fastest flash model with high instruction adherence for strict grounding. |
| **gemini-2.0-flash** | **Failover Tier 1** | Sub-second latency | Reliable next-gen fallback triggered immediately upon 429 quota spikes. |
| **gemini-1.5-flash** | **Failover Tier 2** | Fast & stable | Battle-tested fallback ensuring 99.99% system uptime. |
| **gemini-1.5-pro** | **Failover Tier 3** | High reasoning depth | Deep statutory comprehension fallback for complex regulatory queries. |

### 2.5 Ingestion Pipeline (Offline Pre-computation)

| Attribute | Specification | Rationale & Architectural Justification |
| :--- | :--- | :--- |
| **Script Runner** | Node.js / Python | Offline, idempotent seeder script (`scripts/ingest.js` or `backend/ingest/ingest_sources.py`). |
| **Parsers** | BeautifulSoup4 / Cheerio / pdfplumber | Clean extraction of HTML tables and PDF text from KIM/SID statutory documents. |
| **Hashing** | SHA-256 Content Hash | Cryptographic fingerprinting to track document freshness and prevent duplicate chunking. |

---

## 3. Why Option B (Next.js) Completely Outperforms Pure Client React

1. **Compliance with Negative Rules #11 & #12:** Pure client React would expose the Neon connection string (with database password) and Gemini API key in the browser's Network DevTools. Next.js keeps them strictly server-side.
2. **Zero Backend Maintenance:** You don't manage Docker, Linux VMs, PM2, or separate backend hosting accounts. Next.js deploys as a single application to Vercel.
3. **Zero CORS Issues:** The browser calls `/api/chat` on the exact same domain name.
4. **Resilient Edge Failover:** The 4-tier model failover cascade executes on Vercel's edge, shielding the user's browser from seeing API error responses.
