# CreatorOps — Cloud-Native Content Operations Platform
## Digital Assignment 1 / Project Review 1 Report
**Course:** BCSE408L — Cloud Computing & Full Stack Application Development  
**Institution:** School of Computer Science Engineering and Information Systems (SCOPE), VIT Chennai  
**Academic Year:** 2026–2027  
**Candidate Name:** Kathyayani T T  
**Project Title:** Project 12: CreatorOps (Marketing SaaS Application)  
**Live Public Deployment:** [https://creatorops-rho.vercel.app](https://creatorops-rho.vercel.app)  
**GitHub Repository:** [https://github.com/ttkathyayani/CreatorOps](https://github.com/ttkathyayani/CreatorOps)  

---

### Project Metadata Overview

| Parameter | Specification & Project Value |
| :--- | :--- |
| **SaaS Domain** | Marketing SaaS / Creator Operations & Competitor Intelligence Platform |
| **Target User Base** | Creative Agencies, Multi-Platform Creators, Corporate Brand Clients, Market Analysts |
| **Evaluation Stage** | Digital Assignment 1 (Review 1 Deliverable — 10 Marks) |
| **Architectural Model** | Multi-Tenant Cloud-Native SaaS with 8-State Approval Machine & Competitor Harvester |
| **Hosting & Cloud Database** | Vercel Serverless Edge Platform & Managed Cloud PostgreSQL (3NF Schema) |

---

## 1. Executive Summary & Problem Context

**CreatorOps** is an enterprise-grade, cloud-native Software-as-a-Service (SaaS) application engineered for the modern Creator Economy and Marketing Agency domain. As social media campaigns expand across platforms (Instagram, YouTube, TikTok, LinkedIn), creative teams and agencies face crippling operational chaos due to scattered feedback, lack of version control, premature client publishing, and zero structured audit trails.

> 💡 **SaaS Operational Mandate:**  
> CreatorOps replaces fragmented messaging channels with **"One campaign, One workspace, One approval trail."** It enforces a strict 8-state workflow machine, dual-tier approval gating (Agency Manager & Brand Client), automated script quality audits, centralized cloud media asset storage, and autonomous **Public Social Media Competitor Benchmarking** (YouTube, TikTok, Instagram).

---

## 2. Problem Statement & Existing System Deficiencies

In existing marketing agency workflows, content creation, collaboration, and client sign-offs rely on disconnected consumer tools such as WhatsApp groups, Slack messages, Google Drive folders, and Notion boards. Furthermore, marketing teams lack visibility into public competitor performance, producing content blindly without data on what hooks or formats drive engagement on social media platforms. This ad-hoc methodology leads to systemic operational failures:

### Operational Friction & Risk Comparison

| Friction Area | Existing Ad-Hoc Method | Failure Mode / Business Risk | CreatorOps Cloud Solution |
| :--- | :--- | :--- | :--- |
| **Feedback & Revisions** | Scattered WhatsApp, Slack, & Email threads | Conflicting feedback, missed comments, 43% rework delays | Contextual threaded comments locked to exact content versions |
| **Version Integrity** | Files named `video_final_v2_edit.mp4` on Drive | Accidental publishing of outdated revisions & overwritten edits | Automated immutable version snapshotting with visual diff viewer |
| **Approval Governance** | Verbal or informal chat *"looks good"* messages | Premature posting without client sign-off; breach of contract | Two-tier cryptographic approval gates (Internal Manager &rarr; Client) |
| **Media Asset Control** | Scattered personal cloud links with expired URLs | Missing creative assets, broken download links, asset loss | Centralized Amazon S3 cloud object storage with presigned URLs |
| **Brand Compliance** | Manual proofreading of scripts and hooks | Publishing non-compliant claims, banned terms, poor retention | Automated AI script quality, pacing, hook placement, & safety audits |
| **Market Competitor Gap** | Zero tracking of competitor post reach or viral hooks | Blind content production; lower reach; wasted ad spend | Automated Public Social Ingestion & Head-to-Head Benchmarking Matrix |

---

## 3. Proposed System Architecture & Core Innovations

The proposed CreatorOps platform introduces a multi-tenant, cloud-native architecture designed to eliminate operational friction through five foundational innovations:

- **Multi-Tenant Agency Workspaces:** Provides complete tenant data isolation, enabling agencies to manage multiple separate brand clients and creator teams within segregated security boundaries.
- **8-State Sequential Approval State Machine:** Enforces a programmatic state transition model where content deliverables cannot bypass internal agency checks or client sign-offs.
- **Automated Script & Content Quality Engine:** Real-time analysis of script text for hook effectiveness, estimated speech duration, readability score, and brand safety compliance.
- **Cloud Object Storage Abstraction:** Pluggable storage architecture supporting local development and production cloud object storage (Amazon S3 / MinIO) for high-resolution video and image assets.
- **Public Social Ingestion & Competitor Benchmarking:** Autonomous telemetry collection aggregating public video views, likes, comments, and engagement rates across YouTube, TikTok, and Instagram to calculate market-relative performance and AI content optimization tips.

---

## 4. Non-Vague Technology Stack Specifications

CreatorOps employs an explicit, modern technology stack with pinned component versions, concrete runtime specifications, and dedicated cloud tiers:

| Layer / Subsystem | Technology & Exact Version | Runtime / Protocol / Port | Architectural Role & Scope |
| :--- | :--- | :--- | :--- |
| **Frontend UI & SPA** | React 19.0.0, Vite 5.3.1, TypeScript 5.4.5 | Browser DOM / Node.js 20.14 LTS | Responsive dark-mode UI, reactive state, client routing, zero-bundle overhead |
| **CSS & Design System** | Tailwind CSS v4.0.0, Lucide React 0.395 | PostCSS 8.5 / CSS Variables | Dark slate styling (`#0f172a`, `#1e293b`, `#4f46e5`), high-contrast accessibility |
| **Backend REST Engine** | FastAPI 0.111.0, Starlette 0.37.2 | Python 3.12.2 / ASGI (Uvicorn 0.30) | Asynchronous route handling, OpenAPI 3.1 generation, dependency injection |
| **Data Serialization** | Pydantic v2.7.4, pydantic-settings 2.2.1 | Native Rust-backed core validation | Strict JSON schema enforcement, request validation, environment configuration |
| **Database ORM** | SQLAlchemy 2.0.30, Alembic 1.13.1 | Python / Connection Pooling (Pool 10) | Normalized 3NF relational mapping, declarative models, automated migrations |
| **Relational Database** | PostgreSQL 14.23 (Local port 5433 / Neon Cloud) | TCP Port 5432/5433, SSL required | ACID transactional guarantees, relational foreign keys, multi-tenant schemas |
| **Cloud Object Storage** | Amazon S3 API / MinIO (Boto3 1.34.120) | HTTPS REST / Presigned URLs | High-throughput asset storage for 4K video drafts, scripts, and brand guidelines |
| **Public Social Scraper** | YouTube Data API v3, HTTPX 0.27, BS4 4.12 | Async HTTPS REST / JSON Ingestion | Autonomous harvesting of public video views, likes, and competitor metrics |
| **Security & Auth** | Passlib 1.7.4 (PBKDF2 SHA-256 390k), Jose 3.3 | HMAC-SHA256 Signed JWT Tokens | Cryptographic password hashing, RBAC token verification, audit logging |
| **Edge Hosting & CI/CD** | Vercel Anycast Edge Platform, GitHub Actions | Global CDN / Git Hook Deployments | Zero-downtime atomic rollbacks, sub-200ms global TTFB, CI lint & test pipeline |

---

## 5. Target Stakeholders & Role-Based Access Control (RBAC)

| Stakeholder Role | Operational Scope | Primary Responsibilities | System Permissions & Access |
| :--- | :--- | :--- | :--- |
| **Content Creator** | Creative Studio & Workspace | Drafts scripts, uploads raw media, views revision requests, inspects hook recommendations. | Create & edit assigned content; upload media; view contextual comments. |
| **Agency Manager** | Campaign & Review Governance | Allocates campaign budgets, schedules timelines, reviews creator drafts, benchmarks rivals. | CRUD on campaigns; review content; approve internal drafts; competitor analytics. |
| **Brand Client** | External Review Portal | Reviews manager-approved deliverables, provides brand feedback, grants final sign-off. | View approved deliverables; post timestamped feedback; approve/reject content. |
| **Market Analyst** | Competitor Intelligence Hub | Monitors public competitor views, analyzes viral hooks, generates content gap reports. | Inspect competitor telemetry; filter platforms; trigger ingestion refresh. |
| **System Administrator** | Platform & Infrastructure | Manages agency workspaces, provisions cloud databases, monitors API uptime. | Global tenant configuration; audit log inspection; system health monitoring. |

---

## 6. Software Requirements Specifications (SRS)

### 6.1 Functional Requirements Matrix

| Req ID | Requirement Name | System Trigger & Input | Expected System Output | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | User Authentication & RBAC | User registration / Login credentials | Cryptographically hashed PBKDF2 verification; signed JWT token | Mandatory (High) |
| **FR-02** | Multi-Tenant Workspaces | Create agency workspace & slug | Isolated workspace database bounds; tenant switcher | Mandatory (High) |
| **FR-03** | Client Brand CRM | Client profile creation & guidelines | Persisted brand roster, contact emails, and visual standards | Mandatory (High) |
| **FR-04** | Campaign Operations | Create campaign, budget, & dates | Campaign timeline, channel allocation, and objective tracking | Mandatory (High) |
| **FR-05** | Content Studio & Editing | Title, social channel, & script body | Saved deliverable with word counter, hook score, & status badge | Mandatory (High) |
| **FR-06** | Immutable Version History | Creator updates script or assets | Automatic creation of sequential revision snapshot (Rev 1, Rev 2...) | Mandatory (High) |
| **FR-07** | Cloud Media Storage | Upload video/image assets (up to 100MB) | S3 cloud object storage persistence; signed CDN delivery URLs | Mandatory (High) |
| **FR-08** | Two-Tier Approval Gate | Manager / Client approve/reject action | State machine transition; audit log record; email notification | Mandatory (High) |
| **FR-09** | Automated Script Auditing | Trigger AI script review check | Readability grade, hook rating, speaking duration, safety flag | Desirable (Med) |
| **FR-10** | Operational Analytics | Aggregated campaign metrics request | Dashboard reporting on approval SLA, active campaigns, deliverables | Mandatory (High) |
| **FR-11** | Public Social Ingestion & Benchmarking | Competitor handle or URL (YT/TikTok/IG) | Public views, likes, engagement % vs benchmark, and AI hook tips | Mandatory (High) |

---

## 7. Visual Interface & Architectural Diagrams

### Figure 1: UML Use Case Diagram
![UML Use Case Diagram](docs/figures/use_case_diagram.png)

### Figure 2: Live Competitor Intelligence & Benchmarking Dashboard
![Live Competitor Analytics](docs/figures/creatorops_competitor_analytics_live.png)

### Figure 3: Executed Application Dashboard & System Telemetry
![Live Dashboard Telemetry](docs/figures/creatorops_live_dashboard.png)

### Figure 4: Approval Studio & Script Review Workspace
![Approval Studio UI](docs/figures/approval_studio_ui.jpg)

### Figure 5: 8-State Content Approval Workflow Engine
![8-State Workflow Machine](docs/figures/workflow_state_machine.png)

---

## 8. Initial SRS Summary & Semester Roadmap

| Milestone | Evaluation Date | Marks | Target Deliverables & Verified Outcomes | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Review 1 (DA1)** | 20 August 2026 | 10 Marks | Problem statement, non-vague tech stack, SRS specifications, UML use case diagram, UI wireframes, project scope. | **COMPLETED** |
| **Review 2 (DA2)** | 17 September 2026 | 10 Marks | 3-Tier System architecture, cloud edge topology, 3NF database ERD, REST API catalog, initial deployment. | **READY** |
| **Review 3 (DA3)** | 15 October 2026 | 10 Marks | Full SaaS application demonstration, competitor intelligence suite, live public URL, automated test suite, 22-section final report. | **FINAL DEMO** |
