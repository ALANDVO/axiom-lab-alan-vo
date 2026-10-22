import { useState, FormEvent } from 'react';
import type { DictionaryKind, LookupResponse, LookupResultType } from '../types/api';
import { useDictionaryLookup } from '../hooks/useDictionaryLookup';

export function DictionarySearch() {
  const [kind, setKind] = useState<DictionaryKind>('skill');
  const [term, setTerm] = useState('');
  const { result, loading, error, lookup, clear, getResultBadge } = useDictionaryLookup();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (term.trim()) {
      lookup(kind, term.trim());
    }
  };

  const handleClear = () => {
    setTerm('');
    clear();
  };

  return (
    <div className="card">
      <h2 style={{ marginTop: '0', marginBottom: '1.25rem' }}>Dictionary Coverage Checker</h2>
      <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
        Look up a skill, role, or industry to see if freehire recognizes it.
        Uses the same dictionaries that power job enrichment -- no approximations.
      </p>

      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
          <div className="form-group" style={{ flex: '1', minWidth: '140px', marginBottom: '0' }}>
            <label htmlFor="kind">Type</label>
            <select
              id="kind"
              value={kind}
              onChange={(e) => setKind(e.target.value as DictionaryKind)}
            >
              <option value="skill">Skill</option>
              <option value="role">Role</option>
              <option value="industry">Industry</option>
            </select>
          </div>
          <div className="form-group" style={{ flex: '3', minWidth: '200px', marginBottom: '0' }}>
            <label htmlFor="term">Term</label>
            <input
              id="term"
              type="text"
              value={term}
              onChange={(e) => setTerm(e.target.value)}
              placeholder="e.g., k8s, frontend engineer, fintech"
              disabled={loading}
              style={{ width: '100%' }}
            />
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button type="submit" className="btn btn-primary" disabled={loading || !term.trim()}>
            {loading ? 'Checking...' : 'Check'}
          </button>
          {result && (
            <button type="button" className="btn btn-secondary" onClick={handleClear}>
              Clear
            </button>
          )}
        </div>
      </form>

      {error && (
        <div style={{ marginTop: '1rem', padding: '0.875rem', background: '#fee2e2', borderRadius: '6px', color: '#991b1b' }}>
          {error}
        </div>
      )}

      {result && (
        <DictionaryResult result={result} getResultBadge={getResultBadge} />
      )}
    </div>
  );
}

function DictionaryResult({
  result,
  getResultBadge,
}: {
  result: LookupResponse;
  getResultBadge: (type: LookupResultType) => { label: string; className: string };
}) {
  const badge = getResultBadge(result.result_type);

  return (
    <div className="result-card">
      <div className="result-header">
        <span className={`badge ${badge.className}`}>{badge.label}</span>
        <span className="result-detail">
          <strong>"{result.term}"</strong> ({result.kind})
        </span>
      </div>

      {result.result_type === 'canonical' && (
        <div className="result-detail">
          Canonical entry: <strong>{result.display_label}</strong> (slug: <code>{result.canonical_slug}</code>)
        </div>
      )}

      {result.result_type === 'alias' && (
        <div className="result-detail">
          Resolves to: <strong>{result.display_label}</strong> (slug: <code>{result.resolved_to}</code>)
        </div>
      )}

      {result.result_type === 'miss' && (
        <div>
          <div className="result-detail">
            This term is not in freehire's dictionaries.
          </div>
          <div className="miss-actions">
            <p style={{ margin: '0 0 0.75rem', color: '#6b7280', fontSize: '0.875rem' }}>
              It has been recorded for maintainer review. Thank you for helping improve coverage!
            </p>
            <span className="badge badge-miss">Added to miss list</span>
          </div>
        </div>
      )}
    </div>
  );
}