# PROJECT REVIEW 2 REPORT

**Course Code:** BCSE408L — Cloud Computing and Full Stack Application Development  
**Project No. & Title:** Project 12 — CreatorOps  
**Project Domain:** Marketing SaaS Application  
**Student Name:** Kathyayani T T  
**GitHub Repository:** https://github.com/ttkathyayani/CreatorOps  
**Live URL:** https://creatorops-rho.vercel.app  

---

## 1. System Architecture

CreatorOps is built as a three-tier web application using Django for backend logic, Django REST Framework for REST APIs, and a relational database for persistent storage.

![Figure 1: System Architecture of CreatorOps](static/img/system_architecture.png)

### 1.1 Presentation Tier
- **Frontend Interface:** Server-rendered HTML templates built with HTML5, CSS3, and vanilla JavaScript. Provides a dashboard, content creation forms, and review interfaces.
- **API Consumers:** External clients or mobile devices communicate with the backend using standard JSON over HTTPS.

### 1.2 Application Tier
- **Django Application Server:** Handles URL routing, authentication, request validation, and business logic.
- **REST API Layer:** Django REST Framework ViewSets expose standard CRUD endpoints for clients, campaigns, and content deliverables.
- **AI Processing Modules:** Python modules in `agents/` execute script checks (reading time, word count, hook detection, forbidden brand terms) and generate content ideas.
- **Static Asset Serving:** WhiteNoise serves collected CSS, JavaScript, and image assets directly through the WSGI layer.

### 1.3 Data Tier
- **Database:** PostgreSQL for production; SQLite used during local development.
- **File Storage:** Local media handling for development, with AWS S3 support configured via `django-storages` for production media uploads.

---

## 2. Cloud Architecture

The application is deployed on Vercel's cloud platform. Incoming requests pass through Vercel's edge network and are handled by serverless Python runtimes executing the WSGI application.

![Figure 2: Cloud Deployment Model](static/img/cloud_architecture.png)

### 2.1 Deployment Pipeline
1. **Source Control:** Code is pushed to the `main` branch on GitHub (`ttkathyayani/CreatorOps`).
2. **Build Stage:** Vercel detects changes, installs dependencies from `requirements.txt`, runs `collectstatic`, and prepares the WSGI entrypoint.
3. **Execution:** Requests route to serverless Python 3.12 workers. If dynamic requests require database access, they connect via the configured `DATABASE_URL` connection pool.
4. **Static Caching:** CSS, JavaScript, and static diagrams are cached at edge locations for low-latency delivery.

---

## 3. Database Design

The relational schema is normalized to Third Normal Form (3NF) and contains 9 core tables structured around multi-tenant workspaces.

### Table 1: Database Entities and Field Specifications

| Table | Primary Key | Foreign Keys | Key Fields | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **Workspace** | `id` | None | `name`, `slug`, `description`, `created_at` | `slug` is unique |
| **Membership** | `id` | `user_id`, `workspace_id` | `role` (Admin, Manager, Creator, Client) | Unique on `(user, workspace)` |
| **Client** | `id` | `workspace_id` | `name`, `contact_email`, `brand_guidelines` | Unique on `(workspace, name)` |
| **Campaign** | `id` | `client_id` | `title`, `objective`, `budget`, `status` | `budget >= 0` |
| **ContentItem** | `id` | `campaign_id`, `creator_id` | `title`, `platform`, `script_body`, `status` | State machine enum |
| **ContentVersion**| `id` | `content_item_id`, `created_by` | `revision_number`, `script_snapshot`, `caption_snapshot` | Unique on `(content_item, revision_number)` |
| **Approval** | `id` | `content_item_id`, `reviewer_id` | `decision`, `comment`, `timestamp` | Decision choices |
| **Asset** | `id` | `content_item_id`, `uploaded_by` | `file`, `filename`, `size_bytes` | File extension filter |
| **CampaignMetric**| `id` | `campaign_id` | `metric_name`, `metric_value`, `recorded_date` | Date indexing |

---

## 4. Entity-Relationship (ER) Diagram

The relationships among workspaces, clients, campaigns, content deliverables, versions, and approvals are shown below:

![Figure 3: Entity-Relationship Diagram](static/img/erd_diagram.png)

### 4.1 Cardinalities:
- One Workspace has many Memberships ($1 : N$).
- One Workspace manages many Clients ($1 : N$).
- One Client has many Campaigns ($1 : N$).
- One Campaign contains many Content Items ($1 : N$).
- One Content Item records multiple Content Versions ($1 : N$).
- One Content Item receives multiple Approval reviews ($1 : N$).
- One Content Item holds multiple media Assets ($1 : N$).

---

## 5. Module Design

The project is structured into domain-specific Django apps:

- **`accounts`**: User registration, login, logout, and profile management.
- **`workspaces`**: Workspace creation, member role management, and tenant filtering.
- **`clients`**: Client brand profiles, contact details, and brand voice guidelines.
- **`campaigns`**: Marketing campaigns, goals, budget tracking, and timelines.
- **`content`**: Content items, social platform assignment, script drafting, and revision snapshots.
- **`approvals`**: Two-step approval queue (Manager approval $\rightarrow$ Client sign-off).
- **`assets`**: File attachment handling and media storage.
- **`analytics`**: Dashboard metric aggregation and summary reports.
- **`agents`**: Script quality evaluation, hook recommendations, and comment summarization.
- **`config`**: Project configuration, URL routing, and WSGI entry point.

---

## 6. API Design

The application provides RESTful endpoints built using Django REST Framework:

### Table 2: REST API Specifications

| Method | Endpoint | Description | Permitted Roles |
| :--- | :--- | :--- | :--- |
| `GET / POST` | `/api/clients/` | List or create clients in active workspace | Authenticated member |
| `GET / PUT / DELETE` | `/api/clients/{id}/` | Retrieve, update, or delete a client | Admin, Manager |
| `GET / POST` | `/api/campaigns/` | List or create campaigns | Authenticated member |
| `GET / PUT / DELETE` | `/api/campaigns/{id}/` | Retrieve, update, or delete a campaign | Admin, Manager |
| `GET / POST` | `/api/content/` | List or create content deliverables | Authenticated member |
| `GET / PUT / DELETE` | `/api/content/{id}/` | Retrieve, update, or delete content item | Creator, Manager |
| `POST` | `/api/content/{id}/review/` | Submit manager or client approval decision | Manager, Client |
| `GET` | `/api/reports/campaigns/{id}/` | Generate summary performance metrics | Authenticated member |
| `POST` | `/api/agents/script-review/` | Analyze script for word count, hook, and brand rules | Creator, Manager |

---

## 7. Authentication and Role-Based Access Control

User authentication and role authorization are implemented using Django's built-in authentication system with custom middleware and decorators:

1. **Password Security:** Stored as PBKDF2 hashes with SHA-256.
2. **Session Security:** Standard session cookies with CSRF token verification on all POST/PUT/DELETE operations.
3. **Multi-Tenancy:** Each request resolves the active workspace from session data. Database queries filter by `workspace_id` to prevent cross-tenant data leaks.
4. **Role Permissions:**
   - **Admin:** Manages workspace settings and team invitations.
   - **Manager:** Sets up clients, creates campaigns, and reviews drafts before client viewing.
   - **Creator:** Writes scripts, uploads media, and submits items for review.
   - **Client Reviewer:** Reviews items that have passed manager review and provides final sign-off.

---

## 8. Core Modules Implementation Summary

1. **Content Lifecycle State Machine:** Tracks items through 7 explicit states: `draft`, `pending_manager`, `pending_client`, `approved`, `changes_requested`, `scheduled`, and `published`. Items cannot jump from draft to client review without manager sign-off.
2. **Revision History:** Whenever a script is updated, a `ContentVersion` record stores an exact snapshot of the text, author, and timestamp, allowing side-by-side comparison.
3. **Automated Script Checking:** The script review module parses creator scripts, calculates estimated spoken duration (~130 words/min), detects hook keywords in the opening sentence, and checks against forbidden words defined in the client's brand guidelines.

---

## 9. GitHub Repository

- **Repository URL:** https://github.com/ttkathyayani/CreatorOps
- **Default Branch:** `main`
- **Source Files:** All Django application code, migrations, templates, static assets, and test files are committed and maintained under git version control.

---

## 10. Initial Cloud Deployment Verification

- **Hosting Platform:** Vercel Serverless Edge Platform
- **Live URL:** https://creatorops-rho.vercel.app
- **Deployment Status:** Active
- **Verification:**
  - Root redirect and user login operational.
  - Workspace dashboard and navigation verified.
  - Static assets and diagrams served with HTTP 200 responses.
  - SSL certificate active via Let's Encrypt / Vercel Edge.
