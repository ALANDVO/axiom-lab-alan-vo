from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String, DateTime, Integer, Index, UniqueConstraint, ForeignKey
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class DictionaryKind(str, PyEnum):
    SKILL = "skill"
    ROLE = "role"
    INDUSTRY = "industry"


class LookupResultType(str, PyEnum):
    CANONICAL = "canonical"
    ALIAS = "alias"
    MISS = "miss"


class DictionaryEntry(Base):
    __tablename__ = "dictionary_entries"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String(20), nullable=False, index=True)
    canonical_slug = Column(String(100), nullable=False, index=True)
    display_label = Column(String(200), nullable=False)
    aliases = Column(String(1000), nullable=True)  # comma-separated aliases
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("kind", "canonical_slug", name="uq_kind_canonical"),
        Index("ix_kind_slug", "kind", "canonical_slug"),
    )


class DictionaryMiss(Base):
    __tablename__ = "dictionary_misses"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String(20), nullable=False, index=True)
    raw_term = Column(String(200), nullable=False)
    normalized_term = Column(String(200), nullable=False, index=True)
    request_count = Column(Integer, default=1, nullable=False)
    first_requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_requested_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    submitted_by = Column(String(100), nullable=True)
    status = Column(String(20), default="pending", nullable=False)  # pending, accepted, rejected
    resolution_note = Column(String(500), nullable=True)

    __table_args__ = (
        UniqueConstraint("kind", "normalized_term", name="uq_kind_normalized_miss"),
        Index("ix_kind_status", "kind", "status"),
    )