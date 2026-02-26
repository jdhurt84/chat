# Monitoring & Trigger Intelligence MVP Spec

## 1) Product Goal
Build a monitoring system that continuously scans the web for institutions you care about (schools, private schools, hospitals, venues, clubs), classifies relevant developments into trigger categories, scores each item for actionability, and alerts only when attention is warranted.

---

## 2) Core Outcomes
- Detect relevant institutional changes earlier than manual research.
- Reduce noise by filtering and ranking with a trigger matrix.
- Route the highest-value opportunities into a sales workflow (sheet/Airtable/HubSpot).

---

## 3) Source Collection (MVP)
Use a layered ingestion approach for speed + coverage + resilience:

1. **GDELT (primary breadth + speed)**
   - Poll at 4–6 hour intervals.
   - Use article-level monitoring signals where possible.
   - Good for broad media and international/local pickup.

2. **NewsAPI (primary article retrieval/cleanup)**
   - Use `Everything` endpoint for keyword/entity search.
   - Use top headlines where helpful for recent trend capture.
   - Normalize metadata fields for scoring and de-duplication.

3. **Google Alerts / RSS (backup + institution watchlists)**
   - Maintain institution-specific and executive-specific terms.
   - Ingest RSS feeds as a low-friction fallback channel.

4. **Do not use Bing News/Search APIs as core dependency**
   - Not recommended as a strategic dependency due to support end state referenced in requirements.

---

## 4) Trigger Matrix
Each article/post should map to one or more trigger categories:

- Leadership change
- Strategic plan / capital campaign
- Facility upgrades
- Boarding / enrollment shifts
- Parent & student feedback
- Program innovation
- Financial performance
- Non-core use of campus
- Vendor tenure / rotation
- Peer influence

---

## 5) Data Model (per article)
Required fields:

- `organization_name`
- `region`
- `sector` (private school, boarding school, hospital, event venue, golf/country club, etc.)
- `trigger_category`
- `confidence_score` (0–100)
- `opportunity_score` (0–100)
- `urgency` (`low|medium|high`)
- `reason` (short explanation)
- `source_url`
- `published_date`
- `source_type` (`press_release|board_material|strategic_plan|local_news|social|other`)

Recommended additional fields:

- `source_name`
- `headline`
- `summary`
- `raw_text_excerpt`
- `institution_id` (internal canonical ID)
- `is_target_account` (bool)
- `is_profile_similar` (bool)
- `dedupe_key`
- `first_seen_at`
- `last_seen_at`
- `syndication_count`

---

## 6) Scoring Framework
`opportunity_score = trigger_strength + geographic_fit + account_fit + freshness + evidence_quality`

### 6.1 Trigger Strength
- Leadership change: +20
- Strategic plan / campaign: +18
- Dining/facility upgrade: +25
- Enrollment growth / boarding expansion: +15
- Wellness / sustainability / farm-to-table initiative: +12
- Student complaints / food dissatisfaction: +15
- Financial pressure / deficits: +20
- Rentals / camps / external events: +10
- Peer-school upgrade nearby: +8

### 6.2 Geographic Fit
- Northeast or Florida: +15
- Adjacent market: +8

### 6.3 Account Fit
- Existing target account: +20
- Similar to target profile: +10

### 6.4 Freshness
- Published within 7 days: +15
- Published within 30 days: +8

### 6.5 Evidence Quality
- School press release / board materials / strategic plan: +15
- Local news: +10
- Social post / rumor: +3

### 6.6 Thresholds
- **Instant alert**: score >= 75
- **Daily digest**: score 50–74
- **Store only**: score < 50

---

## 7) Classification Pipeline
For each ingested item:

1. Parse title, snippet, and body (if available).
2. Run lightweight NLP + LLM classification:
   - Identify organization(s), region, sector.
   - Assign trigger category.
   - Estimate confidence.
   - Generate concise “why it matters”.
3. Apply deterministic scoring rubric.
4. Route according to threshold.

Prompt outputs should be JSON-structured and schema-validated.

---

## 8) Deduplication Rules
1. **Institution-trigger merge window**
   - If same `organization_name` + same `trigger_category` within 14 days, merge into one evolving signal thread.

2. **Syndication collapse**
   - If substantially identical article appears across multiple sources, keep one canonical record:
     - Prefer evidence quality rank: strategic/board docs > press release > local news > social.
     - Keep alternates as related references.

3. **Near-duplicate heuristic**
   - Compare normalized title similarity + publication time + named entities.

---

## 9) Notification Design
Delivery channels:
- Slack (fast team triage)
- Email (digest + archive)
- SMS (optional, high urgency only)

Payload should include:
- Organization
- Trigger type
- Score
- 2-sentence summary
- Recommended next action
- Source URL + published date

### Example Alert Format
**Alert:** Hotchkiss School — Facility Upgrade Trigger  
**Score:** 87  
**Why flagged:** Recent reporting says Hotchkiss reopened/reimagined its dining commons with expanded seating and modernized systems. This maps directly to “facility upgrades” and indicates a likely high-priority dining strategy conversation.  
**Recommended next step:** Verify self-op vs outsourced model, identify facilities/operations leaders, and monitor follow-on signals around wellness/community/student-experience messaging.

---

## 10) CRM / Workflow Output
Push high-score alerts into Airtable/HubSpot/Sheet queue with:
- `owner`
- `status`
- `notes`
- `follow_up_date`

Recommended statuses:
- `new`
- `triaged`
- `contacted`
- `opportunity_open`
- `closed_lost`
- `closed_won`

---

## 11) Best MVP Stack

### Ingestion & Jobs
- **Python** (fast iteration for APIs + NLP)
- **Prefect** or **cron + lightweight worker** for scheduled polling every 4–6 hours
- HTTP clients: `httpx`

### Storage
- **PostgreSQL** for canonical articles, signals, and scoring records
- Optional **Redis** for short-term dedupe cache and queue buffering

### Processing
- Rule-based scorer + LLM classification step (JSON schema constrained)
- `pydantic` models for validation

### API / Internal Service
- **FastAPI** for:
  - ingestion webhooks (optional)
  - query/review endpoints
  - alert-preview endpoints

### Notifications
- Slack webhook API
- Transactional email provider (e.g., SendGrid/Postmark)
- Twilio (optional high urgency)

### CRM Sync
- Airtable API and/or HubSpot API push for score >= 75

### Observability
- Structured logs (JSON)
- Basic metrics: ingest count, dedupe rate, classified count, alert count, false-positive feedback
- Error alerts via Slack

---

## 12) MVP Milestones

### Milestone 1: Core ingestion + scoring (Week 1)
- Source connectors (GDELT, NewsAPI, RSS)
- Basic schema + database
- Deterministic scoring engine

### Milestone 2: Classification + dedupe + alerting (Week 2)
- LLM classifier for trigger/category/reason/confidence
- Deduplication and merge windows
- Slack/email alerts + daily digest job

### Milestone 3: CRM handoff + feedback loop (Week 3)
- Airtable/HubSpot push for high-score signals
- Analyst feedback field (good lead / false positive)
- Score tuning based on feedback

---

## 13) Success Metrics (First 30 Days)
- Precision of high-score alerts (>=75) >= 60%
- Median time from publication to alert < 6 hours
- False-positive rate in instant alerts < 25%
- At least 1 qualified outbound action per 20 alerts

---

## 14) Risks & Mitigations
- **Noise from broad media** -> stronger entity disambiguation + dedupe + source weighting
- **Over-reliance on single source** -> maintain multi-source redundancy
- **LLM hallucinations** -> require extractive evidence snippets and schema validation
- **Alert fatigue** -> strict thresholds + digest default for mid-band scores
