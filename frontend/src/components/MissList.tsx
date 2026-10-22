import { useState } from 'react';
import { useMisses } from '../hooks/useMisses';

export function MissList({ kind }: { kind?: string }) {
  const [filterKind, setFilterKind] = useState<string>(kind || '');
  const { misses, loading, error, refetch } = useMisses(filterKind || undefined);

  const kinds = ['skill', 'role', 'industry'] as const;

  return (
    <div className="card miss-list">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <h2 style={{ margin: '0' }}>Recorded Misses</h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <label htmlFor="miss-kind-filter" style={{ marginBottom: '0', fontSize: '0.875rem' }}>Filter:</label>
          <select
            id="miss-kind-filter"
            value={filterKind}
            onChange={(e) => setFilterKind(e.target.value)}
            style={{ width: 'auto', padding: '0.375rem 0.75rem' }}
          >
            <option value="">All Types</option>
            {kinds.map((k) => (
              <option key={k} value={k}>{k.charAt(0).toUpperCase() + k.slice(1)}</option>
            ))}
          </select>
          <button className="btn btn-secondary" onClick={refetch} style={{ padding: '0.375rem 0.75rem' }}>
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div style={{ padding: '0.875rem', background: '#fee2e2', borderRadius: '6px', color: '#991b1b', marginBottom: '1rem' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>Loading...</div>
      ) : misses.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
          No misses recorded yet. Search for unknown terms to populate this list.
        </div>
      ) : (
        <div>
          {misses.map((miss) => (
            <div key={miss.id} className="miss-item">
              <div className="miss-info">
                <span className="miss-term">
                  <code>{miss.raw_term}</code> (normalized: <code>{miss.normalized_term}</code>)
                </span>
                <span className="miss-meta">
                  Kind: <strong>{miss.kind}</strong> {'\u2022'} Requests: <strong>{miss.request_count}</strong> {'\u2022'}
                  First: {new Date(miss.first_requested_at).toLocaleDateString()} {'\u2022'}
                  Last: {new Date(miss.last_requested_at).toLocaleDateString()}
                  {miss.submitted_by && ` {'\u2022'} By: ${miss.submitted_by}`}
                  {miss.status !== 'pending' && ` {'\u2022'} Status: ${miss.status}`}
                </span>
              </div>
              <span className={`badge ${miss.status === 'pending' ? 'badge-miss' : miss.status === 'accepted' ? 'badge-canonical' : 'badge-alias'}`}>
                {miss.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}