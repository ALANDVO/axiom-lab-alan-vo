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
        "ai/ml": "artificial-intelligence",
        "genai": "generative-ai",
        "llm": "large-language-models",
        "rag": "retrieval-augmented-generation",
        "mcp": "model-context-protocol",
        "agentic": "ai-agents",
        "rdbms": "relational-databases",
        "nosql": "nosql-databases",
        "k8s operator": "kubernetes-operator",
        "cncf": "cloud-native-computing-foundation",
        "istio": "istio",
        "linkerd": "linkerd",
        "argocd": "argocd",
        "flux": "fluxcd",
        "helm": "helm",
        "helm charts": "helm",
        "terraform": "terraform",
        "tf": "terraform",
        "iac": "infrastructure-as-code",
        "cloudformation": "cloudformation",
        "pulumi": "pulumi",
        "ansible": "ansible",
        "chef": "chef",
        "puppet": "puppet",
        "saltstack": "saltstack",
        "vault": "hashicorp-vault",
        "consul": "consul",
        "nomad": "nomad",
        "packer": "packer",
        "vagrant": "vagrant",
        "docker compose": "docker-compose",
        "docker-compose": "docker-compose",
        "compose": "docker-compose",
        "swarm": "docker-swarm",
        "ecs": "aws-ecs",
        "eks": "aws-eks",
        "gke": "google-gke",
        "aks": "azure-aks",
        "openshift": "openshift",
        "rancher": "rancher",
        "knative": "knative",
        "serverless": "serverless",
        "faas": "function-as-a-service",
        "lambda": "aws-lambda",
        "cloud functions": "google-cloud-functions",
        "cloud run": "google-cloud-run",
        "fargate": "aws-fargate",
        # Roles
        "se": "software-engineer",
        "senior swe": "senior-software-engineer",
        "staff swe": "staff-software-engineer",
        "principal swe": "principal-software-engineer",
        "tech lead": "technical-lead",
        "tech lead manager": "tech-lead-manager",
        "engineering lead": "engineering-lead",
        "engineering director": "engineering-director",
        "vp engineering": "vp-engineering",
        "head of engineering": "head-of-engineering",
        "backend dev": "backend-engineer",
        "frontend dev": "frontend-engineer",
        "fullstack dev": "fullstack-engineer",
        "devops eng": "devops-engineer",
        "sre eng": "site-reliability-engineer",
        "platform eng": "platform-engineer",
        "platform engineer": "platform-engineer",
        "ml eng": "machine-learning-engineer",
        "mle": "machine-learning-engineer",
        "data eng": "data-engineer",
        "data engineer": "data-engineer",
        "analytics eng": "analytics-engineer",
        "ds": "data-scientist",
        "applied scientist": "applied-scientist",
        "research scientist": "research-scientist",
        "quant": "quantitative-researcher",
        "quant researcher": "quantitative-researcher",
        "security eng": "security-engineer",
        "appsec": "application-security-engineer",
        "netsec": "network-security-engineer",
        "cloud sec": "cloud-security-engineer",
        "secops": "security-operations-engineer",
        "devsecops": "devsecops-engineer",
        "qa": "quality-assurance-engineer",
        "qe": "quality-engineer",
        "sdet": "software-development-engineer-in-test",
        "test eng": "test-engineer",
        "release eng": "release-engineer",
        "build eng": "build-engineer",
        "mobile eng": "mobile-engineer",
        "ios eng": "ios-engineer",
        "android eng": "android-engineer",
        "flutter dev": "flutter-engineer",
        "react native dev": "react-native-engineer",
        "web eng": "web-engineer",
        "ui eng": "ui-engineer",
        "ux eng": "ux-engineer",
        "design eng": "design-engineer",
        "product eng": "product-engineer",
        "sales eng": "sales-engineer",
        "solutions arch": "solutions-architect",
        "solutions architect": "solutions-architect",
        "cloud arch": "cloud-architect",
        "system arch": "system-architect",
        "enterprise arch": "enterprise-architect",
        "data arch": "data-architect",
        "security arch": "security-architect",
        # Industries
        "genai": "generative-ai",
        "llmops": "llm-operations",
        "mlops": "ml-operations",
        "dataops": "data-operations",
        "devsecops": "devsecops",
        "gitops": "gitops",
        "aiops": "ai-operations",
        "cloud native": "cloud-native",
        "k8s native": "kubernetes-native",
        "edge computing": "edge-computing",
        "iot": "internet-of-things",
        "iiot": "industrial-iot",
        "industrial iot": "industrial-iot",
        "robotics": "robotics",
        "autonomous vehicles": "autonomous-vehicles",
        "av": "autonomous-vehicles",
        "space tech": "space-technology",
        "new space": "space-technology",
        "climate tech": "climate-technology",
        "cleantech": "clean-technology",
        "greentech": "green-technology",
        "agritech": "agricultural-technology",
        "foodtech": "food-technology",
        "proptech": "property-technology",
        "legaltech": "legal-technology",
        "regtech": "regulatory-technology",
        "insurtech": "insurance-technology",
        "wealthtech": "wealth-technology",
        "payments": "payments-technology",
        "defi": "decentralized-finance",
        "web3": "web3",
        "nft": "non-fungible-tokens",
        "dao": "decentralized-autonomous-organizations",
        "gamefi": "game-finance",
        "metaverse": "metaverse",
        "xr": "extended-reality",
        "ar/vr": "augmented-virtual-reality",
        "spatial computing": "spatial-computing",
        "quantum": "quantum-computing",
        "quantum computing": "quantum-computing",
        "hpc": "high-performance-computing",
        "supercomputing": "high-performance-computing",
        "bioinformatics": "bioinformatics",
        "computational biology": "computational-biology",
        "drug discovery": "drug-discovery",
        "genomics": "genomics",
        "proteomics": "proteomics",
        "digital health": "digital-health",
        "telemedicine": "telemedicine",
        "medtech": "medical-technology",
        "diagnostics": "diagnostics",
        "personalized medicine": "personalized-medicine",
        "precision medicine": "precision-medicine",
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
        # New Skills
        ("skill", "generative-ai", "Generative AI", "genai"),
        ("skill", "large-language-models", "Large Language Models", "llm"),
        ("skill", "retrieval-augmented-generation", "Retrieval Augmented Generation", "rag"),
        ("skill", "model-context-protocol", "Model Context Protocol", "mcp"),
        ("skill", "ai-agents", "AI Agents", "agentic"),
        ("skill", "relational-databases", "Relational Databases", "rdbms"),
        ("skill", "nosql-databases", "NoSQL Databases", "nosql"),
        ("skill", "kubernetes-operator", "Kubernetes Operator", "k8s operator"),
        ("skill", "cloud-native-computing-foundation", "Cloud Native Computing Foundation", "cncf"),
        ("skill", "istio", "Istio", ""),
        ("skill", "linkerd", "Linkerd", ""),
        ("skill", "argocd", "ArgoCD", ""),
        ("skill", "fluxcd", "FluxCD", "flux"),
        ("skill", "helm", "Helm", "helm charts"),
        ("skill", "terraform", "Terraform", "tf"),
        ("skill", "infrastructure-as-code", "Infrastructure as Code", "iac"),
        ("skill", "cloudformation", "CloudFormation", ""),
        ("skill", "pulumi", "Pulumi", ""),
        ("skill", "ansible", "Ansible", ""),
        ("skill", "chef", "Chef", ""),
        ("skill", "puppet", "Puppet", ""),
        ("skill", "saltstack", "SaltStack", ""),
        ("skill", "hashicorp-vault", "HashiCorp Vault", "vault"),
        ("skill", "consul", "Consul", ""),
        ("skill", "nomad", "Nomad", ""),
        ("skill", "packer", "Packer", ""),
        ("skill", "vagrant", "Vagrant", ""),
        ("skill", "docker-compose", "Docker Compose", "docker compose,docker-compose,compose"),
        ("skill", "docker-swarm", "Docker Swarm", "swarm"),
        ("skill", "aws-ecs", "AWS ECS", "ecs"),
        ("skill", "aws-eks", "AWS EKS", "eks"),
        ("skill", "google-gke", "Google GKE", "gke"),
        ("skill", "azure-aks", "Azure AKS", "aks"),
        ("skill", "openshift", "OpenShift", ""),
        ("skill", "rancher", "Rancher", ""),
        ("skill", "knative", "Knative", ""),
        ("skill", "serverless", "Serverless", ""),
        ("skill", "function-as-a-service", "Function as a Service", "faas"),
        ("skill", "aws-lambda", "AWS Lambda", "lambda"),
        ("skill", "google-cloud-functions", "Google Cloud Functions", "cloud functions"),
        ("skill", "google-cloud-run", "Google Cloud Run", "cloud run"),
        ("skill", "aws-fargate", "AWS Fargate", "fargate"),
        # New Roles
        ("role", "senior-software-engineer", "Senior Software Engineer", "senior swe"),
        ("role", "staff-software-engineer", "Staff Software Engineer", "staff swe"),
        ("role", "principal-software-engineer", "Principal Software Engineer", "principal swe"),
        ("role", "technical-lead", "Technical Lead", "tech lead"),
        ("role", "tech-lead-manager", "Tech Lead Manager", "tech lead manager"),
        ("role", "engineering-lead", "Engineering Lead", "engineering lead"),
        ("role", "engineering-director", "Engineering Director", "engineering director"),
        ("role", "vp-engineering", "VP Engineering", "vp engineering"),
        ("role", "head-of-engineering", "Head of Engineering", "head of engineering"),
        ("role", "backend-engineer", "Backend Engineer", "backend dev"),
        ("role", "frontend-engineer", "Frontend Engineer", "frontend dev"),
        ("role", "fullstack-engineer", "Fullstack Engineer", "fullstack dev"),
        ("role", "devops-engineer", "DevOps Engineer", "devops eng"),
        ("role", "site-reliability-engineer", "Site Reliability Engineer", "sre eng"),
        ("role", "platform-engineer", "Platform Engineer", "platform eng,platform engineer"),
        ("role", "machine-learning-engineer", "Machine Learning Engineer", "ml eng,mle"),
        ("role", "data-engineer", "Data Engineer", "data eng,data engineer"),
        ("role", "analytics-engineer", "Analytics Engineer", "analytics eng"),
        ("role", "data-scientist", "Data Scientist", "ds"),
        ("role", "applied-scientist", "Applied Scientist", "applied scientist"),
        ("role", "research-scientist", "Research Scientist", "research scientist"),
        ("role", "quantitative-researcher", "Quantitative Researcher", "quant,quant researcher"),
        ("role", "security-engineer", "Security Engineer", "security eng"),
        ("role", "application-security-engineer", "Application Security Engineer", "appsec"),
        ("role", "network-security-engineer", "Network Security Engineer", "netsec"),
        ("role", "cloud-security-engineer", "Cloud Security Engineer", "cloud sec"),
        ("role", "security-operations-engineer", "Security Operations Engineer", "secops"),
        ("role", "devsecops-engineer", "DevSecOps Engineer", "devsecops"),
        ("role", "quality-assurance-engineer", "Quality Assurance Engineer", "qa"),
        ("role", "quality-engineer", "Quality Engineer", "qe"),
        ("role", "software-development-engineer-in-test", "Software Development Engineer in Test", "sdet"),
        ("role", "test-engineer", "Test Engineer", "test eng"),
        ("role", "release-engineer", "Release Engineer", "release eng"),
        ("role", "build-engineer", "Build Engineer", "build eng"),
        ("role", "mobile-engineer", "Mobile Engineer", "mobile eng"),
        ("role", "ios-engineer", "iOS Engineer", "ios eng"),
        ("role", "android-engineer", "Android Engineer", "android eng"),
        ("role", "flutter-engineer", "Flutter Engineer", "flutter dev"),
        ("role", "react-native-engineer", "React Native Engineer", "react native dev"),
        ("role", "web-engineer", "Web Engineer", "web eng"),
        ("role", "ui-engineer", "UI Engineer", "ui eng"),
        ("role", "ux-engineer", "UX Engineer", "ux eng"),
        ("role", "design-engineer", "Design Engineer", "design eng"),
        ("role", "product-engineer", "Product Engineer", "product eng"),
        ("role", "sales-engineer", "Sales Engineer", "sales eng"),
        ("role", "solutions-architect", "Solutions Architect", "solutions arch,solutions architect"),
        ("role", "cloud-architect", "Cloud Architect", "cloud arch"),
        ("role", "system-architect", "System Architect", "system arch"),
        ("role", "enterprise-architect", "Enterprise Architect", "enterprise arch"),
        ("role", "data-architect", "Data Architect", "data arch"),
        ("role", "security-architect", "Security Architect", "security arch"),
        # New Industries
        ("industry", "generative-ai", "Generative AI", "genai"),
        ("industry", "llm-operations", "LLM Operations", "llmops"),
        ("industry", "ml-operations", "ML Operations", "mlops"),
        ("industry", "data-operations", "Data Operations", "dataops"),
        ("industry", "devsecops", "DevSecOps", "devsecops"),
        ("industry", "gitops", "GitOps", "gitops"),
        ("industry", "ai-operations", "AI Operations", "aiops"),
        ("industry", "cloud-native", "Cloud Native", "cloud native"),
        ("industry", "kubernetes-native", "Kubernetes Native", "k8s native"),
        ("industry", "edge-computing", "Edge Computing", "edge computing"),
        ("industry", "internet-of-things", "Internet of Things", "iot,iiot,industrial iot"),
        ("industry", "robotics", "Robotics", ""),
        ("industry", "autonomous-vehicles", "Autonomous Vehicles", "av,autonomous vehicles"),
        ("industry", "space-technology", "Space Technology", "space tech,new space"),
        ("industry", "climate-technology", "Climate Technology", "climate tech"),
        ("industry", "clean-technology", "Clean Technology", "cleantech"),
        ("industry", "green-technology", "Green Technology", "greentech"),
        ("industry", "agricultural-technology", "Agricultural Technology", "agritech"),
        ("industry", "food-technology", "Food Technology", "foodtech"),
        ("industry", "property-technology", "Property Technology", "proptech"),
        ("industry", "legal-technology", "Legal Technology", "legaltech"),
        ("industry", "regulatory-technology", "Regulatory Technology", "regtech"),
        ("industry", "insurance-technology", "Insurance Technology", "insurtech"),
        ("industry", "wealth-technology", "Wealth Technology", "wealthtech"),
        ("industry", "payments-technology", "Payments Technology", "payments"),
        ("industry", "decentralized-finance", "Decentralized Finance", "defi"),
        ("industry", "web3", "Web3", "web3"),
        ("industry", "non-fungible-tokens", "Non-Fungible Tokens", "nft"),
        ("industry", "decentralized-autonomous-organizations", "Decentralized Autonomous Organizations", "dao"),
        ("industry", "game-finance", "Game Finance", "gamefi"),
        ("industry", "metaverse", "Metaverse", ""),
        ("industry", "extended-reality", "Extended Reality", "xr"),
        ("industry", "augmented-virtual-reality", "Augmented Virtual Reality", "ar/vr"),
        ("industry", "spatial-computing", "Spatial Computing", "spatial computing"),
        ("industry", "quantum-computing", "Quantum Computing", "quantum,quantum computing"),
        ("industry", "high-performance-computing", "High Performance Computing", "hpc,supercomputing"),
        ("industry", "bioinformatics", "Bioinformatics", ""),
        ("industry", "computational-biology", "Computational Biology", "computational biology"),
        ("industry", "drug-discovery", "Drug Discovery", "drug discovery"),
        ("industry", "genomics", "Genomics", ""),
        ("industry", "proteomics", "Proteomics", ""),
        ("industry", "digital-health", "Digital Health", "digital health"),
        ("industry", "telemedicine", "Telemedicine", ""),
        ("industry", "medical-technology", "Medical Technology", "medtech"),
        ("industry", "diagnostics", "Diagnostics", ""),
        ("industry", "personalized-medicine", "Personalized Medicine", "personalized medicine"),
        ("industry", "precision-medicine", "Precision Medicine", "precision medicine"),
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