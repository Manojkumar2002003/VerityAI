import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { NotFoundPage } from './NotFoundPage';
import { renderWithRouter } from '../test/test-utils';

describe('NotFoundPage component', () => {
  it('renders the 404 heading and helpful explanation', () => {
    renderWithRouter(<NotFoundPage />);

    expect(
      screen.getByRole('heading', { level: 1, name: /Page Not Found/i })
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /The requested page does not exist or has not been implemented yet/i
      )
    ).toBeInTheDocument();
  });

  it('renders a return to home navigation link pointing to "/"', () => {
    renderWithRouter(<NotFoundPage />);

    const homeLink = screen.getByRole('link', { name: /Return to Home/i });
    expect(homeLink).toBeInTheDocument();
    expect(homeLink).toHaveAttribute('href', '/');
  });
});
