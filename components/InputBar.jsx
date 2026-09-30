import React, { useState } from 'react';
import { Send } from 'lucide-react';

export default function InputBar({ onSendMessage, disabled }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      backgroundColor: 'var(--bg-secondary)',
      border: '1px solid var(--glass-border)',
      borderRadius: 'var(--radius-pill)',
      padding: '6px 8px 6px 18px',
      boxShadow: 'var(--shadow-card)',
      transition: 'border-color 0.2s ease'
    }}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask a factual question (e.g., minimum SIP, exit load, ELSS lock-in)..."
        disabled={disabled}
        style={{
          flex: 1,
          background: 'transparent',
          border: 'none',
          outline: 'none',
          color: 'var(--text-primary)',
          fontSize: '14px'
        }}
      />

      <button
        type="submit"
        disabled={disabled || !input.trim()}
        style={{
          width: '38px',
          height: '38px',
          borderRadius: '50%',
          backgroundColor: input.trim() && !disabled ? 'var(--accent-cyan)' : 'var(--bg-surface)',
          color: input.trim() && !disabled ? '#07090E' : 'var(--text-muted)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.2s ease',
          cursor: input.trim() && !disabled ? 'pointer' : 'not-allowed'
        }}
      >
        <Send size={18} />
      </button>
    </form>
  );
}
