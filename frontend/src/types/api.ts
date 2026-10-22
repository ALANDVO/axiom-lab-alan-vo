export type DictionaryKind = 'skill' | 'role' | 'industry';

export type LookupResultType = 'canonical' | 'alias' | 'miss';

export interface LookupRequest {
  kind: DictionaryKind;
  term: string;
  submitted_by?: string;
}

export interface LookupResponse {
  result_type: LookupResultType;
  kind: DictionaryKind;
  term: string;
  canonical_slug?: string;
  display_label?: string;
  resolved_to?: string;
}

export interface MissResponse {
  id: number;
  kind: string;
  raw_term: string;
  normalized_term: string;
  request_count: number;
  first_requested_at: string;
  last_requested_at: string;
  submitted_by?: string;
  status: string;
  resolution_note?: string;
}