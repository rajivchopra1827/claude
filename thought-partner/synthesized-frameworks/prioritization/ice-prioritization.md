# ICE Prioritization with Confidence Meter

## Purpose

ICE Prioritization with Confidence Meter helps teams prioritize product ideas by scoring them on Impact, Confidence, and Ease, while explicitly tracking how confident you are in those estimates. This prevents teams from making big bets on ideas with low confidence and helps focus validation efforts where they matter most.

## When to Use

- When you have multiple product ideas or features to prioritize
- To avoid making decisions based on weak signals (opinions, trends, HIPPO)
- When you need to justify prioritization decisions with evidence
- To identify which ideas need more validation before building
- For ongoing prioritization as you gather more evidence

## Key Components/Steps

### ICE Score Calculation

**ICE Score = Impact × Confidence × Ease**

1. **Impact** (1-10): Estimate how much the idea will positively affect your key metric
2. **Confidence** (0-10): How sure you are about the Impact estimate (and to some degree, Ease)
3. **Ease** (1-10): Inverse of effort - how easy/quick it is to implement (lower effort = higher ease)

### Confidence Meter

The Confidence Meter assigns confidence values based on types of evidence:

- **Near Zero (0.1)**: Self conviction, thematic support, others' opinions
- **Low (0.5)**: Anecdotal support (customers asked for it)
- **Low-Medium (0.8-1.5)**: Estimates & plans, market data (surveys)
- **Medium (2-3)**: Qualitative research (user studies, interviews)
- **Medium-High (3-6.5)**: MVP results, quantitative validation
- **High (7+)**: Production data, proven results

### Incremental Validation Process

1. **Round 1**: Initial ICE scores based on intuition
2. **Round 2**: Get engineering estimates, refine impact estimates
3. **Round 3**: Gather market data (surveys, analytics)
4. **Round 4**: Conduct user research (interviews, usability studies)
5. **Round 5**: Build and test MVPs to validate with real usage

## Key Principles

- **Confidence matters**: High impact + low confidence = risky bet. Test to increase confidence before building.
- **Evidence-based**: Confidence comes from evidence, not opinions. Use the Confidence Meter to be honest about what you know.
- **Incremental validation**: Start with low-investment tests and increase investment as confidence grows.
- **Relative scoring**: Use consistent 1-10 scales across ideas for fair comparison.
- **Continuous refinement**: Update ICE scores as you gather more evidence.

## Common Pitfalls

- Making decisions with low confidence scores (high risk)
- Treating opinions as evidence (they're near-zero confidence)
- Not updating scores as you learn (scores should evolve)
- Over-investing in ideas before validating (build MVPs first)
- Ignoring confidence and only looking at impact/ease

## Related Frameworks

- **Opportunity Solution Trees**: Use ICE to prioritize opportunities and solutions within the tree
- **Assumption Mapping**: ICE confidence aligns with assumption validation
- **A/B Testing**: One way to increase confidence through quantitative validation
- **GIST Framework**: ICE fits into the Ideas phase of GIST

## Example Use Cases

- **Feature Prioritization**: Dashboard idea has Impact=5, Ease=4, Confidence=0.5 (low - only anecdotal support). Chatbot has Impact=8, Ease=2, Confidence=0.1 (near zero - just opinions). Dashboard wins initially, but both need more validation.
- **After MVP Testing**: Dashboard MVP shows Impact=8, Ease=4, Confidence=6.5 (medium-high - proven with users). Chatbot shows Impact=2, Ease=1, Confidence=0.5 (low - MVP revealed issues). Dashboard clearly wins.
