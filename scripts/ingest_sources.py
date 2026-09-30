import urllib.request
import json
import hashlib
import time

DB_URL = 'postgresql://neondb_owner:npg_b1cyE8oAPfCs@ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require'
SQL_ENDPOINT = 'https://ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/sql'
GEMINI_KEY = 'AQ.Ab8RN6JXmbSM0kd88Dh7RTwqouoBhgyEM9-vsVxD3y5t6Fn4Tg'
EMBED_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={GEMINI_KEY}'

OFFICIAL_SOURCES = [
    {
        "title": "Mirae Asset Large Cap Fund - Scheme Overview & Facts",
        "url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-large-cap-fund",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset Large Cap Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset Large Cap Fund]
[Category: Equity - Large Cap Fund]
Investment Objective: The investment objective of the scheme is to generate long term capital appreciation by capitalizing on potential investment opportunities by predominantly investing in equities of large cap companies.
Benchmark Index: Nifty 100 Total Returns Index (TRI).
Riskometer: Very High Risk. Investors understand that their principal will be at Very High risk.
Total Expense Ratio (TER): Direct Plan TER is approximately 0.54% p.a.; Regular Plan TER is approximately 1.54% p.a. as per latest monthly disclosures.
Fund Managers: Mr. Gaurav Misra and Mr. Gaurav Khandelwal.
Allotment Date: April 04, 2008.
Portfolio Asset Allocation: Minimum 80% of total assets in Large Cap equity companies (top 100 companies by market capitalization as defined by SEBI).
"""
    },
    {
        "title": "Mirae Asset Large Cap Fund - KIM & Key Statutory Details",
        "url": "https://www.miraeassetmf.co.in/downloads/regulatory/scheme-information-documents",
        "source_type": "KIM",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset Large Cap Fund",
        "document_type": "Key Information Memorandum",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset Large Cap Fund]
[Topic: Minimum Investment & Exit Load Details]
Minimum Investment Amount (Lumpsum): Minimum initial investment of Rs. 5,000 and in multiples of Re. 1 thereafter.
Minimum Additional Purchase: Rs. 1,000 and in multiples of Re. 1 thereafter.
Minimum SIP (Systematic Investment Plan) Amount:
- Monthly SIP: Minimum Rs. 500 and in multiples of Re. 1 thereafter (minimum 5 installments).
- Quarterly SIP: Minimum Rs. 1,500 and in multiples of Re. 1 thereafter (minimum 3 installments).
Exit Load Structure:
- If redeemed or switched out within 365 days (1 year) from the date of allotment: 1.00% of the applicable NAV.
- If redeemed or switched out after 365 days from the date of allotment: Nil.
Plans & Options Available: Direct Plan and Regular Plan, with Growth Option and Income Distribution cum Capital Withdrawal (IDCW) Option (with Payout and Reinvestment facilities).
Lock-in Period: None. Open-ended equity scheme with redemption available on all business days at applicable NAV.
"""
    },
    {
        "title": "Mirae Asset Flexi Cap Fund - Scheme Overview & Asset Allocation",
        "url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset Flexi Cap Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset Flexi Cap Fund]
[Category: Equity - Flexi Cap Fund]
Investment Objective: The investment objective of the scheme is to provide long-term capital appreciation from a dynamic portfolio of equity and equity-related instruments across market capitalizations (large cap, mid cap, and small cap companies).
Benchmark Index: Nifty 500 Total Returns Index (TRI).
Riskometer: Very High Risk.
Total Expense Ratio (TER): Direct Plan TER is approximately 0.58% p.a.; Regular Plan TER is approximately 1.72% p.a.
Asset Allocation Flexibility: Under SEBI guidelines for Flexi Cap funds, the scheme invests minimum 65% of total assets in equity and equity-related securities without fixed market-cap ceilings, giving the fund manager full flexibility across large, mid, and small cap stocks.
Allotment Date: February 24, 2023.
"""
    },
    {
        "title": "Mirae Asset Flexi Cap Fund - KIM, SIP Limits & Exit Load",
        "url": "https://www.miraeassetmf.co.in/downloads/regulatory/key-information-memorandum",
        "source_type": "KIM",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset Flexi Cap Fund",
        "document_type": "Key Information Memorandum",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset Flexi Cap Fund]
[Topic: Purchase, SIP & Exit Load Terms]
Minimum Lumpsum Purchase: Rs. 5,000 and in multiples of Re. 1 thereafter.
Minimum Additional Investment: Rs. 1,000 and in multiples of Re. 1 thereafter.
Minimum SIP Amount:
- Monthly SIP: Minimum Rs. 500 and in multiples of Re. 1 thereafter.
- Quarterly SIP: Minimum Rs. 1,500 and in multiples of Re. 1 thereafter.
Exit Load Provisions:
- If redeemed/switched out within 365 days (1 year) from the date of allotment: 1.00% of applicable NAV.
- If redeemed/switched out after 365 days from the date of allotment: Nil.
Lock-in Period: Nil. Units can be redeemed on any business day.
Eligibility: Open to Resident Individuals, Non-Resident Indians (NRIs), HUFs, Corporate bodies, and Trust entities as per AMC guidelines.
"""
    },
    {
        "title": "Mirae Asset ELSS Tax Saver Fund - Scheme Overview & Tax Benefits",
        "url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset ELSS Tax Saver Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset ELSS Tax Saver Fund]
[Category: Equity - Equity Linked Savings Scheme (ELSS)]
Investment Objective: To generate long-term capital appreciation from a diversified portfolio of predominantly equity and equity-related securities along with income tax deduction benefits.
Tax Benefit Section: Investments qualify for tax deduction under Section 80C of the Income Tax Act, 1961 up to Rs. 1,50,000 per financial year (under the Old Tax Regime).
Statutory Lock-in Period: Mandatory 3-year statutory lock-in period from the date of allotment. Units cannot be redeemed, transferred, pledged, or switched out until completion of 3 full years from the date of each respective investment/installment.
Benchmark Index: Nifty 500 Total Returns Index (TRI).
Riskometer: Very High Risk.
Total Expense Ratio (TER): Direct Plan TER is approx 0.59% p.a.; Regular Plan TER is approx 1.63% p.a.
"""
    },
    {
        "title": "Mirae Asset ELSS Tax Saver Fund - KIM, Minimum SIP & Exit Load",
        "url": "https://www.miraeassetmf.co.in/downloads/regulatory/scheme-information-documents-elss",
        "source_type": "KIM",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset ELSS Tax Saver Fund",
        "document_type": "Key Information Memorandum",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset ELSS Tax Saver Fund]
[Topic: Minimum SIP, Lock-in Rules & Exit Load]
Minimum Investment (Lumpsum): Minimum Rs. 500 and in multiples of Rs. 500 thereafter.
Minimum Additional Purchase: Rs. 500 and in multiples of Rs. 500 thereafter.
Minimum SIP Amount: Minimum Rs. 500 per month (and in multiples of Rs. 500 thereafter).
Important SIP Lock-in Note: In an ELSS SIP, each monthly installment has its own independent 3-year lock-in period. For instance, an installment paid in March 2025 unlocks only in March 2028.
Exit Load: Nil. There is NO exit load applicable on redemption after the completion of the statutory 3-year lock-in period. Redemption prior to 3 years is legally not permitted under Central Government ELSS guidelines.
Allotment Date: December 28, 2015.
"""
    },
    {
        "title": "Mirae Asset Midcap Fund - Scheme Overview & Portfolio Mandate",
        "url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-midcap-fund",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset Midcap Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset Midcap Fund]
[Category: Equity - Mid Cap Fund]
Investment Objective: The investment objective of the scheme is to provide long-term capital appreciation by investing predominantly in equity and equity-related securities of mid cap companies.
SEBI Categorization Mandate: Minimum 65% of total assets must be invested in equity shares of Mid Cap companies (defined as 101st to 250th companies by market capitalization).
Benchmark Index: Nifty Midcap 150 Total Returns Index (TRI).
Riskometer: Very High Risk.
Total Expense Ratio (TER): Direct Plan TER is approx 0.61% p.a.; Regular Plan TER is approx 1.74% p.a.
Allotment Date: July 29, 2019.
Fund Managers: Mr. Ankit Jain.
"""
    },
    {
        "title": "Mirae Asset Midcap Fund - KIM, Minimum Investment & Exit Load",
        "url": "https://www.miraeassetmf.co.in/downloads/regulatory/key-information-memorandum-midcap",
        "source_type": "KIM",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "Mirae Asset Midcap Fund",
        "document_type": "Key Information Memorandum",
        "published_at": "2025-01-01",
        "content": """
[Scheme: Mirae Asset Midcap Fund]
[Topic: Minimum SIP, Lumpsum & Exit Load]
Minimum Initial Investment (Lumpsum): Rs. 5,000 and in multiples of Re. 1 thereafter.
Minimum Additional Investment: Rs. 1,000 and in multiples of Re. 1 thereafter.
Minimum SIP Investment:
- Monthly SIP: Minimum Rs. 500 and in multiples of Re. 1 thereafter (minimum 5 installments).
- Quarterly SIP: Minimum Rs. 1,500 and in multiples of Re. 1 thereafter.
Exit Load Details:
- If redeemed or switched out within 365 days (1 year) from allotment: 1.00% of applicable NAV.
- If redeemed or switched out after 365 days: Nil.
Lock-in Period: Nil. Units can be redeemed on any business day.
"""
    },
    {
        "title": "Mirae Asset Investor Services - Account Statement Download Procedure",
        "url": "https://www.miraeassetmf.co.in/investor-services/account-statement",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "All Schemes",
        "document_type": "Investor Services Guide",
        "published_at": "2025-01-01",
        "content": """
[Topic: How to Download Mutual Fund Account Statement (SOA)]
Investors holding folios with Mirae Asset Mutual Fund can download their Statement of Account (SOA) using the official investor service portal:
Step 1: Navigate to the official Mirae Asset MF website at miraeassetmf.co.in and select 'Investor Services' > 'Account Statement'.
Step 2: Enter your registered Folio Number or PAN along with your registered Email ID or Mobile Number.
Step 3: Verify identity via One-Time Password (OTP) delivered to your registered mobile/email.
Step 4: Select the desired statement period (e.g. Current Financial Year, Last Financial Year, or Specific Date Range).
Step 5: Choose delivery method: Direct PDF download or receive encrypted PDF on registered email.
Consolidated Account Statement (CAS): Investors can also generate a single unified CAS across all mutual funds through CAMS, KFintech, or MF Central portals.
"""
    },
    {
        "title": "Mirae Asset Investor Services - Capital Gains Statement for Tax Filing",
        "url": "https://www.miraeassetmf.co.in/investor-services/capital-gains-statement",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "All Schemes",
        "document_type": "Investor Services Guide",
        "published_at": "2025-01-01",
        "content": """
[Topic: How to Download Capital Gains Statement]
The Capital Gains Statement summarizes realized short-term capital gains (STCG) and long-term capital gains (LTCG) for income tax return filing:
Step 1: Visit miraeassetmf.co.in and click on 'Investor Services' -> 'Capital Gains Statement'.
Step 2: Enter your PAN (Permanent Account Number) and registered email address.
Step 3: Select the relevant Assessment Year / Financial Year (e.g., FY 2024-25).
Step 4: Authenticate using the OTP received on your registered phone/email.
Step 5: Click 'Generate Statement'. The password-protected PDF/Excel statement will be emailed to your registered address within minutes or downloaded instantly. The password format is typically your PAN in UPPERCASE or PAN + Date of Birth.
"""
    },
    {
        "title": "Mirae Asset General FAQs - Folio Operations, KYC & Nominee Update",
        "url": "https://www.miraeassetmf.co.in/faqs/general-faqs",
        "source_type": "AMC_PAGE",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "All Schemes",
        "document_type": "Official FAQs",
        "published_at": "2025-01-01",
        "content": """
[Topic: Folio Maintenance, KYC & Nominees]
KYC Requirement: As per SEBI regulations, KYC (Know Your Customer) compliance is mandatory for all mutual fund investments. Investors can check their KYC status via CVL-KRA, NDML, or KFintech websites using their PAN.
Folio Lookup: Investors can view all mutual fund folios under their PAN by logging into the Mirae Asset Investor Portal or checking their latest Consolidated Account Statement (CAS).
Nomination Facility: Nomination is mandatory for all individual folios. Investors can add, modify, or opt out of nomination online via OTP authentication on the Mirae Asset portal or through MF Central.
Redemption Payout Timelines: For equity mutual fund schemes, redemption proceeds are credited to the investor's verified bank account on T+2 business days as per SEBI settlement guidelines.
"""
    },
    {
        "title": "Mirae Asset Monthly Factsheet - TER Disclosure & Portfolio Ratios",
        "url": "https://www.miraeassetmf.co.in/downloads/factsheet",
        "source_type": "FACTSHEET",
        "organization": "Mirae Asset Mutual Fund",
        "amc_name": "Mirae Asset Mutual Fund",
        "scheme_name": "All Schemes",
        "document_type": "Monthly Factsheet",
        "published_at": "2025-01-01",
        "content": """
[Topic: Total Expense Ratio (TER) & Direct vs Regular Plans]
What is TER: Total Expense Ratio represents the annual percentage of fund assets charged by the AMC to manage the scheme, covering management fees, registrar fees, marketing, and audit expenses.
Direct Plan vs Regular Plan:
- Direct Plans: Purchased directly from the AMC without distributor commission. Therefore, Direct Plans have a significantly lower TER and higher NAV.
- Regular Plans: Purchased through mutual fund distributors or brokers. The distributor commission is included in the TER, making its expense ratio higher.
TER Transparency: Under SEBI guidelines, any change in TER is communicated to investors via email/SMS at least 3 working days prior to implementation and published on the AMC website.
"""
    },
    {
        "title": "AMFI Guidelines - Riskometer Definitions & Review Frequency",
        "url": "https://www.amfiindia.com/investor-corner/knowledge-center/riskometer.html",
        "source_type": "AMFI_GUIDE",
        "organization": "AMFI",
        "amc_name": "Industry-Wide",
        "scheme_name": "All Schemes",
        "document_type": "Investor Guidance",
        "published_at": "2025-01-01",
        "content": """
[Topic: AMFI / SEBI Riskometer Guidelines]
Riskometer Structure: The Riskometer is a pictorial risk representation with 6 distinct levels:
1. Low Risk
2. Low to Moderate Risk
3. Moderate Risk
4. Moderately High Risk
5. High Risk
6. Very High Risk
Mandatory Review Norms: AMCs must evaluate the risk level of all schemes on a monthly basis based on portfolio liquidity, credit risk, and volatility. Any change in the Riskometer level must be communicated to investors and published on AMFI and AMC websites.
Equity Scheme Classification: Most diversified equity funds, including Large Cap, Flexi Cap, ELSS, and Midcap funds, are typically classified as 'Very High Risk' due to stock market volatility.
"""
    },
    {
        "title": "AMFI Knowledge Center - Systematic Investment Plan (SIP) Mechanics",
        "url": "https://www.amfiindia.com/investor-corner/knowledge-center/sip.html",
        "source_type": "AMFI_GUIDE",
        "organization": "AMFI",
        "amc_name": "Industry-Wide",
        "scheme_name": "All Schemes",
        "document_type": "Investor Guidance",
        "published_at": "2025-01-01",
        "content": """
[Topic: SIP Rules, Mandates & Pause Facility]
How SIP Works: A Systematic Investment Plan allows an investor to invest fixed amounts at regular intervals (monthly/quarterly) in a mutual fund scheme, promoting rupee cost averaging.
Bank Mandates (NACH / e-Mandate): SIP installments are automatically debited through National Automated Clearing House (NACH) or online bank e-mandates authorized by the investor.
SIP Pause Facility: Investors can temporarily pause their SIP installments (usually for 1 to 3 months) without terminating the SIP registration by submitting an online pause request at least 15-30 days prior to the debit date.
SIP Cancellation: An investor can cancel a SIP mandate anytime online with zero penalty. Existing accumulated units remain invested in the scheme until redeemed.
"""
    },
    {
        "title": "AMFI Research - Total Expense Ratio (TER) Regulatory Caps",
        "url": "https://www.amfiindia.com/research-information/ter-data",
        "source_type": "AMFI_GUIDE",
        "organization": "AMFI",
        "amc_name": "Industry-Wide",
        "scheme_name": "All Schemes",
        "document_type": "Regulatory Rules",
        "published_at": "2025-01-01",
        "content": """
[Topic: Statutory TER Limits under SEBI Regulation 52]
SEBI prescribes strict maximum TER limits on equity mutual funds based on scheme Asset Under Management (AUM) slabs:
- On the first Rs. 500 Crores of daily net assets: 2.25%
- On the next Rs. 250 Crores: 2.00%
- On the next Rs. 1,250 Crores: 1.75%
- On the next Rs. 3,000 Crores: 1.60%
- On the next Rs. 5,000 Crores: 1.50%
- On subsequent assets: Reduced by 0.05% for every increase of Rs. 5,000 Crores or part thereof.
Direct Plan Cap: The TER of Direct Plans must be lower than the Regular Plan by at least the commission amount paid to distributors.
"""
    },
    {
        "title": "SEBI Mutual Fund Categorization & Rationalization Circular",
        "url": "https://www.sebi.gov.in/legal/circulars/oct-2017/categorization-and-rationalization-of-mutual-fund-schemes_36199.html",
        "source_type": "SEBI_CIRCULAR",
        "organization": "SEBI",
        "amc_name": "Industry-Wide",
        "scheme_name": "All Schemes",
        "document_type": "Regulatory Circular",
        "published_at": "2017-10-06",
        "content": """
[Topic: SEBI Scheme Categorization Definitions]
Under SEBI circular SEBI/HO/IMD/DF3/CIR/P/2017/114, mutual funds are uniformly categorized:
1. Large Cap Fund: Minimum investment in equity and equity-related instruments of large cap companies: 80% of total assets. Large Cap companies are defined as 1st to 100th company in terms of full market capitalization.
2. Mid Cap Fund: Minimum investment in equity shares of mid cap companies: 65% of total assets. Mid Cap companies are defined as 101st to 250th company in terms of full market capitalization.
3. Flexi Cap Fund: Minimum investment in equity & equity-related instruments of 65% of total assets with dynamic allocation across large cap, mid cap, and small cap stocks.
4. ELSS: Minimum investment in equity of 80% of total assets with mandatory 3-year statutory lock-in as per Central Government ELSS notification.
"""
    },
    {
        "title": "SEBI SCORES 2.0 - Investor Grievance Redressal Mechanism",
        "url": "https://scores.sebi.gov.in/",
        "source_type": "SEBI_CIRCULAR",
        "organization": "SEBI",
        "amc_name": "Industry-Wide",
        "scheme_name": "All Schemes",
        "document_type": "Investor Protection Guide",
        "published_at": "2024-04-01",
        "content": """
[Topic: SEBI SCORES Grievance Redressal]
What is SCORES: SCORES (SEBI Complaints Redress System) is a centralized web grievance redressal platform launched by SEBI to protect mutual fund and securities investors.
Escalation Flow:
1. Level 1: Investor first files complaint directly with the AMC / Mutual Fund Registrar.
2. Level 2: If the AMC does not resolve the complaint within 21 calendar days or the resolution is unsatisfactory, the investor can lodge a formal grievance on SCORES 2.0.
3. Level 3: In case of non-resolution, the grievance can be escalated through online dispute resolution (ODR) portals or designated authorities.
"""
    },
    {
        "title": "SEBI Master Circular on Mutual Funds - ELSS Statutory Lock-in Provisions",
        "url": "https://www.sebi.gov.in/legal/master-circulars/jun-2023/master-circular-for-mutual-funds_73236.html",
        "source_type": "SEBI_CIRCULAR",
        "organization": "SEBI",
        "amc_name": "Industry-Wide",
        "scheme_name": "ELSS Funds",
        "document_type": "Master Circular",
        "published_at": "2023-06-27",
        "content": """
[Topic: Statutory Regulations Governing ELSS Schemes]
Mandatory Statutory Lock-in: Equity Linked Savings Schemes are governed by the Equity Linked Savings Scheme, 2005 guidelines notified by the Ministry of Finance.
Section 80C Lock-in: No redemption, repurchase, or transfer of units is permitted until completion of a 3-year statutory holding period from the date of allotment.
No Loan / Lien: Units of an ELSS scheme during the 3-year lock-in cannot be pledged as collateral or lien to any financial institution.
Exit Load Exemption: Under regulatory provisions, since ELSS units are locked for 3 years, mutual fund houses do not levy any exit load when units are redeemed after the lock-in window expires.
"""
    }
]

def run_sql(query):
    headers = {
        'Neon-Connection-String': DB_URL,
        'Content-Type': 'application/json'
    }
    data = json.dumps({'query': query}).encode('utf-8')
    req = urllib.request.Request(SQL_ENDPOINT, data=data, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"SQL Error {e.code}: {e.read().decode('utf-8')}")
            raise e
        except Exception as e:
            print(f"Network error on SQL attempt {attempt+1}: {e}. Retrying in 2s...")
            time.sleep(2)
    raise Exception("Failed to execute SQL query after 5 attempts")

def get_embedding(text):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "content": {
            "parts": [{"text": text}]
        },
        "outputDimensionality": 768
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(EMBED_URL, data=data, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                return res['embedding']['values']
        except Exception as e:
            print(f"Embedding error (attempt {attempt+1}): {e}")
            time.sleep(2)
    raise Exception(f"Failed to generate embedding after 5 attempts")

def ingest():
    print(f"Starting Ingestion of {len(OFFICIAL_SOURCES)} Official Documents into Neon...")
    
    total_chunks = 0
    for idx, doc in enumerate(OFFICIAL_SOURCES, 1):
        content = doc['content'].strip()
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # 1. Insert Source
        escaped_title = doc['title'].replace("'", "''")
        escaped_url = doc['url'].replace("'", "''")
        escaped_org = doc['organization'].replace("'", "''")
        escaped_amc = doc['amc_name'].replace("'", "''")
        escaped_scheme = doc['scheme_name'].replace("'", "''")
        escaped_doc_type = doc['document_type'].replace("'", "''")
        
        source_sql = f"""
        INSERT INTO sources (title, url, source_type, organization, amc_name, scheme_name, document_type, content_hash, published_at, last_verified_at)
        VALUES ('{escaped_title}', '{escaped_url}', '{doc['source_type']}', '{escaped_org}', '{escaped_amc}', '{escaped_scheme}', '{escaped_doc_type}', '{content_hash}', '{doc['published_at']}', CURRENT_TIMESTAMP)
        ON CONFLICT (url) DO UPDATE SET
            title = EXCLUDED.title,
            content_hash = EXCLUDED.content_hash,
            last_verified_at = CURRENT_TIMESTAMP
        RETURNING id;
        """
        source_res = run_sql(source_sql)
        source_id = source_res['rows'][0]['id']
        
        # 2. Chunking: For these official statutory excerpts, each document has 1-2 dense factual chunks
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # Clean existing chunks for this source if re-ingesting
        run_sql(f"DELETE FROM chunks WHERE source_id = {source_id};")
        
        for c_idx, chunk_text in enumerate(paragraphs):
            print(f"[{idx}/{len(OFFICIAL_SOURCES)}] Embedding chunk {c_idx+1}/{len(paragraphs)} for '{doc['title'][:40]}...'")
            embedding = get_embedding(chunk_text)
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
            
            escaped_chunk = chunk_text.replace("'", "''")
            metadata = json.dumps({
                "scheme": doc['scheme_name'],
                "organization": doc['organization'],
                "document_type": doc['document_type'],
                "url": doc['url']
            }).replace("'", "''")
            
            chunk_sql = f"""
            INSERT INTO chunks (source_id, chunk_index, chunk_text, token_count, embedding, metadata)
            VALUES ({source_id}, {c_idx}, '{escaped_chunk}', {len(chunk_text.split())}, '{embedding_str}'::vector, '{metadata}'::jsonb);
            """
            run_sql(chunk_sql)
            total_chunks += 1
            time.sleep(0.3) # Rate limit safety
            
        print(f"Ingested source ID {source_id} successfully.")

    print(f"\n--- Ingestion Completed! ---")
    print(f"Total Sources Seeded: {len(OFFICIAL_SOURCES)}")
    print(f"Total Vector Chunks Created: {total_chunks}")
    
    # Verification count
    res = run_sql("SELECT count(*) as total_sources FROM sources;")
    print("Database Sources Count:", res['rows'][0]['total_sources'])
    res = run_sql("SELECT count(*) as total_chunks FROM chunks;")
    print("Database Chunks Count:", res['rows'][0]['total_chunks'])

if __name__ == '__main__':
    ingest()
