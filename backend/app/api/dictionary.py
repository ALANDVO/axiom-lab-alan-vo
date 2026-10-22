from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dictionary import DictionaryKind, DictionaryMiss, LookupResultType
from app.services.dictionary import (
    lookup_term, get_misses, seed_dictionary, LookupResult
)


router = APIRouter(prefix="/api/dictionary", tags=["dictionary"])


class LookupRequest(BaseModel):
    kind: DictionaryKind
    term: str = Field(..., min_length=1, max_length=200)
    submitted_by: Optional[str] = None


class LookupResponse(BaseModel):
    result_type: LookupResultType
    kind: DictionaryKind
    term: str
    canonical_slug: Optional[str] = None
    display_label: Optional[str] = None
    resolved_to: Optional[str] = None


class MissResponse(BaseModel):
    id: int
    kind: str
    raw_term: str
    normalized_term: str
    request_count: int
    first_requested_at: datetime
    last_requested_at: datetime
    submitted_by: Optional[str] = None
    status: str
    resolution_note: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/lookup", response_model=LookupResponse)
def lookup_dictionary(request: LookupRequest, db: Session = Depends(get_db)):
    """Look up a term in the dictionary. Returns canonical hit, alias hit, or miss."""
    result = lookup_term(db, request.kind, request.term)
    return LookupResponse(
        result_type=result.result_type,
        kind=result.kind,
        term=result.term,
        canonical_slug=result.canonical_slug,
        display_label=result.display_label,
        resolved_to=result.resolved_to,
    )


@router.get("/misses", response_model=list[MissResponse])
def list_misses(
    kind: Optional[DictionaryKind] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """List recorded dictionary misses for admin review."""
    misses = get_misses(db, kind, status, limit, offset)
    return misses


@router.post("/seed")
def seed_dictionary_endpoint(db: Session = Depends(get_db)):
    """Seed initial dictionary entries (idempotent)."""
    seed_dictionary(db)
    return {"status": "seeded"}