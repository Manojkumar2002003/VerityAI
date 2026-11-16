import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import App from './app/App';
import { routes } from './app/router';

describe('VerityAI Frontend Application Shell', () => {
  it('renders the complete application without crashing', () => {
    render(<App />);
    expect(
      screen.getByRole('heading', {
        name: /VerityAI — AI-Generated Text Detection/i,
      })
    ).toBeInTheDocument();
  });

  it('renders header with VerityAI logo and product descriptor', () => {
    render(<App />);
    expect(screen.getByLabelText(/VerityAI Home/i)).toBeInTheDocument();
    expect(screen.getByText(/AI Text Analysis/i)).toBeInTheDocument();
  });

  it('renders home page introducing the platform and foundational status', () => {
    render(<App />);
    expect(
      screen.getByText(/VerityAI is being engineered to analyze written English text/i)
    ).toBeInTheDocument();
    expect(
      screen.getByRole('heading', { name: /Text Analysis Workspace/i })
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Module Deferred to Subsequent Feature/i)
    ).toBeInTheDocument();
  });

  it('renders footer with probabilistic detection disclaimer', () => {
    render(<App />);
    expect(
      screen.getByText(/Automated AI-text detection is probabilistic/i)
    ).toBeInTheDocument();
  });

  describe('Routing', () => {
    it('renders home page on "/" route', () => {
      const testRouter = createMemoryRouter(routes, {
        initialEntries: ['/'],
      });

      render(<RouterProvider router={testRouter} />);

      expect(
        screen.getByRole('heading', {
          name: /VerityAI — AI-Generated Text Detection/i,
        })
      ).toBeInTheDocument();
    });

    it('renders NotFoundPage on unknown route', () => {
      const testRouter = createMemoryRouter(routes, {
        initialEntries: ['/non-existent-page'],
      });

      render(<RouterProvider router={testRouter} />);

      expect(
        screen.getByRole('heading', { name: /Page Not Found/i })
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          /The requested page does not exist or has not been implemented yet/i
        )
      ).toBeInTheDocument();
      expect(screen.getByRole('link', { name: /Return to Home/i })).toBeInTheDocument();
    });

    it('navigates back to home from NotFoundPage', async () => {
      const user = userEvent.setup();
      const testRouter = createMemoryRouter(routes, {
        initialEntries: ['/some/nested/unknown/route'],
      });

      render(<RouterProvider router={testRouter} />);

      const returnLink = screen.getByRole('link', { name: /Return to Home/i });
      await user.click(returnLink);

      expect(
        await screen.findByRole('heading', {
          name: /VerityAI — AI-Generated Text Detection/i,
        })
      ).toBeInTheDocument();
    });
  });
});
