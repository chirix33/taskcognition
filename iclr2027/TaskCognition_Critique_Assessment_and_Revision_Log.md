# TaskCognition Major Revision Log

## Revision status

This revision is a **pre-results protocol manuscript**. No TaskCognition experiment, power study, feasibility run, held-out audit, test, or comparator evaluation was performed. The project originals were not overwritten. The revised temporary manuscript remains anonymous, uses the ICLR 2027 style, and retains the exact title **“TaskCognition: When Does Overuse of Reasoning Models Degrade Answer Performance?”**

The revised system still contains **exactly two inference packages**—direct D and bounded native-thinking R—plus **exactly one input-only pre-generation gate** and **exactly one deployed answer call**. No tool, agent, checkpoint, third answer policy, post-generation router, or automatic direct recovery after R failure was added.

## Point-by-point accepted revisions

| Critique item | Decision and reader-facing reason | Manuscript location |
|---|---|---|
| Contribution and scope | **Accepted.** The paper now presents its novelty as an empirical question: whether direct-relative paired benefit plus independent-draw perfect-to-imperfect supervision improves constrained deployment over same-resource winner and factorized outcome routers. This is the narrow claim the eventual data can actually adjudicate. The audit is identified as a deployment safeguard rather than new statistics. “Overuse” is defined as policy-relative routing to R when the declared objective would prefer D. | Abstract; §1 Introduction; §2 Related Work; §10 Limitations and Conclusion |
| Object of study and causal language | **Accepted.** The revision consistently describes D and R as named package distributions on one checkpoint. It rejects causal-switch and latent-cognition interpretations because independent package draws cannot identify what reasoning “caused” inside one answer. | §1 Scope; §3 Estimands; §5 Exactly two packages; §10 Limitations |
| Independent-draw spoilage | **Accepted with clarification.** Independent copies are explicit, and `h_ind=p_D(1-p_R)` is named package-relative independent-draw perfect-to-imperfect spoilage. It remains the primary risk because it asks the prespecified absolute safety question; it is not same-seed flipping. | §3, Eqs. (2)–(3) |
| Direct–direct redraw reference | **Accepted as descriptive only.** The revision adds `h_DD`, `R_DD`, and `Delta_DD` to expose ordinary stochastic disagreement under D. It does not replace absolute cross-package spoilage because doing so would answer a different and weaker safety question. | §3, Eq. (4); Tables 1 and Appendix discussion |
| Finite-K estimators and dependence | **Accepted.** The manuscript gives `p_hat`, `h_hat_ind`, the unbiased distinct-direct-draw estimator `K/(K-1)p_hat_D(1-p_hat_D)`, and the cross-product `d_hat_epsilon`. It states that overlapping pair cells are dependent and that the complete input is the inferential cluster. This prevents false K-squared sample-size claims. | §3, Eqs. (6)–(7) |
| Partial-credit degradation | **Accepted.** `d_epsilon` is defined with independent package copies and epsilon values 0.10 and 0.25, with all-input and routed-subset aggregation planned. It remains descriptive so it does not silently alter the registered spoilage constraint. | §3, Eq. (5); §10; Appendix B |
| Benefit loss | **Accepted.** The primary loss is squared error on `T_b=mean(S_R)-mean(S_D)`, which targets the conditional mean used by the decision rule. Huber is sensitivity-only because it need not elicit that mean outside its quadratic region. | §4 TaskCognition and Learning Targets |
| Harm loss | **Accepted.** One soft-label log loss is used per input for `T_h=p_hat_D(1-p_hat_R)`. Only outcome-independent frozen weights are allowed. This preserves the probability target and explicitly does not turn reused cross-products into independent examples. | §4, Eq. (10) |
| Local q threshold | **Accepted with restricted interpretation.** The two-threshold gate remains because it is the intended simple policy family. The text now says q is a local joint-harm screen, not pointwise conditional spoilage and not proof of global optimization. | §4, Eq. (11) and following paragraph |
| Factorized baseline | **Accepted.** The incomplete absolute score/cost router is replaced with an equally resourced factorized outcome router predicting `p_D`, `p_R`, `mu_D`, and `mu_R`, then forming the same benefit and harm quantities. Cost prediction appears only if a declared decision rule uses it. The paper expressly claims no informational advantage, only a possible finite-data, calibration, or shift advantage. | §6 Equally resourced learned comparators, Eq. (12) |
| Winner baseline and learned-method fairness | **Accepted.** Winner ties go to direct. Winner, factorized, and TaskCognition receive matched information, features, total capacity, search, calibration, threshold family, tuning objective, family weights, accounting, one tune-frozen candidate, identical audit, and their own direct fallback. | §6; §7; Tables 1–2 |
| Cascades | **Accepted as a scope correction.** Cascades were removed from the primary table. The appendix gives only a future preview-conditional estimand and requires full preview/escalation charging. This prevents comparing policies that observe different information under one risk definition. | §2 Cascades and risk control; §6; Appendix B |
| Development before final labels | **Accepted.** DEVELOPMENT is now a separate, disjoint stage that validates modes, templates, parser, retries, timeout handling, throughput, cost, cap, and sample design. It contributes no final rollout labels. Changing a package after freeze invalidates all rollout-derived labels. | Figure 1; §5; Appendix A.1 |
| Cellwise cap rule | **Accepted.** Cap 1,024 is allowed only if every mode-by-family strict-valid-FINAL cell is at least 99%; otherwise 2,048 is allowed only if every cell reaches 99%; otherwise the bounded confirmatory package is infeasible and the study stops. Larger caps remain development diagnostics. This avoids choosing a package after seeing training outcomes. | §5 Development before labels; Figure 1 |
| Qwen sampling | **Accepted.** The controlled primary uses temperature 0.6, top-p 0.95, top-k 20, and min-p 0 for both modes. Mode-recommended settings are sensitivities only; recommended long caps are not called primary. | §5 Exactly two packages |
| Parser order | **Accepted.** The exact sequence is native-think channelization, strict FINAL validation on the final channel, then version-pinned native adapter/scorer. Trace-contained FINAL-like text is nonauthoritative. | §5 Parser, retry, and failure contract |
| Retry, timeout, and failure behavior | **Accepted.** Every draw has one admitted answer generation. Retry is pre-admission only, all dispatched attempts are charged, unknown admission counts as admitted, admitted missing/timeout failures score zero, and R failure never invokes D. This preserves the two-package, one-call action space. | §5 Parser, retry, and failure contract |
| Fixed-family estimand | **Accepted.** `E_w` is defined as the equal 1/6 average over six families and is required for every tuning, audit, and primary test quantity. This makes the finite-family target explicit. | §3, Eq. (1); §§6–9 |
| Common budget | **Accepted.** The exogenous budget is `c_D^ref + 1/2(c_R^ref-c_D^ref)`, based on development reference charges and frozen before tuning. A method’s gate cannot inflate its own budget. | §3, Eq. (9) |
| One scalar ledger | **Accepted.** The manuscript requires either a monetary token/call schedule or hardware service time as the scalar constraint, not both for the same work. Calls, tokens, and latency remain separate reports. | §3 after Eq. (9); §5 Development |
| Held-out audit | **Accepted with validated replacement.** The old percentile-bootstrap decision and the initial symmetric-Hoeffding proposal are replaced by the finite-sample empirical-Bernstein audit specified in the task. Each of six families supplies equal `n_f=n/6` independent complete clusters. Rows B, Z, Delta, and C, sample variances, ranges, and the exact radius are defined. | §7, Eqs. (13)–(15) |
| Four-way pass rule | **Accepted.** Deployment requires spoilage `U_Z<=0`, common-budget `U_C<=beta`, denominator `L_B>=b_min>0`, and score `L_Delta>=0`. The score condition is noninferiority; superiority is reserved for test. | §7, Eq. (15) |
| Audit interpretation | **Accepted.** The rule is called a level-gamma intersection–union pass rule for one frozen candidate under independent clusters. No Bonferroni correction is used for this conjunctive decision, and the component bounds are not sold as a joint confidence region. The manuscript explicitly rejects conformal, pointwise, distribution-free, and shift-guarantee descriptions. | §7 following Eq. (15) |
| Denominator adequacy | **Accepted.** The false label “100 effective direct-correct instances” is removed. Reports now separate selected inputs, weighted routing, B and its lower bound, raw nested direct successes, and Kish weight concentration. | §7 final paragraph; Appendix Table 4 |
| Power and feasibility planning | **Accepted.** A disjoint high-repeat development pool and full TRAIN→TUNE→AUDIT→TEST simulation must choose balanced n, b_min, K, alpha/beta feasibility, and planning power before final labels. Required outputs include enablement, false enablement, fallback, bound widths, and conditional/unconditional test power. The example counts are clearly placeholders, not results. | §8 Primary Test, Planning, and Reporting; Appendix Table 3 |
| Primary test and contribution alignment | **Accepted.** The confirmatory universe is the six original-renderer Reasoning Gym families with equal weights. The paper requires one-sided family-stratified paired input-cluster bootstrap lower bounds above frozen `delta_score` against always-direct, winner deployment, and factorized deployment. Each learned baseline is its own audit-selected deployment. No exact sign-flip claim remains. | §8, Eq. (16); Table 1 |
| Renderer handling | **Accepted.** A renderer comparison is paired only through a shared latent problem ID; otherwise variants are unpaired fixed-case descriptions with no renderer-effect attribution. | §6 Splits and provisional counts; §10; Appendix B |
| External diagnostic | **Accepted.** The diagnostic remains independently generated and new. Generator/version and construct-validation criteria freeze before final generation; validation failure leaves only a procedural diagnostic label. | §6 Splits and provisional counts |
| Family-only reference | **Accepted.** A nondeployable family-only allocation reference is added to show whether an input router exceeds coarse family allocation, without permitting family ID as a deployment feature. | §6 Comparators; Table 1 |
| Oracle relabeling | **Accepted.** The oracle is now the “same-rollout empirical oracle (optimistic under stochastic finite-K selection)” and is excluded from claims. | §6 Comparators; §10 |
| Required sources | **Accepted.** The bibliography now includes and cites Hoeffding (1948), Hoeffding (1963), Maurer and Pontil (2009), Berger and Hsu (1996), Field and Welsh (2007), and Angelopoulos et al. (2025). The manuscript does not equate its audit with Conformal Risk Control or Learn then Test. | §2; §§3, 7–8; `/home/ubuntu/taskcognition_critique_rev.bib` |
| Figure | **Accepted and redrawn.** The vector 2×2 figure explicitly shows DEVELOPMENT before TRAIN, package freeze, one candidate per method, the four empirical-Bernstein checks, pass-to-gate, fail-to-D with gate bypass, one deployed answer call, and offline-only test policy swap. | Figure 1 and caption |
| Source-of-truth governance | **Accepted.** The active TeX and a dated hash-bound manifest governed by `PROTOCOL_SOURCE_OF_TRUTH.md` are named as the sole implementation specification. Historical conflicting notes remain superseded rather than silently driving code. | §5 opening; Reproducibility statement |

## Narrowed or declined requests

| Request | Decision and user-friendly explanation | Manuscript location |
|---|---|---|
| Replace the title | **Declined.** The exact title is retained because it is interrogative rather than a universal result claim. A scope sentence now tells readers precisely that “overuse” is policy-relative. | Title; §1 Scope |
| Substitute `h_DD` or `h_ind-h_DD` for `h_ind` | **Declined.** That substitution would change the safety question and could tolerate substantial absolute perfect-to-imperfect risk. Direct–direct redraw is informative context, so it is reported descriptively instead. | §3, Eqs. (2)–(4) |
| Route using per-query confidence bounds | **Declined.** Per-query bounds would introduce a materially different decision rule and unsupported pointwise interpretation. The paper keeps one restricted point-score threshold family and audits aggregate deployment behavior. | §4 Eq. (11); Appendix B |
| Require a Lagrangian decision rule | **Narrowed to outside the core protocol.** A cost-aware Lagrangian is reasonable, but it changes the candidate family and would obscure the central paired-versus-factorized supervision comparison. | Appendix B |
| Keep cascades in the primary comparison | **Declined.** A cascade observes a realized direct preview, so its selected population and risk estimand differ from the input-only gate. It is retained only as a future/secondary preview-conditional analysis. | §2; §6; Appendix B |
| Add new policies, tools, agents, checkpoints, tree-of-thought, or post-answer checks | **Declined.** These additions would violate the exact two-package, one-gate, one-answer-call question and make an unfavorable core result easy to evade through scope growth. | §1 Scope; §5; Appendix B |
| Treat K-by-K pairs as independent samples | **Declined.** Cross-products reuse the same draws. They are computations within one input cluster, not new inferential units. | §3 Eq. (7) and following text |
| Claim simultaneous family-specific guarantees | **Declined for the core study.** Equal family weighting supports one finite-family aggregate audit. Per-family results remain diagnostic; stronger familywise certification would need a separately powered protocol. | §3 Eq. (1); §10; Appendix B |

## Special audit correction: Hoeffding replaced by empirical Bernstein

The synthesized critique originally proposed a symmetric Hoeffding audit. The supplied validation script showed that this rule is **mathematically valid but operationally infeasible at the initial `n=450` under a midpoint budget**: even idealized zero-spoilage routing cannot satisfy both its cost and spoilage margins. The manuscript therefore does not claim that 450 inputs suffice.

Following the authoritative task correction, the revision uses the specified finite-sample **empirical-Bernstein** radius based on the sample variance, with gamma 0.05 and frozen row ranges. This is a scope-preserving statistical replacement: it changes the held-out acceptance calculation, not the gate, packages, deployed call count, or scientific estimand. Development simulation must freeze n, K, b_min, cost bounds, alpha, and beta before final labels and must validate false-enable behavior for the complete pipeline. No feasibility or audit-passage claim is made in advance.

## Build and validation record

The manuscript was built in `/home/ubuntu` with copied official `iclr2027_conference.sty`, `iclr2027_conference.bst`, `natbib.sty`, and `fancyhdr.sty`. The final build sequence was `pdflatex → bibtex → pdflatex → pdflatex`, followed by additional stable LaTeX passes after figure and layout corrections.

**Page boundary:** main text ends on **page 7**. References begin on **page 8** and continue through **page 10**. Appendix A begins on **page 10** after the references and continues on **page 11**. Thus all required main-text statements fit within the 9-page ICLR limit.

Validation confirmed: anonymous ICLR 2027 formatting; exact title; 11 total pages; no unresolved citations or cross-references; BibTeX completion without errors; no LaTeX errors; no overfull boxes after the final wrap correction; vector/PDF figure inclusion; all primary and audit result cells represented only by em dashes; and no reported experimental, power, feasibility, effect, or audit-passage result.

## Temporary artifacts

- Revised TeX: `/home/ubuntu/taskcognition_critique_rev.tex`
- Revised BibTeX: `/home/ubuntu/taskcognition_critique_rev.bib`
- Figure SVG: `/home/ubuntu/figures/taskcognition_critique_architecture.svg`
- Figure PDF: `/home/ubuntu/figures/taskcognition_critique_architecture.pdf`
- Figure PNG: `/home/ubuntu/figures/taskcognition_critique_architecture.png`
- Compiled manuscript: `/home/ubuntu/taskcognition_critique_rev.pdf`
- This log: `/home/ubuntu/taskcognition_critique_revision_log.md`

## References

[1]: https://arxiv.org/abs/0907.3740 "Empirical Bernstein Bounds and Sample Variance Penalization"

[2]: https://doi.org/10.1214/ss/1032280304 "Bioequivalence Trials, Intersection-Union Tests and Equivalence Confidence Sets"

[3]: https://doi.org/10.1111/j.1467-9868.2007.00593.x "Bootstrapping Clustered Data"

[4]: https://doi.org/10.1214/aoms/1177730196 "A Class of Statistics with Asymptotically Normal Distribution"

[5]: https://www.jstor.org/stable/2282952 "Probability Inequalities for Sums of Bounded Random Variables"

[6]: https://doi.org/10.1214/24-AOAS1998 "Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control"

## Final independent-review corrections

A second independent methods review found two genuine, narrow blockers after the first revision. Both are now corrected in the final manuscript source.

| Review finding | Final correction | Why it matters |
|---|---|---|
| The winner comparator had no executable learning target, calibrated score, or gate, yet the paper claimed it received the same threshold family as TaskCognition. | The winner baseline now uses one per-input native-score winner label, a binary-log-loss trained and calibrated winner probability, and a single tuned threshold under the same equal-family score/cost/spoilage objective. The paper now accurately claims matched resources, audit, and fallback—not an identical two-head threshold family. | One of the three primary comparison deployments is now reproducible and fair as an alternative routing approach. |
| The draft made a present-tense claim that a frozen manifest already existed. | The paper now uses future-tense language: the current TeX and source-of-truth file govern the draft; a dated frozen manifest must be created after DEVELOPMENT and before final labels. A pre-development template is included in the publication package. | The repository’s governance claim now matches the actual pre-results state. |
| The primary bootstrap lacked key reproducibility fields. | The paper fixes percentile lower bounds, 10,000 within-family complete-cluster resamples, a manifest-bound seed, K-draw aggregation, failed-resample handling, and its asymptotic interpretation. | Borderline test conclusions cannot depend on an unspecified bootstrap variation. |
| Independence and cost-support assumptions were too implicit. | The audit section now specifies independent latent-ID and RNG sampling, treatment of shared failure units, retained failed rows, and analytical—not observed—cost bounds. | These are necessary for the stated empirical-Bernstein conditions to be meaningful. |
| The package-quality reporting table conflated routed-method adequacy with D/R mode-by-family health. | The appendix now separates a learned-method adequacy table from a mode-by-family package QC table. | The cap rule, parser contract, and quality-control reporting are now executable. |

The final source was compiled after these corrections. The final PDF contains **12 total pages**: main text ends on page **7**, references start on page **8**, and appendices follow after references. This remains inside ICLR’s nine-page main-text limit. The final build has no LaTeX errors, unresolved citations/references, or overfull boxes. It reports only non-blocking underfull spacing notices in bibliography/layout material.
