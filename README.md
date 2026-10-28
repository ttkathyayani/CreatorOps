# CreatorOps — Content Planning, Collaboration, Approval & Competitor Intelligence SaaS

> **One campaign. One workspace. One approval trail. Unfair competitive advantage.**

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live%20Production-black?style=flat&logo=vercel)](https://creatorops-rho.vercel.app)
[![Django](https://img.shields.io/badge/Django-6.1.2-092E20?style=flat&logo=django)](https://docs.djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql)](https://www.postgresql.org)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v3.4-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)

CreatorOps is an enterprise-grade cloud SaaS platform engineered for marketing agencies, content creators, and brand managers. It delivers multi-tenant campaign management, a deterministic 7-stage content approval workflow engine, **Direct Social Media Publishing (Meta Graph, YouTube, and TikTok APIs)**, autonomous AI agent assistants with human-readable operational briefings, and **public social competitor performance benchmarking** (YouTube, TikTok, Instagram).

- **Live Public SaaS URL:** [https://creatorops-rho.vercel.app](https://creatorops-rho.vercel.app)
- **GitHub Repository:** [https://github.com/ttkathyayani/CreatorOps](https://github.com/ttkathyayani/CreatorOps)
- **Review 1 Deliverable Report:** [https://creatorops-rho.vercel.app/reports/review1/](https://creatorops-rho.vercel.app/reports/review1/)
- **Review 2 Deliverable Report:** [https://creatorops-rho.vercel.app/reports/review2/](https://creatorops-rho.vercel.app/reports/review2/)
- **Review 3 Final Report:** [https://creatorops-rho.vercel.app/reports/review3/](https://creatorops-rho.vercel.app/reports/review3/)

---

## 🚀 Key Features

### 1. Direct Social Media Publishing (Meta Graph, YouTube, & TikTok)
- **Multi-Platform API Integration:** Native service integration (`content.publishing_service.SocialPublishingService`) enabling direct one-click publication of approved content:
  - **Meta Graph API v19.0:** Generates Instagram Reels / Posts containers, verifies media processing status, and executes direct publishing with live permalinks.
  - **YouTube Data API v3:** Ingests video snippets, titles, tags, and category IDs to upload YouTube Shorts and videos directly to client channels.
  - **TikTok Content Posting API v2:** Initializes video posts and queries asynchronous publishing status.
- **Permanent Audit Trail:** Automatically logs every publication event to `SocialPublishLog` in the database, tracking remote post IDs, response payloads, publish timestamps, and the approving user.
- **In-Studio Publishing Modal:** Interactive dialog on content items with live platform selector, payload inspector, and remote post status badges.

### 2. Competitor Intelligence & Public Social Benchmarking
- **Automated Public Telemetry Aggregation:** Continuously indexes public video performance data (total views, likes, comments, shares, estimated reach, and engagement rates) from YouTube Shorts, TikTok, and Instagram Reels.
- **Executive Comparative KPI Cards:**
  - **Agency Total Views:** 2.45M (`+44.9%` market outperformance vs competitor average 1.69M).
  - **Average Engagement Rate:** 5.8% (`+48.7%` market outperformance vs competitor average 3.9%).
  - **Hook Retention Rate:** 60.0% (`-7.7%` market gap vs competitor average 65.0%).
  - **Weekly Publishing Cadence:** 4.2 posts/week (`-35.4%` market gap vs competitor average 6.5 posts/week).
- **Head-to-Head Performance Matrix:** Real-time filterable comparison across channels (Nexus Media, ViralReach Lab, Quantum Creators, Apex Studios, Momentum Content) highlighting content strategy gaps and rival hook techniques.
- **Actionable AI Content Recommendations:** Pinpoints visual hook adjustments, optimal video duration windows (28–42s), and optimal publishing hours to seize competitor audience share.
- **Interactive Tracking Modal:** Add any public YouTube, TikTok, or Instagram handle to track competitors in real-time.

### 3. Human-Readable AI Agent Studio
- Converted all previous raw JSON agent responses into rich, interactive, human-readable operational cards:
  - **Content Ideas Agent:** Generates formatted cards with punchy titles, psychological hooks, target formats, and estimated reach indicators.
  - **Script Review Agent:** Renders a visual Hook Score badge (e.g. `91/100`), Pacing Analysis, Detailed Diagnostic Findings, and Optimization Recommendations.
  - **Approval Summary Agent:** Produces a prioritized executive checklist categorizing pending assets, blocked bottlenecks, and immediate client actions.
  - **Campaign Analytics Agent:** Delivers clean executive metric briefings with KPIs, key drivers, and tactical next steps.
  - **Raw JSON Debugger:** Collapsible `{ } View Raw JSON Debug` panel retained for developer troubleshooting.

### 3. Multi-Tenant Workspace & Client Isolation
- Strict organizational data partitioning by agency workspace with role-based access control (Admin, Manager, Creator, Analyst, and Client Reviewer).
- Dedicated client portals enabling external client reviewers to leave feedback without accessing internal agency pipelines.

### 4. Deterministic 8-State Content Approval Workflow Engine
- State machine preventing unapproved releases:
  `DRAFT` → `INTERNAL_REVIEW` → `CHANGES_REQUESTED` → `CLIENT_REVIEW` → `CLIENT_CHANGES_REQUESTED` → `APPROVED` → `SCHEDULED` → `PUBLISHED`.
- Immutable audit log tracking actor, timestamp, previous state, new state, and review comments.

### 5. Cloud Media Asset Management
- High-throughput video and creative asset uploads backed by cloud object storage (Amazon S3 / MinIO) with presigned URLs and metadata extraction.

---

## 🛠️ Technology Stack Specifications

| Layer / Subsystem | Technology & Exact Version | Architectural Scope |
| :--- | :--- | :--- |
| **Backend & Web Framework** | Python 3.13 / Django 6.1.2 | MVC architecture, ORM models, auth middleware, REST views |
| **Database Persistence** | SQLite 3 / PostgreSQL 15+ (Neon Cloud) | 3NF relational schema, foreign key constraints, transactional ACID |
| **Static Assets & CDN** | WhiteNoise 6.12.0 / Vercel Edge CDN | Zero-latency gzip/brotli static asset caching at edge locations |
| **Cloud Object Storage** | Boto3 1.43 / Amazon S3 / MinIO | Scalable bucket storage for 4K video drafts, thumbnails, and PDFs |
| **Styling & UI Theme** | Tailwind CSS / Custom Dark Theme | High-contrast dark palette (`#0B0F19`, `#111827`, `#4F46E5`) |
| **AI Agent Logic** | Rule-Based Expert System & Generative Logic | Content ideation, script diagnostics, approval briefings, analytics |
| **Cloud Deployment** | Vercel Serverless Anycast Edge | Automated CI/CD from GitHub, zero-downtime atomic rollbacks |

---

## 📁 Repository Structure

```text
CreatorOps/
├── accounts/           # User authentication, RBAC profiles, role switcher
├── agents/             # Autonomous AI Agents (Content, Script, Approval, Campaign)
├── analytics/          # Performance metrics, Competitor Intelligence engine
│   ├── competitor_service.py  # Public social telemetry collection & benchmarks
│   ├── views.py               # Competitor matrix views & REST API endpoints
│   └── urls.py                # Analytics URL routing
├── approvals/          # 8-State workflow state machine & audit log
├── assets/             # Cloud media asset library & S3 integration
├── campaigns/          # Multi-client marketing campaign management
├── clients/            # Client directory & client portal views
├── config/             # Django settings, WSGI entrypoint, root URL routing
├── content/            # Content calendar, Kanban board, script editor
├── docs/               # Academic review reports and architecture figures
│   ├── Review 1_final.pdf     # Digital Assignment 1 Official Deliverable
│   ├── Review 2_final.pdf     # Digital Assignment 2 Official Deliverable
│   ├── review 3_final.pdf     # Digital Assignment 3 Official Deliverable
│   └── figures/               # System diagrams and verified UI screenshots
├── static/             # CSS stylesheets, JavaScript modules, diagrams
├── templates/          # Responsive HTML5 Django templates
│   ├── agents/         # Human-readable AI Agent Studio interface
│   ├── analytics/      # Competitor Intelligence dashboard & modals
│   ├── dashboard/      # Executive analytics & competitor pulse banner
│   └── ...
├── workspaces/         # Multi-tenant workspace management
├── db.sqlite3          # Pre-seeded demonstration relational database
├── manage.py           # Django administrative CLI
├── requirements.txt    # Production Python dependencies
├── REVIEW_1_REPORT.html # Interactive Review 1 Academic Engineering Report
├── REVIEW_1_REPORT.md  # Review 1 Academic Report in GitHub Markdown
└── Review 1_final.pdf  # Review 1 Official PDF Report (in root for grading)
```

---

## 🏃 Local Development Quickstart

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/ttkathyayani/CreatorOps.git
cd CreatorOps

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Migration & Server Execution
```bash
# Verify system integrity
python manage.py check

# Run local development server
python manage.py runserver 8000
```
- Access web application: `http://127.0.0.1:8000`
- Access Competitor Benchmarking: `http://127.0.0.1:8000/analytics/competitors/`
- Access AI Agent Studio: `http://127.0.0.1:8000/analytics/agents/`
- Access Review 1 Report: `http://127.0.0.1:8000/reports/review1/`

### Demo Login Credentials
- **Admin / Agency Owner:** `admin` / `admin123`
- **Content Creator:** `creator` / `creator123`
- **Client Reviewer:** `client` / `client123`

---

## 🎓 Academic Review Deliverables

| Deliverable | Topic & Scope | Access Formats |
| :--- | :--- | :--- |
| **Review 1** | Problem Statement, Existing System Critique, Proposed System, Functional & Non-Functional Requirements, Scope, UML Use Case, UI Mockups, Initial SRS | [Interactive Web Report](https://creatorops-rho.vercel.app/reports/review1/) • [Word Document](Review_1_Report.docx) • [Markdown](REVIEW_1_REPORT.md) |
| **Review 2** | System Architecture, Cloud Architecture, Database Design (3NF), ER Diagram, Module Design, REST API Design, Authentication, Core Modules, GitHub Repo, Cloud Deployment | [Interactive Web Report](https://creatorops-rho.vercel.app/reports/review2/) • [Word Document](Review_2_Report.docx) • [Markdown](REVIEW_2_REPORT.md) |
| **Review 3 Final** | Full Project Engineering Report, Direct Social Publishing (Meta Graph, YouTube, TikTok), 10 Automated Tests (100% Pass), Vercel Serverless Deployment | [Interactive Web Report](https://creatorops-rho.vercel.app/reports/review3/) • [Word Document](Review_3_Final_Report.docx) • [Markdown](REVIEW_3_FINAL_REPORT.md) |


---

## 📄 License
Academic project developed for **BCSE408L — Cloud Computing and Full Stack Application Development**, School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Chennai.
