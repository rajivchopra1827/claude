# Posts Strategy: Greystar Decision Framework

*Prep for Greystar Strategy Session - Jan 28, 2026*

---

## TL;DR

Posts must transition from Zumper (~$3M ARR at risk by 2027) to direct revenue. Target: $1.2M ARR by EOY 2026.

**Three business models:**
- **Path A:** Agency Service (we operate it) - ~$360k ARR
- **Path B:** Standalone SaaS (they operate it) - B.1: ~$420k ARR, B.2: ???
- **Path C:** Enterprise Platform (Greystar white-label) - ~$720k ARR

**Reality:** No single path gets us to $1.2M ARR target by EOY.

**Key constraint:** Q1 on Zumper, limited resources (2 engineers, no PM/designer)

**Tomorrow's goal:** Choose which business model(s) to commit to for 2026.

---

## Context

**Current state:**
- Zumper partnership: ~$3M ARR (at risk by 2027)
- Serve ~3,000 properties through agency (~30% portfolio penetration)
- Total properties of our PMC clients: ~10,000
- Organic social penetration: 5.8% (171 properties at $468/prop avg)
- SEO penetration: 19.6% (578 properties at $5,459/prop avg)
- Greystar = ~1,000 of the 3,000 properties we serve

**Greystar interest:** 3-month pilot, white-label platform, strong relationship with Jamie (DCO/E)

**⚠️ Critical question:** Why is organic social penetration only 5.8%? Does Posts change this?

---

## Three Paths: Quick Comparison

| | Path A: Agency Service | Path B: Standalone SaaS | Path C: Enterprise Platform |
|---|---|---|---|
| **Customer** | ~3,000 props we serve | B.1: ~7,000 other props of PMCs<br>B.2: Broader market | Greystar (~2,000 props) |
| **What we sell** | Service (we operate) | Product (they use) | Platform (white-label) |
| **Distribution** | ✅ Agency upsell | B.1: ✅ Agency relationships<br>B.2: ❌ Cold market (ads, SEO, PLG) | ✅ Jamie relationship |
| **Revenue ceiling** | Limited (~3,000 props) | B.1: Medium (~7,000 props)<br>B.2: Large but uncertain | Capped ($720k/yr) |
| **Revenue potential** | Uncertain (5.8% penetration) | B.1: Depends on reach<br>B.2: Large if distribution works | $720k certain |
| **Timeline** | Shortest | B.1: Medium<br>B.2: Longest | Medium |

---

## Path A: Agency Service

**Vision:** We operate Posts for agency clients - they don't touch it.

**Target:** ~3,000 properties we currently serve

**Value prop:** "Digible handles it" - vendor consolidation + trust

**Economics:**
- Pricing: $40-60/prop/mo (bundled or add-on)
- Revenue: Unknown - depends on penetration
- **Key question:** Why is penetration only 5.8%? Will Posts change this?

**What we need to build:**
- Internal dashboard for team to manage properties
- Easy onboarding / data feed setup
- Data management tooling

**Operational requirements:**
- Shannon's team operates (no customer service needed)
- Requires Shannon buy-in and training

**Trade-offs:**
- ✅ Shortest timeline, validated channel, no customer service
- ⚠️ Revenue uncertain, limited ceiling (~3,000 props), service model, needs Shannon buy-in

---

## Path B: Standalone SaaS

**Vision:** Properties/PMCs buy and use the product themselves (not a service).

**Two distribution approaches:**

### B.1: Agency-Led Distribution

**Target:** ~7,000 other properties of PMCs we have relationships with
- We serve ~30% of our PMC clients' portfolios today (~3,000 of ~10,000)
- Remaining 70% = ~7,000 properties we could reach through relationships

**Distribution:** Leverage existing PMC relationships to sell to their other properties

**Economics:**
- Pricing: $40-60/prop/mo
- Revenue ceiling: ~7,000 properties (if we reach all of them)
- More realistic: Depends on what % we can actually reach

**Why B.1 first:** Easier distribution (warm relationships) + proves product works before cold market

---

### B.2: Cold Market Distribution

**Target:** SMB multifamily market (no relationship to us)

**Distribution:** Build from scratch - ads, SEO, content, PLG, partnerships
- Current reach: ≈ 0
- Would need significant investment ($100k-300k+)

**Economics:**
- Pricing: $40-60/prop/mo
- Market size: ~6M Class A multifamily properties exist
- **Realistic reach:** Unknown - Zumper currently serves ~3,000 properties with their sales team/GTM as benchmark
- Revenue: Distribution is the limiting factor, not market size

**Why B.2 later:** Hardest distribution problem, but largest upside if it works

---

### Path B: What We Need (Same for B.1 and B.2)

**Product requirements:**
- Customer-facing dashboard (self-serve product)
- Self-serve onboarding experience
- Billing management
- For B.2: Distribution engine (SEO, content, ads, PLG)

**Operational requirements:**
- Customer service/support team
- For B.2: Significant distribution investment

**Natural sequencing:** B.1 → B.2 (prove it with easier distribution first)

**Trade-offs:**
- ✅ B.1 has medium revenue ceiling, B.2 has unlimited ceiling
- ✅ Aligns with long-term product vision, best reputation/visibility
- ⚠️ Requires product + support infrastructure
- ❌ B.2 has longest timeline, hardest distribution

---

## Path C: Enterprise Platform (Greystar)

**Vision:** White-label platform for Greystar (and maybe Willowbridge?).

**Target:** Greystar (~2,000 properties - uncertain), strong Jamie (DCO/E) relationship

**Value prop:** White-label with governance, compliance, control

**Economics:**
- Pricing: $30/mo per property (enterprise volume discount)
- Revenue: ~2,000 × $30/mo = ~$720k ARR (property count uncertain)
- **Reality:** Essentially one customer (Willowbridge maybe?)
- **Revenue ceiling:** Capped at ~$720k

**What we need to build:**
- White-label capabilities (branding, custom domains)
- Governance layer (multiple access levels, permissions)
- Property-facing interface
- Central governance/compliance dashboard
- Compliance features (Fair Housing, etc.)

**Operational requirements:**
- Medium support/account management (white-glove for enterprise)
- Dedicated partnership/enterprise relationship management

**Trade-offs:**
- ✅ Best certain revenue ($720k), strong buyer relationship, medium timeline
- ❌ One-customer risk, revenue ceiling ($720k), worst reputation impact (no visibility), significant build complexity

---

## Path Comparison: Economics + Decision Filters

| Path | Revenue (ARR) | Ceiling | Confidence | Timeline | Culture | Reputation | Key Trade-off |
|------|---------------|---------|------------|----------|---------|------------|---------------|
| **Path A** | ~$360k | ~3k props | Medium | Shortest | Best | Decent | Capped + uncertain penetration |
| **Path B.1** | ~$420k | ~7k props | Low | Medium | Worst (?) | Best | Moderate ceiling, unproven |
| **Path B.2** | ??? | Large | Low | Longest | Worst (?) | Best | Distribution-limited, unproven |
| **Path C** | ~$720k | $720k | High | Medium | Mediocre | Worst | Certain but capped, one customer |

**Economics assumptions:**
- **Path A:** 3k props × 20% penetration × $50/mo (currently 5.8%)
- **Path B.1:** 7k props × 10% reach × $50/mo  
- **Path B.2:** ??? (6M MF props exist, Zumper serves ~3k as benchmark)
- **Path C:** ~2k props (uncertain) × 100% × $30/mo

**None of these paths alone gets us to $1.2M ARR target.**

**The choice:**
- **Path A:** Culture + collaboration, but capped + uncertain
- **Path B:** Reputation + long-term scale, but unproven
- **Path C:** Near-term revenue certainty, but capped + one customer risk

---

## Key Questions for Tomorrow

**The core problem:** No single path gets us to $1.2M ARR target by EOY.

**Strategic decisions:**
1. **What are we optimizing for?** Revenue? Certainty? Culture? Long-term scale?
2. **Do we need to combine paths?** (e.g., A + B.1, or A + C?)
3. **Path A:** Does Shannon see this as value-add or complication? Why is penetration 5.8%?
4. **Path B:** Why is this worst culturally? What's the actual concern?
5. **Path C (Greystar):** 
   - Are we okay with ~$720k ceiling and one-customer risk?
   - What do they actually need? How much work?
   - If we say "Q3/Q4," do we lose them?
6. **Decision:** Which path(s) do we commit to for 2026?

---

## Appendix: Key Data Points

**Properties:**
- Serve: ~3,000 (30% portfolio penetration)
- Total PMC portfolios: ~10,000
- Addressable for B.1: ~7,000
- Greystar: ~1,000 of the 3,000

**Current penetration:**
- Organic social: 171 (5.8%) at $468/prop avg
- SEO: 578 (19.6%) at $5,459/prop avg

**Benchmarks:**
- Zumper currently serves ~3,000 properties with full sales/GTM team
- Relevant for Path B.2 (cold market) realistic reach

**Path economics (ARR):**
- Path A: ~$360k ARR (20% penetration assumption), ceiling ~3,000 props
- Path B.1: ~$420k ARR (10% reach assumption), ceiling ~7,000 props
- Path B.2: Unknown (distribution-limited, Zumper ~3k benchmark)
- Path C: ~$720k ARR (certain, capped)
- **Target:** $1.2M ARR by EOY 2026 - no single path achieves this

**Resources:**
- 2 engineers + JD + part-time support
- No PM, no designer
- Q1 committed to Zumper negotiation
