import { render, screen } from '@testing-library/react';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { Layout } from './Layout';

describe('Layout component', () => {
  it('renders header, main content outlet, and footer', () => {
    const router = createMemoryRouter(
      [
        {
          path: '/',
          element: <Layout />,
          children: [
            {
              index: true,
              element: <div data-testid="outlet-content">Test Page Content</div>,
            },
          ],
        },
      ],
      { initialEntries: ['/'] }
    );

    render(<RouterProvider router={router} />);

    // Header presence
    expect(screen.getByLabelText(/VerityAI Home/i)).toBeInTheDocument();

    // Outlet content presence
    expect(screen.getByTestId('outlet-content')).toBeInTheDocument();
    expect(screen.getByText('Test Page Content')).toBeInTheDocument();

    // Footer presence
    expect(
      screen.getByText(/Automated AI-text detection is probabilistic/i)
    ).toBeInTheDocument();
  });
});
