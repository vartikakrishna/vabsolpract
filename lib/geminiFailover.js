/**
 * 4-Tier Multi-Model Gemini Failover Cascade Engine
 * Failover sequence: gemini-2.5-flash -> gemini-2.0-flash -> gemini-1.5-flash -> gemini-1.5-pro
 */

export const MODEL_CASCADE = [
  'gemini-3.5-flash-lite',
  'gemini-flash-lite-latest',
  'gemini-3.1-flash-lite',
  'gemini-3.6-flash',
  'gemini-3.7-flash',
  'gemini-3.8-flash'
];

export async function generateGroundedAnswerWithFailover(userQuery, retrievedChunks) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error('GEMINI_API_KEY environment variable is missing.');
  }

  // Format context strictly from retrieved official chunks
  const contextSnippet = retrievedChunks.map((chunk, i) => {
    return `[OFFICIAL SOURCE ${i+1}: ${chunk.source_title} | URL: ${chunk.source_url}]\n${chunk.chunk_text}`;
  }).join('\n\n---\n\n');

  const systemInstruction = `You are the Facts-Only Mutual Fund Assistant for INDMoney.
Answer the user's factual mutual fund question using ONLY the provided official source context.

CRITICAL RULES:
1. Grounding: Rely strictly and exclusively on the retrieved official context. If the query asks about HDFC Mutual Fund and the information cannot be found in the provided context, output EXACTLY:
"I couldn't find that information in the available HDFC Mutual Fund source documents."
For other schemes or general queries without context, output:
"I couldn't verify that fact from the official sources available to me."
2. Length: Your answer must be NO MORE than 3 concise sentences.
3. No Advice: Never give investment advice, fund recommendations, or future predictions. Never say a fund is "best" or that a user "should invest".
4. No Calculations: Never compute hypothetical portfolio returns or CAGR.
5. Factual Clarity: State exact numbers, percentages, lock-ins, and exit load timeframes clearly. Mention the relevant fund name.
6. No Invented Links: Do not output URLs in your text. The system automatically attaches official citations.`;

  const promptText = `Retrieved Official Context:
${contextSnippet}

User Question: ${userQuery}
Answer (<= 3 concise sentences, factual only):`;

  let lastError = null;

  for (const model of MODEL_CASCADE) {
    try {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
      const payload = {
        contents: [
          {
            role: 'user',
            parts: [{ text: promptText }]
          }
        ],
        systemInstruction: {
          parts: [{ text: systemInstruction }]
        },
        generationConfig: {
          temperature: 0.1,
          maxOutputTokens: 800
        }
      };

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errText = await response.text();
        console.warn(`[Failover] Model ${model} returned HTTP ${response.status}: ${errText}. Cascading...`);
        lastError = new Error(`HTTP ${response.status}: ${errText}`);
        continue;
      }

      const data = await response.json();
      const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text?.trim();

      if (!generatedText) {
        console.warn(`[Failover] Model ${model} returned empty content. Cascading...`);
        continue;
      }

      // Enforce <= 3 sentences programmatically as a safeguard
      const sentences = generatedText.match(/[^.!?\n]+[.!?]+/g) || [generatedText];
      const boundedAnswer = (sentences.length > 3 ? sentences.slice(0, 3).join(' ') : generatedText).trim();

      return {
        answer: boundedAnswer,
        modelUsed: model
      };
    } catch (err) {
      console.warn(`[Failover] Error with ${model}: ${err.message}. Cascading...`);
      lastError = err;
    }
  }

  throw new Error(`All models in cascade failed. Last error: ${lastError?.message}`);
}
