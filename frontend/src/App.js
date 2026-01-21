/**
 * Main App component for KCL Student Bot
 */

import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { TimetableModal } from './components/TimetableModal';
import { AgentLogs } from './components/AgentLogs';
import { chatAPI, timetableAPI, sessionAPI } from './services/api';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [icalUrl, setIcalUrl] = useState('');
  const [hasTimetable, setHasTimetable] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isTimetableOpen, setIsTimetableOpen] = useState(false);
  const [agentLogs, setAgentLogs] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
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
      } catch (error) {
        console.error('Error creating session on mount:', error);
        // Don't show error - session will be created on first message
      }
    };

    initSession();
  }, []);

  // Handle sending a message with streaming logs
  const handleSendMessage = async (query) => {
    // Create session if not exists
    let currentSessionId = sessionId;
    if (!currentSessionId) {
      try {
        const res = await sessionAPI.create();
        currentSessionId = res.session_id;
        setSessionId(currentSessionId);
      } catch (error) {
        console.error('Failed to create session:', error);
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
    setIsStreaming(true);
    setAgentLogs([]); // Clear previous logs

    // Extract conversation history (exclude welcome message)
    const conversationHistory = messages
      .filter(msg => msg.id !== '1')  // Exclude welcome message
      .map(msg => ({
        role: msg.role === 'ai' ? 'assistant' : msg.role,
        content: msg.content
      }));

    // Use streaming API
    chatAPI.streamMessage(query, currentSessionId, icalUrl || null, conversationHistory, {
      onLog: (logData) => {
        setAgentLogs((prev) => [...prev, logData]);
      },
      onResponse: (response) => {
        // Add AI response to UI
        const aiMsg = {
          id: `ai-${Date.now()}`,
          role: 'ai',
          content: response,
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, aiMsg]);
      },
      onError: (errorMessage) => {
        console.error('Stream error:', errorMessage);
        const errorMsg = {
          id: `error-${Date.now()}`,
          role: 'ai',
          content:
            "I'm sorry, I encountered an error processing your message. Please try again.",
          timestamp: new Date().toISOString()
        };
        setMessages((prev) => [...prev, errorMsg]);
        setIsLoading(false);
        setIsStreaming(false);
      },
      onDone: () => {
        setIsLoading(false);
        setIsStreaming(false);
        // Keep logs visible for a moment, then clear
        setTimeout(() => {
          setAgentLogs([]);
        }, 3000);
      }
    });
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

          {/* Agent Logs - shown while streaming */}
          {(isStreaming || agentLogs.length > 0) && (
            <div className="flex w-full mb-6 justify-start">
              <AgentLogs logs={agentLogs} isStreaming={isStreaming} />
            </div>
          )}

          {/* Loading indicator - only show if loading but no logs yet */}
          {isLoading && agentLogs.length === 0 && (
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
