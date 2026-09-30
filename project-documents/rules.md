# PROJECT DEVELOPMENT RULES & STANDARDS
## Facts-Only Mutual Fund RAG Assistant (INDMoney)

**Document Version:** 2.0.0  
**Author:** Lead Software Architect & Principal Quality Engineer  
**Applicability:** All Code, Data Pipelines, UI Components & Git Commits  

---

## 1. Absolute Negative Rules (Zero-Tolerance Violations)

The codebase, API handlers, prompts, and UI components must strictly enforce these 24 negative rules:

1. **NO Invented Facts:** The assistant must never synthesize facts outside the retrieved official context.
2. **NO Invented URLs:** Citations must originate exclusively from verified database metadata (`sources.url`).
3. **NO Third-Party Sources:** Financial blogs, aggregators, YouTube, Reddit, Quora, and social media must never enter the corpus.
4. **NO Investment Advice:** Never suggest whether a user should invest, redeem, hold, or switch.
5. **NO Mutual Fund Recommendations:** Never recommend or endorse a specific mutual fund scheme.
6. **NO Fund Rankings:** Never rank mutual funds based on historical or anticipated performance.
7. **NO Return Predictions:** Never predict future returns, NAV targets, or market conditions.
8. **NO Performance Calculations:** Never calculate CAGR or hypothetical growth scenarios for fund selection.
9. **NO Advisory Comparisons:** Never compare schemes for the purpose of recommending one over another.
10. **NO PII Storage or Processing:** Never store PAN, Aadhaar, OTPs, phone numbers, or emails.
11. **NO Exposed API Keys:** `GEMINI_API_KEY` must never be hard-coded, exposed in client bundles, or logged.
12. **NO Exposed Database Credentials:** Neon connection strings must never appear in frontend assets or logs.
13. **NO Hard-Coded Secrets:** Use environment variables and `.env.example` templates with sanitized placeholders.
14. **NO Unapproved Data Deletions:** Never drop tables or delete existing Neon data without explicit user approval.
15. **NO Unjustified Architecture Changes:** Stick to the approved Jamstack + Neon HTTP API + Gemini Cascade architecture.
16. **NO Unnecessary Infrastructure:** Do not introduce separate vector databases (Pinecone, Chroma) or heavy servers.
17. **NO Second Neon Projects:** Operate strictly within existing Neon Project ID `br-dawn-waterfall-b5vklo5s`.
18. **NO Assumed Credentials:** Never fake or assume API keys; verify them actively.
19. **NO False Freshness Claims:** `Last updated from sources: [DATE]` must reflect actual verified timestamps.
20. **NO General LLM Knowledge Answering:** If the required fact is absent from retrieved sources, refuse immediately.
21. **NO Unsourced Factual Answers:** Every factual answer must be accompanied by an official source URL.
22. **NO Backend Screenshots as Corpus:** Use only public, authorized textual documents and circulars.
23. **NO Pretended Capabilities:** Never claim features or integrations that are not operational.
24. **NO Continuing Past Missing Information Gates:** Halt and notify the user if an essential dependency is missing.

---

## 2. Coding & Implementation Standards

### 2.1 JavaScript & React Standards
* Standard ES2023+ syntax with clean functional components.
* Strict state sanitization: Input state must be trimmed and passed through PII regex before external dispatch.
* Scoped CSS tokens matching the Executive Gloss specification (`#07090E` dark slate, `#00D4AA` cyan).

### 2.2 Security & Data Protection Guardrails
* **Client-Side In-Memory PII Gate:**
  ```javascript
  const PII_PATTERNS = [
    /[A-Z]{5}[0-9]{4}[A-Z]/,                    // PAN Card
    /\b\d{4}\s?\d{4}\s?\d{4}\b/,                // Aadhaar Card
    /(\+91[\-\s]?)?[6-9]\d{9}/,                 // Indian Mobile Numbers
    /\b\d{4,6}\b.*?(otp|verification)/i,        // OTPs
    /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/ // Emails
  ];
  ```
  If any match is detected, the query is immediately rejected and discarded with zero network transmission.

### 2.3 Grounding & Length Guardrails
* Post-generation output inspection: Answers exceeding 3 sentences are programmatically truncated to the third sentence boundary.
* If the Gemini model returns a generic answer not present in the retrieved chunks, the response is replaced with:
  > *"I couldn't verify that fact from the official sources available to me."*

---

## 3. Git & Conventional Commits

All commits must follow the Conventional Commits specification:
* `feat(rag)`: Adding retrieval or grounding features.
* `feat(ui)`: Implementing Executive Gloss UI components.
* `fix(guardrails)`: Enhancing PII or advice regex patterns.
* `test(qa)`: Adding compliance test cases.
* `docs`: Updating documentation and implementation plans.
