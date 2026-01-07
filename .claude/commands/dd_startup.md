# Startup Evaluation Request - Job Seeker Due Diligence
# Usage: Evaluate a startup for job seekers: <COMPANY_NAME> [COMPANY_WEBSITE]

# Parse inputs
Set COMPANY_NAME to first argument from $Arguments
Set COMPANY_WEBSITE to second argument from $Arguments (optional)
Validate that COMPANY_NAME is provided, otherwise error "Please provide the company name to evaluate"

## Objective
Provide a comprehensive due diligence analysis of the specified startup from a job seeker's risk/opportunity perspective, helping them make an informed career decision.

---

## Phase 1: Data Collection (Execute in Parallel)

### Group 1: Company Fundamentals
Fetch from these sources simultaneously:
- **Company Website**: Product info, team page, careers, blog, press releases
- **Crunchbase**: Funding rounds, investors, team, acquisitions
- **LinkedIn Company Page**: Employee count, growth trends, job postings

### Group 2: Financial & Investor Data
- **Crunchbase/PitchBook**: All funding rounds, valuations, investors
- **News Sources**: Recent funding announcements, financial news
- **SEC Filings**: If any public filings available (Form D, etc.)

### Group 3: Leadership & Culture
- **LinkedIn**: Founder profiles, leadership team backgrounds
- **Twitter/X**: Founder activity, communication style
- **Glassdoor/Blind**: Employee reviews, ratings, interview experiences
- **GitHub/Tech Blogs**: Technical culture indicators (if applicable)

### Group 4: Market & Product
- **G2/Capterra**: Product reviews (if B2B SaaS)
- **App Store/Play Store**: App reviews (if consumer app)
- **News/TechCrunch**: Product announcements, pivots, market positioning
- **Competitors**: Who else is in this space?

---

## Phase 2: Analysis Framework

### 1. FINANCIAL STABILITY & FUNDING (Weight: 30%)

#### Data to Extract
| Metric | Value | Source | Confidence |
|--------|-------|--------|------------|
| Total Raised | $[X]M | Crunchbase | High/Med/Low |
| Last Round | Series [X], $[X]M | [Source] | |
| Last Round Date | [Date] | | |
| Key Investors | [Names] | | |
| Valuation (if known) | $[X]M | | |
| Employee Count | [X] | LinkedIn | |
| Burn Rate (estimated) | $[X]M/month | Calculated | |
| Runway (estimated) | [X] months | Calculated | |

#### Scoring Rubric
| Factor | Score 1-5 | Weight |
|--------|-----------|--------|
| Runway > 18 months | | 25% |
| Top-tier investors | | 25% |
| Recent funding (< 12 months) | | 20% |
| No layoff history | | 15% |
| Revenue signals | | 15% |

**Financial Risk Score**: [X]/5
**Employment Stability**: LOW / MEDIUM / HIGH RISK

#### Red Flags to Check
- [ ] Layoffs in past 24 months
- [ ] Down round or flat round
- [ ] > 18 months since last funding
- [ ] Unknown/non-institutional investors
- [ ] Founder departures

#### Green Flags to Check
- [ ] Top-tier VCs (a16z, Sequoia, Accel, etc.)
- [ ] Recent funding with valuation increase
- [ ] Path to profitability visible
- [ ] Strong investor follow-on participation

---

### 2. FOUNDERS & LEADERSHIP (Weight: 25%)

#### Leadership Profile
| Person | Role | Background | Previous Exits | LinkedIn |
|--------|------|------------|----------------|----------|
| [Name] | CEO | [Summary] | [Yes/No - details] | [URL] |
| [Name] | CTO | [Summary] | | |

#### Scoring Rubric
| Factor | Score 1-5 | Weight |
|--------|-----------|--------|
| Relevant domain expertise | | 30% |
| Previous startup success | | 25% |
| Team completeness | | 20% |
| Industry reputation | | 15% |
| Communication/transparency | | 10% |

**Leadership Score**: [X]/5

#### Culture Indicators
| Source | Rating | Key Themes | Sample Size |
|--------|--------|------------|-------------|
| Glassdoor | [X]/5 | [themes] | [n] reviews |
| Blind | [X]/5 | [themes] | [n] reviews |
| LinkedIn Comments | | [themes] | |

---

### 3. PRODUCT-MARKET FIT (Weight: 25%)

#### Product Summary
| Aspect | Assessment |
|--------|------------|
| **What they do** | [One sentence] |
| **Target customer** | [Profile] |
| **Problem solved** | [Pain point] |
| **Differentiation** | [Unique value] |
| **Business model** | [How they make money] |

#### Market Analysis
| Factor | Assessment | Source |
|--------|------------|--------|
| TAM (Total Addressable Market) | $[X]B | |
| Market growth rate | [X]% CAGR | |
| Key competitors | [List] | |
| Competitive moat | [Weak/Medium/Strong] | |

#### Traction Evidence
| Signal | Evidence | Strength |
|--------|----------|----------|
| Customer logos | [Names] | Strong/Weak |
| Revenue indicators | [Any public info] | |
| User growth | [If available] | |
| Product reviews | [Rating, count] | |
| Case studies | [Yes/No] | |

#### PMF Scoring Rubric
| Factor | Score 1-5 | Weight |
|--------|-----------|--------|
| Clear value proposition | | 25% |
| Evidence of traction | | 30% |
| Market timing | | 20% |
| Competitive position | | 25% |

**Product-Market Fit Score**: [X]/5
**PMF Stage**: Pre-PMF / Finding PMF / Strong PMF

---

### 4. CAREER OPPORTUNITY (Weight: 20%)

#### Growth Potential
| Factor | Assessment |
|--------|------------|
| Company growth trajectory | [Accelerating/Stable/Slowing] |
| Role scope potential | [High/Medium/Low] |
| Learning opportunities | [List areas] |
| Network value | [Investor/advisor quality] |
| Resume impact | [Strong/Medium/Weak brand] |

#### Exit Scenarios (3-5 year horizon)
| Scenario | Probability | Your Outcome |
|----------|-------------|--------------|
| IPO | [Low/Med/High] | [Equity value estimate] |
| Acquisition | [Low/Med/High] | [Likely outcome] |
| Continued growth | [Low/Med/High] | [Career trajectory] |
| Failure/shutdown | [Low/Med/High] | [Risk mitigation] |

#### Compensation Assessment
| Factor | Assessment |
|--------|------------|
| Base salary competitiveness | [Above/At/Below market] |
| Equity value (realistic) | [$ range estimate] |
| Total comp vs. alternatives | [Compare to FAANG/other startups] |

**Career Opportunity Score**: [X]/5

---

## Phase 3: Output Report

### Executive Summary
| Field | Value |
|-------|-------|
| **Company** | [Name] |
| **Stage** | [Seed/Series A/B/C/etc.] |
| **Overall Rating** | [X]/10 |
| **Recommendation** | STRONG CONSIDER / PROCEED WITH CAUTION / AVOID |
| **Confidence Level** | High / Medium / Low |

[2-3 paragraph summary of key findings and recommendation rationale]

---

### Composite Scorecard
| Category | Score (1-5) | Weight | Weighted Score |
|----------|-------------|--------|----------------|
| Financial Stability | [X] | 30% | [X] |
| Leadership & Team | [X] | 25% | [X] |
| Product-Market Fit | [X] | 25% | [X] |
| Career Opportunity | [X] | 20% | [X] |
| **TOTAL** | | 100% | **[X]/5** |

---

### Risk Matrix
| Risk Category | Level | Key Factors | Mitigation |
|---------------|-------|-------------|------------|
| Financial | [1-5] | [Factors] | [What to negotiate/ask] |
| Leadership | [1-5] | [Factors] | |
| Product/Market | [1-5] | [Factors] | |
| Career | [1-5] | [Factors] | |

---

### SWOT Analysis
| Strengths | Weaknesses |
|-----------|------------|
| - [Point] | - [Point] |
| - [Point] | - [Point] |

| Opportunities | Threats |
|---------------|---------|
| - [Point] | - [Point] |
| - [Point] | - [Point] |

---

### Interview Questions to Ask
Based on identified gaps and concerns, ask these specific questions:

#### Financial Health
1. "What's your current runway, and what are the plans for the next funding round?"
2. "Can you share the company's path to profitability?"

#### Leadership & Culture
3. "How has the leadership team evolved, and what key hires are planned?"
4. "What's the typical career progression for someone in this role?"

#### Product & Market
5. "What are your key metrics, and how have they trended over the past 12 months?"
6. "Who do you see as your main competitors, and what's your differentiation?"

#### Role-Specific
7. "[Based on specific concerns about the role]"
8. "[Based on specific concerns about the role]"

---

### Final Recommendation

**Overall Rating**: [X]/10

**Best For**:
- [Type of candidate who would thrive here]
- [Career stage that fits]
- [Risk tolerance level]

**Avoid If**:
- [Deal-breaker scenarios]
- [Risk factors that matter most]

**Negotiation Leverage**:
- [What to ask for given the risk profile]
- [Equity considerations]

**Decision Factors**:
- Key positive: [What could make this great]
- Key negative: [What could make this fail]
- Tiebreaker: [What additional info would help decide]

---

### Data Confidence & Limitations
| Data Category | Confidence | Notes |
|---------------|------------|-------|
| Funding data | High/Med/Low | [Source quality] |
| Team info | High/Med/Low | |
| Traction data | High/Med/Low | |
| Culture data | High/Med/Low | [Sample size] |

**Information Gaps**: [List what couldn't be verified]

---

## Analysis Guidelines
- Be objective and data-driven; cite sources
- Clearly distinguish facts vs. estimates vs. speculation
- Acknowledge information gaps honestly
- Compare to industry benchmarks where possible
- Remember: This is someone's career decision—be thorough and honest
- Update assessment if given additional information
