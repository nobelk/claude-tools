---
name: prd-to-design-doc
description: Generate a Developer Design Document (Design Doc / RFC) from a Product Requirements Document (PRD). Use when the user provides a PRD and wants to create a technical design document, software design specification, RFC, or engineering design doc. This skill produces markdown-formatted design documents that follow the industry-standard practices used at companies like Google, Uber, Airbnb, Slack, Stripe, and Spotify — emphasizing trade-off analysis, alternatives considered, cross-cutting concerns, and phased rollout planning. The output is a comprehensive design-level document without code.
---

# PRD to Developer Design Document (RFC-Style)

## Overview

This skill transforms a Product Requirements Document (PRD) into a Developer Design Document following the RFC/Design Doc conventions used by leading software engineering organizations (Google, Uber, Airbnb, Slack, Stripe, HashiCorp, Spotify).

### Industry Context

Design Docs (also called RFCs or Technical Specs) are the standard planning artifact at modern engineering organizations. They are:

- **Trade-off focused** — the central purpose is to document _why_ a solution was chosen by exploring the trade-offs between alternatives (Google)
- **Informal but structured** — prose-driven with diagrams, not table-heavy bureaucratic documents (Google, Stripe)
- **Reviewer-aware** — include explicit metadata for authors, reviewers, and approval status (Uber, HashiCorp, Spotify)
- **Scope-bounded** — clearly state what is and is not a goal, so reviewers know what to focus on (Google, Airbnb)
- **Living documents** — carry a lifecycle status (Draft → Under Review → Approved → In Progress → Completed)

## Workflow

### Step 1: PRD Analysis

Thoroughly analyze the PRD to extract and categorize:

1. **Problem Statement** — What problem is being solved and why now?
2. **Functional Requirements** — Core features and capabilities
3. **Non-Functional Requirements** — Performance, scalability, security, reliability, observability targets
4. **Constraints** — Technical, business, regulatory, timeline limitations
5. **Stakeholders** — Teams, users, systems that interact with or depend on this
6. **Success Criteria** — Measurable outcomes that define completion

### Step 2: Architecture and Technology Research

Use web search to gather current information on:

1. **Architecture patterns** suitable for the requirements (microservices, modular monolith, serverless, event-driven, etc.)
2. **Current best practices** for similar systems at scale
3. **Libraries, frameworks, and SDKs** — current stable versions, maintenance status, licensing, community health
4. **Testing and observability tools** appropriate for the chosen stack
5. **Cross-cutting concerns** — current best practices for security, privacy, monitoring relevant to the domain

### Step 3: Generate the Design Document

Create a single markdown file following the template in `references/design-document-template.md`. The document structure follows the common sections found across Google, Uber, Airbnb, HashiCorp, Slack, and Stripe design doc formats.

**Required sections (in order):**

1. **Metadata Header** — Title, authors, reviewers, status, date, PRD reference
2. **Overview** — 2-3 paragraphs: what this doc proposes at a glance (HashiCorp: "anyone opening the document will form a clear understanding of the intent")
3. **Context and Scope** — Background facts, current state, why this is needed now (Google: "entirely focused on objective background facts")
4. **Goals and Non-Goals** — Explicit scope boundaries. Non-goals are things that _could_ reasonably be goals but are explicitly excluded (Google: "sometimes more important than goals")
5. **The Design** — The proposed solution:
   - System-context diagram showing how it fits in the existing landscape (Google standard)
   - High-level architecture with Mermaid diagram
   - Key component descriptions
   - Data model and storage approach
   - API surface (if applicable)
   - Data flow narrative
6. **Alternatives Considered** — At least one alternative with trade-off analysis. Google: "one of the most important sections — shows explicitly why the selected solution is the best"
7. **Cross-Cutting Concerns** — Security, privacy, observability/monitoring, accessibility (Google: organizations should "standardize what these concerns are")
8. **Technology Choices** — Key libraries/frameworks/SDKs with justification and version
9. **Testing and Verification Strategy** — How to verify the design meets requirements
10. **Rollout and Implementation Plan** — Phased milestones (Uber, Resend pattern)
11. **Risks and Open Questions** — Known risks with mitigations, unresolved questions with owners
12. **Abandoned Ideas** — Approaches that were explored and deliberately rejected, with reasons (HashiCorp pattern)

### Step 4: Review and Verification

After generating the document, perform a review pass:

1. **PRD Coverage** — Verify every significant PRD requirement is addressed somewhere in the design
2. **Trade-off Quality** — Ensure the Alternatives Considered section gives a fair comparison (not a strawman)
3. **Library Currency** — Confirm recommended libraries/SDKs are current and actively maintained
4. **Cross-Cutting Completeness** — Security, privacy, and observability are addressed
5. **Consistency** — No contradictions between sections
6. **Appropriate Length** — Google recommends 10-20 pages for larger projects; shorter is fine for smaller scope

## Section-by-Section Guidance

### Metadata Header

Follow the RFC convention used by Uber, HashiCorp, Spotify, and others:

```
Title, Author(s), Reviewers, Status (Draft/Under Review/Approved/In Progress/Completed),
Created date, Last updated date, PRD reference link
```

### Overview

Write for the busiest reader. Google: "ensure that the start of your document answers your readers' essential questions." 1-2 paragraphs max. No deep dives — just what the goal is.

### Context and Scope

Follows the Google design doc pattern. The goal: a newcomer (new hire, team transfer) should be able to read this section and follow links to get full context of why this change is necessary. Keep it factual and objective.

### Goals and Non-Goals

Google pattern. Non-goals are NOT negated goals (not "the system shouldn't crash"). They are things that _could_ reasonably be goals but are explicitly chosen not to be. Example: "ACID compliance" for a database design — you'd want to know if that's a goal or non-goal.

### The Design (Core Section)

This is the heart of the document. Follow Google's guidance:

- **Focus on trade-offs** — "The design doc is the place to write down the trade-offs you made"
- **System-context diagram** — Show the new system in the context of existing systems
- **Appropriate detail** — Not an implementation manual; focus on decisions and reasoning
- **APIs and data storage** — Sketch key APIs and data models at a high level, not formal definitions
- **No code** — "Design docs should rarely contain code" (Google). Describe approaches conceptually.
- **Mermaid diagrams** for architecture visualization

### Alternatives Considered

Google: "The focus should be on the trade-offs that each respective design makes and how those trade-offs led to the decision." Present alternatives fairly — show why they were reasonable but why the chosen approach is better for _this_ specific context and goals.

Include a structured comparison:
- Comparison table (key criteria rated for each approach)
- Prose explanation of the decision rationale

### Cross-Cutting Concerns

Google requires dedicated sections for privacy, security, and observability. Keep these focused: explain how the design impacts each concern and how it's addressed.

### Technology Choices

For each significant technology decision, document:
- What it is and why it was chosen
- Version and license
- What was considered instead
- Keep this concise — inline justification, not exhaustive per-library tables

### Testing and Verification

Cover the approach, not a test plan:
- Unit, integration, and E2E testing approaches
- How non-functional requirements (performance, security, scalability) are verified
- Recommended frameworks (without code)

### Rollout and Implementation Plan

Follow the phased rollout pattern used at Uber and Resend:
- Break into milestones with clear deliverables
- Include incremental production deployment strategy
- Note any feature flags, A/B tests, or gradual rollout mechanics

### Risks and Open Questions

- Risks with probability/impact/mitigation
- Open questions with designated owners and timeline
- Dependencies on external teams or systems

### Abandoned Ideas

HashiCorp: "Rather than simply deleting them, organize them into sections that make it clear they're abandoned while explaining why." This prevents future readers from going down the same dead ends.

## Output Format

- **Single markdown file** with clear hierarchical headings (H1-H4)
- **Prose-first** — Use narrative paragraphs to explain trade-offs and reasoning, not just tables
- **Mermaid diagrams** for architecture and data flow visualization
- **Tables** for structured comparisons (alternatives, technology choices, risks)
- **No code snippets** — Describe approaches conceptually
- **Professional but informal tone** — Like a senior engineer explaining to peers, not a formal specification
- **Appropriate length** — 10-20 pages for major projects; 3-5 pages for smaller scope

## Example Invocations

- "Create a design document from this PRD"
- "Generate an RFC from the attached product requirements"
- "Create a technical design doc with emphasis on scalability"
- "Transform this product spec into a developer design document"

## Resources

### references/

- `design-document-template.md` — Complete template following industry-standard sections
- `architecture-patterns.md` — Pattern selection guide with trade-off analysis

## Key Principles

1. **Trade-offs are the point** — The document's primary value is recording _why_ decisions were made, not just _what_ was decided
2. **No code** — Conceptual descriptions only
3. **Web search required** — Always verify library versions and current best practices
4. **Alternatives must be fair** — Never present strawman alternatives; each should be genuinely viable
5. **Cross-cutting concerns are mandatory** — Security, privacy, observability must be addressed
6. **Living document** — Include status lifecycle and revision tracking
7. **Scope-appropriate depth** — Match document length to project complexity; don't over-engineer for simple changes
