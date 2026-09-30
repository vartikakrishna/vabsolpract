import React from 'react';
import { Info, ExternalLink } from 'lucide-react';

export default function WelcomeCard() {
  return (
    <div style={{
      backgroundColor: 'var(--bg-secondary)',
      border: '1px solid var(--glass-border)',
      borderRadius: 'var(--radius-lg)',
      padding: '24px',
      margin: '20px 0',
      boxShadow: 'var(--shadow-card)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '4px',
        height: '100%',
        backgroundColor: 'var(--accent-cyan)'
      }} />

      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '14px' }}>
        <div style={{
          backgroundColor: 'var(--accent-cyan-dim)',
          padding: '10px',
          borderRadius: 'var(--radius-md)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <Info size={20} color="var(--accent-cyan)" />
        </div>
        <div>
          <h2 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '6px' }}>
            Welcome to the Facts-Only Mutual Fund Assistant
          </h2>
          <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            This assistant provides factual mutual-fund information from official sources only. It does not provide investment advice, fund recommendations, or portfolio rankings.
          </p>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '12px',
            marginTop: '12px',
            fontSize: '12px',
            color: 'var(--text-muted)'
          }}>
            <span>• <strong>AMCs:</strong> HDFC Mutual Fund &amp; Mirae Asset</span>
            <span>• <strong>HDFC Schemes:</strong> Large Cap, Flexi Cap, ELSS Tax Saver, Large &amp; Mid Cap</span>
            <span>• <strong>Regulators:</strong> SEBI &amp; AMFI Guidelines</span>
          </div>
        </div>
      </div>
    </div>
  );
}
