'use client';

import React, { useState } from 'react';
import Header from '@/components/Header';
import WelcomeCard from '@/components/WelcomeCard';
import ExamplePills from '@/components/ExamplePills';
import ChatStream from '@/components/ChatStream';
import InputBar from '@/components/InputBar';
import DisclaimerFooter from '@/components/DisclaimerFooter';

export default function Page() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeModel, setActiveModel] = useState('Gemini 2.5 Flash');

  const handleSendMessage = async (queryText) => {
    if (!queryText.trim() || isLoading) return;

    // Add user message
    const userMessage = { role: 'user', text: queryText };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: queryText })
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const data = await response.json();

      if (data.model_used) {
        setActiveModel(data.model_used);
      }

      const assistantMessage = {
        role: 'assistant',
        text: data.answer,
        type: data.type || 'FACTUAL',
        source_url: data.source_url,
        source_title: data.source_title,
        last_verified_at: data.last_verified_at
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: 'An error occurred while communicating with the assistant. Please try again.',
          type: 'UNVERIFIED'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh',
      maxWidth: '860px',
      margin: '0 auto',
      width: '100%'
    }}>
      <Header activeModel={activeModel} />

      <main style={{
        flex: 1,
        padding: '0 20px 100px 20px',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <WelcomeCard />

        <ExamplePills
          onSelectQuery={handleSendMessage}
          disabled={isLoading}
        />

        <ChatStream messages={messages} isLoading={isLoading} />
      </main>

      <div style={{
        position: 'fixed',
        bottom: '40px',
        left: 0,
        right: 0,
        maxWidth: '860px',
        margin: '0 auto',
        padding: '0 20px',
        zIndex: 30
      }}>
        <InputBar onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>

      <div style={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 20 }}>
        <DisclaimerFooter />
      </div>
    </div>
  );
}
