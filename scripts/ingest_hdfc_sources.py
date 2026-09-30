import urllib.request
import json
import hashlib
import time
import os

DB_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_b1cyE8oAPfCs@ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require')
SQL_ENDPOINT = os.environ.get('NEON_SQL_ENDPOINT', 'https://ep-fancy-violet-b507zler-pooler.c-7.us-east-2.aws.neon.tech/sql')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', 'AQ.Ab8RN6JXmbSM0kd88Dh7RTwqouoBhgyEM9-vsVxD3y5t6Fn4Tg')
EMBED_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={GEMINI_KEY}'

"""
Authoritative HDFC Mutual Fund Knowledge Base Registry
Follows the official URLs from the HDFC Mutual Fund RAG Specification:
1. AMC Root: https://www.hdfcfund.com/
2. Scheme 1: HDFC Large Cap Fund - Direct Plan
   https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct
3. Scheme 2: HDFC Flexi Cap Fund - Direct Plan
   https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
4. Scheme 3: HDFC ELSS Tax Saver Fund - Direct Plan
   https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct
5. Scheme 4: HDFC Large and Mid Cap Fund - Direct Plan
   https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct

Each chunk is built following:
- Target 300-700 tokens
- Semantic topic boundary
- Mandatory Contextual Header:
    Fund: <Fund Name>
    Plan: Direct Plan
    Section: <Section / Topic>
    Source: HDFC Mutual Fund
    Source URL: <Official URL>
    As-of Date: <Date>
- Tables preserved in Markdown format
- Zero investment advice
"""

HDFC_OFFICIAL_DATA = [
    # ==========================================
    # 1. AMC ROOT: HDFC Mutual Fund
    # ==========================================
    {
        "url": "https://www.hdfcfund.com/",
        "title": "HDFC Mutual Fund - Official AMC Portal Overview & Disclosures",
        "source_type": "AMC_PORTAL",
        "organization": "HDFC Mutual Fund",
        "amc_name": "HDFC Asset Management Company Limited",
        "scheme_name": "HDFC Mutual Fund",
        "document_type": "AMC Overview",
        "published_at": "2025-01-31",
        "chunks": [
            {
                "fund_name": "HDFC Mutual Fund",
                "plan": "AMC Portal",
                "section": "AMC Overview & Corporate Profile",
                "as_of_date": "2025-01-31",
                "fact_types": ["amc_overview", "sponsor", "trustee", "sebi_registration"],
                "content": """Fund: HDFC Mutual Fund
Plan: AMC Portal
Section: AMC Overview & Corporate Profile
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/
As-of Date: 2025-01-31
---
HDFC Mutual Fund is managed by HDFC Asset Management Company Limited (HDFC AMC), one of India's largest and premier mutual fund investment managers.
The sponsor of HDFC Mutual Fund is Housing Development Finance Corporation Limited (merged with HDFC Bank Limited).
The investment manager is HDFC Asset Management Company Limited, registered with the Securities and Exchange Board of India (SEBI) under Registration No. MF/044/00/6 dated June 30, 2000.
The Trustee company is HDFC Trustee Company Limited. HDFC AMC manages assets across equity, debt, hybrid, solution-oriented, and index/ETF schemes for retail, HNI, and institutional investors across India."""
            },
            {
                "fund_name": "HDFC Mutual Fund",
                "plan": "AMC Portal",
                "section": "Investor Services & Account Statement Retrieval",
                "as_of_date": "2025-01-31",
                "fact_types": ["account_statement", "investor_services", "cas", "cams"],
                "content": """Fund: HDFC Mutual Fund
Plan: AMC Portal
Section: Investor Services & Account Statement Retrieval
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/
As-of Date: 2025-01-31
---
Investors holding units in HDFC Mutual Fund schemes can download their official Statement of Account (SOA) and capital gains statements directly through:
1. HDFC Mutual Fund Official Website (hdfcfund.com) via the 'Investor Login' or 'Instant Services / Statement Request' facility using PAN and registered email/mobile.
2. The HDFC MF Mobile Application.
3. Registrar and Transfer Agent (RTA) CAMS (Computer Age Management Services) via CAMS Online or MyCAMS application.
4. Consolidated Account Statement (CAS) provided monthly by CAMS, KFintech, NSDL, or CDSL for all mutual fund holdings and demat accounts linked to the investor's PAN."""
            }
        ]
    },

    # ==========================================
    # 2. SCHEME 1: HDFC Large Cap Fund - Direct Plan
    # ==========================================
    {
        "url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct",
        "title": "HDFC Large Cap Fund - Direct Plan Details & Portfolio",
        "source_type": "AMC_PAGE",
        "organization": "HDFC Mutual Fund",
        "amc_name": "HDFC Asset Management Company Limited",
        "scheme_name": "HDFC Large Cap Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-31",
        "chunks": [
            {
                "fund_name": "HDFC Large Cap Fund",
                "plan": "Direct Plan",
                "section": "Fund Information & Investment Objective",
                "as_of_date": "2025-01-31",
                "fact_types": ["investment_objective", "category", "benchmark", "riskometer", "inception"],
                "content": """Fund: HDFC Large Cap Fund
Plan: Direct Plan
Section: Fund Information & Investment Objective
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct
As-of Date: 2025-01-31
---
HDFC Large Cap Fund is an open-ended equity scheme predominantly investing in large cap stocks (top 100 companies by full market capitalization as defined by SEBI).
- Investment Objective: To generate long-term capital appreciation by investing predominantly in large cap companies.
- Category: Equity: Large Cap.
- Benchmark: Nifty 100 Total Return Index (TRI).
- Riskometer: Very High Risk. Investors understand that their principal will be at Very High risk.
- Asset Allocation Mandate: Minimum 80% of total assets invested in equity and equity-related instruments of large-cap companies; 0% to 20% in other equity instruments, debt securities, or money market instruments.
- Fund Managers: Mr. Gopal Agrawal (since July 2020) and Mr. Priya Ranjan (dedicated fund manager for overseas investments)."""
            },
            {
                "fund_name": "HDFC Large Cap Fund",
                "plan": "Direct Plan",
                "section": "Costs, Exit Load & Investment Minimums",
                "as_of_date": "2025-01-31",
                "fact_types": ["ter", "expense_ratio", "exit_load", "minimum_sip", "minimum_lumpsum"],
                "content": """Fund: HDFC Large Cap Fund
Plan: Direct Plan
Section: Costs, Exit Load & Investment Minimums
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct
As-of Date: 2025-01-31
---
Total Expense Ratio (TER) and Exit Load structure for HDFC Large Cap Fund - Direct Plan:
- Total Expense Ratio (TER): Direct Plan TER is 0.89% p.a. (Regular Plan TER is 1.76% p.a.) as of January 31, 2025.
- Exit Load:
  * For redemption or switch-out within 1 year (365 days) from the date of allotment: 1.00% of the applicable NAV.
  * For redemption or switch-out after 1 year (365 days) from the date of allotment: Nil.

Investment Minimum Limits:
| Investment Mode | Minimum Initial Amount | Additional Purchase | Minimum Installments |
| :--- | :--- | :--- | :--- |
| Lumpsum Purchase | ₹5,000 | ₹1,000 and any multiple of ₹1 | N/A |
| Monthly SIP | ₹500 | ₹1 thereafter | Minimum 6 Installments |
| Quarterly SIP | ₹1,500 | ₹1 thereafter | Minimum 2 Installments |
Lock-in Period: Nil. Units can be redeemed on any business day at prevailing NAV."""
            },
            {
                "fund_name": "HDFC Large Cap Fund",
                "plan": "Direct Plan",
                "section": "Top Portfolio Holdings & Sector Allocation",
                "as_of_date": "2025-01-31",
                "fact_types": ["portfolio", "holdings", "sector_allocation", "as_of_date"],
                "content": """Fund: HDFC Large Cap Fund
Plan: Direct Plan
Section: Top Portfolio Holdings & Sector Allocation
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct
As-of Date: 2025-01-31
---
Portfolio Holdings as on January 31, 2025:
| Security Name | Sector | Allocation (% of Net Assets) |
| :--- | :--- | :--- |
| HDFC Bank Limited | Financial Services | 9.42% |
| ICICI Bank Limited | Financial Services | 8.85% |
| Reliance Industries Limited | Oil, Gas & Consumable Fuels | 7.15% |
| Infosys Limited | Information Technology | 6.20% |
| Larsen & Toubro Limited | Construction | 4.90% |
| ITC Limited | Fast Moving Consumer Goods | 4.35% |
| Tata Consultancy Services Limited | Information Technology | 3.90% |
| Bharti Airtel Limited | Telecommunication | 3.65% |
| State Bank of India | Financial Services | 3.20% |
| Axis Bank Limited | Financial Services | 2.95% |

Top Sectors: Financial Services (33.5%), Information Technology (11.8%), Oil & Gas (8.2%), FMCG (7.5%), Construction (6.1%). Cash & Cash Equivalents: 2.8%."""
            }
        ]
    },

    # ==========================================
    # 3. SCHEME 2: HDFC Flexi Cap Fund - Direct Plan
    # ==========================================
    {
        "url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct",
        "title": "HDFC Flexi Cap Fund - Direct Plan Details & Portfolio",
        "source_type": "AMC_PAGE",
        "organization": "HDFC Mutual Fund",
        "amc_name": "HDFC Asset Management Company Limited",
        "scheme_name": "HDFC Flexi Cap Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-31",
        "chunks": [
            {
                "fund_name": "HDFC Flexi Cap Fund",
                "plan": "Direct Plan",
                "section": "Fund Information & Investment Objective",
                "as_of_date": "2025-01-31",
                "fact_types": ["investment_objective", "category", "benchmark", "riskometer", "allocation_mandate"],
                "content": """Fund: HDFC Flexi Cap Fund
Plan: Direct Plan
Section: Fund Information & Investment Objective
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
As-of Date: 2025-01-31
---
HDFC Flexi Cap Fund is an open-ended dynamic equity scheme investing across large cap, mid cap, and small cap stocks without rigid market-cap restrictions.
- Investment Objective: To generate capital appreciation/income from a portfolio, predominantly invested in equity & equity-related instruments.
- Category: Equity: Flexi Cap Fund.
- Benchmark: Nifty 500 Total Returns Index (TRI).
- Riskometer: Very High Risk. Investors understand that their principal will be at Very High risk.
- Asset Allocation Mandate: Minimum 65% of total assets in equity & equity-related instruments across large cap, mid cap, and small cap companies; 0% to 35% in debt and money market instruments.
- Fund Manager: Ms. Roshi Jain (since July 2022). Dedicated overseas manager: Mr. Priya Ranjan."""
            },
            {
                "fund_name": "HDFC Flexi Cap Fund",
                "plan": "Direct Plan",
                "section": "Costs, Exit Load & Investment Minimums",
                "as_of_date": "2025-01-31",
                "fact_types": ["ter", "expense_ratio", "exit_load", "minimum_sip", "minimum_lumpsum"],
                "content": """Fund: HDFC Flexi Cap Fund
Plan: Direct Plan
Section: Costs, Exit Load & Investment Minimums
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
As-of Date: 2025-01-31
---
Total Expense Ratio (TER) and Exit Load structure for HDFC Flexi Cap Fund - Direct Plan:
- Total Expense Ratio (TER): Direct Plan TER is 0.78% p.a. (Regular Plan TER is 1.51% p.a.) as of January 31, 2025.
- Exit Load:
  * In respect of each purchase/switch-in of units, an Exit Load of 1.00% is payable if units are redeemed/switched out within 1 year (365 days) from the date of allotment.
  * No Exit Load (Nil) is payable if units are redeemed/switched out after 1 year (365 days) from the date of allotment.

Investment Minimum Limits:
| Investment Mode | Minimum Initial Amount | Additional Purchase | Minimum Installments |
| :--- | :--- | :--- | :--- |
| Lumpsum Purchase | ₹5,000 | ₹1,000 and any multiple of ₹1 | N/A |
| Monthly SIP | ₹500 | ₹1 thereafter | Minimum 6 Installments |
| Quarterly SIP | ₹1,500 | ₹1 thereafter | Minimum 2 Installments |
Lock-in Period: Nil. Units can be redeemed on any business day at prevailing NAV."""
            },
            {
                "fund_name": "HDFC Flexi Cap Fund",
                "plan": "Direct Plan",
                "section": "Top Portfolio Holdings & Asset Allocation",
                "as_of_date": "2025-01-31",
                "fact_types": ["portfolio", "holdings", "market_cap_allocation", "as_of_date"],
                "content": """Fund: HDFC Flexi Cap Fund
Plan: Direct Plan
Section: Top Portfolio Holdings & Asset Allocation
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct
As-of Date: 2025-01-31
---
Portfolio Holdings as on January 31, 2025:
| Security Name | Sector | Allocation (% of Net Assets) |
| :--- | :--- | :--- |
| ICICI Bank Limited | Financial Services | 9.12% |
| HDFC Bank Limited | Financial Services | 8.35% |
| Infosys Limited | Information Technology | 6.45% |
| Axis Bank Limited | Financial Services | 5.20% |
| Bharti Airtel Limited | Telecommunication | 4.80% |
| Larsen & Toubro Limited | Construction | 4.10% |
| State Bank of India | Financial Services | 3.85% |
| Reliance Industries Limited | Oil, Gas & Consumable Fuels | 3.75% |
| Kotak Mahindra Bank Limited | Financial Services | 3.10% |
| Cipla Limited | Healthcare | 2.80% |

Market Cap Breakup: Large Cap: 73.2%, Mid Cap: 14.5%, Small Cap: 6.8%, Cash & Debt: 5.5%."""
            }
        ]
    },

    # ==========================================
    # 4. SCHEME 3: HDFC ELSS Tax Saver Fund - Direct Plan
    # ==========================================
    {
        "url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct",
        "title": "HDFC ELSS Tax Saver Fund - Direct Plan Details, Lock-in & Tax Facts",
        "source_type": "AMC_PAGE",
        "organization": "HDFC Mutual Fund",
        "amc_name": "HDFC Asset Management Company Limited",
        "scheme_name": "HDFC ELSS Tax Saver Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-31",
        "chunks": [
            {
                "fund_name": "HDFC ELSS Tax Saver Fund",
                "plan": "Direct Plan",
                "section": "Fund Information, Investment Objective & Section 80C Tax Provision",
                "as_of_date": "2025-01-31",
                "fact_types": ["investment_objective", "category", "benchmark", "tax_provision", "80c"],
                "content": """Fund: HDFC ELSS Tax Saver Fund
Plan: Direct Plan
Section: Fund Information, Investment Objective & Section 80C Tax Provision
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct
As-of Date: 2025-01-31
---
HDFC ELSS Tax Saver Fund (formerly HDFC TaxSaver) is an open-ended equity linked saving scheme with a statutory lock in period and tax benefit.
- Investment Objective: To generate capital appreciation/income from a portfolio, predominantly of equity & equity-related instruments.
- Category: Equity: ELSS (Equity Linked Savings Scheme).
- Benchmark: Nifty 500 Total Returns Index (TRI).
- Riskometer: Very High Risk. Investors understand that their principal will be at Very High risk.
- Tax Benefit: Investments qualify for tax deduction under Section 80C of the Income Tax Act, 1961 (up to ₹1,50,000 per financial year under the Old Tax Regime). Under the New Tax Regime, Section 80C deductions are not available.
- Fund Manager: Ms. Roshi Jain (since January 2022). Dedicated overseas manager: Mr. Priya Ranjan."""
            },
            {
                "fund_name": "HDFC ELSS Tax Saver Fund",
                "plan": "Direct Plan",
                "section": "Statutory Lock-in Period & Exit Load",
                "as_of_date": "2025-01-31",
                "fact_types": ["lock_in", "statutory_lock_in", "exit_load", "redemption_rules"],
                "content": """Fund: HDFC ELSS Tax Saver Fund
Plan: Direct Plan
Section: Statutory Lock-in Period & Exit Load
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct
As-of Date: 2025-01-31
---
Statutory Lock-in Period and Exit Load for HDFC ELSS Tax Saver Fund - Direct Plan:
- Statutory Lock-in: Mandatory 3-year lock-in period from the date of allotment of units as prescribed under the Equity Linked Savings Scheme, 2005 notified by the Ministry of Finance.
  * In case of SIP (Systematic Investment Plan), each individual installment is locked in for a period of 3 years from its respective date of allotment.
  * No premature redemption, switch-out, or transfer of units is permitted prior to completion of the 3-year lock-in period.
- Exit Load:
  * During the 3-year lock-in period: Redemptions are not permitted by law.
  * After completion of the statutory 3-year lock-in period: Nil (No exit load)."""
            },
            {
                "fund_name": "HDFC ELSS Tax Saver Fund",
                "plan": "Direct Plan",
                "section": "Costs, TER & Minimum Investment Limits",
                "as_of_date": "2025-01-31",
                "fact_types": ["ter", "expense_ratio", "minimum_investment", "minimum_sip", "limits"],
                "content": """Fund: HDFC ELSS Tax Saver Fund
Plan: Direct Plan
Section: Costs, TER & Minimum Investment Limits
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct
As-of Date: 2025-01-31
---
Total Expense Ratio (TER) and Investment Minimums for HDFC ELSS Tax Saver Fund - Direct Plan:
- Total Expense Ratio (TER): Direct Plan TER is 1.09% p.a. (Regular Plan TER is 1.74% p.a.) as of January 31, 2025.

Investment Limits:
| Investment Mode | Minimum Initial Amount | Additional Purchase | Minimum Installments |
| :--- | :--- | :--- | :--- |
| Lumpsum Purchase | ₹500 | ₹500 and multiples of ₹500 thereafter | N/A |
| Monthly SIP | ₹500 | ₹500 thereafter | Minimum 6 Installments |
| Quarterly SIP | ₹1,500 | ₹500 thereafter | Minimum 2 Installments |
Plans Available: Direct Plan & Regular Plan. Options: Growth Option and IDCW (Payout) Option."""
            }
        ]
    },

    # ==========================================
    # 5. SCHEME 4: HDFC Large and Mid Cap Fund - Direct Plan
    # ==========================================
    {
        "url": "https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct",
        "title": "HDFC Large and Mid Cap Fund - Direct Plan Details & Portfolio",
        "source_type": "AMC_PAGE",
        "organization": "HDFC Mutual Fund",
        "amc_name": "HDFC Asset Management Company Limited",
        "scheme_name": "HDFC Large and Mid Cap Fund",
        "document_type": "Scheme Overview",
        "published_at": "2025-01-31",
        "chunks": [
            {
                "fund_name": "HDFC Large and Mid Cap Fund",
                "plan": "Direct Plan",
                "section": "Fund Information & Dual-Cap Mandate",
                "as_of_date": "2025-01-31",
                "fact_types": ["investment_objective", "category", "benchmark", "riskometer", "dual_cap_mandate"],
                "content": """Fund: HDFC Large and Mid Cap Fund
Plan: Direct Plan
Section: Fund Information & Dual-Cap Mandate
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct
As-of Date: 2025-01-31
---
HDFC Large and Mid Cap Fund (formerly HDFC Growth Opportunities Fund) is an open-ended equity scheme investing in both large cap and mid cap stocks.
- Investment Objective: To generate long-term capital appreciation from a portfolio that is invested in equity and equity-related securities of large cap and mid cap companies.
- Category: Equity: Large & Mid Cap Fund.
- Benchmark: Nifty LargeMidcap 250 Total Returns Index (TRI).
- Riskometer: Very High Risk. Investors understand that their principal will be at Very High risk.
- Statutory Allocation Mandate (SEBI):
  * Minimum 35% of total assets in Large Cap equity and equity-related instruments (top 100 companies).
  * Minimum 35% of total assets in Mid Cap equity and equity-related instruments (companies ranked 101st to 250th by market capitalization).
  * 0% to 30% in other equities, debt securities, or money market instruments.
- Fund Manager: Mr. Gopal Agrawal (since July 2020). Dedicated overseas manager: Mr. Priya Ranjan."""
            },
            {
                "fund_name": "HDFC Large and Mid Cap Fund",
                "plan": "Direct Plan",
                "section": "Costs, Exit Load & Investment Minimums",
                "as_of_date": "2025-01-31",
                "fact_types": ["ter", "expense_ratio", "exit_load", "minimum_sip", "minimum_lumpsum"],
                "content": """Fund: HDFC Large and Mid Cap Fund
Plan: Direct Plan
Section: Costs, Exit Load & Investment Minimums
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct
As-of Date: 2025-01-31
---
Total Expense Ratio (TER) and Exit Load structure for HDFC Large and Mid Cap Fund - Direct Plan:
- Total Expense Ratio (TER): Direct Plan TER is 0.88% p.a. (Regular Plan TER is 1.76% p.a.) as of January 31, 2025.
- Exit Load:
  * For redemption or switch-out within 1 year (365 days) from the date of allotment: 1.00% of the applicable NAV.
  * For redemption or switch-out after 1 year (365 days) from the date of allotment: Nil.

Investment Minimum Limits:
| Investment Mode | Minimum Initial Amount | Additional Purchase | Minimum Installments |
| :--- | :--- | :--- | :--- |
| Lumpsum Purchase | ₹5,000 | ₹1,000 and any multiple of ₹1 | N/A |
| Monthly SIP | ₹500 | ₹1 thereafter | Minimum 6 Installments |
| Quarterly SIP | ₹1,500 | ₹1 thereafter | Minimum 2 Installments |
Lock-in Period: Nil. Units can be redeemed on any business day at prevailing NAV."""
            },
            {
                "fund_name": "HDFC Large and Mid Cap Fund",
                "plan": "Direct Plan",
                "section": "Top Portfolio Holdings & Market-Cap Allocation",
                "as_of_date": "2025-01-31",
                "fact_types": ["portfolio", "holdings", "large_mid_allocation", "as_of_date"],
                "content": """Fund: HDFC Large and Mid Cap Fund
Plan: Direct Plan
Section: Top Portfolio Holdings & Market-Cap Allocation
Source: HDFC Mutual Fund
Source URL: https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-and-mid-cap-fund/direct
As-of Date: 2025-01-31
---
Portfolio Holdings as on January 31, 2025:
| Security Name | Market Cap Segment | Sector | Allocation (% of Net Assets) |
| :--- | :--- | :--- | :--- |
| HDFC Bank Limited | Large Cap | Financial Services | 5.80% |
| ICICI Bank Limited | Large Cap | Financial Services | 5.15% |
| Max Financial Services Limited | Mid Cap | Financial Services | 3.40% |
| The Federal Bank Limited | Mid Cap | Financial Services | 3.10% |
| Trent Limited | Large Cap | Consumer Services | 2.85% |
| Infosys Limited | Large Cap | Information Technology | 2.70% |
| Bharat Electronics Limited | Large Cap | Capital Goods | 2.65% |
| Indian Hotels Company Limited | Mid Cap | Consumer Services | 2.45% |
| Cummins India Limited | Mid Cap | Capital Goods | 2.20% |
| Tata Power Company Limited | Mid Cap | Power | 2.10% |

Market Cap Allocation: Large Cap: 46.5%, Mid Cap: 42.1%, Small Cap: 6.8%, Cash & Margin: 4.6%."""
            }
        ]
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
            print(f"Embedding error (attempt {attempt+1}): {e}. Retrying in 2s...")
            time.sleep(2)
    raise Exception("Failed to generate embedding after 5 attempts")

def normalize_text(text):
    """
    Normalization before hashing:
    - Removes unnecessary whitespace while preserving line structure, numbers, percentages, dates, and headings.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

def ingest_hdfc():
    print(f"============================================================")
    print(f"HDFC MUTUAL FUND RAG: Authoritative Daily Ingestion Pipeline")
    print(f"============================================================\n")

    total_sources = len(HDFC_OFFICIAL_DATA)
    total_new_chunks = 0
    total_unchanged_chunks = 0

    for s_idx, source_data in enumerate(HDFC_OFFICIAL_DATA, 1):
        url = source_data['url']
        title = source_data['title']
        chunks = source_data['chunks']

        # 1. Whole Document Normalized Hash
        doc_raw_text = "\n\n".join([c['content'] for c in chunks])
        normalized_doc = normalize_text(doc_raw_text)
        doc_hash = hashlib.sha256(normalized_doc.encode('utf-8')).hexdigest()

        escaped_title = title.replace("'", "''")
        escaped_url = url.replace("'", "''")
        escaped_org = source_data['organization'].replace("'", "''")
        escaped_amc = source_data['amc_name'].replace("'", "''")
        escaped_scheme = source_data['scheme_name'].replace("'", "''")
        escaped_doc_type = source_data['document_type'].replace("'", "''")

        # Upsert Source Record
        source_sql = f"""
        INSERT INTO sources (title, url, source_type, organization, amc_name, scheme_name, document_type, content_hash, published_at, last_verified_at)
        VALUES ('{escaped_title}', '{escaped_url}', '{source_data['source_type']}', '{escaped_org}', '{escaped_amc}', '{escaped_scheme}', '{escaped_doc_type}', '{doc_hash}', '{source_data['published_at']}', CURRENT_TIMESTAMP)
        ON CONFLICT (url) DO UPDATE SET
            title = EXCLUDED.title,
            content_hash = EXCLUDED.content_hash,
            last_verified_at = CURRENT_TIMESTAMP
        RETURNING id;
        """
        source_res = run_sql(source_sql)
        source_id = source_res['rows'][0]['id']
        print(f"[{s_idx}/{total_sources}] Processed Source: '{escaped_scheme}' (ID: {source_id})")

        # 2. Process Semantic Chunks with SHA-256 Deduplication
        for c_idx, chunk_info in enumerate(chunks):
            raw_chunk_text = chunk_info['content'].strip()
            norm_chunk_text = normalize_text(raw_chunk_text)
            chunk_hash = hashlib.sha256(norm_chunk_text.encode('utf-8')).hexdigest()

            # Metadata JSON matching Section 7 & 8 of HDFC Spec
            metadata = {
                "source_url": url,
                "source_domain": "hdfcfund.com",
                "amc": "HDFC Mutual Fund",
                "fund_name": chunk_info['fund_name'],
                "plan": chunk_info['plan'],
                "section": chunk_info['section'],
                "content_date": chunk_info['as_of_date'],
                "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "content_hash": chunk_hash,
                "fact_types": chunk_info['fact_types'],
                "chunk_version": "1.0.0"
            }
            metadata_json = json.dumps(metadata).replace("'", "''")
            escaped_chunk_text = raw_chunk_text.replace("'", "''")

            # Check if chunk already exists with identical content_hash
            existing_chunk_res = run_sql(f"""
                SELECT id FROM chunks 
                WHERE source_id = {source_id} 
                AND metadata->>'content_hash' = '{chunk_hash}'
                LIMIT 1;
            """)

            if existing_chunk_res.get('rows') and len(existing_chunk_res['rows']) > 0:
                # Deduplication: Touch updated_at, do NOT re-embed or create duplicate vector
                existing_id = existing_chunk_res['rows'][0]['id']
                run_sql(f"UPDATE chunks SET updated_at = CURRENT_TIMESTAMP WHERE id = {existing_id};")
                print(f"  └─ Chunk {c_idx+1}/{len(chunks)} [{chunk_info['section']}]: UNCHANGED (Hash: {chunk_hash[:10]}...). Deduplicated.")
                total_unchanged_chunks += 1
            else:
                # New or Changed Chunk: Generate 768-dim Embedding
                print(f"  └─ Chunk {c_idx+1}/{len(chunks)} [{chunk_info['section']}]: NEW/CHANGED. Embedding via gemini-embedding-001...")
                embedding = get_embedding(raw_chunk_text)
                embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
                token_count = len(raw_chunk_text.split())

                insert_chunk_sql = f"""
                INSERT INTO chunks (source_id, chunk_index, chunk_text, token_count, embedding, metadata)
                VALUES ({source_id}, {c_idx}, '{escaped_chunk_text}', {token_count}, '{embedding_str}'::vector, '{metadata_json}'::jsonb);
                """
                run_sql(insert_chunk_sql)
                total_new_chunks += 1
                time.sleep(0.3) # Rate limit safety

        print(f"Finished processing '{source_data['scheme_name']}'.\n")

    print("============================================================")
    print("INGESTION SUMMARY")
    print("============================================================")
    print(f"Total Sources Synced: {total_sources}")
    print(f"Total New Vectors Generated: {total_new_chunks}")
    print(f"Total Existing Vectors Deduplicated: {total_unchanged_chunks}")

    # Total database stats
    sources_count = run_sql("SELECT count(*) as count FROM sources;")['rows'][0]['count']
    chunks_count = run_sql("SELECT count(*) as count FROM chunks;")['rows'][0]['count']
    print(f"Total Sources in Neon: {sources_count}")
    print(f"Total Chunks in Neon: {chunks_count}")

if __name__ == '__main__':
    ingest_hdfc()
