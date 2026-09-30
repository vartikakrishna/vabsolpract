import urllib.request
import json
import sys

DB_URL = 'postgresql://neondb_owner:npg_b1cyE8oAPfCs@ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require'
SQL_ENDPOINT = 'https://ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/sql'

def run_sql(query):
    headers = {
        'Neon-Connection-String': DB_URL,
        'Content-Type': 'application/json'
    }
    data = json.dumps({'query': query}).encode('utf-8')
    req = urllib.request.Request(SQL_ENDPOINT, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        raise e

def migrate():
    print("Migrating Neon PostgreSQL Database Schema...")
    
    # 1. Enable pgvector
    print("1. Enabling pgvector extension...")
    run_sql("CREATE EXTENSION IF NOT EXISTS vector;")
    
    # 2. sources table
    print("2. Creating sources table...")
    run_sql("""
    CREATE TABLE IF NOT EXISTS sources (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        url TEXT UNIQUE NOT NULL,
        source_type VARCHAR(50) NOT NULL,
        organization VARCHAR(100) NOT NULL,
        amc_name VARCHAR(100),
        scheme_name VARCHAR(150),
        document_type VARCHAR(50),
        content_hash VARCHAR(64) NOT NULL,
        published_at DATE,
        last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 3. chunks table
    print("3. Creating chunks table...")
    run_sql("""
    CREATE TABLE IF NOT EXISTS chunks (
        id SERIAL PRIMARY KEY,
        source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
        chunk_index INTEGER NOT NULL,
        chunk_text TEXT NOT NULL,
        token_count INTEGER,
        embedding vector(768) NOT NULL,
        metadata JSONB DEFAULT '{}'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 4. HNSW Vector Index
    print("4. Creating HNSW vector index on chunks(embedding)...")
    run_sql("""
    CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw 
    ON chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
    """)
    
    # 5. ingestion_runs table
    print("5. Creating ingestion_runs audit table...")
    run_sql("""
    CREATE TABLE IF NOT EXISTS ingestion_runs (
        id SERIAL PRIMARY KEY,
        source_id INTEGER REFERENCES sources(id) ON DELETE CASCADE,
        status VARCHAR(50) NOT NULL,
        started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP WITH TIME ZONE,
        chunks_created INTEGER DEFAULT 0,
        error_message TEXT,
        content_hash VARCHAR(64)
    );
    """)
    
    # 6. Relational indexes
    print("6. Creating relational indexes...")
    run_sql("CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(url);")
    run_sql("CREATE INDEX IF NOT EXISTS idx_chunks_source_id ON chunks(source_id);")
    
    print("Verifying tables in public schema...")
    res = run_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [r['table_name'] for r in res.get('rows', [])]
    print(f"Migration Complete! Tables successfully created: {tables}")

if __name__ == '__main__':
    migrate()
