# HDFC Mutual Fund RAG — Daily Data Ingestion & Chunking Specification

## 1. Specification Overview & Mandate
This document governs the automated data ingestion, semantic chunking, deduplication hashing, metadata enrichment, and daily synchronization pipeline for the **Facts-Only Mutual Fund Assistant**, focusing on **HDFC Mutual Fund** (Asset Management Company) and its designated flagship direct plan schemes.

### Core Product Mandate
> **"Facts only. Verified HDFC official sources. No investment advice."**  
> Under no circumstances may the ingestion or retrieval engine synthesize investment recommendations, fund ratings, return predictions, buy/sell/hold suggestions, or personalized financial planning.

---

## 2. Authoritative Source Registry

The pipeline operates exclusively on official HDFC Mutual Fund domains and regulatory frameworks (SEBI, AMFI). Third-party websites, financial portals (Moneycontrol, ValueResearch), aggregators, and social media are strictly prohibited.

| Entity | Scope / Category | Authoritative Official URL | Target Fact Types |
| :--- | :--- | :--- | :--- |
| **AMC Root** | AMC-Level Overview & Services | `https://www.hdfcfund.com/` | General AMC overview, investor servicing, KYC, grievance redressal, official disclosures |
| **Scheme 1** | HDFC Large Cap Fund — Direct Plan | `https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct` | Investment objective, AUM, TER, Exit load, Min investment/SIP, Benchmark, Riskometer, Fund managers |
| **Scheme 2** | HDFC Flexi Cap Fund — Direct Plan | `https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct` | Dynamic equity allocation (Min 65%), TER, Exit load, Min SIP, Benchmark (Nifty 500 TRI), Riskometer |
| **Scheme 3** | HDFC ELSS Tax Saver Fund — Direct Plan | `https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct` | Section 80C tax deduction, 3-year statutory lock-in, Exit load (Nil after lock-in), Min investment (₹500) |
| **Scheme 4** | HDFC Large & Mid Cap Fund — Direct Plan | `https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct` | Dual-cap mandate (Min 35% large, Min 35% mid), TER, Exit load, Min SIP, Benchmark, Riskometer |

---

## 3. Daily Ingestion & Automated Synchronization Protocol

The ingestion workflow runs on a daily schedule (or via cron trigger) to maintain vector freshness while avoiding redundant compute and vector bloat:

```text
Fetch Target URL
      │
      ▼
HTML / Document Extraction
      │
      ▼
Content Normalization (whitespace, headings, numbers, percentages)
      │
      ▼
Compute Content Hash: SHA256(normalized_content)
      │
      ▼
Check Existing Database Hash (sources.content_hash)
      ├── Identical Hash ──► Touch `last_verified_at = CURRENT_TIMESTAMP` (Skip re-chunking/embedding)
      └── Hash Changed / New ──► Proceed to Semantic Chunking
                                     │
                                     ▼
                      Semantic Chunk Extraction (300–700 tokens)
                                     │
                                     ▼
                      Prepend Context Headers (Fund, Plan, Section, Source)
                                     │
                                     ▼
                      Compute Chunk Hash: SHA256(chunk_text)
                                     │
                                     ▼
                      Deduplicate against existing chunks
                                     ├── Identical Chunk Hash ──► Update retrieved_at timestamp
                                     └── Changed / New Chunk ──► Generate Vector (gemini-embedding-001)
                                                                 Insert into Neon pgvector
```

---

## 4. Semantic Chunking Rules & Hierarchy

### 4.1 Anti-Pattern Warning
* **PROHIBITED:** Blind slicing by arbitrary character count (e.g. slicing strictly every 500 or 1000 characters).
* **MANDATORY:** Meaning-based semantic chunking. A chunk must represent **one coherent factual topic**.

### 4.2 Structural Hierarchy
```text
SOURCE (HDFC Mutual Fund)
 └── FUND (e.g., HDFC Flexi Cap Fund)
      └── PLAN (Direct Plan)
           └── SECTION (e.g., Fund Information, Costs & Fees, Portfolio)
                └── SUBSECTION (e.g., Exit Load, Minimum Investment, Benchmark)
                     └── FACTUAL CONTENT (Heading + Values + Conditions + Dates)
```

### 4.3 Target Chunk Sizing Bounds
* **Target Size:** 300–700 tokens
* **Preferred Window:** 400–600 tokens
* **Hard Upper Bound:** ~800 tokens
* *Core Principle:* Semantic integrity takes precedence over strict token counts. Headings, rules, conditions, and applicable dates must never be bifurcated across boundaries.

---

## 5. Mandatory Contextual Header Injection

To prevent semantic drift and ambiguity in dense vector space, **every chunk must start with contextual metadata headers** before the body text:

```text
Fund: HDFC Flexi Cap Fund
Plan: Direct Plan
Section: Costs & Exit Load
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
As-of Date: 2025-01-31
---
Exit Load Structure:
- For redemption/switch-out within 1 year from the date of allotment: 1.00% of applicable NAV.
- For redemption/switch-out after 1 year from the date of allotment: Nil.
Applicable to all units allotted under Direct and Regular plans.
```

---

## 6. Granular Fact Categories & Extraction Specifications

### 6.1 Basic Scheme Information
* Scheme name, Category (SEBI classification), Plan (Direct Plan), Option (Growth / IDCW), Inception Date.

### 6.2 Investment Objectives & Allocation Mandate
* Core investment philosophy, equity/debt allocation floors (e.g., HDFC Large Cap: minimum 80% in top 100 large-cap stocks; HDFC Large & Mid Cap: minimum 35% large, minimum 35% mid).

### 6.3 Costs, Loads & Investment Thresholds
* **Total Expense Ratio (TER):** Regular TER vs. Direct TER percentage and as-of date.
* **Exit Load:** Tiers, holding thresholds (e.g., 1 year / 365 days), and nil load exceptions.
* **Minimum Investment:** Initial lump-sum purchase, additional investment, and monthly/quarterly SIP minimums.

### 6.4 Statutory Tax Disclosures (ELSS)
* Section 80C deduction provisions (up to ₹1.5 Lakhs under Old Regime).
* Mandatory 3-year statutory lock-in period. Zero early redemption allowed. Exit load: Nil post lock-in.
* *Note:* Factual presentation only; no individualized tax advisory.

### 6.5 Benchmark Indices & Riskometer
* Exact primary benchmark index (e.g., Nifty 100 TRI, Nifty 500 TRI, Nifty LargeMidcap 250 TRI).
* Riskometer classification (e.g., "Very High Risk") and review cadence (monthly evaluation).

### 6.6 Fund Management Team
* Names, designated tenure, roles, and AMC-published biographical credentials.

### 6.7 Portfolio Holdings & Asset Allocation
* Top 10 equity holdings, sector allocations, cash equivalents, and portfolio turnover ratios.
* **Mandatory Rule:** Always bind portfolio tables with `as_of_date` (e.g. `Portfolio as on January 31, 2025`). Historical holdings must never be presented as current holdings.

### 6.8 Operational FAQs & Statements
* Step-by-step account statement (SOA) generation, Consolidated Account Statement (CAS), and capital gains tax document retrieval.

---

## 7. Metadata Schema Specification

Every vector chunk stored in Neon PostgreSQL `chunks` table must contain a rich JSONB metadata payload:

```json
{
  "source_url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct",
  "source_domain": "hdfcfund.com",
  "amc": "HDFC Mutual Fund",
  "fund_name": "HDFC Large Cap Fund",
  "plan": "Direct Plan",
  "section": "Costs & Charges",
  "subsection": "Exit Load",
  "source_type": "AMC_PAGE",
  "document_type": "scheme_overview",
  "retrieved_at": "2026-09-27T11:21:00Z",
  "content_date": "2025-01-31",
  "chunk_version": "1.0.0",
  "content_hash": "a1b2c3d4e5f6...",
  "fact_types": ["exit_load", "holding_period", "direct_plan"]
}
```

---

## 8. Table & Tabular Data Preservation Protocol

Mutual fund pages frequently display numerical facts in tables (TER slabs, SIP frequencies, Exit load duration tiers).
* **Prohibition:** Tables must not be flattened into generic continuous prose.
* **Standard:** Tables are transformed into clear Markdown table syntax or key-value structured semantic pairs.
* **Example:**
  ```markdown
  Fund: HDFC Large & Mid Cap Fund
  Plan: Direct Plan
  Section: Minimum Investment Limits
  
  | Investment Mode | Minimum Initial Amount | Minimum Subsequent Multiple | Minimum Installments |
  | :--- | :--- | :--- | :--- |
  | Lumpsum Purchase | ₹5,000 | ₹1 | N/A |
  | Additional Purchase | ₹1,000 | ₹1 | N/A |
  | Monthly SIP | ₹500 | ₹1 | 6 Installments |
  | Quarterly SIP | ₹1,500 | ₹1 | 2 Installments |
  ```

---

## 9. Retrieval Prioritization & Re-Ranking Strategy

When a user query enters the RAG retrieval pipeline:
1. **Fund-Level Scoping:** Heuristics isolate the scheme entity (e.g., query mentioning "ELSS" scopes to `fund_name = 'HDFC ELSS Tax Saver Fund'`).
2. **Topic Identification:** Pinpoints fact category (e.g., "lock-in", "exit load", "TER", "statement").
3. **Metadata Filtering:** Prioritizes scheme-specific chunks over generic AMC-level notes.
4. **Freshness Ranking:** In the event of multiple historical portfolio records, prioritizes the latest `content_date`.
5. **Similarity Cutoff:** Cosine distance cutoff `similarity >= 0.65`.

---

## 10. Chatbot Grounding & Negative Response Rules

When generating the response:
* Rely **strictly on retrieved chunks**.
* Answers must be **at most 3 sentences**.
* Must attach the exact official HDFC source URL and `Last updated from sources: [DATE]`.
* If a fact cannot be verified in the retrieved documents, the assistant outputs:
  > *"I couldn't find that information in the available HDFC Mutual Fund source documents."*
* Never provide investment recommendations, buy/sell ratings, or CAGR projections.
