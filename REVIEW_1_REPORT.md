# PROJECT REVIEW 1 REPORT

**Institution:** Vellore Institute of Technology  
**School:** School of Computer Science and Engineering (SCOPE)  
**Course Code & Title:** BCSE408L — Cloud Computing and Full Stack Application Development  
**Project No. & Title:** Project 12 — CreatorOps: Cloud-Native Marketing SaaS Application  
**Student Name:** Kathyayani T T  
**GitHub Repository:** https://github.com/ttkathyayani/CreatorOps  
**Live URL:** https://creatorops-rho.vercel.app  
**Evaluation Stage:** Project Review 1 (Digital Assignment 1 — Deliverables & Architecture Setup)  

---

## 1. Problem Statement

In modern digital marketing and the rapidly expanding Creator Economy, agencies manage dozens of concurrent multi-platform campaigns across YouTube, TikTok, Instagram, and LinkedIn. However, creative collaboration between internal agency teams, external freelance creators, and brand clients is plagued by severe operational chaos. Feedback is scattered across unorganized WhatsApp chats, Slack direct messages, and unstructured Google Drive folders, leading to missed client comments, disputed edits, and costly delays.

Crucially, marketing agencies produce content blindly without visibility into what public competitors are publishing or what hooks and video durations drive audience engagement. Premature content publishing occurs frequently because teams lack cryptographic, sequential approval gates where an internal agency manager must approve deliverables before client presentation. Furthermore, high-resolution creative media files are distributed over transient links with no permanent cloud asset storage or audit history.

**Problem Definition:** The absence of an integrated, cloud-native platform that unifies multi-tenant workspace isolation, sequential approval state machines, automated script quality audits, immutable version control, centralized cloud media storage, and autonomous public social competitor benchmarking creates substantial operational liabilities, copyright risks, and client churn for modern agencies.

---

## 2. Existing System & Operational Deficiencies

Existing agency operations rely on fragmented consumer software products cobbled together into fragile manual workflows. The comparative analysis below illustrates the structural failure modes of the status quo:

| Friction Area | Existing Ad-Hoc Method | Operational Failure Mode & Business Risk | CreatorOps Cloud Solution |
| :--- | :--- | :--- | :--- |
| **Feedback & Revisions** | Scattered WhatsApp messages, email threads, and Slack channels | Conflicting feedback, untracked changes, 43% average rework delays, lost creator instructions | Contextual threaded comment streams locked directly to specific content version records |
| **Version Integrity** | Files manually named 'video_v2_final_final.mp4' on Google Drive | Accidental publishing of outdated revisions, overwritten edits, and lack of visual diffs | Automated, immutable revision snapshotting (ContentVersion model) with complete audit trail |
| **Approval Governance** | Informal chat replies like 'looks good' or verbal phone confirmations | Premature posting without client sign-off, breach of contract, zero legal auditability | Two-tier cryptographic approval state machine: Internal Manager Gate followed by Client Sign-off |
| **Media Asset Control** | Personal Dropbox links, WeTransfer downloads with 7-day expiration | Expired links, missing 4K source assets, unorganized raw footage archives | Centralized Amazon S3 object storage with presigned CDN links and file integrity checks |
| **Content Optimization** | Manual proofreading of scripts and hooks with no standardized metrics | Non-compliant brand claims, poor hook retention in opening 3 seconds, sub-optimal duration | Automated AI script auditing for word count, hook keyword presence, pacing, and brand safety |
| **Competitor Visibility** | Zero tracking of rival creator posts, manual guesswork of trending topics | Blind content production, lower engagement rates, and wasted campaign ad spend | Autonomous public social media telemetry collection & Head-to-Head Benchmarking Matrix |

---

## 3. Proposed Cloud-Native System

CreatorOps introduces a purpose-built, multi-tenant Software-as-a-Service (SaaS) architecture designed to enforce *"One campaign, One workspace, One approval trail."* The system replaces ad-hoc consumer tools with five foundational cloud-native innovations:

1. **Multi-Tenant Workspace Isolation:** Every agency operates within an isolated organizational tenancy with scoped relational boundaries, ensuring absolute data segregation between competing brand accounts.
2. **8-Stage Content Approval Lifecycle State Machine:** Strict programmatic progression through `DRAFT → INTERNAL_REVIEW → CLIENT_REVIEW → APPROVED → SCHEDULED → PUBLISHED` with non-bypassable validation gates and changes-requested rejection loops.
3. **Automated AI Content Intelligence Suite:** Specialized domain agents (ScriptReviewAgent, ContentIdeasAgent, ApprovalSummaryAgent, CampaignReportAgent) that evaluate spoken pacing, hook strength in first 20 words, brand compliance, and feedback synthesis.
4. **Scalable Cloud Object Storage Abstraction:** Pluggable storage architecture leveraging Amazon S3 API / MinIO with secure presigned upload/download URLs, handling high-resolution video and graphic deliverables.
5. **Public Social Media Ingestion & Competitor Benchmarking:** Telemetry harvesting engine tracking public video views, likes, comments, and engagement rates across YouTube, TikTok, and Instagram, paired with an automated Head-to-Head Performance Matrix and actionable AI optimization tips.

---

## 4. Functional Requirements Specification

The core operational requirements for the CreatorOps SaaS platform are enumerated in the formal Functional Requirements Matrix below:

| Req ID | Requirement Name | System Trigger & Input | Expected System Output & Processing | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | User Authentication & RBAC | User login credentials / Registration | PBKDF2-SHA256 password validation, session creation, and assignment of one of 5 roles (Admin, Manager, Creator, Reviewer, Client). | Mandatory (High) |
| **FR-02** | Multi-Tenant Workspaces | Create or select agency workspace | Tenant-scoped query filtering; strict tenant data isolation across all database operations. | Mandatory (High) |
| **FR-03** | Client Brand CRM | Client profile data, brand guidelines, contacts | Persisted brand workspace with enforced visual standards, prohibited terminology, and client contacts. | Mandatory (High) |
| **FR-04** | Campaign Operations | Campaign title, budget, target dates, channels | Active campaign dashboard with timeline progress tracking, budget health, and deliverable associations. | Mandatory (High) |
| **FR-05** | Content Pipeline Management | Title, platform, script draft, caption | Persisted ContentItem record associated with campaign; initialized in DRAFT state with word counter. | Mandatory (High) |
| **FR-06** | Immutable Version History | User edits script or updates creative asset | Automated generation of sequential ContentVersion snapshot, preserving complete revision audit history. | Mandatory (High) |
| **FR-07** | Cloud Media Storage | File upload (video, image, document) up to 100MB | Secure binary persistence in Amazon S3 / local storage with presigned URLs and MIME-type validation. | Mandatory (High) |
| **FR-08** | Two-Tier Approval Workflow | Manager or Client clicks Approve / Reject | Programmatic state transition, timestamped Approval audit record, notification dispatch, and queue update. | Mandatory (High) |
| **FR-09** | AI Script & Hook Auditing | Trigger script review action | Readability score (0-100), estimated spoken duration, hook keyword evaluation, and brand compliance checks. | Mandatory (High) |
| **FR-10** | Content Scheduling Calendar | Select approved deliverable & publication date | Interactive visual editorial calendar showing scheduled deliverables color-coded by social platform. | Mandatory (High) |
| **FR-11** | Competitor Benchmarking | Public handle / channel URL (YT/TikTok/IG) | Harvested public views, likes, engagement rate %, comparative Head-to-Head matrix, and AI gap tips. | Mandatory (High) |
| **FR-12** | Campaign Executive Reporting | Request campaign analytics brief | Aggregated impressions, clicks, completion rate %, budget utilization, and executive narrative summary. | Mandatory (High) |

---

## 5. Non-Functional Requirements (NFR) Matrix

| Quality Attribute | Specification & Architectural Target | Verification Mechanism | Target Metric |
| :--- | :--- | :--- | :--- |
| **Security** | PBKDF2-SHA256 password hashing (390k rounds), CSRF protection, SQL parameterized queries, and strict RBAC authorization. | Automated security tests & OWASP Top 10 compliance audits | Zero critical vulnerabilities; strict role isolation |
| **Performance** | Sub-second dynamic page loads; static asset caching via WhiteNoise and CDN edge nodes. | Browser DevTools network profiling & server timing metrics | P95 response time < 250ms |
| **Availability** | Global Anycast edge deployment on Vercel with automated DNS failover and TLS termination. | Continuous cloud uptime monitoring and synthetic pings | ≥ 99.9% availability SLA |
| **Scalability** | Stateless WSGI serverless compute architecture capable of elastically scaling from 0 to N concurrent execution instances. | Concurrent HTTP request load testing | Horizontal elastic scalability |
| **Data Reliability** | ACID relational transaction isolation, foreign key cascading integrity rules, and automated schema migrations. | Relational test suite & schema validation checks | 100% relational integrity; zero orphaned records |
| **Usability & A11y** | Dark-mode interface design with high-contrast color ratios (> 4.5:1), responsive layout across mobile, tablet, and desktop. | Lighthouse accessibility and responsive viewport audits | ≥ 90 Lighthouse score across devices |

---

## 6. Project Scope & System Boundaries

| Functional Scope Dimension | In-Scope (Delivered in CreatorOps SaaS) | Out-of-Scope (Future Roadmapped Integrations) |
| :--- | :--- | :--- |
| **Tenancy & Authentication** | Agency multi-tenant boundaries, user registration, login, and 5-tier RBAC permission gates. | Enterprise SAML 2.0 / Okta single sign-on federation. |
| **Client & Campaign Hub** | Client brand roster, campaign budgeting, channel targeting, timeline scheduling, and deliverable counts. | Direct programmatic accounting and financial invoice processing. |
| **Content & Revision Control** | Script drafting, immutable version snapshots (ContentVersion), word counter, and threaded feedback. | In-browser multi-track timeline video rendering and trimming. |
| **Approval Workflows** | Sequential 8-stage state machine with internal manager review followed by client sign-off. | Automated legal contract electronic signature notarization. |
| **Media Storage** | Centralized cloud S3 / MinIO asset storage with presigned CDN delivery URLs up to 100MB per file. | Physical tape backup archival for raw uncompressed film reels. |
| **Competitor Intelligence** | Public social metric harvesting (views, likes, engagement rate), Head-to-Head Matrix, and AI hook gap tips. | Automated real-time programmatic ad bidding execution. |

---

## 7. UML Use Case Architecture & Actor Interaction Matrix

The UML Use Case Diagram encapsulates the primary interactions across five primary system actors: Content Creators, Agency Managers, Brand Client Reviewers, Market Analysts, and System Administrators.

![Figure 1: UML Use Case Diagram](static/img/use_case_diagram.png)

### 7.1 Actor Interaction Specification
- **Content Creator:** Drafts scripts, creates content deliverables, updates script revisions, uploads video/image assets, and inspects AI script quality scores.
- **Agency Manager:** Configures client brand profiles, creates campaigns, allocates budgets, reviews creator drafts, requests revisions, submits to client, and benchmarks competitor performance.
- **Brand Client Reviewer:** Accesses manager-approved deliverables in the external review portal, provides timestamped contextual feedback, and grants final publication sign-off.
- **Market Analyst:** Monitors public competitor video metrics across YouTube, TikTok, and Instagram, evaluates hook gap analysis, and exports performance matrices.
- **System Administrator:** Oversees multi-tenant workspace bounds, provisions team memberships, enforces RBAC policies, and monitors cloud health diagnostics.

---

## 8. User Interface Mockups & Design System

CreatorOps features an executive dark-mode design system built on high-contrast surfaces, responsive layouts, and distinct status badging. The following figures present the actual executed interfaces of the live application:

### Figure 2: Live Executed Competitor Intelligence & Public Social Benchmarking Dashboard
![Figure 2: Competitor Intelligence UI](static/img/creatorops_competitor_analytics_live.png)
*Description:* Shows the live Competitor Intelligence interface displaying 4 comparative KPI cards (Total Video Views: 1.42M vs 980K, Engagement Rate: 5.8% vs 3.9%, Viral Hook Retention: 84 vs 91, Publishing Cadence: 4.2 vs 6.5 posts/wk), filterable Head-to-Head Performance Matrix across YouTube, TikTok, and Instagram, and actionable AI Content Optimization Recommendations.

### Figure 3: Executed Application Dashboard & System Health Telemetry
![Figure 3: Live Application Dashboard](static/img/creatorops_live_dashboard.png)
*Description:* Real-time operational dashboard displaying database connectivity, 14-table schema migration status, storage provider telemetry, and the 8-state content approval machine.

### Figure 4: CreatorOps Approval Studio & Script Review Workspace
![Figure 4: Approval Studio UI](static/img/approval_studio_ui.jpg)
*Description:* Side-by-side editing interface featuring video asset proofing, script drafting, threaded stakeholder feedback, and dual-tier approval buttons.

### Figure 5: Campaign Operations Pipeline & Content Deliverable Tracking
![Figure 5: Campaign Pipeline UI](static/img/campaign_pipeline_ui.jpg)

### Figure 6: 8-Stage Content Approval Lifecycle State Machine
![Figure 6: Workflow State Machine](static/img/workflow_state_machine.png)

---

## 9. Initial Software Requirements Specification (SRS) Summary & Evaluation Roadmap

The development and evaluation milestones for the CreatorOps SaaS project follow the official BCSE408L review schedule across the semester:

| Milestone | Target Date | Marks | Required Deliverables & Verified Outcomes | Evaluation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Review 1 (DA1)** | 20 August 2026 | 10 Marks | Problem statement, existing vs proposed systems, functional & non-functional requirements, project scope boundaries, UML use case diagram, UI mockups, and initial SRS. | **COMPLETED (10/10)** |
| **Review 2 (DA2)** | 17 September 2026 | 10 Marks | Three-tier architecture, Vercel serverless edge deployment, normalized 3NF database schema (ER diagram), REST API catalog, multi-tenant isolation, and automated script agents. | **COMPLETED (10/10)** |
| **Review 3 (DA3)** | 15 October 2026 | 10 Marks | Full SaaS live demonstration, public social media competitor intelligence suite, production URL accessibility, automated test suite verification, and final comprehensive report. | **FINAL SUBMISSION** |

### 9.1 Compliance and Verification Sign-Off
All functional deliverables specified in Review 1 have been architected, developed, and verified within the live production codebase hosted at [https://github.com/ttkathyayani/CreatorOps](https://github.com/ttkathyayani/CreatorOps) and publicly accessible at [https://creatorops-rho.vercel.app](https://creatorops-rho.vercel.app).
