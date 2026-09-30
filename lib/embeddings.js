/**
 * Google GenAI text-embedding service using gemini-embedding-001 with outputDimensionality 768
 */

export async function embedQuery(text) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error('GEMINI_API_KEY environment variable is missing.');
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${apiKey}`;

  const payload = {
    content: {
      parts: [{ text: text.trim() }]
    },
    outputDimensionality: 768
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Embedding API Error (${response.status}): ${errorText}`);
  }

  const data = await response.json();
  if (!data.embedding || !data.embedding.values) {
    throw new Error('Invalid embedding response format from Google GenAI API.');
  }

  return data.embedding.values;
}
