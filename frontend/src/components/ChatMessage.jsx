/**
 * ChatMessage component - Individual message bubble
 * Supports Markdown rendering for AI responses
 */

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export function ChatMessage({ msg }) {
  const isAI = msg.role === 'ai' || msg.role === 'assistant';

  return (
    <div className={`flex w-full mb-6 ${isAI ? 'justify-start' : 'justify-end'}`}>
      <div className={`flex flex-col max-w-[85%] sm:max-w-[75%] ${isAI ? 'items-start' : 'items-end'}`}>
        <div
          className={`px-5 py-3.5 text-[15px] leading-relaxed rounded-2xl shadow-sm ${
            isAI
              ? 'bg-white text-slate-700 border border-slate-100 rounded-tl-none'
              : 'bg-charcoal text-white rounded-tr-none shadow-md'
          }`}
        >
          {isAI ? (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              className="markdown-content"
              components={{
                // Paragraphs
                p: ({ children }) => <p className="mb-3 last:mb-0">{children}</p>,
                // Headers
                h1: ({ children }) => <h1 className="text-xl font-bold mb-3 mt-4 first:mt-0">{children}</h1>,
                h2: ({ children }) => <h2 className="text-lg font-bold mb-2 mt-3 first:mt-0">{children}</h2>,
                h3: ({ children }) => <h3 className="text-base font-bold mb-2 mt-2 first:mt-0">{children}</h3>,
                // Lists
                ul: ({ children }) => <ul className="list-disc list-inside mb-3 space-y-1">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside mb-3 space-y-1">{children}</ol>,
                li: ({ children }) => <li className="ml-2">{children}</li>,
                // Code
                code: ({ inline, children }) =>
                  inline ? (
                    <code className="bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded text-sm font-mono">
                      {children}
                    </code>
                  ) : (
                    <code className="block bg-slate-100 text-slate-800 p-3 rounded-lg my-2 text-sm font-mono overflow-x-auto">
                      {children}
                    </code>
                  ),
                pre: ({ children }) => <pre className="my-2">{children}</pre>,
                // Links
                a: ({ href, children }) => (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    {children}
                  </a>
                ),
                // Blockquotes
                blockquote: ({ children }) => (
                  <blockquote className="border-l-4 border-slate-300 pl-4 italic my-2 text-slate-600">
                    {children}
                  </blockquote>
                ),
                // Strong/Bold
                strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                // Emphasis/Italic
                em: ({ children }) => <em className="italic">{children}</em>,
                // Horizontal rule
                hr: () => <hr className="my-4 border-slate-200" />,
              }}
            >
              {msg.content}
            </ReactMarkdown>
          ) : (
            <div className="whitespace-pre-wrap">{msg.content}</div>
          )}
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
