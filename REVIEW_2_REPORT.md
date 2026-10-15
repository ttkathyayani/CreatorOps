# CreatorOps — Review 2 Deliverables Report
**Course:** Cloud Computing & Full Stack Application Development (BCSE408L)  
**Project No. & Title:** Project 12 — CreatorOps  
**Domain:** Marketing SaaS / Multi-Tenant Cloud Application  
**Student Name:** Kathyayani T T  
**GitHub Account:** [ttkathyayani](https://github.com/ttkathyayani)  
**GitHub Repository:** [https://github.com/ttkathyayani/CreatorOps](https://github.com/ttkathyayani/CreatorOps)  
**Live Production URL:** [https://creatorops-rho.vercel.app](https://creatorops-rho.vercel.app)  

---

## Executive Summary
**Review 2** of the course **BCSE408L**. It details the **System Architecture**, **Cloud Deployment Architecture**, **Database Schema & ER Diagram**, **Modular Software Design**, **REST API Specifications**, **Authentication & Multi-Tenant Role-Based Access Control (RBAC)**, and **Initial Cloud Deployment Verification**.

---

## 1. System Architecture

CreatorOps adopts a **Three-Tier Cloud-Native Architecture** built upon the **Model-View-Template (MVT)** and **RESTful API** paradigms:

![System Architecture](static/img/system_architecture.png)

### Tier 1: Client Layer (Presentation Tier)
- **Web & Mobile Browsers:** Responsive Single-Page UI and Server-Rendered Views styled via an intentional Black-and-Yellow Design System (`#111111`, `#1C1C1C`, `#FACC15`).
- **REST API Clients:** Third-party webhooks, mobile apps, and automated testing suites communicating via standard JSON over HTTPS.

### Tier 2: Application Layer (Logic Tier)
- **Django 6.1 WSGI Application:** Implements core business rules, multi-tenant workspace isolation, and state machine transitions.
- **Django REST Framework (DRF 3.18):** Provides standardized serialization, token/session authentication, and nested ModelViewSets.
- **AI Agent Engine (`agents/`):** Autonomous heuristic and NLP intelligence engine executing script auditing, creative brainstorming, feedback clustering, and performance reporting.
- **WhiteNoise Static File Engine:** Integrated WSGI middleware providing gzip/Brotli compression, unique hash fingerprints, and CDN-compatible caching.

### Tier 3: Data & Storage Layer (Persistence Tier)
- **Relational Database:** Dual-mode support for Cloud PostgreSQL (Neon/Supabase) in production and SQLite in isolated development environments.
- **Cloud Object Storage:** Amazon S3 integration via `boto3` for high-throughput video and image asset storage.

---

## 2. Cloud Architecture

CreatorOps is deployed on the **Vercel Global Serverless Edge Platform**, delivering serverless elasticity, zero-downtime deployments, and global low-latency access:

![Cloud Architecture](static/img/cloud_architecture.png)

### Key Architectural Flow:
1. **Edge Ingestion:** User requests hit Vercel's Anycast Edge Network with automated TLS/SSL termination and Cloudflare DDoS protection.
2. **Serverless WSGI Execution:** Dynamic requests route to Python 3.12 Serverless Functions running `config/wsgi.py`. Cold starts are minimized using lightweight packaging (~15MB max lambda footprint).
3. **Static Asset Offloading:** Static assets (`/static/*`) are served directly via Vercel's global CDN cache and WhiteNoise.
4. **Cloud Database Connection:** The serverless runtime connects to a managed PostgreSQL database via pooled connection strings (`DATABASE_URL`), with read/write `/tmp` database replication for serverless isolation.
5. **Asset Storage Pipeline:** Media deliverables (MP4 videos, PNG graphics) stream to an AWS S3 bucket with signed URL retrieval.

---

## 3. Database Design

The relational schema comprises **9 normalized entities (3NF)** structured around multi-tenant boundaries:

| Entity Name | Primary Key | Foreign Keys | Key Attributes |
| :--- | :--- | :--- | :--- |
| **Workspace** | `id` (BigInt) | None | `name`, `slug` (unique), `description`, `created_at` |
| **Membership** | `id` (BigInt) | `user_id`, `workspace_id` | `role` (ADMIN, MANAGER, CREATOR, CLIENT_REVIEWER) |
| **Client** | `id` (BigInt) | `workspace_id` | `name`, `contact_email`, `industry`, `brand_guidelines` |
| **Campaign** | `id` (BigInt) | `client_id` | `title`, `objective`, `target_audience`, `budget`, `status` |
| **ContentItem** | `id` (BigInt) | `campaign_id`, `creator_id` | `title`, `platform`, `script_body`, `caption`, `status`, `due_date` |
| **ContentVersion**| `id` (BigInt) | `content_item_id`, `created_by` | `revision_number`, `script_snapshot`, `caption_snapshot` |
| **Approval** | `id` (BigInt) | `content_item_id`, `reviewer_id`| `decision`, `comment`, `timestamp` |
| **Asset** | `id` (BigInt) | `content_item_id`, `uploaded_by`| `file`, `filename`, `s3_object_key`, `size_bytes` |
| **CampaignMetric**| `id` (BigInt) | `campaign_id` | `metric_name`, `metric_value`, `recorded_date` |

### Key Integrity Constraints:
- `Membership.unique_together = ("user", "workspace")`: Prevents duplicate roles in a single organization.
- `Client.unique_together = ("workspace", "name")`: Prevents client name collisions within a tenant.
- `ContentVersion.unique_together = ("content_item", "revision_number")`: Guarantees sequential, tamper-proof version numbering.

---

## 4. Entity-Relationship (ER) Diagram

![ER Diagram](static/img/erd_diagram.png)

### Cardinality Summary:
- **Workspace to Membership:** $1 : N$ (One workspace has many members).
- **Workspace to Client:** $1 : N$ (One workspace owns multiple brand clients).
- **Client to Campaign:** $1 : N$ (One client runs multiple marketing campaigns).
- **Campaign to ContentItem:** $1 : N$ (One campaign groups multiple deliverables).
- **ContentItem to ContentVersion:** $1 : N$ (One deliverable maintains an audit trail of revisions).
- **ContentItem to Approval:** $1 : N$ (One deliverable records manager and client review decisions).
- **ContentItem to Asset:** $1 : N$ (One deliverable links multiple video/image assets).
- **Campaign to CampaignMetric:** $1 : N$ (One campaign tracks time-series performance metrics).

---

## 5. Module Design

The codebase adheres to **Domain-Driven Design (DDD)** organized into 9 modular packages:

```
CreatorOps/
├── accounts/      --> Authentication lifecycle, registration, user profiles
├── workspaces/    --> Tenant organization, membership RBAC, context processors
├── clients/       --> Brand CRM, client profiles, brand voice rules
├── campaigns/     --> Marketing initiatives, budget tracking, milestone goals
├── content/       --> Content matrix, 7-stage state machine, versioning studio
├── approvals/     --> Two-tier approval queue (Manager & Client gates)
├── assets/        --> Cloud file storage abstraction, S3 streaming, size formatting
├── analytics/     --> Executive dashboard, KPI aggregation, report views
├── agents/        --> Autonomous AI Agent Engine (4 specialized agents)
└── config/        --> Settings, WSGI serverless bridge, root URL routing
```

---

## 6. API Design (Django REST Framework)

All REST endpoints require authentication and return standard JSON schemas:

| Method | Endpoint | Description | Permission Required |
| :--- | :--- | :--- | :--- |
| `GET / POST` | `/api/clients/` | List all workspace clients / Create new client | Authenticated Member |
| `GET / PUT / DEL` | `/api/clients/{id}/` | Retrieve, update, or remove client profile | Admin / Manager |
| `GET / POST` | `/api/campaigns/` | List campaigns / Create new campaign | Authenticated Member |
| `GET / PUT / DEL` | `/api/campaigns/{id}/` | Retrieve, update, or delete campaign | Admin / Manager |
| `GET / POST` | `/api/content/` | List content items / Create new deliverable | Authenticated Member |
| `GET / PUT / DEL` | `/api/content/{id}/` | Retrieve, update, or delete content item | Creator / Manager |
| `POST` | `/api/content/{id}/review/` | Submit manager/client approval decision | Manager / Client |
| `GET` | `/api/reports/campaigns/{id}/` | Generate AI executive campaign report | Authenticated Member |
| `POST` | `/api/agents/script-review/` | Real-time script quality & brand audit | Creator / Manager |
| `POST` | `/api/agents/{agent_type}/` | Trigger dynamic AI agent execution | Authenticated Member |

### Sample JSON Request & Response (`/api/agents/script-review/`):
```json
// POST /api/agents/script-review/
{
  "script": "Stop scrolling! Here is the secret to glowing skin in 3 steps. Subscribe for more!",
  "brand_rules": "Avoid cheap, fake. Required hashtag: #GlowSkin",
  "platform": "Instagram"
}

// HTTP 200 OK Response
{
  "agent": "Script Review Agent",
  "passed": true,
  "score": 95,
  "word_count": 16,
  "estimated_duration_sec": 7,
  "findings": ["All script checks passed successfully!"],
  "suggestions": ["The script structure and pacing look optimal for production."]
}
```

---

## 7. Authentication & Role-Based Access Control (RBAC)

### Security Flow:
1. **Password Hashing:** Django PBKDF2 with SHA-256 (390,000 iterations).
2. **Session Integrity:** Secure HTTP-only session cookies with CSRF token validation on all state-mutating requests.
3. **Workspace Injection:** Custom `@workspace_required` decorator extracts and verifies active tenant ID from session, binding `request.workspace` and `request.membership`.
4. **Role Enforcement:** Custom `@role_required([roles])` decorator and DRF `IsWorkspaceAdminOrManager` permission classes restrict access:

```
[Incoming Request]
       │
       ▼
[Is Authenticated?] ── No ──> Redirect to Login
       │ Yes
       ▼
[Active Workspace in Session?] ── No ──> Auto-assign first membership
       │ Yes
       ▼
[User Role in Allowed Roles?] ── No ──> HTTP 403 Forbidden
       │ Yes
       ▼
[Execute View Logic]
```

---

## 8. Core Modules Implementation Summary

1. **Multi-Tenant Engine (`workspaces`):** Complete data isolation per workspace with auto-slug generation.
2. **Content Production Engine (`content`):** 7-stage state machine (`draft` $\rightarrow$ `pending_manager` $\rightarrow$ `pending_client` $\rightarrow$ `approved` $\rightarrow$ `scheduled` $\rightarrow$ `published`) with immutable `ContentVersion` snapshots.
3. **Two-Tier Approval Queue (`approvals`):** Gated sign-offs ensuring deliverables cannot reach clients without manager approval.
4. **AI Agent Suite (`agents`):** 4 autonomous heuristic agents executing quality checks, creative brainstorming, feedback clustering, and performance reporting.
5. **Asset Storage (`assets`):** Dual-mode file upload supporting local media and AWS S3 streaming.

---

## 9. GitHub Repository & Engineering Practices

- **Repository Link:** [https://github.com/ttkathyayani/CreatorOps](https://github.com/ttkathyayani/CreatorOps)
- **Primary Branch:** `main`
- **Version Control Metrics:**
  - Initial platform release: Commit `8979b69` (123 files).
  - Vercel zero-config cloud deployment: Commit `da51772`.
  - Comprehensive review & viva documentation: Commit `8cefdae`.
  - Commit history demonstrates continuous integration and modular feature deployment.

---

## 10. Initial Cloud Deployment Verification

- **Cloud Platform:** Vercel Global Edge Network
- **Deployment URL:** [https://creatorops-rho.vercel.app](https://creatorops-rho.vercel.app)
- **Deployment Status:** **Ready (Active Production)**
- **Verification Proof:**
  - HTTP 200 responses verified on root domain, `/dashboard/`, `/clients/`, `/campaigns/`, `/content/`, and `/guide/`.
  - SSL/TLS Certificate issued and validated via Let's Encrypt / Vercel Edge.
  - WhiteNoise serving compressed static assets at edge with HTTP 304 caching.
