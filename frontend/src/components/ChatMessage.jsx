/**
 * ChatMessage component - Individual message bubble
 */

import React from 'react';

export function ChatMessage({ msg }) {
  const isAI = msg.role === 'ai' || msg.role === 'assistant';

  return (
    <div className={`flex w-full mb-6 ${isAI ? 'justify-start' : 'justify-end'}`}>
      <div className={`flex flex-col max-w-[85%] sm:max-w-[75%] ${isAI ? 'items-start' : 'items-end'}`}>
        <div
          className={`px-5 py-3.5 text-[15px] leading-relaxed rounded-2xl shadow-sm whitespace-pre-wrap ${
            isAI
              ? 'bg-white text-slate-700 border border-slate-100 rounded-tl-none'
              : 'bg-charcoal text-white rounded-tr-none shadow-md'
          }`}
        >
          {msg.content}
        </div>
        <span className="text-[10px] text-slate-400 mt-1.5 px-1 font-medium">
          {new Date(msg.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </span>
      </div>
    </div>
  );
}
