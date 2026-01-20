/**
 * Header component with branding and timetable sync button
 */

import React from 'react';
import { GraduationCap, Calendar, CheckCircle2, Trash2 } from 'lucide-react';

export function Header({ onOpenTimetable, hasTimetable, onClearChat }) {
  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-white/90 backdrop-blur-md border-b border-slate-200 z-50 flex items-center justify-between px-6 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-charcoal rounded-lg flex items-center justify-center text-muted-gold">
          <GraduationCap className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-charcoal">King's AI</h1>
          <p className="text-xs text-slate-500 font-medium">Student Assistant</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={onClearChat}
          className="px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 border bg-white text-slate-600 border-slate-200 hover:border-red-400 hover:text-red-600 hover:bg-red-50"
          title="Clear chat"
        >
          <Trash2 className="w-4 h-4" />
          <span className="hidden sm:inline">Clear Chat</span>
        </button>

        <button
          onClick={onOpenTimetable}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 border ${
            hasTimetable
              ? 'bg-muted-gold/10 text-muted-gold border-muted-gold hover:bg-muted-gold/20'
              : 'bg-white text-slate-600 border-slate-200 hover:border-charcoal hover:text-charcoal'
          }`}
        >
          {hasTimetable ? (
            <CheckCircle2 className="w-4 h-4" />
          ) : (
            <Calendar className="w-4 h-4" />
          )}
          <span className="hidden sm:inline">
            {hasTimetable ? 'Timetable Synced' : 'Sync Timetable'}
          </span>
        </button>
      </div>
    </header>
  );
}
