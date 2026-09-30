/**
 * In-Memory PII & Investment Advice Guardrails
 * Facts-Only MF Assistant for INDMoney
 */

const PII_PATTERNS = [
  { name: 'PAN Card', regex: /[A-Z]{5}[0-9]{4}[A-Z]/ },
  { name: 'Aadhaar Card', regex: /\b\d{4}\s?\d{4}\s?\d{4}\b/ },
  { name: 'Indian Phone Number', regex: /(\+91[\-\s]?)?[6-9]\d{9}/ },
  { name: 'OTP / Verification Code', regex: /\b\d{4,6}\b.*?(otp|verification|passcode|code)/i },
  { name: 'Email Address', regex: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/ },
  { name: 'Bank Account Number', regex: /\b(account|acct|acc|folio)[\s#:]*\d{9,18}\b/i }
];

const ADVICE_KEYWORDS = [
  'should i buy',
  'should i sell',
  'should i invest',
  'where should i invest',
  'where to invest',
  'which fund is better',
  'which is better',
  'best fund to invest',
  'recommend a fund',
  'recommend me',
  'predict return',
  'future return',
  'will it give',
  'will mirae asset',
  'return next year',
  'give me 20%',
  'give me',
  'calculate cagr',
  'cagr calculation',
  'target price',
  'highest return',
  'portfolio allocation',
  'suggest me'
];

/**
 * Validates input for sensitive personal information.
 * Intercepts immediately before DB query or LLM execution.
 */
export function checkPIIGuardrail(text) {
  if (!text || typeof text !== 'string') return { hasPII: false };
  for (const pattern of PII_PATTERNS) {
    if (pattern.regex.test(text)) {
      return {
        hasPII: true,
        violationType: pattern.name,
        refusalMessage: 'Please do not share sensitive personal information (such as PAN, Aadhaar, account numbers, or OTP). INDMoney will never ask for confidential personal credentials in chat.'
      };
    }
  }
  return { hasPII: false };
}

/**
 * Validates input for investment advice, recommendations, or return predictions.
 */
export function checkAdviceGuardrail(text) {
  if (!text || typeof text !== 'string') return { isAdvice: false };
  const lower = text.toLowerCase();
  for (const keyword of ADVICE_KEYWORDS) {
    if (lower.includes(keyword)) {
      return {
        isAdvice: true,
        refusalMessage: 'I provide factual mutual-fund information from official sources only. I do not provide investment advice, fund recommendations, or return predictions. Please consult a SEBI-registered financial advisor for personal investment guidance.',
        educationalUrl: 'https://www.amfiindia.com/investor-corner/knowledge-center/sip.html'
      };
    }
  }
  return { isAdvice: false };
}
