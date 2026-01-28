# A/B Testing

## Purpose

A/B testing allows teams to compare two or more variants of a product experience to determine which performs better against a specific metric. It provides statistical evidence for product decisions rather than relying on intuition or opinions.

## When to Use

- When you have multiple solution options and need to choose the best one
- To validate hypotheses about what will improve a metric
- When you need quantitative evidence for a product decision
- For optimizing existing features (conversion rates, engagement, etc.)
- When you have enough traffic/users to achieve statistical significance

## Key Components/Steps

### Test Planning

1. **Define Hypothesis**: State what you're testing and expected outcome
2. **Identify Metric**: Choose the primary metric to measure (and guardrail metrics)
3. **Design Variants**: Create the different versions to test
4. **Determine Sample Size**: Calculate how many users needed for statistical significance
5. **Set Duration**: Determine how long to run the test

### Test Execution

6. **Launch Test**: Deploy variants to user segments
7. **Monitor**: Watch for anomalies or issues
8. **Collect Data**: Gather results over the test period

### Analysis

9. **Analyze Results**: Compare variants against metrics
10. **Check Significance**: Determine if results are statistically significant
11. **Make Decision**: Choose winning variant or iterate

## Key Principles

- **One variable**: Test one change at a time to understand causality
- **Statistical significance**: Ensure results aren't due to chance
- **Guardrail metrics**: Monitor secondary metrics to avoid unintended consequences
- **Sample size matters**: Need enough users to detect meaningful differences
- **Duration matters**: Run long enough to account for day-of-week effects

## Common Pitfalls

- Testing too many variables at once (can't determine what caused the result)
- Stopping tests too early (not reaching statistical significance)
- Ignoring guardrail metrics (winning on primary metric but hurting others)
- Testing when you don't have enough traffic (results won't be reliable)
- Treating A/B testing as the only validation method (combine with qualitative research)

## Related Frameworks

- **Assumption Mapping**: A/B tests validate assumptions
- **Analytics**: A/B test results feed into analytics dashboards
- **Opportunity Solution Trees**: Tests help prioritize solutions
- **Continuous Discovery**: A/B testing is one tool in continuous validation

## Example Use Cases

- **Conversion Optimization**: Test different checkout button colors, copy, or layouts to improve conversion rate.
- **Feature Adoption**: Test different onboarding flows to see which leads to higher feature discovery.
- **Messaging**: Test different value propositions to see which resonates better with users.
