import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Header } from './Header';
import { renderWithRouter } from '../../test/test-utils';

describe('Header component', () => {
  it('renders the branding logo and home link', () => {
    renderWithRouter(<Header />);

    const homeLink = screen.getByLabelText(/VerityAI Home/i);
    expect(homeLink).toBeInTheDocument();
    expect(homeLink).toHaveAttribute('href', '/');
    expect(screen.getByText('Verity')).toBeInTheDocument();
    expect(screen.getByText('AI')).toBeInTheDocument();
  });

  it('renders the product descriptor badge', () => {
    renderWithRouter(<Header />);

    expect(screen.getByText(/AI Text Analysis/i)).toBeInTheDocument();
  });

  it('renders the sprint status indicator', () => {
    renderWithRouter(<Header />);

    expect(screen.getByText(/Sprint 1 Foundation/i)).toBeInTheDocument();
  });
});
