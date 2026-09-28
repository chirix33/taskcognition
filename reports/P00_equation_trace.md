# P00 equation-to-code trace

Evidence kind: `fixture`. No theorem, power, or empirical comparison verified here.

The governing PDF was read across all 12 pages with text extraction; pages 2 and 5
were also rendered and visually inspected for equation structure. The initial console
extraction failed under cp1252; `-X utf8` resolved it. Original TeX equations were
read and checked against the PDF and supplied operational contracts.

| Contract / PDF | Implementation | Independent expected example |
|---|---|---|
| S in [0,1], Y=1{S=1}, p_hat mean Y / p.2 | `contracts.DrawRecord`, `targets.aggregate` | A near-one score is not perfect; partial .75 contributes .75 to mean and 0 to Y. |
| T_b = mean R - mean D / p.3 | `targets.aggregate` | K=4 means .5 - .75 = -.25. |
| T_h = p_D (1-p_R) / p.2 | `targets.aggregate` | .75 * .5 = .375. |
| h_DD = K/(K-1) p_D(1-p_D) / p.2 | `targets.aggregate` | (4/3)*(.75)*(.25) = .25. |
| d_epsilon = cross-pair decline fraction / p.2 | `targets.aggregate` | 3 direct successes * 2 reasoning failures / 16 = .375 at both .10 and .25. |
| W=1{mean R > mean D} / p.5 | `targets.aggregate` | Exact ties choose D; all-perfect example has W=0. |

Six copies of the same fixed score example are tagged with the six approved family
names solely to test fixture organization. They are not samples from Reasoning Gym.
The fixture report gives six input clusters and 16 overlapping pairs per cluster;
it never calls the pairs independent observations or calculates confidence bounds.
RNG identifiers distinguish input, split, package and draw, but P00 performs no
stochastic model sampling and cannot empirically establish conditional independence.

Tests cover incomplete/corrupt evidence, duplicate IDs, reused streams, exact perfect
correctness, partial scores, failure retention, input-only feature allowlists, split
boundaries, overwrite refusal, restart verification, and fixture/final path isolation.
Real native FINAL parsing, request admission, time/cost enforcement, balanced-audit
rules, empirical-Bernstein assumptions/constants, ratio conventions and bootstrap
coverage remain for their authorized phases. No production parser is claimed by P00.
