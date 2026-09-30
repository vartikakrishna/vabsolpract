import { NextResponse } from 'next/server';
import { checkPIIGuardrail, checkAdviceGuardrail } from '@/lib/guardrails';
import { embedQuery } from '@/lib/embeddings';
import { searchNeonVector } from '@/lib/neonClient';
import { generateGroundedAnswerWithFailover } from '@/lib/geminiFailover';

export async function POST(request) {
  try {
    const body = await request.json();
    const query = body?.query?.trim();

    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter is required.' },
        { status: 400 }
      );
    }

    // 1. PII Check (Zero Storage Gate)
    const piiResult = checkPIIGuardrail(query);
    if (piiResult.hasPII) {
      return NextResponse.json({
        type: 'PII_REJECTION',
        answer: piiResult.refusalMessage,
        source_url: null,
        last_verified_at: null,
        model_used: 'Guardrail Engine'
      });
    }

    // 2. Investment Advice & Performance Gate
    const adviceResult = checkAdviceGuardrail(query);
    if (adviceResult.isAdvice) {
      return NextResponse.json({
        type: 'ADVICE_REFUSAL',
        answer: adviceResult.refusalMessage,
        source_url: adviceResult.educationalUrl,
        last_verified_at: new Date().toISOString().split('T')[0],
        model_used: 'Guardrail Engine'
      });
    }

    // 3. Generate 768-dim Vector Embedding for User Query
    const queryVector = await embedQuery(query);

    // 4. Vector Search in Neon PostgreSQL via Serverless HTTP (/sql)
    const retrievedChunks = await searchNeonVector(queryVector, 0.65, 4);

    // If similarity is below confidence threshold or no chunks found
    if (!retrievedChunks || retrievedChunks.length === 0) {
      const isHdfc = query.toLowerCase().includes('hdfc');
      const fallbackMsg = isHdfc
        ? "I couldn't find that information in the available HDFC Mutual Fund source documents."
        : "I couldn't verify that fact from the official sources available to me.";
      return NextResponse.json({
        type: 'UNVERIFIED',
        answer: fallbackMsg,
        source_url: null,
        last_verified_at: null,
        model_used: 'RAG Retriever'
      });
    }

    // 5. Multi-Model Gemini Failover Cascade
    const { answer, modelUsed } = await generateGroundedAnswerWithFailover(query, retrievedChunks);

    // Primary official citation from top-ranking chunk
    const topMatch = retrievedChunks[0];
    const sourceUrl = topMatch.source_url;
    const lastVerified = topMatch.last_verified_at
      ? new Date(topMatch.last_verified_at).toISOString().split('T')[0]
      : new Date().toISOString().split('T')[0];

    return NextResponse.json({
      type: 'FACTUAL',
      answer,
      source_url: sourceUrl,
      source_title: topMatch.source_title,
      last_verified_at: lastVerified,
      model_used: modelUsed
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'An unexpected error occurred while processing your request. Please try again.' },
      { status: 500 }
    );
  }
}
