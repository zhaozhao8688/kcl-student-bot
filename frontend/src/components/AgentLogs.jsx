/**
 * AgentLogs component - displays streaming agent execution logs
 */

import React, { useEffect, useRef } from 'react';
import { Terminal, Loader2, CheckCircle, AlertCircle, Search, Globe, Calendar, Video } from 'lucide-react';

// Tool icons mapping
const toolIcons = {
  search: Search,
  scraper: Globe,
  timetable: Calendar,
  tiktok: Video
};

export function AgentLogs({ logs, isStreaming }) {
  const logsEndRef = useRef(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  if (!logs || logs.length === 0) {
    return null;
  }

  return (
    <div className="w-full mb-4">
      <div className="max-w-[85%] sm:max-w-[75%]">
        {/* Header */}
        <div className="flex items-center gap-2 mb-2 text-xs text-slate-500">
          <Terminal size={14} />
          <span>Agent Execution</span>
          {isStreaming && (
            <Loader2 size={12} className="animate-spin text-muted-gold" />
          )}
        </div>

        {/* Logs container */}
        <div className="bg-slate-900 rounded-lg p-3 font-mono text-xs overflow-hidden">
          <div className="max-h-48 overflow-y-auto space-y-1">
            {logs.map((log, index) => (
              <LogEntry key={index} log={log} />
            ))}
            <div ref={logsEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}

function LogEntry({ log }) {
  const { type, content, iteration, action_input } = log;

  // Determine icon and color based on log type/content
  let icon = null;
  let textColor = 'text-slate-300';

  if (content?.startsWith('ReAct reasoning')) {
    icon = <Loader2 size={12} className="animate-spin text-blue-400" />;
    textColor = 'text-blue-400';
  } else if (content?.startsWith('Thought:')) {
    icon = <span className="text-yellow-400">💭</span>;
    textColor = 'text-yellow-300';
  } else if (content?.startsWith('Action:')) {
    // Check if it's a tool action
    const actionMatch = content.match(/Action:\s*(\w+)/);
    if (actionMatch) {
      const toolName = actionMatch[1];
      const IconComponent = toolIcons[toolName];
      if (IconComponent) {
        icon = <IconComponent size={12} className="text-purple-400" />;
      } else if (toolName === 'final_answer') {
        icon = <CheckCircle size={12} className="text-green-400" />;
      }
    }
    textColor = 'text-purple-300';
  } else if (content?.startsWith('Executing tool:')) {
    const toolMatch = content.match(/Executing tool:\s*(\w+)/);
    if (toolMatch) {
      const IconComponent = toolIcons[toolMatch[1]];
      if (IconComponent) {
        icon = <IconComponent size={12} className="text-cyan-400 animate-pulse" />;
      }
    }
    textColor = 'text-cyan-300';
  } else if (content?.startsWith('Tool') && content?.includes('completed')) {
    icon = <CheckCircle size={12} className="text-green-400" />;
    textColor = 'text-green-300';
  } else if (content?.startsWith('Tool') && content?.includes('failed')) {
    icon = <AlertCircle size={12} className="text-red-400" />;
    textColor = 'text-red-300';
  } else if (content?.startsWith('Observation:')) {
    icon = <span className="text-slate-400">📝</span>;
    textColor = 'text-slate-400';
  } else if (content?.startsWith('Completed')) {
    icon = <CheckCircle size={12} className="text-green-400" />;
    textColor = 'text-green-400';
  }

  return (
    <div className={`flex items-start gap-2 ${textColor}`}>
      {iteration && (
        <span className="text-slate-600 shrink-0">[{iteration}]</span>
      )}
      {icon && <span className="shrink-0 mt-0.5">{icon}</span>}
      <span className="break-words">{content}</span>
    </div>
  );
}

export default AgentLogs;
