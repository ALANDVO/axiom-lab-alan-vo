import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, beforeEach, expect } from 'vitest';
import { MissList } from './MissList';
import { useMisses } from '../hooks/useMisses';

vi.mock('../hooks/useMisses');

describe('MissList', () => {
  const mockMisses = [
    {
      id: 1,
      kind: 'skill',
      raw_term: 'quantum-computing',
      normalized_term: 'quantum-computing',
      request_count: 5,
      first_requested_at: '2024-01-15T10:00:00Z',
      last_requested_at: '2024-01-20T10:00:00Z',
      submitted_by: 'user123',
      status: 'pending',
    },
    {
      id: 2,
      kind: 'role',
      raw_term: 'quantum-engineer',
      normalized_term: 'quantum-engineer',
      request_count: 2,
      first_requested_at: '2024-01-10T10:00:00Z',
      last_requested_at: '2024-01-18T10:00:00Z',
      submitted_by: null,
      status: 'pending',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    (useMisses as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      misses: mockMisses,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
  });

  it('renders misses list with filter', () => {
    render(<MissList />);
    expect(screen.getByText('Recorded Misses')).toBeInTheDocument();
    expect(screen.getByLabelText('Filter:')).toBeInTheDocument();
    expect(screen.getByText('quantum-computing')).toBeInTheDocument();
    expect(screen.getByText('quantum-engineer')).toBeInTheDocument();
  });

  it('filters by kind', () => {
    render(<MissList />);
    fireEvent.change(screen.getByLabelText('Filter:'), { target: { value: 'skill' } });
    expect(screen.getByText('quantum-computing')).toBeInTheDocument();
    expect(screen.queryByText('quantum-engineer')).not.toBeInTheDocument();
  });

  it('shows loading state', () => {
    (useMisses as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      misses: [],
      loading: true,
      error: null,
      refetch: vi.fn(),
    });
    render(<MissList />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('shows empty state', () => {
    (useMisses as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      misses: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    render(<MissList />);
    expect(screen.getByText('No misses recorded yet')).toBeInTheDocument();
  });

  it('shows error state', () => {
    (useMisses as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      misses: [],
      loading: false,
      error: 'Failed to fetch',
      refetch: vi.fn(),
    });
    render(<MissList />);
    expect(screen.getByText('Failed to fetch')).toBeInTheDocument();
  });

  it('displays miss metadata correctly', () => {
    render(<MissList />);
    expect(screen.getByText('Kind: skill')).toBeInTheDocument();
    expect(screen.getByText('Requests: 5')).toBeInTheDocument();
    expect(screen.getByText('By: user123')).toBeInTheDocument();
    expect(screen.getByText('Status: pending')).toBeInTheDocument();
  });
});