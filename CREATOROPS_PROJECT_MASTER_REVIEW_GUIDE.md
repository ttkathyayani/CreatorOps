# CreatorOps — Project Master Review & Viva Guide
**Scalable Multi-Tenant Creator Campaign Management & Content Production Cloud SaaS**

---

## 📌 Document Metadata
- **Project Name:** CreatorOps
- **Academic Context:** B.Tech / BE Computer Science & Engineering Capstone / Project Review
- **Course Reference:** Cloud Computing & Full-Stack Application Development (BCSE408L)
- **Live Cloud URL:** [https://creatorops-rho.vercel.app](https://creatorops-rho.vercel.app)
- **GitHub Repository:** [https://github.com/ttkathyayani/CreatorOps](https://github.com/ttkathyayani/CreatorOps)
- **Primary Color Palette:** Minimalist Black & Charcoal (`#111111`, `#1C1C1C`) with Yellow Accents (`#FACC15`, `#EAB308`)

---

# TABLE OF CONTENTS
1. [Executive Summary & Problem Statement](#1-executive-summary--problem-statement)
2. [Technology Stack & Architectural Decisions](#2-technology-stack--architectural-decisions)
3. [Database Architecture & Entity Relationships (ERD)](#3-database-architecture--entity-relationships-erd)
4. [7-Stage Content Production State Machine](#4-7-stage-content-production-state-machine)
5. [Role-Based Access Control (RBAC) Matrix](#5-role-based-access-control-rbac-matrix)
6. [AI Agent Architecture & Mathematical Heuristics](#6-ai-agent-architecture--mathematical-heuristics)
7. [Screen-by-Screen Complete Walkthrough (All 18 Web Pages)](#7-screen-by-screen-complete-walkthrough)
8. [End-to-End 5-Minute Live Review Demo Script](#8-end-to-end-5-minute-live-review-demo-script)
9. [Top 20 Review & Viva Defense Questions & Answers](#9-top-20-review--viva-defense-questions--answers)
10. [Pre-Seeded Credentials Reference](#10-pre-seeded-credentials-reference)

---

# 1. Executive Summary & Problem Statement

### The Problem
In modern digital marketing and influencer agencies:
1. **Scattered Workflows:** Content ideation, talking points, script revisions, and media assets are scattered across WhatsApp, Google Drive, Slack, and email threads.
2. **Approval Bottlenecks:** External brand clients take days to approve assets because feedback is disorganized and lack audit trails.
3. **No Quality Compliance:** Creator scripts frequently fail brand guidelines, miss call-to-actions (CTAs), or exceed optimal platform durations.
4. **Multi-Tenant Chaos:** Marketing agencies handling multiple brands struggle with cross-client data privacy and permission leakage.

### The CreatorOps Solution
CreatorOps is a centralized, cloud-native **Multi-Tenant SaaS platform** that unifies:
- **Campaign Portfolios & Budgets** for diverse client brands.
- **Content Deliverables Matrix** across Instagram, YouTube, LinkedIn, TikTok, and Twitter/X.
- **Immutable Content Versioning** with automated snapshots.
- **Role-Based Two-Tier Approval Queue** (Internal Manager Sign-off $\rightarrow$ External Client Sign-off).
- **Embedded AI Agent Studio** providing automated script audits, creative concept generation, feedback clustering, and executive reporting.
- **Zero-Trust Multi-Tenancy** guaranteeing strict tenant isolation per Workspace.

---

# 2. Technology Stack & Architectural Decisions

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Backend Framework** | **Django 6.1 (Python 3.12)** | Built-in ORM, secure session auth, robust migrations, and administrative capabilities. |
| **API Architecture** | **Django REST Framework (DRF 3.18)** | ModelViewSets, Token/Session authentication, nested serializers, and standardized JSON responses. |
| **Frontend Architecture** | **Django Dynamic Templates + Vanilla JS** | Server-side rendering for optimal SEO and rapid load times; zero heavy npm dependencies. |
| **Design System** | **Custom CSS3 (Black & Yellow Design)** | Modern dark aesthetic (`#111111`, `#1C1C1C`, `#FACC15`) with glassmorphic cards and responsive flex/grid layouts. |
| **Database** | **SQLite (Demo/Dev) / PostgreSQL (Cloud)** | Environment-aware database adapter supporting `DATABASE_URL` (Neon/Supabase) and `/tmp` copy on Vercel serverless lambdas. |
| **Static File Delivery** | **WhiteNoise 6.12** | Serves compressed, cache-header-tagged static assets directly from WSGI without separate Nginx configuration. |
| **Asset Storage** | **Dual Storage (AWS S3 via Boto3 + Local)** | Enterprise cloud object storage for heavy media (MP4, PNG, MOV) with local fallback. |
| **Cloud Hosting** | **Vercel Python Serverless Runtime** | Zero-downtime, global Edge network deployment with automatic SSL certificate management. |

---

# 3. Database Architecture & Entity Relationships (ERD)

CreatorOps features **9 core relational models** designed around strict relational integrity:

```
[Workspace] 1 ──── ∞ [Membership] ∞ ──── 1 [User]
     │
     └── 1 ──── ∞ [Client]
                     │
                     └── 1 ──── ∞ [Campaign] 1 ──── ∞ [CampaignMetric]
                                     │
                                     └── 1 ──── ∞ [ContentItem]
                                                     ├── 1 ──── ∞ [ContentVersion]
                                                     ├── 1 ──── ∞ [Approval]
                                                     └── 1 ──── ∞ [Asset]
```

### Detailed Model Schema Breakdown

#### 1. `Workspace` (`workspaces/models.py`)
- `id` (BigAutoField): Primary Key.
- `name` (CharField, 255): Tenant name (e.g., "Creator Studio Pro").
- `slug` (SlugField, 255): Auto-generated unique URL slug with conflict-resolution counter.
- `description` (TextField): Agency bio or operational mandate.
- `created_at` / `updated_at` (DateTimeField): Audit timestamps.

#### 2. `Membership` (`workspaces/models.py`)
- `id` (BigAutoField): Primary Key.
- `user` (ForeignKey $\rightarrow$ `auth.User`): Associated user.
- `workspace` (ForeignKey $\rightarrow$ `Workspace`): Tenant boundary.
- `role` (CharField, 20): One of `ADMIN`, `MANAGER`, `CREATOR`, `CLIENT_REVIEWER`.
- **Constraint:** `unique_together = ("user", "workspace")`. Prevents duplicate memberships.

#### 3. `Client` (`clients/models.py`)
- `id` (BigAutoField): Primary Key.
- `workspace` (ForeignKey $\rightarrow$ `Workspace`): Tenant owner.
- `name` (CharField, 255): Brand name (e.g., "GlowSkin Organics").
- `contact_email` (EmailField): Client primary stakeholder email.
- `industry` (CharField, 100): Domain (e.g., "Beauty & Wellness").
- `company_notes` (TextField): Internal agency relationship notes.
- `brand_guidelines` (TextField): Critical tone-of-voice and prohibited word rules ingested by AI agents.
- **Constraint:** `unique_together = ("workspace", "name")`.

#### 4. `Campaign` (`campaigns/models.py`)
- `id` (BigAutoField): Primary Key.
- `client` (ForeignKey $\rightarrow$ `Client`): Brand owner.
- `title` (CharField, 255): Campaign headline.
- `objective` (TextField): Goal, key messages, target outcomes.
- `target_audience` (CharField, 255): Demographic focus.
- `status` (CharField, 20): `PLANNING`, `ACTIVE`, `PAUSED`, `COMPLETED`.
- `start_date` / `end_date` (DateField): Schedule window.
- `budget` (DecimalField, 12, 2): Financial allocation.
- **Computed Properties:** `total_content_items`, `published_count`, `pending_count`.

#### 5. `ContentItem` (`content/models.py`)
- `id` (BigAutoField): Primary Key.
- `campaign` (ForeignKey $\rightarrow$ `Campaign`): Parent campaign.
- `creator` (ForeignKey $\rightarrow$ `auth.User`, nullable): Assigned creator.
- `title` (CharField, 255): Deliverable title.
- `platform` (CharField, 50): `Instagram`, `YouTube`, `LinkedIn`, `Twitter/X`, `TikTok`.
- `script_body` (TextField): Talking points, script, or storyboard.
- `caption` (TextField): Copy, hashtags, CTA links.
- `due_date` (DateField): Calendar deadline.
- `status` (CharField, 30): 7 workflow states.
- **Method `create_version(user)`:** Takes an atomic snapshot into `ContentVersion`.

#### 6. `ContentVersion` (`content/models.py`)
- `content_item` (ForeignKey $\rightarrow$ `ContentItem`): Parent item.
- `revision_number` (PositiveIntegerField): Incremental version number (v1, v2, v3).
- `script_snapshot` / `caption_snapshot` (TextField): Frozen copy state.
- `created_by` (ForeignKey $\rightarrow$ `auth.User`, nullable): Author of the revision.
- `created_at` (DateTimeField): Timestamp.

#### 7. `Approval` (`approvals/models.py`)
- `content_item` (ForeignKey $\rightarrow$ `ContentItem`): Associated deliverable.
- `reviewer` (ForeignKey $\rightarrow$ `auth.User`): Stakeholder making the decision.
- `decision` (CharField, 50): `MANAGER_APPROVED`, `MANAGER_CHANGES_REQUESTED`, `CLIENT_APPROVED`, `CLIENT_CHANGES_REQUESTED`.
- `comment` (TextField): Detailed constructive feedback or approval sign-off note.
- `timestamp` (DateTimeField): Immutable audit log timestamp.

#### 8. `Asset` (`assets/models.py`)
- `content_item` (ForeignKey $\rightarrow$ `ContentItem`): Deliverable link.
- `file` (FileField): Uploaded media.
- `filename` (CharField): Original file name.
- `s3_object_key` (CharField): AWS S3 key path.
- `mime_type` (CharField): Media format (e.g., `video/mp4`, `image/png`).
- `size_bytes` (BigIntegerField): Raw byte size.
- `file_size_display`: Formatted size property (`2.4 MB`, `500 KB`).

#### 9. `CampaignMetric` (`analytics/models.py`)
- `campaign` (ForeignKey $\rightarrow$ `Campaign`): Linked campaign.
- `metric_name` (CharField): KPI identifier (`Impressions`, `Clicks`, `Conversions`, `Engagement Rate`).
- `metric_value` (DecimalField, 14, 2): Numeric telemetry data.
- `recorded_date` (DateField): Observation timestamp.

---

# 4. 7-Stage Content Production State Machine

Every piece of content traverses a rigorous, sequential lifecycle:

```
[1. DRAFT]
    │  (Creator submits)
    ▼
[2. PENDING MANAGER REVIEW]
    ├── (Manager requests changes) ──> [5. CHANGES REQUESTED] ──> (Creator edits & re-submits) ──┐
    │                                                                                            │
    └── (Manager approves)                                                                       │
           │                                                                                     │
           ▼                                                                                     │
     [3. PENDING CLIENT APPROVAL]                                                                │
           ├── (Client requests changes) ────────────────────────────────────────────────────────┘
           │
           └── (Client approves)
                  │
                  ▼
            [4. APPROVED]
                  │
                  ▼
            [6. SCHEDULED]
                  │
                  ▼
            [7. PUBLISHED]
```

### State Definitions & Enforced Logic
1. **`draft`**: The creator is drafting copy and scripts. The item is not visible in approval queues.
2. **`pending_manager`**: Internal quality control. Agency managers check script quality and brand safety.
3. **`pending_client`**: Client sign-off gate. The client brand reviews the asset via the client portal.
4. **`approved`**: Both internal manager and client have formally signed off. Ready for scheduling.
5. **`changes_requested`**: Either manager or client submitted feedback requiring a revision. The item drops back to creator editing mode.
6. **`scheduled`**: Asset has a fixed publication date and time on the editorial calendar.
7. **`published`**: Content is live on social platforms. Metrics begin tracking against it.

---

# 5. Role-Based Access Control (RBAC) Matrix

| Feature / Action | Agency Admin (`ADMIN`) | Campaign Manager (`MANAGER`) | Content Creator (`CREATOR`) | Client Reviewer (`CLIENT_REVIEWER`) |
| :--- | :---: | :---: | :---: | :---: |
| **View Dashboard & Telemetry** | ✅ Full | ✅ Full | ✅ Full | ⚠️ Portal View |
| **Manage Workspaces & Members** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Create / Edit Clients** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Create / Edit Campaigns** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Create / Edit Content Drafts** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Run AI Script Review Agent** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Manager Approval Sign-Off** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Client Approval Sign-Off** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Upload Media Assets** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Record Analytics Metrics** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **View AI Executive Reports** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

---

# 6. AI Agent Architecture & Mathematical Heuristics

CreatorOps includes an autonomous, modular AI Agent Engine under `agents/`:

### Agent 1: Script Review Agent (`ScriptReviewAgent`)
- **Objective:** Evaluates creator scripts before internal review.
- **Heuristic Calculations:**
  - **Pacing & Duration:** $\text{Duration (seconds)} = \left(\frac{\text{Word Count}}{130 \text{ wpm}}\right) \times 60$.
  - **Platform Thresholds:** Short-form video (Instagram/TikTok/Reels) > 150 words deducts 15 points (exceeds 60-second retention limit).
  - **Call-to-Action (CTA) Audit:** Scans for conversion tokens (`subscribe`, `link in bio`, `save`, `comment`, `sign up`). Missing CTA deducts 20 points.
  - **Opening Hook Check:** Evaluates the first 20 words for curiosity drivers (`why`, `how`, `stop`, `secret`, `mistake`, `truth`, `?`, `!`). Missing hook deducts 15 points.
  - **Brand Rule Compliance:** Cross-references `Client.brand_guidelines` for prohibited words (`avoid`, `don't use`, `no`). Deducts 15 points per violation.
  - **Overall Score:** Clamped dynamically between $0$ and $100$.

### Agent 2: Content Ideas Agent (`ContentIdeasAgent`)
- **Objective:** Generates creative angles and formats tailored to industry, audience, and platform.
- **Platform Strategy:**
  - *Instagram / TikTok*: 30–45s contrarian reels, 7-slide transparent behind-the-scenes carousels, before-and-after split-screen transformations.
  - *YouTube*: 12–15 min full masterclasses with screen recordings, 8–10 min video essays.
  - *LinkedIn*: Executive text posts with data infographics, 5-lesson curated PDF carousels.
  - *Twitter/X*: 8–10 tweet visual tactical threads.

### Agent 3: Approval Summary Agent (`ApprovalSummaryAgent`)
- **Objective:** Synthesizes multiple disparate stakeholder comments into a prioritized action checklist.
- **NLP Categorization:**
  - Classifies feedback into 5 operational domains: *Hook & Pacing*, *Call to Action*, *Visuals & Assets*, *Branding*, *Copywriting*.
  - Determines priority: "High" if comments contain urgent imperative language (`must`, `crucial`, `critical`), otherwise "Medium".
  - Generates a clear executive readiness verdict: `approved_ready` vs `action_required`.

### Agent 4: Campaign Report Agent (`CampaignReportAgent`)
- **Objective:** Converts raw numerical telemetry into an executive campaign performance report.
- **Formulae:**
  - $\text{Completion Rate (\%)} = \left(\frac{\text{Published Content}}{\text{Total Content}}\right) \times 100$.
  - $\text{Avg Engagement Rate (\%)} = \frac{\sum \text{Engagement Values}}{\text{Number of Observations}}$ (or $\frac{\text{Total Clicks}}{\text{Total Impressions}} \times 100$).
  - $\text{Cost Per Acquisition (CPA)} = \frac{\text{Campaign Budget}}{\text{Total Conversions}}$.
  - **Health Assessment:** Computes health status (*On Track*, *Needs Review / Bottleneck*, *Strong Performance*) and outputs narrative paragraphs for client presentations.

---

# 7. Screen-by-Screen Complete Walkthrough

CreatorOps features **18 distinct web pages**, styled in the Black-and-Yellow UI.

---

### Screen 1: Login Page
- **URL:** `/accounts/login/`
- **Template:** [`templates/accounts/login.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/accounts/login.html)
- **Authorized Users:** Anyone (Unauthenticated).
- **What's on the Screen:**
  - CreatorOps Logo in yellow highlight.
  - Charcoal card surface (`#1C1C1C`) with subtle border.
  - **Username & Password input fields** with yellow focus outlines.
  - **"Sign In" Button** (Bright yellow `#FACC15` with black text).
  - Quick-Reference Demo Credentials banner (`admin / admin123`, `manager / admin123`, `creator / admin123`, `client / admin123`).
  - Link to "Create an Account" for self-service signup.
- **Backend Action:** Submits POST request to `accounts:login`. Authenticates credentials, activates Django session, and sets active workspace.

---

### Screen 2: User Registration Page
- **URL:** `/accounts/register/`
- **Template:** [`templates/accounts/register.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/accounts/register.html)
- **Authorized Users:** New visitors.
- **What's on the Screen:**
  - Username, Email, and Password fields.
  - **Agency / Workspace Name field**: Automatically creates a dedicated workspace for the new user.
  - **Default Role selector**: Admin, Manager, Creator, or Client.
  - "Create Account" button.
- **Backend Action:** Creates `User`, generates a new `Workspace`, creates `Membership` with `ADMIN` privileges, and redirects directly to Dashboard.

---

### Screen 3: Executive Dashboard
- **URL:** `/dashboard/`
- **Template:** [`templates/dashboard/index.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/dashboard/index.html)
- **Authorized Users:** All authenticated roles.
- **What's on the Screen:**
  - **Top KPI Stat Cards**:
    - *Total Clients* (Total active brand accounts).
    - *Active Campaigns* (Live marketing campaigns).
    - *Total Deliverables* (Total content items).
    - *Published Assets* (Completed deliverables).
  - **Production Pipeline Progress Bar**: Visual bar showing percentage breakdown of content items across Draft, Review, Approved, and Published.
  - **Action Required / Pending Approval Alerts Box**: Highlights deliverables waiting for the logged-in user's role.
  - **Recent Deliverables Table**: Displays latest 6 items with status badges, platforms, and quick links.
  - **Active Campaigns Grid**: Quick view of live campaign progress.
- **Backend Action:** Aggregates database queries across `Client`, `Campaign`, and `ContentItem` filtered strictly by `request.workspace`.

---

### Screen 4: Client Brands Portfolio (List)
- **URL:** `/clients/`
- **Template:** [`templates/clients/list.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/clients/list.html)
- **Authorized Users:** All workspace members.
- **What's on the Screen:**
  - Header with "+ Add New Client" button (visible to Admin/Manager).
  - **Client Card Grid**: Each card shows:
    - Client Name & Industry Badge (e.g. *SaaS*, *Fitness*, *Beauty*).
    - Primary Contact Email.
    - Active Campaign count & Total Deliverables count.
    - Snippet of Brand Voice Guidelines.
    - "View Portfolio" action button.
- **Backend Action:** Queries `Client.objects.filter(workspace=request.workspace)`.

---

### Screen 5: Client Detail & Brand Guidelines View
- **URL:** `/clients/<id>/`
- **Template:** [`templates/clients/detail.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/clients/detail.html)
- **Authorized Users:** All workspace members.
- **What's on the Screen:**
  - Client Overview Banner (Industry, Contact Email, Created Date).
  - **Brand Voice & Compliance Guidelines Card**: Highlights required hashtags, tone rules, and prohibited keywords ingested by AI agents.
  - **Associated Campaigns Table**: Shows all active and completed campaigns for this client.
  - Action buttons: "Edit Guidelines", "+ New Campaign", "Delete Client".
- **Backend Action:** Retrieves client and prefetches related `campaigns` and `content_items`.

---

### Screen 6: Client Creation & Edit Form
- **URL:** `/clients/create/` and `/clients/<id>/edit/`
- **Template:** [`templates/clients/form.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/clients/form.html)
- **Authorized Users:** Admin, Manager.
- **What's on the Screen:**
  - Client Name input.
  - Contact Email input.
  - Industry input.
  - **Brand Guidelines Textarea**: Formatted input where managers define brand rules (e.g., *"Tone: Professional and inspiring. Never use slang. Required hashtag: #GlowNatural"*).
  - "Save Client" button.
- **Backend Action:** Validates inputs and saves `Client` instance associated with `request.workspace`.

---

### Screen 7: Client Delete Confirmation
- **URL:** `/clients/<id>/delete/`
- **Template:** [`templates/clients/confirm_delete.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/clients/confirm_delete.html)
- **Authorized Users:** Admin.
- **What's on the Screen:**
  - Warning alert stating all associated campaigns and content will be deleted (Cascade).
  - "Yes, Delete" danger button & "Cancel" button.

---

### Screen 8: Campaigns Directory (List)
- **URL:** `/campaigns/`
- **Template:** [`templates/campaigns/list.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/campaigns/list.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - "+ Create Campaign" button.
  - **Campaigns Table / Cards**:
    - Campaign Title & Client Brand.
    - Status Badge (`PLANNING`, `ACTIVE`, `PAUSED`, `COMPLETED`) color-coded.
    - Budget counter (e.g. `$15,000.00`).
    - Schedule window (Start Date $\rightarrow$ End Date).
    - Progress Bar showing Published / Total Deliverables.
    - Quick actions: "View Details", "AI Report".

---

### Screen 9: Campaign Command Center (Detail)
- **URL:** `/campaigns/<id>/`
- **Template:** [`templates/campaigns/detail.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/campaigns/detail.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - **Header Banner**: Campaign objective, target audience, budget, date range, status badge.
  - **Deliverables Funnel Bar**: Shows how many deliverables are in Draft, Pending Review, Approved, or Published.
  - **Content Deliverables Matrix**: Table of all linked content with platform badges, creators, due dates, and statuses.
  - **Executive Actions**:
    - "+ Add Deliverable"
    - "Generate AI Performance Report" (opens Screen 16)
    - "Edit Campaign"
- **Backend Action:** Fetches `Campaign` with related `client`, `content_items`, and `metrics`.

---

### Screen 10: Campaign Creation & Edit Form
- **URL:** `/campaigns/create/` and `/campaigns/<id>/edit/`
- **Template:** [`templates/campaigns/form.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/campaigns/form.html)
- **Authorized Users:** Admin, Manager.
- **What's on the Screen:**
  - Client dropdown selector.
  - Campaign Title input.
  - Objective textarea.
  - Target Audience input.
  - Budget decimal input.
  - Status dropdown (`PLANNING`, `ACTIVE`, `PAUSED`, `COMPLETED`).
  - Start & End Date pickers.
  - "Save Campaign" button.

---

### Screen 11: Content Deliverables Matrix (List)
- **URL:** `/content/`
- **Template:** [`templates/content/list.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/content/list.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - **Multi-Filter Bar**:
    - Filter by Status (Draft, Pending Manager, Pending Client, Approved, etc.).
    - Filter by Platform (Instagram, YouTube, LinkedIn, TikTok, Twitter/X).
    - Filter by Campaign.
  - "+ New Content Item" button.
  - **Deliverables Table**:
    - Title & Platform icon badge.
    - Campaign & Client brand.
    - Assigned Creator avatar/username.
    - Due Date.
    - Workflow Status Badge with distinct color coding.
    - "Open Workspace" button.
- **Backend Action:** Implements dynamic query filtering using Django ORM `.filter()`.

---

### Screen 12: Content Item Workspace & Versioning Studio (Detail)
- **URL:** `/content/<id>/`
- **Template:** [`templates/content/detail.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/content/detail.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - **Top Workflow Bar**: Displays current state in the 7-stage lifecycle with forward-action buttons (e.g. "Submit for Manager Review").
  - **Left Column — Content Studio**:
    - Script Draft & Talking Points box.
    - Final Caption & Hashtags box.
    - **"Run AI Script Review" Button**: Calls the AI Script Review Agent via AJAX and renders an interactive diagnostic card with score, word count, hook check, and suggestions right on the page.
    - **Media Assets Gallery**: Displays uploaded video/image assets with download links and file size badges.
    - "Upload New Asset" form.
  - **Right Column — Approval & History**:
    - **AI Feedback Summary Card**: Synthesizes reviewer comments into actionable checkboxes.
    - **Approval Log**: Complete chronological audit trail of all manager and client reviews with decision badges and comments.
    - **Version History Table**: Shows all previous versions (v1, v2, v3) with timestamps and snapshot links.
- **Backend Action:** Combines `ContentItem`, `ContentVersion`, `Approval`, `Asset`, and invokes `ApprovalSummaryAgent`.

---

### Screen 13: Content Item Creation Form
- **URL:** `/content/create/`
- **Template:** [`templates/content/form.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/content/form.html)
- **Authorized Users:** Admin, Manager, Creator.
- **What's on the Screen:**
  - Campaign dropdown.
  - Title input.
  - Social Platform selector (Instagram, YouTube, LinkedIn, TikTok, Twitter/X).
  - Due Date picker.
  - Script Body textarea (talking points / storyboard).
  - Caption textarea (copy & hashtags).
  - Initial Status selector.
  - "Create Deliverable" button.

---

### Screen 14: Editorial Content Calendar
- **URL:** `/content/calendar/`
- **Template:** [`templates/calendar/index.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/calendar/index.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - Visual timeline grid of all deliverables organized by scheduled publication deadlines (`due_date`).
  - Cards color-coded by social platform and workflow status.
  - Direct links to open content workspaces.
- **Backend Action:** Queries `ContentItem.objects.filter(due_date__isnull=False).order_by('due_date')`.

---

### Screen 15: Two-Tier Approval Queue
- **URL:** `/approvals/`
- **Template:** [`templates/approvals/queue.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/approvals/queue.html)
- **Authorized Users:** All members (prioritized by role).
- **What's on the Screen:**
  - **Role-Aware Banner**: Explains what the current user is responsible for approving:
    - Managers see deliverables in **Pending Manager Review**.
    - Clients see deliverables in **Pending Client Approval**.
  - **Review Action Modal / Card**:
    - Script and caption preview.
    - Decision selector: **Approve** (Green) vs **Request Changes** (Amber).
    - Review Comment textarea (mandatory feedback for revision requests).
    - "Submit Decision" button.
- **Backend Action:** Executes state machine transitions upon submission and logs an immutable `Approval` record.

---

### Screen 16: AI Executive Campaign Report
- **URL:** `/analytics/campaigns/<id>/report/`
- **Template:** [`templates/reports/campaign_report.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/reports/campaign_report.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - **Executive Narrative Banner**: Auto-generated by `CampaignReportAgent`, stating overall campaign health (*On Track*, *Bottleneck*, *Strong*).
  - **Performance KPI Cards**: Total Impressions, Clicks, Conversions, Avg Engagement Rate, Completion Rate (%).
  - **Strategic Recommendations**: 3 prioritized action points generated by the AI agent for client stakeholders.
  - **Record New Metric Form**: Input fields to add live campaign metrics (Impressions, Clicks, Conversions).
  - **Recorded Telemetry Table**: Full history of recorded metrics with dates and values.
  - "Export / Print Report" button for client presentations.

---

### Screen 17: AI Agent Studio
- **URL:** `/analytics/agents/`
- **Template:** [`templates/agents/workspace.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/agents/workspace.html)
- **Authorized Users:** All members.
- **What's on the Screen:**
  - Interactive workbench to test all 4 AI Agents on demand:
    1. **Script Review Agent**: Paste script and brand rules $\rightarrow$ Click "Analyze Script" $\rightarrow$ See score, duration, CTA check, and suggestions in real time.
    2. **Content Ideas Agent**: Select industry, audience, goal, and platform $\rightarrow$ Click "Generate Concepts" $\rightarrow$ Get 3 platform-tailored ideas with hooks, formats, and angles.
    3. **Approval Summary Agent**: Test comment clustering into action items.
    4. **Campaign Report Agent**: Test executive summary generation.
  - Live JSON response inspector tab for API evaluation.

---

### Screen 18: Team & RBAC Management
- **URL:** `/workspaces/members/`
- **Template:** [`templates/workspaces/members.html`](file:///d:/DOWNLOADS/SEMESTER%205/PROJX/New%20folder/templates/workspaces/members.html)
- **Authorized Users:** Admin.
- **What's on the Screen:**
  - Workspace details (Name, slug, creation date).
  - **Active Members Table**:
    - Username & Email.
    - Role Badge (`Agency Admin`, `Campaign Manager`, `Creator`, `Client Reviewer`).
    - Joined Date.
    - Role update dropdown (Admin only).
  - **"Invite New Member" Form**: Assigns a user to the workspace with a designated role.

---

# 8. End-to-End 5-Minute Live Review Demo Script

Follow this exact sequence to deliver a flawless project presentation to your evaluators:

### Step 1: Login & The Problem Statement (1 Minute)
1. Open **`https://creatorops-rho.vercel.app`** in your browser.
2. Explain: *"CreatorOps is a Multi-Tenant SaaS platform solving content production bottlenecks between marketing agencies, creators, and client brands."*
3. Log in as **`admin`** / **`admin123`**.

### Step 2: Dashboard & Tenant Navigation (1 Minute)
1. Point out the **KPI Stat Cards**, **Production Pipeline Bar**, and **Action Required Alerts**.
2. Navigate to **Clients** (`/clients/`): Show **GlowSkin Organics** and open its details to display the **Brand Guidelines** (required hashtags, tone of voice).
3. Navigate to **Campaigns** (`/campaigns/`): Open **Summer Glow Launch 2026** to show budget, dates, and linked deliverables.

### Step 3: Content Creation & AI Script Review (1.5 Minutes)
1. Navigate to **Content** (`/content/`): Open deliverable **"5 Morning Skincare Mistakes"**.
2. Click **"Run AI Script Review"**:
   - Show how the AI agent calculates speaking duration (~45s), detects the opening hook, audits the Call-to-Action, and checks brand compliance with a score of 95/100.
3. Show the **Version History** table (v1 vs v2) demonstrating immutable audit trails.

### Step 4: The Two-Tier Approval Queue (1 Minute)
1. Click **Approvals** (`/approvals/`):
   - Show how the queue filters items requiring manager review vs client review.
2. Submit an approval decision with constructive feedback to show the state machine transition in real time.

### Step 5: AI Campaign Performance Report & Cloud Architecture (30 Seconds)
1. Open **AI Executive Report** (`/analytics/campaigns/1/report/`):
   - Highlight the automated executive narrative, engagement rate calculations, and AI strategic recommendations.
2. Conclude: *"The entire platform is deployed live on Vercel Serverless Python Runtime with WhiteNoise static CDN and zero-trust multi-tenancy."*

---

# 9. Top 20 Review & Viva Defense Questions & Answers

### Q1: What architectural pattern does CreatorOps follow?
**Answer:** CreatorOps follows the **Model-View-Template (MVT)** architectural pattern in Django, combined with a **Domain-Driven Design (DDD)** modular structure where each business capability is isolated into an independent app (`accounts`, `workspaces`, `clients`, `campaigns`, `content`, `approvals`, `assets`, `analytics`, and `agents`).

### Q2: How is Multi-Tenancy implemented? How do you prevent data leaks between agencies?
**Answer:** We implemented **Row-Level Tenant Isolation** via the `Workspace` model. Every entity (`Client`, `Campaign`, `ContentItem`, `Asset`) has a foreign key relationship directly or indirectly to `Workspace`. Furthermore, our custom decorator `@workspace_required` automatically injects `request.workspace`, and every ORM query strictly filters by `workspace=request.workspace`. Users cannot query data outside their workspace.

### Q3: Explain your Role-Based Access Control (RBAC). What roles exist?
**Answer:** RBAC is managed via the `Membership` model through four roles:
1. `ADMIN` (Agency Admin): Full administrative control, member management, and deletions.
2. `MANAGER` (Campaign Manager): Manages campaigns, assigns creators, and signs off on internal reviews.
3. `CREATOR` (Content Creator): Drafts copy, uploads media, and runs AI script reviews.
4. `CLIENT_REVIEWER` (Client Brand): External client portal access to approve deliverables or request revisions.
Permissions are enforced at the view layer using our custom `@role_required` decorator and DRF's `IsWorkspaceAdminOrManager` classes.

### Q4: How does the Content Production State Machine prevent unauthorized approvals?
**Answer:** A `ContentItem` can only move from `draft` to `pending_manager`, then to `pending_client`, and finally to `approved`. A creator cannot directly mark an item as `approved`. Only a `MANAGER` can transition an item to `pending_client`, and only a `CLIENT_REVIEWER` can transition it to `approved`. Any rejection drops the status back to `changes_requested`.

### Q5: What makes content versioning "immutable"?
**Answer:** When an item is updated, the `ContentItem.create_version()` method creates a separate `ContentVersion` record containing a frozen snapshot of the `script_body`, `caption`, and timestamp, along with an auto-incrementing `revision_number`. Existing version records are never edited or overwritten, providing a tamper-proof audit trail.

### Q6: How do the AI Agents work? Are they using OpenAI or custom algorithms?
**Answer:** The AI agents are built using an **extensible, decoupled Agent Framework** (`BaseAgent`). They currently implement **deterministic heuristic rule engines and NLP algorithms**:
- `ScriptReviewAgent`: Analyzes word counts, speaking rates (130 wpm), keyword pattern matching for CTAs, and regex token scanning for hooks and prohibited brand terms.
- `ContentIdeasAgent`: Uses platform-specific creative templates with dynamic slot filling based on industry and audience.
- `ApprovalSummaryAgent`: Clusters reviewer sentiment into actionable categories using domain classification.
- `CampaignReportAgent`: Calculates statistical metrics (CPA, Completion %, Engagement Rate) and synthesizes an executive narrative.
Because they inherit from `BaseAgent`, any agent can be swapped with OpenAI, Gemini, or Claude API calls by overriding the `run()` method without modifying the rest of the application.

### Q7: Why did you choose WhiteNoise instead of letting Django serve static files directly?
**Answer:** Django's default static file handler is insecure and inefficient for production (`DEBUG = False`). WhiteNoise sits inside the WSGI pipeline, compresses static files with gzip, generates unique hash fingerprints for cache-busting, and serves them with long-term `Cache-Control` headers directly from the application server without requiring a separate web server.

### Q8: How did you solve Vercel's read-only serverless filesystem limitation with SQLite?
**Answer:** Vercel serverless functions have a read-only filesystem except for the `/tmp` directory. In `config/settings.py`, we detect if `VERCEL` is active. If so, Django copies the bundled `db.sqlite3` file to `/tmp/db.sqlite3` and connects to that path. This allows write operations (sessions, new content, approvals) to succeed without throwing `sqlite3.OperationalError: attempt to write a readonly database`. Additionally, `settings.py` includes native support for cloud PostgreSQL via `DATABASE_URL`.

### Q9: What happens if an external brand client rejects a script?
**Answer:** When a client selects "Request Changes" and enters feedback, the `submit_review` view records an `Approval` record with decision `CLIENT_CHANGES_REQUESTED` and automatically transitions the `ContentItem.status` to `changes_requested`. The creator receives an alert on their dashboard, and the `ApprovalSummaryAgent` categorizes the feedback into a prioritized revision checklist.

### Q10: How are media assets handled? Can you support AWS S3?
**Answer:** Yes. In `assets/storage.py`, we implemented a storage abstraction layer. When `USE_S3 = True` is enabled with AWS credentials in environment variables, files are uploaded directly to an Amazon S3 bucket using `boto3`. If running locally or in demo mode, it seamlessly falls back to Django's local filesystem storage.

### Q11: Explain your Context Processor. Why is it useful?
**Answer:** `workspaces/context_processors.py` defines `workspace_context()`. By registering it in `settings.TEMPLATES`, Django automatically executes it for every rendered page. It injects `active_workspace`, `user_role`, and `user_memberships` into every template context, so navigation bars and role indicators work globally without needing to query the database in every view.

### Q12: Why is CSRF protection important, and how did you configure it for Vercel?
**Answer:** Cross-Site Request Forgery (CSRF) prevents unauthorized commands from being transmitted from a user that the web application trusts. On Vercel, requests originate from `*.vercel.app` domains. We added `https://*.vercel.app` to `CSRF_TRUSTED_ORIGINS` in `settings.py`, which permits secure POST form submissions while blocking malicious cross-origin requests.

### Q13: What is the purpose of `slugify` in the Workspace model?
**Answer:** In `workspaces/models.py`, `Workspace.save()` uses `slugify(self.name)` to convert names like "Creator Studio Pro" into URL-friendly identifiers like `creator-studio-pro`. It also includes a `while` loop that appends an incremental counter (e.g., `-1`, `-2`) if a collision occurs, ensuring all tenant slugs are unique.

### Q14: How does CreatorOps handle REST APIs alongside HTML templates?
**Answer:** In `config/urls.py`, we maintain dual routing:
- Template URLs render HTML templates via server-side Django views.
- REST API URLs (`/api/...`) are handled by DRF's `DefaultRouter` (`ClientViewSet`, `CampaignViewSet`, `ContentItemViewSet`), returning JSON responses with session or token authentication.

### Q15: How does the calendar screen work?
**Answer:** `calendar_view` in `content/views.py` queries all deliverables in the active workspace that have a non-null `due_date`. The template groups these deliverables chronologically, rendering color-coded badges by platform (Instagram, YouTube, etc.) and linking directly to each item's detail view.

### Q16: What database constraints prevent duplicate clients or memberships?
**Answer:** We enforce database-level uniqueness using Django's `Meta.unique_together`:
- In `Client`: `unique_together = ("workspace", "name")` ensures no two clients in the same agency share a name.
- In `Membership`: `unique_together = ("user", "workspace")` ensures a user cannot have two membership records in the same organization.

### Q17: What is the significance of speaking speed in the Script Review Agent?
**Answer:** The average conversational speaking rate for video content is approximately **130 words per minute**. The agent divides the script's word count by 130 and multiplies by 60 to calculate duration in seconds. For short-form platforms (Instagram Reels, TikTok), scripts over 150 words exceed 60 seconds and cause viewer drop-off, which the agent flags as a pacing flaw.

### Q18: How does the application handle responsive layouts on mobile devices?
**Answer:** `static/css/style.css` is built with a mobile-first CSS Grid and Flexbox architecture. On desktop viewports, it displays a 260px fixed sidebar and a multi-column card layout. On screens smaller than 768px, the layout adapts to a single-column stacked view with collapsible navigation.

### Q19: How do you seed test data into the application?
**Answer:** We created a custom Django management command: `python manage.py seed_demo_data` located in `workspaces/management/commands/seed_demo_data.py`. It programmatically provisions 4 user accounts with distinct roles (`admin`, `manager`, `creator`, `client`), 3 client brands, 3 campaigns, 5 deliverables across all workflow states, and analytics metrics in one atomic execution.

### Q20: What future enhancements can be added to CreatorOps?
**Answer:** 
1. **Direct Social Media API Publishing**: Automatic publishing to Instagram Graph API and YouTube Data API upon client approval.
2. **LLM Integration**: Connecting `BaseAgent` directly to Gemini or Claude for dynamic video script rewriting and AI image generation.
3. **Stripe Billing Integration**: Tiered subscription plans based on creator seats and monthly deliverables.

---

# 10. Pre-Seeded Credentials Reference

| Role | Username | Password | Email | Purpose in Review |
| :--- | :--- | :--- | :--- | :--- |
| **Agency Admin** | `admin` | `admin123` | `admin@creatorops.io` | Full system control, workspace members, global KPIs |
| **Campaign Manager** | `manager` | `admin123` | `manager@creatorops.io` | Creating campaigns, assigning creators, internal approval queue |
| **Content Creator** | `creator` | `admin123` | `creator@creatorops.io` | Writing scripts, running AI Script Review, updating copy |
| **Client Brand** | `client` | `admin123` | `client@glowskin.com` | Client portal, reviewing deliverables, approving assets |

---
*Document generated for CreatorOps B.Tech CSE Project Review & Viva Defense.*
