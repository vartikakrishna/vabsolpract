import { NextResponse } from 'next/server';

export async function GET() {
  const dbUrl = process.env.DATABASE_URL;
  const apiKey = process.env.GEMINI_API_KEY;
  const neonEndpoint = process.env.NEON_SQL_ENDPOINT;

  return NextResponse.json({
    status: 'ok',
    has_DATABASE_URL: Boolean(dbUrl),
    has_GEMINI_API_KEY: Boolean(apiKey),
    has_NEON_SQL_ENDPOINT: Boolean(neonEndpoint),
    database_url_host: dbUrl ? dbUrl.split('@')[1]?.split('/')[0] : null,
    gemini_key_prefix: apiKey ? apiKey.substring(0, 6) + '...' : null
  });
}
