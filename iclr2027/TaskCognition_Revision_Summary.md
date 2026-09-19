# TaskCognition Revision 2: Protocol Summary for Ashraf

The manuscript now describes a **pre-results protocol** rather than implying that TaskCognition already works. It keeps the exact requested title and makes the scope precise: the study compares **two fixed inference packages on one frozen Qwen3-8B model**. It does not claim that reasoning models as a class are harmful.

## What changed

### The main goal is now score under two explicit constraints

The primary goal is to maximize the benchmark's native score. The chosen router must stay within an **expected all-in cost budget** and an **aggregate spoilage-risk limit**. Cost includes every component used at deployment. TaskCognition pays for its gate and exactly one selected answer call. A confidence cascade pays for the direct preview, its confidence/router processing, and the reasoning call whenever it escalates. Tokens, calls, and latency are also reported separately. A token-adjusted scalar utility is retained only as a sensitivity analysis, with its normalization and weight fixed before test access.

### The stochastic harm definition no longer relies on same-seed pairing

For an item, the protocol estimates the direct success probability and reasoning success probability from repeated independent draws. It defines

\[
h_{\mathrm{ind}}(x)=p_D(x)\,[1-p_R(x)].
\]

The primary aggregate risk, \(R_{\mathrm{spoil}}\), asks: among items sent to reasoning, and conditional on an independent direct draw being correct, how often would an independent reasoning draw be wrong? The manuscript also reports joint harm mass, rescue quantities, and perfect-correctness flip tables. Same-seed and deterministic flip tables are explicitly secondary sensitivities. The symbol **G** now denotes a reasoning rescue, while **\(\beta\)** denotes the cost budget.

### Training, tuning, certification, and test now have separate roles

For each of six Reasoning Gym families, renderer 1 supplies **200 training, 75 tuning, 75 untouched certification, and 100 in-distribution test items**. Seeds do not overlap, and these four splits use the same parameter range. Training fits the predictor. Tuning selects the architecture and seed, fits isotonic calibration, and chooses one threshold pair. Certification evaluates only that frozen candidate and cannot be used to retune it. Test remains untouched.

The certification step uses one-sided, instance-clustered bootstrap upper bounds for aggregate spoilage and expected all-in cost. This is called an **empirical certificate under stated IID/exchangeability assumptions**, not a distribution-free or pointwise guarantee. If either bound fails, or fewer than 100 effective selected direct-correct instances are available, the certificate is failed or uninformative and deployment defaults to always-direct.

### The gate has a clean, executable rule

There is exactly one learned input-only pre-generation gate. It has a shared trunk, a native-score benefit head, and an independent-draw harm head. The candidate family is

\[
g_{\tau,\eta}(x)=R
\quad\text{only if calibrated benefit}>\tau
\text{ and calibrated harm}\leq\eta.
\]

The threshold pair is chosen on tuning data under the fixed score, cost, and spoilage objective. There is no undefined run-time budget check and no per-query lower/upper confidence-bound claim.

### Partial-credit degradation is now visible

The native score in \([0,1]\) is the primary outcome. Binary correctness is defined only as perfect score, so direct-correct/reasoning-wrong is described accurately as **perfect-to-imperfect spoilage**. For suites with partial credit, the protocol also reports whether reasoning lowers the score by at least prespecified \(\epsilon\) values of 0.10 and 0.25.

### Renderer shift is explicit and limited in scope

Two independently authored unseen renderers contribute 50 items per family each, for **600 renderer-shift items**. The paper describes these as **12 fixed family–renderer case studies**, not evidence about a population of all renderers. A parameter-range shift is optional appendix analysis only. The paper does not claim generalization to unseen task families.

### Qwen3 is treated as two inference packages, not a clean trace intervention

Direct and reasoning use the same frozen original unified Qwen3-8B checkpoint, task information, one-call limit, tool permissions, answer wrapper, and primary decoding settings. The native thinking switch is part of each package. The paper therefore avoids claiming to isolate the causal effect of visible reasoning alone.

The primary comparison uses matched decoding. Mode-recommended decoding is a sensitivity. Temperature zero is only a diagnostic. The output cap is selected from **training completion curves only**: start at 1,024 generated tokens; if either package has less than 99% valid final-tag completion, increase once to 2,048 and freeze. Separate 256- and 512-token runs are sensitivities. Finish reason, reasoning tokens, final-tag truncation, parser failures, and completed-but-wrong answers are all reported separately.

### The answer parser is now a two-level contract

Every response must contain exactly one outer `<FINAL>...</FINAL>` wrapper. The extracted payload must then satisfy the suite's native answer format. LLMThinkBench keeps its required LaTeX boxed form. Reasoning Gym graph coloring keeps its required JSON schema, and other tasks keep their native syntax. A version-pinned adapter passes the payload to the reference evaluator. Planned unit tests cover valid, invalid, repeated-tag, truncated, nested, empty, and adversarial outputs.

### Learned baselines now receive identical resources

Every input-only learned baseline gets the same encoder and features, split roles, trunk parameter budget, optimizer search, initialization count, repeated-rollout table, selection rule, and final cost/risk constraints. The absolute router predicts both policies' expected scores and costs. The winner router predicts the higher mean-score policy, retains ties and both-fail cases, and breaks ties to direct. The no-harm ablation removes only the harm head. Cascades use declared confidence signals and are compared at matched **total deployed cost**, not matched reasoning rate.

### Power and event adequacy are explicit

The instance is the unit of inference; repeated draws are averaged before analysis. Family weights are fixed. A prospective training-only simulation will report 80% power and the minimum detectable paired score effect before execution. Certification cannot be interpreted unless it has at least 100 effective selected direct-correct instances. Paired instance bootstrap and permutation tests are used with finite-family language.

### The third suite is license-safe and accurately named

The paper no longer assumes that Mind Your Step raw data can be redistributed. The planned suite is an **independently generated Mind-Your-Step-inspired diagnostic** based on public task descriptions. Its generator is planned for release under Apache-2.0. Separate validation must show that its difficulty and direct/reasoning behavior reflect the intended construct. Without that validation, it remains a new diagnostic and is not called a replication.

### Reproducibility and disclosure were tightened

The manuscript cites the Qwen3 model card and version-pinned Reasoning Gym and LLMThinkBench software. Conformal Risk Control is cited as an ICLR 2024 proceeding. Hyperlinks use `hidelinks`. Release language is license-limited: raw prompts and outputs will be shared only where permitted; otherwise the release will contain allowed IDs, hashes, derived statistics, and evaluation scripts.

The AI-use statement remains complete but is now explicitly a **draft-stage disclosure**. It states that authors must verify sources, metadata, novelty, code, parsers, licenses, analyses, prose, and every AI suggestion before submission.

## Figure and manuscript status

The architecture figure now shows all four stages in a readable 2×2 layout: training, tuning, untouched certification, and deployment/test. It shows that failed or uninformative certification bypasses learned routing and forces direct execution. It contains exactly one learned gate and exactly two alternative answer policies, of which exactly one is called.

No experimental results were invented. Every planned result cell remains an em dash. The compiled PDF has 11 pages total: main text and the required/recommended statements end on page 7, references begin on page 8, and the appendix begins on page 10. It is therefore within the nine-page ICLR main-text limit. The LaTeX uses the supplied official ICLR 2027 style and compiles with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` without warnings, unresolved references, or overfull boxes.

## Deliverables

- Revised LaTeX: `/home/ubuntu/taskcognition_rev2.tex`
- Revised bibliography: `/home/ubuntu/taskcognition_rev2.bib`
- Architecture PNG: `/home/ubuntu/figures/taskcognition_architecture_rev2.png`
- Vector architecture PDF: `/home/ubuntu/figures/taskcognition_architecture_rev2.pdf`
- Editable architecture source: `/home/ubuntu/figures/taskcognition_architecture_rev2.svg`
- Compiled PDF: `/home/ubuntu/taskcognition_rev2.pdf`
- This summary: `/home/ubuntu/taskcognition_rev2_revision_summary.md`
