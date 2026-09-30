import React from 'react';

export default function DisclaimerFooter() {
  return (
    <footer style={{
      textAlign: 'center',
      padding: '14px 20px',
      fontSize: '12px',
      color: 'var(--text-muted)',
      borderTop: '1px solid var(--glass-border)',
      backgroundColor: 'var(--bg-primary)'
    }}>
      <strong>Facts-only. No investment advice.</strong> Official sources: Mirae Asset Mutual Fund, SEBI, and AMFI.
    </footer>
  );
}
