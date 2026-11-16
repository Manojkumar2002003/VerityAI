import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Footer } from './Footer';

describe('Footer component', () => {
  it('renders the brand title and focus descriptor', () => {
    render(<Footer />);

    expect(screen.getByText('VerityAI')).toBeInTheDocument();
    expect(screen.getByText(/English-Language Text Analysis/i)).toBeInTheDocument();
  });

  it('renders the probabilistic detection limitation disclaimer', () => {
    render(<Footer />);

    const disclaimer = screen.getByText(/Automated AI-text detection is probabilistic/i);
    expect(disclaimer).toBeInTheDocument();
    expect(
      screen.getByText(/informative indicators, not definitive proof/i)
    ).toBeInTheDocument();
  });

  it('renders the shell status notice', () => {
    render(<Footer />);

    expect(screen.getByText(/Sprint 1 • Feature 1.2 Shell/i)).toBeInTheDocument();
  });
});
