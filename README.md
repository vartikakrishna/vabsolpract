# Facts-Only Mutual Fund Assistant
### Verified Factual RAG Chatbot for INDMoney

> **Core Mandate:** Facts only. Verified sources. No investment advice.

A production-ready, compliance-first, citation-backed Retrieval-Augmented Generation (RAG) conversational agent. It answers factual Indian mutual fund queries with strict official source grounding, automated PII protection, and multi-model failover.

---

## 1. Scope (AMCs & Schemes)

The knowledge base is restricted to **23 authoritative, official documents** from primary AMCs and statutory regulators. Third-party portals, blogs, social media, and unofficial aggregators are strictly excluded.

### 1.1 In-Scope AMCs & Regulatory Bodies
* **HDFC Mutual Fund (Primary AMC)**
* **Mirae Asset Mutual Fund**
* **Securities and Exchange Board of India (SEBI)**
* **Association of Mutual Funds in India (AMFI)**

### 1.2 In-Scope Schemes
| AMC | Scheme Name | Category | Covered Statutory Parameters |
| :--- | :--- | :--- | :--- |
| **HDFC Mutual Fund** | HDFC Large Cap Fund | Equity: Large Cap | Minimum SIP, Exit Load, Benchmark, TER, Disclosures |
| **HDFC Mutual Fund** | HDFC Flexi Cap Fund | Equity: Flexi Cap | Asset Allocation Mandate, Exit Load, Minimum Investment |
| **HDFC Mutual Fund** | HDFC ELSS Tax Saver Fund | Equity: ELSS | 3-Year Statutory Lock-in, Section 80C Tax Benefits, Exit Load |
| **HDFC Mutual Fund** | HDFC Large and Mid Cap Fund | Equity: Large & Mid Cap | Portfolio Mix, Exit Load, Minimum SIP |
| **Mirae Asset Mutual Fund** | Mirae Asset Large Cap Fund | Equity: Large Cap | KIM, Minimum SIP (₹500), Exit Load (1% before 365 days) |
| **Mirae Asset Mutual Fund** | Mirae Asset Flexi Cap Fund | Equity: Flexi Cap | 65% Multi-cap equity mandate, KIM details |
| **Mirae Asset Mutual Fund** | Mirae Asset ELSS Tax Saver Fund | Equity: ELSS | 3-Year Lock-in, Exit Load (Nil), Minimum SIP |
| **Mirae Asset Mutual Fund** | Mirae Asset Midcap Fund | Equity: Mid Cap | Min 65% Mid-cap equity mandate, Exit Load, KIM |

### 1.3 General Regulatory & Operational Knowledge
* **AMFI:** TER Regulatory Caps, Systematic Investment Plan (SIP) mechanics, Riskometer tiers & monthly review norms.
* **SEBI:** Master Circular on Mutual Funds, ELSS statutory lock-in provisions, Categorization & Rationalization of Schemes, SCORES 2.0 Investor Grievance Redressal.
* **Investor Services:** Step-by-step procedures for Account Statements, Capital Gains Statements for tax filing, KYC update guidelines, and Nominee updates.

---

## 2. Setup & Installation Steps

### 2.1 Prerequisites
* **Node.js**: `v18+` or `v24.15.0+`
* **Python**: `3.9+` (for running automated database migrations & safety tests)
* **Neon PostgreSQL Account**: With `pgvector` enabled
* **Google Gemini API Key**: From Google AI Studio

### 2.2 Installation
```bash
# 1. Clone the repository
git clone <repo-url>
cd vabsolpract

# 2. Install project dependencies
npm install
```

### 2.3 Environment Configuration
Create a `.env.local` file in the root directory (see `.env.example`):
```env
DATABASE_URL=postgresql://neondb_owner:<password>@<neon-host>/neondb?sslmode=require&channel_binding=require
GEMINI_API_KEY=<your-google-gemini-api-key>
NEON_SQL_ENDPOINT=https://<neon-host>/sql
```

### 2.4 Database Seeding & Ingestion (Optional / First-Time Setup)
```bash
# Set up database schema and pgvector HNSW index
python3 scripts/migrate_db.py

# Ingest and embed the official documents into Neon
python3 scripts/ingest_sources.py
```

### 2.5 Running Locally
```bash
# Launch the Next.js development server
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

To verify a production build:
```bash
npm run build
npm run start
```

---

## 3. Architecture & Core Workflow

```text
[ User Browser / Chat Interface ]
            │
            │ HTTPS POST /api/chat
            ▼
[ Next.js Serverless Route: app/api/chat/route.js ]
            │
            ├── 1. PII Gate (PAN, Aadhaar, Phone, Email, OTP) ──► Block immediately (Zero DB storage)
            ├── 2. Investment Advice Gate ("Should I buy?", CAGR) ──► Refuse politely + Educational Link
            │
            ├── 3. Query Embedding (gemini-embedding-001, 768 dims)
            │
            ├── 4. Neon Vector Search (Serverless HTTP /sql over IPv4 HTTPS)
            │        └── Similarity < 0.65? ──► "I couldn't verify that fact..."
            │
            ├── 5. Multi-Model Gemini Failover Cascade:
            │        gemini-3.5-flash-lite ──► gemini-flash-lite-latest ──► gemini-3.1-flash-lite
            │        ──► gemini-3.6-flash ──► gemini-3.7-flash ──► gemini-3.8-flash
            │
            └── 6. Grounding Clamp (<= 3 concise sentences + 1 Official URL + Last Verified Date)
            │
            ▼
[ Structured Response in Chat UI ]
```

---

## 4. Known Limits & Guardrails

| Constraint / Limit | System Behavior | Rationale & Protection |
| :--- | :--- | :--- |
| **No Investment Advice** | Rejects queries like *"Should I invest in HDFC Top 100?"* or *"Which fund is best?"* | Complies with SEBI Investment Adviser Regulations. Provides educational AMFI links instead. |
| **No Return Calculations** | Will not calculate future CAGR, compound returns, or projected portfolio wealth. | Prevents speculative financial promises and regulatory non-compliance. |
| **Strict Corpus Boundaries** | If asked about unindexed AMCs (e.g., SBI MF, Axis MF, Nippon India) or unknown schemes, outputs: *"I couldn't verify that fact from the official sources available to me."* | Zero tolerance for AI hallucinations outside the verified corpus. |
| **Length Limitation** | All factual responses are clamped to **≤ 3 sentences**. | Eliminates fluff and keeps answers scannable for retail investors. |
| **Zero PII Retention** | Rejects messages containing PAN (e.g. `ABCDE1234F`), Aadhaar, OTPs, phone numbers, or emails before database logging or LLM calls. | Complies with Indian DPDP (Digital Personal Data Protection) Act standards. |
| **Network Dual-Stack (IPv6)** | Uses Node.js native HTTPS with `family: 4` for Neon `/sql` calls. | Prevents silent `ConnectTimeoutError` on networks without routed IPv6 connectivity. |

---

## 5. Verification & Test Suite

Run the automated compliance test runner validating **14 safety & grounding test cases**:
```bash
python3 scripts/test_rag_safety.py
```

### Verified Test Categories:
* **Factual Retrieval (TC-FACT 01 to 05):** Min SIP limits, lock-in periods, exit loads, benchmark indices, statement downloads.
* **Advice Refusal (TC-ADV 01 to 03):** Buy/sell advice requests, return predictions, fund comparisons.
* **Unsupported Facts (TC-UNSUP 01 to 02):** Refusal of unindexed funds without hallucinating.
* **Zero PII Leakage (TC-PII 01 to 03):** Immediate rejection of PAN, Aadhaar, and OTP submissions.
