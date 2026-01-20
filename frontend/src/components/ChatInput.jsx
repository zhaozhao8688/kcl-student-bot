/**
 * ChatInput component - Fixed bottom input area with send button
 */

import React, { useState } from 'react';
import { Send } from 'lucide-react';

export function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput('');
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 p-4 bg-white/80 backdrop-blur-xl border-t border-slate-200 z-40">
      <div className="max-w-3xl mx-auto">
        <form onSubmit={handleSubmit} className="relative group">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={disabled}
            placeholder="Type a message..."
            className="w-full bg-slate-100 border border-slate-200 rounded-2xl py-3.5 pl-5 pr-14 text-charcoal placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-muted-gold focus:ring-1 focus:ring-muted-gold transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || disabled}
            className="absolute right-2 top-2 bottom-2 aspect-square bg-charcoal hover:bg-black disabled:bg-slate-200 disabled:text-slate-400 text-white flex items-center justify-center rounded-xl transition-all active:scale-95"
          >
            <Send className="w-5 h-5 ml-0.5" />
          </button>
        </form>
      </div>
    </div>
  );
}
