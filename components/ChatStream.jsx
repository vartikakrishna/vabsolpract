import React from 'react';
import { ExternalLink, Calendar, CheckCircle2, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function ChatStream({ messages, isLoading }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      paddingBottom: '24px'
    }}>
      {messages.map((msg, idx) => {
        const isUser = msg.role === 'user';

        return (
          <div
            key={idx}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: isUser ? 'flex-end' : 'flex-start',
              width: '100%'
            }}
          >
            {/* Message Bubble */}
            <div style={{
              maxWidth: '85%',
              backgroundColor: isUser ? 'var(--bg-surface-active)' : 'var(--bg-secondary)',
              border: `1px solid ${isUser ? 'rgba(47, 111, 237, 0.3)' : 'var(--glass-border)'}`,
              borderRadius: 'var(--radius-lg)',
              padding: '16px 20px',
              boxShadow: 'var(--shadow-card)',
              position: 'relative'
            }}>
              {/* Type Badge for Assistant */}
              {!isUser && (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  marginBottom: '8px',
                  fontSize: '11px',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em'
                }}>
                  {msg.type === 'FACTUAL' && (
                    <span style={{ color: 'var(--status-verified)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <CheckCircle2 size={13} /> Verified Factual Grounding
                    </span>
                  )}
                  {msg.type === 'ADVICE_REFUSAL' && (
                    <span style={{ color: 'var(--status-refusal)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <AlertTriangle size={13} /> Investment Advice Refusal
                    </span>
                  )}
                  {msg.type === 'PII_REJECTION' && (
                    <span style={{ color: 'var(--status-refusal)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <ShieldAlert size={13} /> PII Security Gate
                    </span>
                  )}
                  {msg.type === 'UNVERIFIED' && (
                    <span style={{ color: 'var(--status-warning)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <AlertTriangle size={13} /> Unverified In Official Sources
                    </span>
                  )}
                </div>
              )}

              {/* Message Content */}
              <p style={{
                fontSize: '14px',
                color: 'var(--text-primary)',
                lineHeight: '1.6',
                whiteSpace: 'pre-wrap'
              }}>
                {msg.text}
              </p>

              {/* Verified Source Link Box */}
              {!isUser && msg.source_url && (
                <div style={{
                  marginTop: '12px',
                  paddingTop: '12px',
                  borderTop: '1px solid var(--glass-border)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px',
                  fontSize: '12px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Source:</span>
                    <a
                      href={msg.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: 'var(--accent-cyan)',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        textDecoration: 'underline',
                        textUnderlineOffset: '3px'
                      }}
                    >
                      <span>{msg.source_title || msg.source_url}</span>
                      <ExternalLink size={12} />
                    </a>
                  </div>

                  {msg.last_verified_at && (
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                      color: 'var(--text-muted)',
                      fontSize: '11px'
                    }}>
                      <Calendar size={11} />
                      <span>Last updated from sources: {msg.last_verified_at}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        );
      })}

      {/* Loading Indicator */}
      {isLoading && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '14px 20px',
          backgroundColor: 'var(--bg-secondary)',
          border: '1px solid var(--glass-border)',
          borderRadius: 'var(--radius-lg)',
          width: 'fit-content'
        }}>
          <div style={{
            width: '8px',
            height: '8px',
            backgroundColor: 'var(--accent-cyan)',
            borderRadius: '50%',
            animation: 'pulse 1.2s infinite'
          }} />
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
            Retrieving verified official sources & generating grounded response...
          </span>
        </div>
      )}
    </div>
  );
}
