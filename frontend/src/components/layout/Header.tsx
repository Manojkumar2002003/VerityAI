import React from 'react';
import { Link } from 'react-router-dom';

export const Header: React.FC = () => {
  return (
    <header className="border-b border-slate-200 bg-white/95 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Link
            to="/"
            className="flex items-center space-x-2 text-slate-900 hover:text-sky-700 transition-colors focus-visible:ring-2 focus-visible:ring-sky-600 rounded-sm"
            aria-label="VerityAI Home"
          >
            <span className="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center text-white font-bold text-lg shadow-sm">
              V
            </span>
            <span className="font-semibold text-xl tracking-tight text-slate-900">
              Verity<span className="text-sky-600">AI</span>
            </span>
          </Link>

          <span
            className="hidden sm:inline-block h-4 w-px bg-slate-300"
            aria-hidden="true"
          />

          <span className="hidden sm:inline-block text-xs font-medium uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
            AI Text Analysis
          </span>
        </div>

        <div className="flex items-center space-x-4">
          <span className="text-xs font-medium text-slate-600 bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-full">
            Sprint 1 Foundation
          </span>
        </div>
      </div>
    </header>
  );
};
