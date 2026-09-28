# P02A native adapter contracts

Evidence kind: `development_observation` for source/config inspection; `fixture` for hand checks. No scientific population freeze.

All six implementations are unmodified bytes from Reasoning Gym `21e6d2a9a581b3e11aafe711abfd37402f8482d5`. The vendored closure has 149,485 source/data bytes before its manifest. `source_manifest.json` records every SHA-256; `native_git_blob_verification.json` independently compares all 15 upstream files with that commit's Git tree. Minimal local package initializers limit imports; they do not change generators, rendering, or scoring. Existing NumPy 2.5.3 suffices; no packages, weights, drivers, or environments were installed/upgraded. License and embedded text-resource notices are preserved.

| Registry family | Native module | Renderer/answer | Native score and tolerance | Adapter syntax |
|---|---|---|---|---|
| number_sorting | algorithmic/number_sorting.py | Original numeric sorting question and native list instructions; numeric list | Binary; sorted order, matching length, each absolute difference <=1 | Existing P01 finite numeric-list syntax, payload unchanged |
| number_format | arithmetic/number_format.py | Original largest/smallest selection across numeric formats; scalar number | Binary; removes commas and requires absolute difference <0.01 | Finite scalar accepting commas/exponents |
| letter_counting | algorithmic/letter_counting.py | Original span from native `in_the_year_2889.txt`; count text | Inherits dataset.py: exact text 1; oracle substring gets len(gold)/len(payload); otherwise 0 | Nonempty native text; do not eliminate substring partial credit with an integer-only rule |
| graph_color | algorithmic/graph_color.py | Original vertex/edge/color lists; JSON map | Valid coloring 1; parsable but invalid coloring 0.01 when verifier returns false; malformed/exception 0 | JSON object; native verifier decides keys, coverage and colors |
| shortest_path | graphs/shortest_path.py | Original grid renderer; space-separated directions or `infeasible` | Exact/alternative shortest path 1; valid longer path 0.5; otherwise 0 | Native directions or literal `infeasible` |
| knights_knaves | logic/knights_knaves.py | Original named inhabitants and native role synonyms; textual assignments | Normalized exact assignment set 1; equal assignment-set sizes with m>0 matches: 0.3+0.7*m/n; otherwise 0 | Nonempty native text, native normalization and precision preserved |

Each family's complete effective default configuration, seed/index, verbatim rendered question, gold/metadata, source reference and latent/input/content hashes is in `artifacts/development/p02a-six-family/outcome_inputs/<family>.json`. Only size=1 and declared seed override defaults. Native internal generation rules (including unique-solvable knights/knaves and greedy-colorable graph sampling) remain unchanged; no external outcome screening or item replacement is performed.

Hand checks in `native_scorer_checks.json` include correct, wrong, malformed and applicable partial-credit answers. They are offline fixtures, not empirical generations. Sorting boundary <=1 and number-format strict <0.01 are preserved. Knights/knaves mathematically 0.65 is stored as the native Python value 0.6499999999999999; no near-one rounding is used. `perfect_correct` is exactly score == 1.

The strict P01 channel/FINAL parser is unchanged. Each syntax is tested with a valid final channel, misleading FINAL tags in thinking, and forbidden trailing text. Parser failures score zero; successfully wrapped native text can be wrong/partial. The native text scorers' permissiveness is disclosed rather than silently narrowed.

The input-only gate projection contains only an opaque identity, original text and character count. Family/config/gold/trace data remain in outcome/evaluation stores; request family fields are worker scorer metadata, not a gate interface. No gate is fitted or invoked.

The 2,048-token serialized-input ceiling was recorded before selecting items. With the 1,024 output cap, the maximum context would be 3,072, below checkpoint max_position_embeddings=40,960. It is a conservative provisional operational limit, not a measured worst-case memory proof or the final population rule. Actual selected inputs are 112–295 tokens. No question was truncated or replaced.

P01 and P02A question hashes are disjoint. Future cap/high-repeat/final namespaces are reserved, but future plans must additionally reject duplicate content/latent items against historical manifests; namespace differences alone are insufficient.
