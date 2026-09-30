import React from 'react';
import { ShieldCheck, Cpu } from 'lucide-react';

export default function Header({ activeModel }) {
  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 40,
      backdropFilter: 'blur(20px)',
      backgroundColor: 'var(--glass-bg)',
      borderBottom: '1px solid var(--glass-border)',
      padding: '16px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: 'var(--radius-md)',
          background: 'linear-gradient(135deg, #00D4AA 0%, #2F6FED 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: 'var(--shadow-glow-cyan)'
        }}>
          <ShieldCheck size={22} color="#07090E" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{
              fontSize: '11px',
              fontWeight: 700,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              color: 'var(--accent-cyan)',
              backgroundColor: 'var(--accent-cyan-dim)',
              padding: '2px 8px',
              borderRadius: 'var(--radius-pill)'
            }}>
              INDMoney
            </span>
            <h1 style={{ fontSize: '17px', fontWeight: 600, color: 'var(--text-primary)' }}>
              Facts-Only MF Assistant
            </h1>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Verified AMC, SEBI & AMFI Sourced • Zero Investment Advice
          </p>
        </div>
      </div>

      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        backgroundColor: 'var(--bg-surface)',
        border: '1px solid var(--glass-border)',
        padding: '6px 12px',
        borderRadius: 'var(--radius-pill)',
        fontSize: '12px',
        color: 'var(--text-secondary)'
      }}>
        <Cpu size={14} color="var(--accent-cyan)" />
        <span>Engine: <strong style={{ color: 'var(--text-primary)' }}>{activeModel || 'Gemini 2.5 Flash'}</strong></span>
      </div>
    </header>
  );
}
