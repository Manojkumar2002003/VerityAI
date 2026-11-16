import React from 'react';

export const HomePage: React.FC = () => {
  return (
    <div className="space-y-10">
      {/* Hero Introduction */}
      <section className="space-y-4 max-w-3xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-sky-50 text-sky-700 border border-sky-200">
          <span
            className="w-2 h-2 rounded-full bg-sky-500 animate-pulse"
            aria-hidden="true"
          />
          <span>Frontend Foundation • Active Development</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
          VerityAI — AI-Generated Text Detection
        </h1>

        <p className="text-base sm:text-lg text-slate-600 leading-relaxed">
          VerityAI is being engineered to analyze written English text and evaluate
          whether it exhibits linguistic and stylistic patterns characteristic of
          AI-generated content.
        </p>
      </section>

      {/* Analysis Workspace Placeholder */}
      <section
        className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden"
        aria-labelledby="workspace-placeholder-heading"
      >
        <div className="border-b border-slate-100 bg-slate-50/75 px-6 py-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div>
            <h2
              id="workspace-placeholder-heading"
              className="text-base font-semibold text-slate-900"
            >
              Text Analysis Workspace
            </h2>
            <p className="text-xs text-slate-500">
              Interactive text submission and document inspection area
            </p>
          </div>
          <span className="inline-flex items-center text-xs font-medium text-amber-800 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-md self-start sm:self-auto">
            Module Deferred to Subsequent Feature
          </span>
        </div>

        <div className="p-6 sm:p-8 space-y-6">
          {/* Visual Workspace Mock / Placeholder */}
          <div className="border-2 border-dashed border-slate-200 rounded-lg p-6 sm:p-8 bg-slate-50/50 text-center space-y-3">
            <div className="mx-auto w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-400">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1.5}
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
                />
              </svg>
            </div>

            <div className="space-y-1">
              <h3 className="text-sm font-semibold text-slate-800">
                Text Submission &amp; Inspection Preview
              </h3>
              <p className="text-xs text-slate-500 max-w-lg mx-auto">
                Text input, file uploads, document-level verdicts, and passage-level
                highlighting will be enabled once the backend API and ML inference engine
                are connected in later milestones.
              </p>
            </div>

            <div className="pt-2">
              <div className="w-full max-w-xl mx-auto h-24 rounded border border-slate-200 bg-white p-3 text-left text-xs text-slate-400 select-none">
                Paste or type English text here for AI detection analysis... (Enabled in
                future sprint feature)
              </div>
            </div>
          </div>

          {/* Planned Capabilities Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="p-4 rounded-lg border border-slate-200 bg-white space-y-1.5">
              <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
                <span
                  className="w-1.5 h-1.5 rounded-full bg-sky-500"
                  aria-hidden="true"
                />
                <span>Transformer Encoder</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Fine-tuned DeBERTa-v3 model architecture evaluated against RoBERTa and
                TF-IDF baselines.
              </p>
            </div>

            <div className="p-4 rounded-lg border border-slate-200 bg-white space-y-1.5">
              <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
                <span
                  className="w-1.5 h-1.5 rounded-full bg-sky-500"
                  aria-hidden="true"
                />
                <span>Calibrated Confidence</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Empirically calibrated probability scores to communicate statistical
                uncertainty honestly.
              </p>
            </div>

            <div className="p-4 rounded-lg border border-slate-200 bg-white space-y-1.5">
              <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
                <span
                  className="w-1.5 h-1.5 rounded-full bg-sky-500"
                  aria-hidden="true"
                />
                <span>Passage Highlighting</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Granular section-by-section analysis to highlight AI-associated text
                segments.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Foundation Status Notice */}
      <section className="bg-slate-100/80 border border-slate-200 rounded-lg p-5">
        <div className="flex items-start space-x-3">
          <div className="mt-0.5 text-slate-500 shrink-0">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.5}
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
              />
            </svg>
          </div>
          <div className="text-xs text-slate-600 space-y-1">
            <p className="font-semibold text-slate-800">
              Sprint 1, Feature 1.2 Status Notice
            </p>
            <p className="leading-relaxed">
              This interface represents the foundational frontend application shell.
              Backend API communication (Feature 1.3), ML inference pipelines, dataset
              validation, and user submission endpoints are intentionally not yet
              connected.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};
