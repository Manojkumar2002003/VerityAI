import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200 bg-white mt-auto">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-slate-800 text-sm">VerityAI</span>
              <span className="text-slate-400 text-xs">•</span>
              <span className="text-xs text-slate-500">
                English-Language Text Analysis
              </span>
            </div>
            <p className="mt-2 text-xs text-slate-500 leading-relaxed max-w-3xl">
              <strong>Disclaimer:</strong> Automated AI-text detection is probabilistic
              and cannot conclusively establish authorship or verify authentic origin.
              Detection signals reflect statistical patterns and should be treated as
              informative indicators, not definitive proof.
            </p>
          </div>

          <div className="text-xs text-slate-400 self-start md:self-auto shrink-0">
            Sprint 1 • Feature 1.2 Shell
          </div>
        </div>
      </div>
    </footer>
  );
};
