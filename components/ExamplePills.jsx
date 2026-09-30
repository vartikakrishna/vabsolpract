import React from 'react';
import { HelpCircle } from 'lucide-react';

export default function ExamplePills({ onSelectQuery, disabled }) {
  const examples = [
    {
      label: 'HDFC ELSS Lock-in',
      query: 'What is the lock-in period for HDFC ELSS Tax Saver Fund?'
    },
    {
      label: 'HDFC Flexi Cap Exit Load',
      query: 'What is the exit load for HDFC Flexi Cap Fund Direct Plan?'
    },
    {
      label: 'HDFC Large Cap TER',
      query: 'What is the expense ratio (TER) of HDFC Large Cap Fund Direct Plan?'
    },
    {
      label: 'Mirae Large Cap SIP',
      query: 'What is the minimum SIP amount for Mirae Asset Large Cap Fund?'
    }
  ];

  return (
    <div style={{ marginBottom: '20px' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        fontSize: '12px',
        color: 'var(--text-muted)',
        marginBottom: '10px',
        textTransform: 'uppercase',
        letterSpacing: '0.05em'
      }}>
        <HelpCircle size={14} />
        <span>Try Asking (One-Click Verification)</span>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
        {examples.map((item, index) => (
          <button
            key={index}
            disabled={disabled}
            onClick={() => onSelectQuery(item.query)}
            style={{
              backgroundColor: 'var(--bg-surface)',
              border: '1px solid var(--glass-border)',
              borderRadius: 'var(--radius-pill)',
              padding: '8px 16px',
              fontSize: '13px',
              color: 'var(--text-primary)',
              textAlign: 'left',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              cursor: disabled ? 'not-allowed' : 'pointer',
              opacity: disabled ? 0.6 : 1
            }}
            onMouseEnter={(e) => {
              if (!disabled) {
                e.currentTarget.style.borderColor = 'var(--accent-cyan)';
                e.currentTarget.style.backgroundColor = 'var(--bg-surface-hover)';
                e.currentTarget.style.transform = 'translateY(-1px)';
              }
            }}
            onMouseLeave={(e) => {
              if (!disabled) {
                e.currentTarget.style.borderColor = 'var(--glass-border)';
                e.currentTarget.style.backgroundColor = 'var(--bg-surface)';
                e.currentTarget.style.transform = 'translateY(0)';
              }
            }}
          >
            <span style={{ color: 'var(--accent-cyan)', fontWeight: 600 }}>Q{index + 1}:</span>
            <span>{item.query}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
