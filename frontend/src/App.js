/**
 * Main App component for KCL Student Bot
 */

import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { TimetableModal } from './components/TimetableModal';
import { chatAPI, timetableAPI, sessionAPI } from './services/api';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [icalUrl, setIcalUrl] = useState('');
  const [hasTimetable, setHasTimetable] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isTimetableOpen, setIsTimetableOpen] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize session on mount
  useEffect(() => {
    const initSession = async () => {
      // Add initial AI message immediately
      setMessages([
        {
          id: '1',
          role: 'ai',
          content:
            "Hey! I'm your King's AI assistant. Ask me anything about campus, libraries, or where to get the best coffee. You can also sync your timetable above!",
          timestamp: new Date().toISOString()
        }
      ]);

      // Try to create session in background
      try {
        const res = await sessionAPI.create();
        setSessionId(res.session_id);
        console.log('Session created:', res.session_id);
      } catch (error) {
        console.error('Error creating session on mount:', error);
        // Don't show error - session will be created on first message
        console.log('Session will be created on first message');
      }
    };

    initSession();
  }, []);

  // Handle sending a message
  const handleSendMessage = async (query) => {
    // Create session if not exists
    let currentSessionId = sessionId;
    if (!currentSessionId) {
      try {
        console.log('Creating session on first message...');
        const res = await sessionAPI.create();
        currentSessionId = res.session_id;
        setSessionId(currentSessionId);
        console.log('Session created:', currentSessionId);
      } catch (error) {
        console.error('Failed to create session:', error);
        // Add error message
        const errorMsg = {
          id: `error-${Date.now()}`,
          role: 'ai',
          content:
            "I'm sorry, I can't connect to the server right now. Please check your internet connection and try again.",
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, errorMsg]);
        return;
      }
    }

    // Add user message to UI
    const userMsg = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Call API
      const res = await chatAPI.sendMessage(query, currentSessionId, icalUrl || null);

      // Add AI response to UI
      const aiMsg = {
        id: `ai-${Date.now()}`,
        role: 'ai',
        content: res.response,
        timestamp: new Date().toISOString()
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error('Chat error:', error);

      // Add error message
      const errorMsg = {
        id: `error-${Date.now()}`,
        role: 'ai',
        content:
          "I'm sorry, I encountered an error processing your message. Please try again.",
        timestamp: new Date().toISOString()
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle timetable sync
  const handleSyncTimetable = async (source) => {
    if (!sessionId) {
      console.error('No session ID available');
      return;
    }

    try {
      await timetableAPI.setUrl(sessionId, source);
      setIcalUrl(source);
      setHasTimetable(true);
      console.log('Timetable synced:', source);
    } catch (error) {
      console.error('Error syncing timetable:', error);
      throw error;
    }
  };

  // Handle clear chat
  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      // Reset to initial welcome message
      setMessages([
        {
          id: '1',
          role: 'ai',
          content:
            "Hey! I'm your King's AI assistant. Ask me anything about campus, libraries, or where to get the best coffee. You can also sync your timetable above!",
          timestamp: new Date().toISOString()
        }
      ]);
      console.log('Chat cleared');
    }
  };

  return (
    <div className="min-h-screen bg-lab-white text-charcoal flex flex-col font-sans">
      {/* Header */}
      <Header
        onOpenTimetable={() => setIsTimetableOpen(true)}
        hasTimetable={hasTimetable}
        onClearChat={handleClearChat}
      />

      {/* Timetable Modal */}
      <TimetableModal
        isOpen={isTimetableOpen}
        onClose={() => setIsTimetableOpen(false)}
        onSync={handleSyncTimetable}
      />

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto pt-24 pb-28 px-4 sm:px-0">
        <div className="max-w-3xl mx-auto flex flex-col">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} msg={msg} />
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex w-full mb-6 justify-start">
              <div className="flex flex-col max-w-[85%] sm:max-w-[75%] items-start">
                <div className="px-5 py-3.5 bg-white text-slate-700 border border-slate-100 rounded-2xl rounded-tl-none shadow-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                      style={{ animationDelay: '0.1s' }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                      style={{ animationDelay: '0.2s' }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Scroll anchor */}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Chat Input */}
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}

export default App;
