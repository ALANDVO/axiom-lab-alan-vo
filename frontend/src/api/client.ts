import type { LookupRequest, LookupResponse, MissResponse } from '../types/api';

const API_BASE = '/api';

async function fetchJson<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  dictionary: {
    lookup: (request: LookupRequest) =>
      fetchJson<LookupResponse>(`${API_BASE}/dictionary/lookup`, {
        method: 'POST',
        body: JSON.stringify(request),
      }),

    listMisses: (params?: { kind?: string; status?: string; limit?: number; offset?: number }) => {
      const searchParams = new URLSearchParams();
      if (params?.kind) searchParams.set('kind', params.kind);
      if (params?.status) searchParams.set('status', params.status);
      if (params?.limit) searchParams.set('limit', String(params.limit));
      if (params?.offset) searchParams.set('offset', String(params.offset));
      return fetchJson<MissResponse[]>(`${API_BASE}/dictionary/misses?${searchParams.toString()}`);
    },

    seed: () =>
      fetchJson<{ status: string }>(`${API_BASE}/dictionary/seed`, {
        method: 'POST',
      }),
  },
};