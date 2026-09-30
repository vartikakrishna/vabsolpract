# SYSTEM DESIGN & ARCHITECTURE
## Facts-Only Mutual Fund RAG Assistant (INDMoney)

**Document Version:** 2.1.0  
**Author:** Principal Software Architect & Database Architect  
**Architecture Pattern:** Unified Next.js (App Router) + Neon Serverless PostgreSQL (Option B)  
**Target Platform:** Vercel Web Portal / Edge Serverless  

---

## 1. High-Level System Architecture & Execution Flow

```text
                                [ 18 Official Sources ]
                    (Mirae Asset AMC | SEBI Circulars | AMFI Portal)
                                        │
                                        ▼
                             [ Ingestion Pipeline ]
                     (HTML/PDF Clean -> Chunk -> SHA-256 Hash)
                                        │
                                        ▼
                         [ Google text-embedding-004 ]
                                        │ (768-dim Vector)
                                        ▼
                   [ Neon PostgreSQL + pgvector (HNSW Index) ]
                                        ▲
════════════════════════════════════════╪════════════════════════════════════════
                     USER RUNTIME EXECUTION PATH (VERCEL)
════════════════════════════════════════╪════════════════════════════════════════
                                        │
             User in Browser ───────────┤
         (Executive Gloss UI)           ▼
                               [ POST /api/chat ]
                          (Next.js Serverless Route)
                                        │
                                        ▼
                           [ Step 1: PII Guardrail ]
                              (Regex + Heuristics)
                        - PAN, Aadhaar, Phone, OTP, Email
                                ├── Match: REJECT (Zero Storage)
                                └── Safe ──┐
                                           ▼
                       [ Step 2: Intent Classifier ]
                       (Advice / Return Proj / Factual)
                        - "Should I invest?", "Which is better?", CAGR
                                ├── Advice: REFUSE (Static Compliance Message)
                                └── Factual ──┐
                                              ▼
                        [ Step 3: Embed User Query ]
                         (Google text-embedding-004)
                                              │
                                              ▼
                    [ Step 4: Cosine Vector Search via Neon ]
                     (Neon Serverless HTTP API: /sql endpoint)
                      (Threshold >= 0.65 | Top-K = 4 Chunks)
                                ├── Below 0.65: "I couldn't verify that fact..."
                                └── Match Found ──┐
                                                  ▼
                     [ Step 5: Grounded Gemini Generation ]
                    (Cascade: 2.5-flash -> 2.0-flash -> 1.5-flash -> 1.5-pro)
                                                  │
                                                  ▼
                     [ Step 6: Response Assembly & Citation ]
                    - Factual Answer (<= 3 sentences)
                    - Official Source URL: https://miraeassetmf.co.in/...
                    - Last updated from sources: [Date]
                                                  │
                                                  ▼
                                         [ JSON Response ]
                                                  │
                                                  ▼
                               [ Rendered in User Browser ]
```

---

## 2. Complete Database Schema (Neon PostgreSQL DDL)

```sql
-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. sources table: Catalog of verified official web pages and statutory documents
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url TEXT UNIQUE NOT NULL,
    source_type VARCHAR(50) NOT NULL,       -- 'AMC_PAGE', 'KIM', 'SID', 'FACTSHEET', 'SEBI_CIRCULAR', 'AMFI_GUIDE'
    organization VARCHAR(100) NOT NULL,     -- 'Mirae Asset Mutual Fund', 'SEBI', 'AMFI'
    amc_name VARCHAR(100),                  -- 'Mirae Asset Mutual Fund'
    scheme_name VARCHAR(150),               -- e.g. 'Mirae Asset Large Cap Fund'
    document_type VARCHAR(50),
    content_hash VARCHAR(64) NOT NULL,      -- SHA-256 for change detection & freshness
    published_at DATE,
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. chunks table: Segmented text chunks with high-dimensional vector embeddings
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    token_count INTEGER,
    embedding vector(768) NOT NULL,         -- Matches Google text-embedding-004 dimensions
    metadata JSONB DEFAULT '{}'::jsonb,     -- {"scheme": "Mirae Asset Large Cap", "topic": "Expense Ratio"}
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. HNSW Vector Index for sub-millisecond approximate nearest neighbor search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw 
ON chunks USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 5. ingestion_runs: Audit logging for freshness tracking and verification
CREATE TABLE IF NOT EXISTS ingestion_runs (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,            -- 'SUCCESS', 'FAILED', 'IN_PROGRESS'
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

## 3. Serverless Route Handler Architecture (`app/api/chat/route.js`)

The Next.js App Router exposes a single POST handler that executes on Vercel's serverless edge:

```javascript
import { NextResponse } from 'next/server';
import { checkPIIGuardrails, checkAdviceIntent } from '@/lib/guardrails';
import { embedQuery } from '@/lib/embeddings';
import { searchNeonVector } from '@/lib/neonClient';
import { generateWithFailoverCascade } from '@/lib/geminiFailover';

export async function POST(request) {
  try {
    const { query } = await request.json();

    // 1. PII Check
    const piiCheck = checkPIIGuardrails(query);
    if (piiCheck.hasPII) {
      return NextResponse.json({
        type: 'PII_REJECTION',
        answer: 'Please do not share sensitive personal information (such as PAN, Aadhaar, account numbers, or OTP). INDMoney will never ask for personal credentials in chat.',
        source_url: null,
        last_verified_at: null
      });
    }

    // 2. Advice Intent Check
    const adviceCheck = checkAdviceIntent(query);
    if (adviceCheck.isAdvice) {
      return NextResponse.json({
        type: 'ADVICE_REFUSAL',
        answer: 'I provide factual mutual-fund information from official sources only. I do not provide investment advice, fund recommendations, or return predictions. Please consult a SEBI-registered financial advisor for personal investment guidance.',
        source_url: 'https://www.amfiindia.com/investor-corner/knowledge-center/sip.html',
        last_verified_at: new Date().toISOString().split('T')[0]
      });
    }

    // 3. Generate 768-dim Embedding
    const queryVector = await embedQuery(query);

    // 4. Neon pgvector Cosine Search
    const retrievedChunks = await searchNeonVector(queryVector, 0.65, 4);
    if (!retrievedChunks || retrievedChunks.length === 0) {
      return NextResponse.json({
        type: 'UNVERIFIED',
        answer: "I couldn't verify that fact from the official sources available to me.",
        source_url: null,
        last_verified_at: null
      });
    }

    // 5. Multi-Model Gemini Failover Cascade
    const result = await generateWithFailoverCascade(query, retrievedChunks);

    return NextResponse.json({
      type: 'FACTUAL',
      answer: result.answer,
      source_url: retrievedChunks[0].source_url,
      last_verified_at: retrievedChunks[0].last_verified_at,
      model_used: result.modelUsed
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'An internal error occurred. Please try again.' },
      { status: 500 }
    );
  }
}
```

---

## 4. Multi-Model Failover Mechanism (`lib/geminiFailover.js`)

```javascript
export const MODEL_CASCADE = [
  'gemini-2.5-flash',  // Primary
  'gemini-2.0-flash',  // Fallback 1
  'gemini-1.5-flash',  // Fallback 2
  'gemini-1.5-pro'     // Fallback 3
];

export async function generateWithFailoverCascade(query, chunks) {
  let lastError = null;
  for (const model of MODEL_CASCADE) {
    try {
      const response = await callGeminiREST(model, query, chunks);
      return { answer: response.text, modelUsed: model };
    } catch (err) {
      console.warn(`Model ${model} failed (${err.message}). Cascading to next tier...`);
      lastError = err;
    }
  }
  throw new Error(`All models in cascade failed: ${lastError?.message}`);
}
```
