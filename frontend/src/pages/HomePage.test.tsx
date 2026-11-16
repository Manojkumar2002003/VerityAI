import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { HomePage } from './HomePage';

describe('HomePage component', () => {
  it('renders hero title and English-language platform description', () => {
    render(<HomePage />);

    expect(
      screen.getByRole('heading', {
        level: 1,
        name: /VerityAI — AI-Generated Text Detection/i,
      })
    ).toBeInTheDocument();

    expect(
      screen.getByText(/VerityAI is being engineered to analyze written English text/i)
    ).toBeInTheDocument();
  });

  it('renders the text analysis workspace placeholder and deferred notice', () => {
    render(<HomePage />);

    expect(
      screen.getByRole('heading', {
        level: 2,
        name: /Text Analysis Workspace/i,
      })
    ).toBeInTheDocument();

    expect(
      screen.getByText(/Module Deferred to Subsequent Feature/i)
    ).toBeInTheDocument();
    expect(screen.getByText(/Text Submission & Inspection Preview/i)).toBeInTheDocument();
  });

  it('displays the three planned architectural capabilities', () => {
    render(<HomePage />);

    expect(screen.getByText('Transformer Encoder')).toBeInTheDocument();
    expect(
      screen.getByText(/Fine-tuned DeBERTa-v3 model architecture/i)
    ).toBeInTheDocument();

    expect(screen.getByText('Calibrated Confidence')).toBeInTheDocument();
    expect(
      screen.getByText(/Empirically calibrated probability scores/i)
    ).toBeInTheDocument();

    expect(screen.getByText('Passage Highlighting')).toBeInTheDocument();
    expect(screen.getByText(/Granular section-by-section analysis/i)).toBeInTheDocument();
  });

  it('renders foundational status notice', () => {
    render(<HomePage />);

    expect(screen.getByText(/Sprint 1, Feature 1.2 Status Notice/i)).toBeInTheDocument();
    expect(
      screen.getByText(
        /This interface represents the foundational frontend application shell/i
      )
    ).toBeInTheDocument();
  });
});
