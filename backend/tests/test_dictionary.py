import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.dictionary import DictionaryEntry, DictionaryKind, DictionaryMiss, LookupResultType
from app.services.dictionary import (
    lookup_term, record_miss, get_misses, seed_dictionary, normalize_term, LookupResult
)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestNormalizeTerm:
    def test_normalize_basic(self):
        assert normalize_term("Kubernetes") == "kubernetes"
        assert normalize_term("  React  ") == "react"
        assert normalize_term("Machine Learning") == "machine learning"

    def test_normalize_collapse_whitespace(self):
        assert normalize_term("full  stack") == "full stack"
        assert normalize_term("devops\nengineer") == "devops engineer"


class TestSeedDictionary:
    def test_seed_populates_entries(self, db_session):
        seed_dictionary(db_session)
        count = db_session.query(DictionaryEntry).count()
        assert count > 20

        # Check specific entries
        k8s = db_session.query(DictionaryEntry).filter(
            DictionaryEntry.kind == "skill",
            DictionaryEntry.canonical_slug == "kubernetes"
        ).first()
        assert k8s is not None
        assert k8s.display_label == "Kubernetes"
        assert "k8s" in k8s.aliases

    def test_seed_idempotent(self, db_session):
        seed_dictionary(db_session)
        count1 = db_session.query(DictionaryEntry).count()
        seed_dictionary(db_session)
        count2 = db_session.query(DictionaryEntry).count()
        assert count1 == count2


class TestLookupTerm:
    def test_canonical_hit_skill(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.SKILL, "kubernetes")
        assert result.result_type == LookupResultType.CANONICAL
        assert result.canonical_slug == "kubernetes"
        assert result.display_label == "Kubernetes"

    def test_canonical_hit_role(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.ROLE, "software-engineer")
        assert result.result_type == LookupResultType.CANONICAL
        assert result.canonical_slug == "software-engineer"
        assert result.display_label == "Software Engineer"

    def test_canonical_hit_industry(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.INDUSTRY, "financial-technology")
        assert result.result_type == LookupResultType.CANONICAL
        assert result.canonical_slug == "financial-technology"
        assert result.display_label == "Financial Technology"

    def test_alias_hit_from_db_aliases(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.SKILL, "k8s")
        assert result.result_type == LookupResultType.ALIAS
        assert result.canonical_slug == "kubernetes"
        assert result.display_label == "Kubernetes"
        assert result.resolved_to == "kubernetes"

    def test_alias_hit_from_static_map(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.SKILL, "golang")
        assert result.result_type == LookupResultType.ALIAS
        assert result.canonical_slug == "go"
        assert result.display_label == "Go"
        assert result.resolved_to == "go"

    def test_alias_hit_role(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.ROLE, "swe")
        assert result.result_type == LookupResultType.ALIAS
        assert result.canonical_slug == "software-engineer"
        assert result.resolved_to == "software-engineer"

    def test_alias_hit_industry(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.INDUSTRY, "fintech")
        assert result.result_type == LookupResultType.ALIAS
        assert result.canonical_slug == "financial-technology"
        assert result.resolved_to == "financial-technology"

    def test_miss_creates_record(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.SKILL, "quantum-computing")
        assert result.result_type == LookupResultType.MISS

        miss = db_session.query(DictionaryMiss).filter(
            DictionaryMiss.kind == "skill",
            DictionaryMiss.normalized_term == "quantum-computing"
        ).first()
        assert miss is not None
        assert miss.request_count == 1
        assert miss.status == "pending"

    def test_miss_deduplicates(self, db_session):
        seed_dictionary(db_session)
        lookup_term(db_session, DictionaryKind.SKILL, "quantum-computing")
        lookup_term(db_session, DictionaryKind.SKILL, "Quantum-Computing")
        lookup_term(db_session, DictionaryKind.SKILL, "  quantum-computing  ")

        miss = db_session.query(DictionaryMiss).filter(
            DictionaryMiss.kind == "skill",
            DictionaryMiss.normalized_term == "quantum-computing"
        ).first()
        assert miss is not None
        assert miss.request_count == 3
        assert miss.raw_term == "quantum-computing"  # first submission preserved

    def test_miss_case_insensitive(self, db_session):
        seed_dictionary(db_session)
        lookup_term(db_session, DictionaryKind.SKILL, "RUST")
        lookup_term(db_session, DictionaryKind.SKILL, "rust")

        miss = db_session.query(DictionaryMiss).filter(
            DictionaryMiss.kind == "skill",
            DictionaryMiss.normalized_term == "rust"
        ).first()
        assert miss.request_count == 2

    def test_miss_submitted_by(self, db_session):
        seed_dictionary(db_session)
        result = lookup_term(db_session, DictionaryKind.SKILL, "rust", submitted_by="user123")

        miss = db_session.query(DictionaryMiss).filter(
            DictionaryMiss.normalized_term == "rust"
        ).first()
        assert miss.submitted_by == "user123"


class TestGetMisses:
    def test_get_misses_empty(self, db_session):
        seed_dictionary(db_session)
        misses = get_misses(db_session)
        assert misses == []

    def test_get_misses_filter_by_kind(self, db_session):
        seed_dictionary(db_session)
        lookup_term(db_session, DictionaryKind.SKILL, "rust")
        lookup_term(db_session, DictionaryKind.ROLE, "quantum-engineer")

        skill_misses = get_misses(db_session, kind=DictionaryKind.SKILL)
        role_misses = get_misses(db_session, kind=DictionaryKind.ROLE)

        assert len(skill_misses) == 1
        assert skill_misses[0].normalized_term == "rust"
        assert len(role_misses) == 1
        assert role_misses[0].normalized_term == "quantum-engineer"

    def test_get_misses_pagination(self, db_session):
        seed_dictionary(db_session)
        for i in range(15):
            lookup_term(db_session, DictionaryKind.SKILL, f"skill-{i}")

        page1 = get_misses(db_session, kind=DictionaryKind.SKILL, limit=10, offset=0)
        page2 = get_misses(db_session, kind=DictionaryKind.SKILL, limit=10, offset=10)

        assert len(page1) == 10
        assert len(page2) == 5

    def test_get_misses_order_by_request_count(self, db_session):
        seed_dictionary(db_session)
        lookup_term(db_session, DictionaryKind.SKILL, "low-count")
        for _ in range(5):
            lookup_term(db_session, DictionaryKind.SKILL, "high-count")

        misses = get_misses(db_session, kind=DictionaryKind.SKILL)
        assert misses[0].normalized_term == "high-count"
        assert misses[0].request_count == 5
        assert misses[1].normalized_term == "low-count"
        assert misses[1].request_count == 1


class TestLookupResultDataclass:
    def test_canonical_result_fields(self):
        result = LookupResult(
            result_type=LookupResultType.CANONICAL,
            kind=DictionaryKind.SKILL,
            term="kubernetes",
            canonical_slug="kubernetes",
            display_label="Kubernetes",
        )
        assert result.result_type == LookupResultType.CANONICAL
        assert result.resolved_to is None

    def test_alias_result_fields(self):
        result = LookupResult(
            result_type=LookupResultType.ALIAS,
            kind=DictionaryKind.SKILL,
            term="k8s",
            canonical_slug="kubernetes",
            display_label="Kubernetes",
            resolved_to="kubernetes",
        )
        assert result.result_type == LookupResultType.ALIAS
        assert result.resolved_to == "kubernetes"

    def test_miss_result_fields(self):
        result = LookupResult(
            result_type=LookupResultType.MISS,
            kind=DictionaryKind.SKILL,
            term="quantum",
        )
        assert result.result_type == LookupResultType.MISS
        assert result.canonical_slug is None
        assert result.resolved_to is None