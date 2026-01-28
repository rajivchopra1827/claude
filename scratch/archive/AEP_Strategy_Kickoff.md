# AEP Strategy Kickoff

**Date:** [Date of kickoff]  
**Purpose:** Align the team on AEP strategy, vision, and approach

---

## 🎯 Why We're Here

Digible is a 150-person bootstrapped digital marketing agency specializing in multifamily apartment marketing. The Agency Enablement Pod (AEP) is being refocused to build an **AI-native, human-assured paid media marketing system**.

### The Problem We're Solving

Platforms like Google and Meta offer automated optimizations, but they only see digital marketing signals. They can't see the multifamily-specific context that actually drives performance:
- Occupancy rates
- Pricing and availability
- Leasing velocity
- Offline lead quality
- Property-specific goals and constraints

### Our Strategic Bet

**Our differentiation comes from combining paid media optimization with multifamily-specific context and data that platforms can't see.** This allows us to optimize for performance in ways that generic automation cannot.

---

## 🧭 Mission & North Star

### Mission

**Help paid media campaign managers improve paid media performance and scale capacity through AI-led automation and recommendations, purpose-built for multifamily.**

### North Star: Confidence

**Confidence is the ultimate North Star** - confidence that our marketing works, confidence in our recommendations, confidence in our system's decisions, and client confidence in our capabilities.

Performance and efficiency are secondary metrics that contribute to building confidence.

- **Confidence**: Measured by [TBD - client confidence scores? campaign manager confidence? system confidence levels?]
  - Status: Metric under construction

- **Performance** (contributes to confidence): Measured by CPA (Cost Per Acquisition)
  - Directional goal: Reduce from ~$30 → ~$15
  - Status: Metric under construction

- **Efficiency** (enables confidence-building work): Measured by accounts per FTE
  - Directional goal: Increase from ~100 → ~300
  - Status: Needs alignment with DPH operations

### Why Confidence First?

Confidence drives everything: client retention, campaign manager effectiveness, and our ability to deliver strategic insights. Performance improvements and efficiency gains are means to building confidence, not ends in themselves.

**Goal**: Build confidence through better performance, strategic insights, and reliable operations, enabling campaign managers to spend less time reacting and more time shaping outcomes.

---

## 🔮 The Vision (1-2 Year Horizon)

An **AI agent that builds confidence** by actively optimizing paid media performance across channels, using multifamily-specific context to make recommendations and take action, with campaign managers focused on **judgment, oversight, and client context** rather than manual execution.

### What This Looks Like in Practice

- **Campaign managers start from insight and recommendation**, not raw data
- **The system surfaces**: What's happening, Why it's happening, What to do about it
- **AI handles** ongoing optimization and execution
- **Humans review, approve, and guide** decisions that require taste, context, or risk judgment

**Result**: Campaign managers and clients have **confidence** that marketing is working optimally, freeing paid media to spend less time reacting and more time **shaping outcomes**.

---

## 🔄 The System: OBSERVE → DECIDE → ACT

A continuous loop: the system **OBSERVEs** the world, **DECIDEs** what to do, **ACTs** on it, and then **OBSERVEs** again to see what happened. **Humans are in the loop at each stage.**

### OBSERVE

**Core question:** Can we get the data we need?

**Functions:**
- **Collect**: Gather initial data at setup or when new property onboards
- **Update**: Refresh dynamic data on schedule or trigger

**Domains:**
- Property data (static): amenities, location, building type
- Property state (dynamic): pricing, availability, concessions, occupancy
- Property goals: targets, constraints, priorities
- Performance data: impressions, clicks, conversions, cost
- Market context: competition, seasonality
- Optimization history: past actions taken, reasoning, outcomes

**What Humans See:**
- Internal: Review data collected, verify accuracy
- External: (Future)

---

### DECIDE

**Core question:** Can we figure out the right thing to do?

**Functions:**
- **Evaluate**: Given all current data, is there a meaningful gap? Should we act?
- **Recommend**: Propose specific, prioritized changes to close gaps
- **Incorporate Feedback**: Human reviews, approves/denies/adjusts; system learns

**Domains:**
- Structure: campaigns, ad groups
- Targeting: keywords, audiences, locations
- Copy: headlines, descriptions, creative
- Allocation: budget across channels, campaigns, over time

**What Humans See:**
- Internal: Review recommendations, Approve / Deny / Adjust
- External: (Future) See what we're recommending

---

### ACT

**Core question:** Can we make changes reliably?

**Functions:**
- **Execute**: Make the change in the platform, confirm it worked
- **Record**: Log what was done, why, and outcome; make visible internally and externally

**Domains:**
- Structure
- Targeting
- Copy
- Allocation

**What Humans See:**
- Internal: See actions taken, audit trail
- External: See what changed + reasoning

---

### The Loop

**ACT → Record** feeds back into **OBSERVE → Optimization history**, which **DECIDE → Evaluate** uses to:
- Avoid churn (don't act too frequently; let things bake)
- Learn from past actions (what worked, what didn't)
- Build confidence through transparent reasoning and outcomes

---

## 📈 System Evolution Over Time: Building Confidence

| Phase | OBSERVE | DECIDE | ACT | Confidence Level |
|-------|---------|--------|-----|-----------------|
| **Early** | Some manual data collection | Human approves every recommendation | Human may still execute some actions | **Low**: Testing hypotheses, building trust in system |
| **Mid** | Mostly automated data collection | Human approves most; some auto-approved | System executes; human monitors | **Growing**: System proving reliable, humans gaining confidence |
| **Mature** | Fully automated | Human handles exceptions only | Fully automated; human audits | **High**: System trusted, humans confident in recommendations and execution |

---

## 🧪 Our Approach: Phased Testing

We'll start with **lowest-risk, highest-signal** combinations and expand systematically.

### Phase 1: Allocation Domain Only

**Why start here?** Allocation is the lowest-risk domain (just changing numbers, reversible).

**What we'll test:**
- **OBSERVE**: Can we pull performance data reliably?
- **DECIDE**: Can we recommend budget shifts that improve CPA?
- **ACT**: Can we make budget changes via API and confirm they worked?
- **Confidence**: Do campaign managers trust these recommendations? Do they improve confidence in our system?

**Success criteria:** [To be defined]

---

### Phase 2: Add Targeting

**What we'll test:**
- **DECIDE**: Can we recommend better keywords/audiences?
- **ACT**: Can we add/remove keywords reliably?

**Success criteria:** [To be defined]

---

### Phase 3: Add Copy

**What we'll test:**
- **DECIDE**: Can we generate compliant copy that performs?
- **ACT**: Can we update ad copy (may require new ad versions)?

**Success criteria:** [To be defined]

---

### Phase 4: Add Structure

**What we'll test:**
- **DECIDE**: Can we recommend restructuring that helps?
- **ACT**: Can we execute multi-step structural changes without breaking things?

**Success criteria:** [To be defined]

---

## ⚠️ Highest-Risk Hypotheses (What We Need to Learn)

| Rank | Stage | Hypothesis | Why It's Risky |
|------|-------|------------|----------------|
| 1 | DECIDE | Allocation recommendations actually improve performance | Core value prop. If AI can't beat status quo, nothing else matters. |
| 2 | OBSERVE | We can integrate with PMS systems to get property state | Without this data, we're just optimizing on marketing signals like everyone else. |
| 3 | DECIDE | Playbooks cover enough of the variance in Structure | If every property is a snowflake, we can't systematize. |
| 4 | ACT | We can execute Structure changes without breaking things | Highest-risk domain for execution. |
| 5 | DECIDE | Generated Copy is compliant and performs | Compliance failures are catastrophic; poor copy undermines performance. |

---

## ❓ Open Questions (How We'll Resolve Them)

### 1. Confidence → Revenue Correlation

**Question:** How does confidence (from performance, insights, reliability) translate to client revenue/retention?

**Why it matters:** Confidence is our North Star, but we need to understand how it drives business outcomes. Previous EPD strategy work showed performance alone didn't drive retention/revenue. How does confidence change that?

**How we'll resolve:**
- [ ] Define confidence metrics and measurement approach
- [ ] Test hypothesis: "Increased confidence (from X, Y, Z sources) → Y% revenue increase"
- [ ] Track confidence-building activities and correlate with client outcomes

**Owner:** [TBD]  
**Timeline:** [TBD]

---

### 2. DPH Overlap & Capacity

**Question:** To what degree can Digital Philippines handle L1 work, freeing this team to focus on performance?

**Why it matters:** Efficiency targets (accounts per FTE) depend on DPH capacity. Need clarity on what work can be offloaded.

**How we'll resolve:**
- [ ] Map current L1 work and identify what DPH can handle
- [ ] Test DPH capacity in Q1
- [ ] Define handoff process and success criteria

**Owner:** [TBD - Taylor?]  
**Timeline:** Q1 2026

---

### 3. Foundational Stability

**Question:** Are existing systems (automated account launches, templates, QAS) stable enough to build on top of?

**Why it matters:** Jenny noted fundamental product stability issues that prevent getting to "Level 3" work. Can't build transformative capabilities on shaky foundation.

**How we'll resolve:**
- [ ] Audit current system stability
- [ ] Define minimum stability requirements for Phase 1
- [ ] Create "Phase 0" if needed to address critical stability issues

**Owner:** [TBD]  
**Timeline:** Before Phase 1 begins

---

### 4. Confidence Metric Definition

**Question:** How do we measure confidence? What are the right metrics for campaign manager confidence, client confidence, and system confidence?

**Why it matters:** Confidence is our North Star, but we need to define how we measure it before we can track progress.

**How we'll resolve:**
- [ ] Define confidence metrics (campaign manager confidence, client confidence, system confidence)
- [ ] Validate CPA and Accounts per FTE as contributing metrics
- [ ] Align Accounts per FTE calculation with DPH operations (Taylor)
- [ ] Define measurement approach and baseline

**Owner:** [TBD]  
**Timeline:** Before Phase 1 begins

---

### 5. Sustain vs. Build Trade-offs

**Question:** What level of investment is needed to sustain existing products (AdOptimizer, QAS, etc.) vs. building new transformative capabilities?

**Why it matters:** Jenny raised tension: sustaining products with stability issues may conflict with building new capabilities that shift how work is done.

**How we'll resolve:**
- [ ] Define decision framework: When to sustain vs. rebuild vs. build new
- [ ] Assess current product portfolio
- [ ] Make explicit trade-off decisions

**Owner:** [TBD]  
**Timeline:** [TBD]

---

## 🎯 Scope: What's In vs. Out

### In Scope

**Invest (Heavy Investment):**
- Optimizations (broad bucket)
- Budget and bidding

**Sustain (Maintain Current State):**
- AdOptimizer (part of budget/bidding)
- Automated account launches
- Optimization notes
- QAS (Quotation Assurance System)

### Out of Scope

- Client services
- Organic marketing
- Admin work for paid media that's purely capacity-saving (vs. necessary for optimizations)

---

## 📋 Immediate Next Steps

### Before Broader Kickoff

- [ ] **Megan**: Create one-pager outlining key assumptions and multiple roadmap paths
- [ ] **Team**: Test critical assumptions in Q1 (DPH L1 capacity, onboarding readiness for AI)
- [ ] **Jenny**: Identify PMT team members for collaboration (detail-oriented, big picture thinkers)
- [ ] **All**: Working session with ground-level team once assumptions documented

### Q1 2026

- [ ] Define Phase 1 success criteria (including confidence metrics)
- [ ] Set up measurement infrastructure for confidence, CPA, and Accounts per FTE
- [ ] Begin Phase 1 testing (Allocation domain)
- [ ] Resolve foundational stability questions
- [ ] Test DPH capacity for L1 work

### Ongoing

- [ ] Address team renaming/rebranding over next 1-2 months (coordinate with agency roundup timing)
- [ ] Regular check-ins on hypothesis testing
- [ ] Update this document as we learn

---

## 💬 Questions & Feedback

**Please add your questions, concerns, or feedback below. Use +1 to vote on questions you'd like to discuss.**

### Questions from Team

[Add questions here - format: Question text +1]

### Sentiment Check-in

**How are you feeling about this strategy?**

- [ ] Excited and ready to go
- [ ] Cautiously optimistic
- [ ] Have concerns but willing to try
- [ ] Need more clarity before feeling confident
- [ ] Other: [your thoughts]

---

## 📚 Reference: Inputs & Outputs

### Inputs (What the System Needs to Know)

**Hit the goals of the property:**
- Leasing Status (stabilized, lease-up, etc.)
- Goals of property (occupancy targets, target dates, etc.)
- Historical Context (what's worked vs not)
- Performance (marketing & MFH metrics, velocity & cost metrics, lead quality, tracking)

**Value to customers:**
- Who are your customers? (Building type, target market)
- What value are you offering? (Property amenities, apartment amenities, pricing, availability, location)

**Differentiation in the market:**
- Competition (pricing, saturation, comparative value)
- Macro factors (seasonality, market trends)
- Reputation (complaints, etc.)

### Outputs (Decisions the System Makes)

**Change where $ goes:**
- To improve performance: Spend across channels, spend within channels
- To stay within budget: Spend over time (pacing)

**Change how the marketing is done:**
- Campaign structure
- Keyword targeting
- Audience targeting
- Location targeting
- Creative (ad copy, media)

---

## 🚫 Anti-Patterns (What We're Avoiding)

- **Performance-first thinking**: Focusing on metrics without building confidence
- **Efficiency-first thinking**: Automating current workflows instead of reimagining operations
- **Building without testing**: Investing in high-risk domains before validating core hypotheses
- **Ignoring foundational stability**: Building on shaky systems that prevent progress
- **Skipping human-in-the-loop**: Fully automating before humans can validate and guide
- **Optimizing in isolation**: Focusing on marketing signals without multifamily context

---

## 📞 How We'll Work Together

### Communication

- **Regular updates**: [Define cadence - weekly? bi-weekly?]
- **Channel**: [Slack channel? Notion updates?]
- **Feedback loops**: This document is living - add questions, concerns, ideas anytime

### Decision-Making

- **Phase gates**: Each phase has success criteria before moving to next
- **Hypothesis testing**: We test riskiest assumptions first
- **Data-driven**: Decisions based on what we learn, not just opinions

### Collaboration

- **Cross-functional**: DPH, PMT, Operations all involved
- **Ground-level input**: Working sessions with people doing the work
- **Transparent**: Share learnings, failures, and wins openly

---

**Last Updated:** [Date]  
**Next Review:** [Date]
