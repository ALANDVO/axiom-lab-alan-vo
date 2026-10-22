import { useState, useEffect } from 'react';
import type { MissResponse } from '../types/api';
import { api } from '../api/client';

export function useMisses(kind?: string) {
  const [misses, setMisses] = useState<MissResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMisses = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.dictionary.listMisses({ kind });
      setMisses(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch misses');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMisses();
  }, [kind]);

  return { misses, loading, error, refetch: fetchMisses };
}