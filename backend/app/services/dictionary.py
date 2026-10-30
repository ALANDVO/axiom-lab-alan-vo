import re
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.dictionary import (
    DictionaryEntry, DictionaryMiss, DictionaryKind, LookupResultType
)


@dataclass
class LookupResult:
    result_type: LookupResultType
    kind: DictionaryKind
    term: str
    canonical_slug: Optional[str] = None
    display_label: Optional[str] = None
    resolved_to: Optional[str] = None  # for alias hits: the canonical it resolves to


def normalize_term(term: str) -> str:
    """Normalize term for dictionary lookup: lowercase, trim, collapse whitespace."""
    return re.sub(r"\s+", " ", term.strip().lower())


def get_alias_map(kind: DictionaryKind) -> dict[str, str]:
    """Returns a mapping of alias -> canonical_slug for the given kind."""
    return {
        # Skills
        "k8s": "kubernetes",
        "kubernetes": "kubernetes",
        "kube": "kubernetes",
        "reactjs": "react",
        "react.js": "react",
        "vuejs": "vue",
        "vue.js": "vue",
        "golang": "go",
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "ml": "machine-learning",
        "ai": "artificial-intelligence",
        "cv": "computer-vision",
        "nlp": "natural-language-processing",
        # Roles
        "swe": "software-engineer",
        "software engineer": "software-engineer",
        "backend engineer": "backend-engineer",
        "frontend engineer": "frontend-engineer",
        "fullstack": "fullstack-engineer",
        "full stack": "fullstack-engineer",
        "devops": "devops-engineer",
        "sre": "site-reliability-engineer",
        "ml engineer": "machine-learning-engineer",
        "data scientist": "data-scientist",
        "product manager": "product-manager",
        "pm": "product-manager",
        # Industries
        "fintech": "financial-technology",
        "healthtech": "health-technology",
        "edtech": "education-technology",
        "saas": "software-as-a-service",
        "ecommerce": "e-commerce",
        "crypto": "cryptocurrency",
        "web3": "blockchain",
    }


def seed_dictionary(db: Session) -> None:
    """Seed initial dictionary entries if empty."""
    if db.query(DictionaryEntry).first():
        return

    entries = [
        # Skills
        ("skill", "kubernetes", "Kubernetes", "k8s,kube"),
        ("skill", "react", "React", "reactjs,react.js"),
        ("skill", "vue", "Vue.js", "vuejs,vue.js"),
        ("skill", "go", "Go", "golang"),
        ("skill", "python", "Python", "py"),
        ("skill", "javascript", "JavaScript", "js"),
        ("skill", "typescript", "TypeScript", "ts"),
        ("skill", "machine-learning", "Machine Learning", "ml"),
        ("skill", "artificial-intelligence", "Artificial Intelligence", "ai"),
        ("skill", "computer-vision", "Computer Vision", "cv"),
        ("skill", "natural-language-processing", "Natural Language Processing", "nlp"),
        ("skill", "docker", "Docker", ""),
        ("skill", "aws", "Amazon Web Services", ""),
        ("skill", "gcp", "Google Cloud Platform", ""),
        ("skill", "azure", "Microsoft Azure", ""),
        ("skill", "postgresql", "PostgreSQL", "postgres"),
        ("skill", "redis", "Redis", ""),
        ("skill", "graphql", "GraphQL", ""),
        ("skill", "rest", "REST APIs", ""),
        # Roles
        ("role", "software-engineer", "Software Engineer", "swe,software engineer"),
        ("role", "backend-engineer", "Backend Engineer", "backend engineer"),
        ("role", "frontend-engineer", "Frontend Engineer", "frontend engineer"),
        ("role", "fullstack-engineer", "Fullstack Engineer", "fullstack,full stack"),
        ("role", "devops-engineer", "DevOps Engineer", "devops"),
        ("role", "site-reliability-engineer", "Site Reliability Engineer", "sre"),
        ("role", "machine-learning-engineer", "Machine Learning Engineer", "ml engineer"),
        ("role", "data-scientist", "Data Scientist", "data scientist"),
        ("role", "product-manager", "Product Manager", "product manager,pm"),
        ("role", "engineering-manager", "Engineering Manager", "eng manager,em"),
        ("role", "cto", "Chief Technology Officer", ""),
        # Industries
        ("industry", "financial-technology", "Financial Technology", "fintech"),
        ("industry", "health-technology", "Health Technology", "healthtech"),
        ("industry", "education-technology", "Education Technology", "edtech"),
        ("industry", "software-as-a-service", "Software as a Service", "saas"),
        ("industry", "e-commerce", "E-Commerce", "ecommerce"),
        ("industry", "cryptocurrency", "Cryptocurrency", "crypto"),
        ("industry", "blockchain", "Blockchain", "web3"),
        ("industry", "artificial-intelligence", "Artificial Intelligence", "ai"),
        ("industry", "cybersecurity", "Cybersecurity", "security"),
        ("industry", "biotechnology", "Biotechnology", "biotech"),
    ]

    for kind, slug, label, aliases in entries:
        entry = DictionaryEntry(
            kind=kind,
            canonical_slug=slug,
            display_label=label,
            aliases=aliases if aliases else None,
        )
        db.add(entry)
    db.commit()


def lookup_term(db: Session, kind: DictionaryKind, term: str, submitted_by: Optional[str] = None) -> LookupResult:
    """
    Look up a term in the dictionary.
    Returns canonical hit, alias hit, or miss.
    """
    normalized = normalize_term(term)
    alias_map = get_alias_map(kind)

    # Check canonical entries first
    entry = db.query(DictionaryEntry).filter(
        DictionaryEntry.kind == kind.value,
        DictionaryEntry.canonical_slug == normalized
    ).first()

    if entry:
        return LookupResult(
            result_type=LookupResultType.CANONICAL,
            kind=kind,
            term=term,
            canonical_slug=entry.canonical_slug,
            display_label=entry.display_label,
        )

    # Check aliases in database entries
    entries = db.query(DictionaryEntry).filter(
        DictionaryEntry.kind == kind.value
    ).all()

    for entry in entries:
        if entry.aliases:
            for alias in entry.aliases.split(","):
                if normalize_term(alias) == normalized:
                    return LookupResult(
                        result_type=LookupResultType.ALIAS,
                        kind=kind,
                        term=term,
                        canonical_slug=entry.canonical_slug,
                        display_label=entry.display_label,
                        resolved_to=entry.canonical_slug,
                    )

    # Check static alias map
    if normalized in alias_map:
        canonical = alias_map[normalized]
        entry = db.query(DictionaryEntry).filter(
            DictionaryEntry.kind == kind.value,
            DictionaryEntry.canonical_slug == canonical
        ).first()
        if entry:
            return LookupResult(
                result_type=LookupResultType.ALIAS,
                kind=kind,
                term=term,
                canonical_slug=entry.canonical_slug,
                display_label=entry.display_label,
                resolved_to=entry.canonical_slug,
            )

    # Miss - record it
    return record_miss(db, kind, term, normalized, submitted_by)


def record_miss(db: Session, kind: DictionaryKind, raw_term: str, normalized: str, submitted_by: Optional[str] = None) -> LookupResult:
    """Record a miss in the dictionary_misses table, deduplicating by (kind, normalized_term)."""
    existing = db.query(DictionaryMiss).filter(
        DictionaryMiss.kind == kind.value,
        DictionaryMiss.normalized_term == normalized
    ).first()

    if existing:
        existing.request_count += 1
        existing.last_requested_at = datetime.now(timezone.utc)
        if submitted_by and not existing.submitted_by:
            existing.submitted_by = submitted_by
        db.commit()
        return LookupResult(
            result_type=LookupResultType.MISS,
            kind=kind,
            term=raw_term,
        )

    miss = DictionaryMiss(
        kind=kind.value,
        raw_term=raw_term,
        normalized_term=normalized,
        submitted_by=submitted_by,
    )
    db.add(miss)
    db.commit()
    return LookupResult(
        result_type=LookupResultType.MISS,
        kind=kind,
        term=raw_term,
    )


def get_misses(db: Session, kind: Optional[DictionaryKind] = None, status: Optional[str] = None, limit: int = 100, offset: int = 0) -> list[DictionaryMiss]:
    """Get recorded misses with optional filtering."""
    query = db.query(DictionaryMiss)
    if kind:
        query = query.filter(DictionaryMiss.kind == kind.value)
    if status:
        query = query.filter(DictionaryMiss.status == status)
    return query.order_by(DictionaryMiss.request_count.desc()).offset(offset).limit(limit).all()