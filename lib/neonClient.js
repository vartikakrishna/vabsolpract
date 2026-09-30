/**
 * Neon Serverless HTTP SQL Client
 * Executes cosine similarity search over pgvector over HTTPS without persistent connection exhaustion.
 */

import https from 'https';

export async function searchNeonVector(queryVector, threshold = 0.65, limit = 4) {
  const dbUrl = process.env.DATABASE_URL;
  const endpoint = process.env.NEON_SQL_ENDPOINT || 'https://ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/sql';

  if (!dbUrl) {
    throw new Error('DATABASE_URL environment variable is missing.');
  }

  const vectorString = '[' + queryVector.join(',') + ']';

  // SQL parameterized cosine similarity query
  const query = `
    SELECT 
      c.id,
      c.chunk_text,
      c.metadata,
      s.title AS source_title,
      s.url AS source_url,
      s.organization,
      s.scheme_name,
      s.last_verified_at,
      1 - (c.embedding <=> '${vectorString}'::vector) AS similarity
    FROM chunks c
    JOIN sources s ON c.source_id = s.id
    WHERE 1 - (c.embedding <=> '${vectorString}'::vector) >= ${threshold}
    ORDER BY similarity DESC
    LIMIT ${limit};
  `;

  const payload = JSON.stringify({ query });
  const urlObj = new URL(endpoint);

  return new Promise((resolve, reject) => {
    const req = https.request(
      {
        hostname: urlObj.hostname,
        port: urlObj.port || 443,
        path: urlObj.pathname + urlObj.search,
        method: 'POST',
        family: 4, // Enforce IPv4 to avoid IPv6 routing/connection timeout
        headers: {
          'Neon-Connection-String': dbUrl,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload)
        },
        timeout: 10000
      },
      (res) => {
        let body = '';
        res.on('data', (chunk) => {
          body += chunk;
        });
        res.on('end', () => {
          if (res.statusCode < 200 || res.statusCode >= 300) {
            return reject(new Error(`Neon SQL API Error (${res.statusCode}): ${body}`));
          }
          try {
            const data = JSON.parse(body);
            resolve(data.rows || []);
          } catch (err) {
            reject(new Error(`Failed to parse Neon response: ${err.message}`));
          }
        });
      }
    );

    req.on('error', (err) => reject(err));
    req.on('timeout', () => {
      req.destroy(new Error('Connection timed out to Neon vector database'));
    });

    req.write(payload);
    req.end();
  });
}
