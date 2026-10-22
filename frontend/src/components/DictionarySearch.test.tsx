import { render, screen, fireEvent } from '@testing-library/react';
import { vi, describe, it, beforeEach, expect } from 'vitest';
import { DictionarySearch } from './DictionarySearch';
import { useDictionaryLookup } from '../hooks/useDictionaryLookup';
import { api } from '../api/client';

// Mock the hook
vi.mock('../hooks/useDictionaryLookup');

// Mock the API
vi.mock('../api/client');

describe('DictionarySearch', () => {
  const mockLookup = vi.fn();
  const mockClear = vi.fn();
  const mockGetResultBadge = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: null,
      loading: false,
      error: null,
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    mockGetResultBadge.mockImplementation((type: string) => ({
      label: type.charAt(0).toUpperCase() + type.slice(1),
      className: `badge-${type}`,
    }));
  });

  it('renders search form with kind selector and term input', () => {
    render(<DictionarySearch />);
    expect(screen.getByLabelText('Type')).toBeInTheDocument();
    expect(screen.getByLabelText('Term')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Check' })).toBeInTheDocument();
  });

  it('calls lookup on form submit', () => {
    render(<DictionarySearch />);
    fireEvent.change(screen.getByLabelText('Term'), { target: { value: 'k8s' } });
    fireEvent.click(screen.getByRole('button', { name: 'Check' }));
    expect(mockLookup).toHaveBeenCalledWith('skill', 'k8s');
  });

  it('changes kind selector', () => {
    render(<DictionarySearch />);
    fireEvent.change(screen.getByLabelText('Type'), { target: { value: 'role' } });
    fireEvent.change(screen.getByLabelText('Term'), { target: { value: 'swe' } });
    fireEvent.click(screen.getByRole('button', { name: 'Check' }));
    expect(mockLookup).toHaveBeenCalledWith('role', 'swe');
  });

  it('shows error state', () => {
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: null,
      loading: false,
      error: 'Network error',
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    render(<DictionarySearch />);
    expect(screen.getByText('Network error')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: null,
      loading: true,
      error: null,
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    render(<DictionarySearch />);
    expect(screen.getByRole('button', { name: 'Checking...' })).toBeInTheDocument();
  });

  it('displays canonical result', () => {
    const mockResult = {
      result_type: 'canonical' as const,
      kind: 'skill' as const,
      term: 'kubernetes',
      canonical_slug: 'kubernetes',
      display_label: 'Kubernetes',
    };
    mockGetResultBadge.mockReturnValue({ label: 'Canonical', className: 'badge-canonical' });
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: mockResult,
      loading: false,
      error: null,
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    render(<DictionarySearch />);
    expect(screen.getByText('Canonical')).toBeInTheDocument();
    expect(screen.getByText('Kubernetes')).toBeInTheDocument();
  });

  it('displays alias result with resolved target', () => {
    const mockResult = {
      result_type: 'alias' as const,
      kind: 'skill' as const,
      term: 'k8s',
      canonical_slug: 'kubernetes',
      display_label: 'Kubernetes',
      resolved_to: 'kubernetes',
    };
    mockGetResultBadge.mockReturnValue({ label: 'Alias', className: 'badge-alias' });
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: mockResult,
      loading: false,
      error: null,
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    render(<DictionarySearch />);
    expect(screen.getByText('Alias')).toBeInTheDocument();
    expect(screen.getByText('Resolves to: Kubernetes')).toBeInTheDocument();
  });

  it('displays miss result with miss list notice', () => {
    const mockResult = {
      result_type: 'miss' as const,
      kind: 'skill' as const,
      term: 'quantum-computing',
    };
    mockGetResultBadge.mockReturnValue({ label: 'Not Found', className: 'badge-miss' });
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: mockResult,
      loading: false,
      error: null,
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    render(<DictionarySearch />);
    expect(screen.getByText('Not Found')).toBeInTheDocument();
    expect(screen.getByText('recorded for maintainer review')).toBeInTheDocument();
  });

  it('clear button resets form', () => {
    const mockResult = {
      result_type: 'canonical' as const,
      kind: 'skill' as const,
      term: 'kubernetes',
      canonical_slug: 'kubernetes',
      display_label: 'Kubernetes',
    };
    (useDictionaryLookup as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
      result: mockResult,
      loading: false,
      error: null,
      lookup: mockLookup,
      clear: mockClear,
      getResultBadge: mockGetResultBadge,
    });
    render(<DictionarySearch />);
    fireEvent.click(screen.getByRole('button', { name: 'Clear' }));
    expect(mockClear).toHaveBeenCalled();
  });
});