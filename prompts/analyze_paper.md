# Research Paper Analysis for Software Engineers
# Usage: Analyze research paper for practical insights: <PAPER_PATH|PAPER_URL>

# Parse input
Set PAPER_SOURCE to $Arguments
Validate that PAPER_SOURCE is provided, otherwise error "Please provide the paper file path or URL to analyze"

## Objective
Analyze the provided software engineering research paper and extract key insights valuable to working engineers and architects, with rigorous evidence assessment.

---

## Phase 1: Initial Paper Scan (Execute in Parallel)

### Stream A: Metadata Extraction
- Title, authors, venue, year
- Paper type (conference/journal/preprint)
- Research area classification
- DOI/URL if available

### Stream B: Structure Analysis
- Identify main sections
- Locate methodology section
- Find evaluation/results section
- Note appendices and supplementary materials

### Stream C: Quick Assessment
- Read abstract and conclusion
- Identify core claim/thesis
- Note stated contributions
- Check for artifacts (code, data)

---

## Phase 2: Deep Analysis (Parallel Streams)

### Stream 1: Methodology Analysis
- Study type identification
- Data collection methods
- Analysis techniques
- Validity threats acknowledged

### Stream 2: Technical Content
- Key algorithms/techniques
- Architecture/design patterns
- Performance characteristics
- Implementation details

### Stream 3: Evidence Assessment
- Sample sizes and statistical methods
- Baseline comparisons
- Reproducibility indicators
- Limitations stated

### Stream 4: Practical Applicability
- Industry relevance
- Implementation effort
- Prerequisites needed
- When to use/not use

---

## Output Format

### Quick Reference Card
| Field | Value |
|-------|-------|
| **Title** | [Paper title] |
| **Authors** | [Author list] |
| **Venue/Year** | [Publication, Year] |
| **Research Area** | [e.g., Distributed Systems, Testing] |
| **Paper Type** | Conference / Journal / Preprint |
| **Maturity Level** | Theoretical / Prototype / Lab-validated / Production-ready |
| **Evidence Strength** | Strong / Moderate / Weak |
| **Practical Value** | High / Medium / Low |
| **Read Recommendation** | Must Read / Skim / Skip |

---

### Executive Summary (3-5 sentences)
[Concise summary: What problem? What solution? What evidence? What's the practical takeaway?]

**Core Claim**: [One sentence thesis] `[§1]`
**Key Finding**: [Most important result] `[§X, Table Y]`
**Bottom Line**: [Should engineers care? Why/why not?]

---

### Paper Classification

#### Study Type
- [ ] Controlled experiment
- [ ] Case study
- [ ] Survey/Interview
- [ ] Empirical analysis
- [ ] System building
- [ ] Formal analysis/proof
- [ ] Literature review

#### Technology Maturity
- [ ] Theoretical concept
- [ ] Research prototype
- [ ] Lab-validated system
- [ ] Production-ready
- [ ] Industry-deployed

#### Reproducibility
| Aspect | Available | Quality |
|--------|-----------|---------|
| Source code | Yes/No/Partial | [Link if available] |
| Dataset | Yes/No/Partial | |
| Methodology detail | High/Med/Low | |

---

### Key Technical Contributions

| # | Contribution | Evidence Type | Validation | Novelty |
|---|--------------|---------------|------------|---------|
| 1 | [What's new] | `[PROVEN/EMPIRICAL/DEMONSTRATED/CLAIMED]` | [How validated] `[§X]` | [vs. prior work] |
| 2 | | | | |
| 3 | | | | |

**Evidence Level Tags**:
- `[PROVEN]` - Formally proven or rigorously validated
- `[EMPIRICAL]` - Supported by experimental data with statistics
- `[DEMONSTRATED]` - Shown via case study or prototype
- `[CLAIMED]` - Asserted without strong evidence
- `[SPECULATIVE]` - Forward-looking or hypothetical

---

### Methodology Assessment

#### Data & Sample
| Metric | Value | Assessment |
|--------|-------|------------|
| Sample size | N = [X] | Adequate / Marginal / Insufficient |
| Data source | [Industry/OSS/Synthetic] | Representative? |
| Time period | [Duration] | Current? |
| Selection method | [How chosen] | Biased? |

#### Statistical Rigor
| Aspect | Present | Notes |
|--------|---------|-------|
| Statistical tests | Yes/No | [Which tests] |
| P-values reported | Yes/No | [Significance level] |
| Effect sizes | Yes/No | [Practical significance] |
| Confidence intervals | Yes/No | |
| Multiple comparisons | Addressed/Not addressed | |

#### Threats to Validity
| Type | Acknowledged | Concerns |
|------|--------------|----------|
| Internal | [Author-stated `[§X]`] | [Your assessment] |
| External | [Author-stated] | [Generalizability concerns] |
| Construct | [Author-stated] | [Measurement issues] |

---

### Architectural Insights

#### Patterns & Principles
| Pattern/Principle | Description | When Applicable | Trade-offs |
|-------------------|-------------|-----------------|------------|
| [Pattern] | [What it is] | [Context] | [What you sacrifice] |

#### Performance Characteristics
| Metric | Reported Value | Conditions | Baseline Comparison |
|--------|----------------|------------|---------------------|
| [Metric] | [Value] `[Table X]` | [Setup] | [vs. alternative] |

#### Scalability
- **Tested scale**: [What was evaluated] `[§X]`
- **Theoretical limits**: [If discussed]
- **Bottlenecks**: [Identified limitations]

---

### Engineering Takeaways

| # | Takeaway | When to Use | When NOT to Use | Effort | Evidence |
|---|----------|-------------|-----------------|--------|----------|
| 1 | [Actionable insight] | [Conditions] | [Anti-patterns] | Low/Med/High | `[§X]` |
| 2 | | | | | |
| 3 | | | | | |

#### Implementation Checklist
For each major takeaway, what's needed:
- [ ] Prerequisites: [What you need first]
- [ ] Skills required: [Team capabilities]
- [ ] Estimated effort: [Time/resources]
- [ ] Expected outcome: [What you'll gain]

---

### Critical Analysis

#### Strengths
| Strength | Evidence | Confidence |
|----------|----------|------------|
| [What's good] | `[§X, Table Y]` | High/Med/Low |

#### Weaknesses
| Weakness | Impact | Severity |
|----------|--------|----------|
| [Methodological issue] | [How it affects conclusions] | High/Med/Low |
| [Evidence gap] | | |
| [Generalizability concern] | | |

#### Claims vs. Evidence Matrix
| Claim | Evidence Provided | Strength | Alternative Explanations |
|-------|-------------------|----------|--------------------------|
| [Major claim] | [Supporting data] | Strong/Mod/Weak | [Other possibilities] |

#### Bias Check
- [ ] Funding/conflicts disclosed?
- [ ] Selection bias in experiments?
- [ ] Only positive results shown?
- [ ] Cherry-picked examples?

---

### Comparison to Alternatives

| Approach | Pros | Cons | Best For | Maturity | Evidence |
|----------|------|------|----------|----------|----------|
| **This paper** | [Advantages] | [Disadvantages] | [Use case] | [Level] | [Quality] |
| Alternative 1 | | | | | |
| Alternative 2 | | | | | |

**Decision Guide**: When to choose this approach vs. alternatives?

---

### Industry Relevance

#### Adoption Timeline
| Timeframe | Applicability | Conditions | Risk |
|-----------|---------------|------------|------|
| **Now** (0-1 yr) | [What's usable today] | [Prerequisites] | Low/Med/High |
| **Soon** (1-3 yr) | [Emerging practices] | [What needs to mature] | |
| **Future** (3+ yr) | [Long-term implications] | [Paradigm shifts] | |

#### Best Fit
- **Organization type**: [Startup / Scale-up / Enterprise]
- **Team size**: [Small / Medium / Large]
- **Project type**: [Greenfield / Migration / Optimization]
- **Domain**: [Specific applicability]

---

### Open Questions

| Question | Type | Impact | Who Can Answer |
|----------|------|--------|----------------|
| [Unanswered question] | Technical/Practical | [What depends on this] | [Researchers/Industry] |

**Research Gaps**: [What follow-up work is needed]
**Practical Gaps**: [What's missing for real-world use]

---

### Watchlist

- **Follow-up papers**: [What to track]
- **Researchers**: [Key people in this area]
- **Projects/Tools**: [Related implementations]
- **Adoption signals**: [How to know if this goes mainstream]

---

### Final Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Methodological Rigor** | 1-5 | [Brief justification] |
| **Evidence Quality** | 1-5 | |
| **Practical Applicability** | 1-5 | |
| **Novelty** | 1-5 | |
| **Clarity** | 1-5 | |
| **OVERALL** | 1-5 | |

**Verdict**:
- [ ] **Must Read** - Significant, well-supported findings with immediate applicability
- [ ] **Worth Reading** - Useful insights, some limitations
- [ ] **Skim** - Interesting ideas, weak evidence or limited applicability
- [ ] **Skip** - Poor methodology or not relevant

**Confidence in Assessment**: High / Medium / Low
**Caveat**: [Any important limitations of this analysis]

---

## Analysis Guidelines

### Citation Standards
- Section: `[§3.2]`
- Table: `[Table 2]`
- Figure: `[Figure 4]`
- Inference: `[Inferred from §3.2: ...]`
- Interpretation: `[One interpretation: ...]`
- Gap: `[Not addressed in paper]`

### Evidence Assessment
Always distinguish:
- What is **proven** vs. **demonstrated** vs. **claimed**
- What is **statistically significant** vs. **practically significant**
- What **generalizes** vs. what is **context-specific**

### Objectivity
- Include both strengths AND weaknesses
- Don't extrapolate beyond what paper demonstrates
- Acknowledge uncertainty with confidence levels
- Consider alternative explanations

### Practical Focus
- Prioritize actionable insights over theoretical contributions
- Assess real-world applicability, not just academic novelty
- Consider cost/benefit from engineering perspective
- Identify prerequisites and barriers to adoption
