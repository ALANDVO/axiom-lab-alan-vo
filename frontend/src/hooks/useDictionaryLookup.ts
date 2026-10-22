import { useState } from 'react';
import type { DictionaryKind, LookupResponse, LookupResultType } from '../types/api';
import { api } from '../api/client';

export function useDictionaryLookup() {
  const [result, setResult] = useState<LookupResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const lookup = async (kind: DictionaryKind, term: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.dictionary.lookup({ kind, term });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Lookup failed');
    } finally {
      setLoading(false);
    }
  };

  const clear = () => {
    setResult(null);
    setError(null);
  };

  const getResultBadge = (type: LookupResultType) => {
    switch (type) {
      case 'canonical':
        return { label: 'Canonical', className: 'badge-canonical' };
      case 'alias':
        return { label: 'Alias', className: 'badge-alias' };
      case 'miss':
        return { label: 'Not Found', className: 'badge-miss' };
    }
  };

  return { result, loading, error, lookup, clear, getResultBadge };
}