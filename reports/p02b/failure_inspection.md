# P02B offline failure inspection

This inspection uses retained final channels and the existing strict-parser/native-scorer replay. Primary scores and completion counts are unchanged. Excerpts below are shortened only for this report; original token IDs, decoded text, thinking and final channels remain intact in the linked raw records. No answer is selected from thinking or ambiguous prose.

| Cap | Mode | Missing both tags | Missing opening tag | Missing closing tag | Forbidden outside prose | Other wrapper subtype | Native channel failure | Native syntax failure | Cap without valid FINAL |
|---|---|---|---|---|---|---|---|---|---|
| 1024 | D | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 1024 | R | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 7 |
| 2048 | D | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2048 | R | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 3 |

Categories may overlap (for example, a cap and a missing closing tag). Counts are descriptive, with six input clusters, not population estimates.

## 00_number_sorting_D_1024_0

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **20**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/00_number_sorting_D_1024_0.json), SHA-256 `e937b993590650884b325ebd15fda7c409c951d76011d8fa5667b02531a139dc`.

Final-channel inspection:

```text
["-64.0", "33.0", "49.7"]
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 02_number_sorting_D_2048_0

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **20**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/02_number_sorting_D_2048_0.json), SHA-256 `d19b26db02f9664e6bf8f747ae73c7e1010d37fe3c7ca9794eed5c0d04d7db56`.

Final-channel inspection:

```text
["-64.0", "33.0", "49.7"]
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 04_number_format_D_2048_0

Primary status `wrong`; native score **0.0**; strict-valid FINAL **True**; finish `eos`; output tokens **23**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/04_number_format_D_2048_0.json), SHA-256 `ebb3acaf5aba044a8ca040eb0b7ed3d328ca386150c3fc050d07fb7f97275a64`.

Final-channel inspection:

```text
<FINAL>382269594.038000</FINAL>
```

## 06_number_format_D_1024_0

Primary status `wrong`; native score **0.0**; strict-valid FINAL **True**; finish `eos`; output tokens **23**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/06_number_format_D_1024_0.json), SHA-256 `7bfa511c5854d1b500001e75041704a7cd9fb491ff2d3ad111e5459fff22097f`.

Final-channel inspection:

```text
<FINAL>382269594.038000</FINAL>
```

## 07_number_format_R_1024_0

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/07_number_format_R_1024_0.json), SHA-256 `ea9f4b2304ccef56481decd3824438cdb087e5a3883c6794d8f77f08d266f4a7`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 12_graph_color_D_2048_0

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **61**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/12_graph_color_D_2048_0.json), SHA-256 `f2798440add67cce91c5ea44dcf550040a72b7f0bb40c5e6ad55d28c96b08fdd`.

Final-channel inspection:

```text
{"0": 1, "1": 2, "2": 2, "3": 1, "4": 3, "5": 3, "6": 1, "7": 2, "8": 1, "9": 2}
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 13_graph_color_R_2048_0

Primary status `partial`; native score **0.01**; strict-valid FINAL **True**; finish `eos`; output tokens **2048**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/13_graph_color_R_2048_0.json), SHA-256 `e57d683db4d306fc52bd2daf4c9f792fd9e38cc9b693bac13294e73ee1c32110`.

Final-channel inspection:

```text


<FINAL>{"0": 1, "1": 1, "2": 2, "3": 1, "4": 2, "5": 2, "8": 3, "9": 1}</FINAL>
```

## 14_graph_color_D_1024_0

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **61**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/14_graph_color_D_1024_0.json), SHA-256 `b5f68e281586020327853df09e3ba0c2b26c619e5594bfcf5abae6f21b73d1ce`.

Final-channel inspection:

```text
{"0": 1, "1": 2, "2": 2, "3": 1, "4": 3, "5": 3, "6": 1, "7": 2, "8": 1, "9": 2}
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 15_graph_color_R_1024_0

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/15_graph_color_R_1024_0.json), SHA-256 `e8f90fe02fdf09f7fd8ed0653d5aa6364b5d871b34d7bbc4e054381b6efe7063`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 16_shortest_path_D_1024_0

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['outer_wrapper_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/16_shortest_path_D_1024_0.json), SHA-256 `6b0ad3f6078ca79ec25497aa87097701348acfa35a493fb448fc7cec4809c7fa`.

Final-channel inspection:

```text
<FINAL>right right down down left left left down down left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left l
[report excerpt shortened; full raw output retained]
 left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left left
```

No eligible unambiguous payload-only diagnostic is reported.

## 17_shortest_path_R_1024_0

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/17_shortest_path_R_1024_0.json), SHA-256 `c181fc63ea70502ca1210605941a84ba800ca2a09f4ee5bddc7349cee2615f4c`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 18_shortest_path_D_2048_0

Primary status `wrong`; native score **0.0**; strict-valid FINAL **True**; finish `eos`; output tokens **20**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/18_shortest_path_D_2048_0.json), SHA-256 `edba5642275535e9b5a14f6f99978a0557c13b3036c3109906112616f337922a`.

Final-channel inspection:

```text
<FINAL>right right down down left left left down down left left left left</FINAL>
```

## 19_shortest_path_R_2048_0

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **2048**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/19_shortest_path_R_2048_0.json), SHA-256 `42c9da20cad480e96a38efdfb93a3e08ebfb9498ae3153b3ac0bd07af707f2b1`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 25_number_sorting_D_2048_1

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **20**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/25_number_sorting_D_2048_1.json), SHA-256 `b847f14225192d9dfaadff5cde7f58f6b1ec361684f34a5b0a8db32ba34e636e`.

Final-channel inspection:

```text
["-64.0", "33.0", "49.7"]
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 27_number_sorting_D_1024_1

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **20**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/27_number_sorting_D_1024_1.json), SHA-256 `6972f1ba553b8572085b44697f80d246fe892257b9ae528060659c9d819d718f`.

Final-channel inspection:

```text
["-64.0", "33.0", "49.7"]
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 28_number_format_R_1024_1

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/28_number_format_R_1024_1.json), SHA-256 `8765e919c044ba509293d2ef6c15b63852023c29fc83ec9165762f25b726a223`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 29_number_format_D_1024_1

Primary status `wrong`; native score **0.0**; strict-valid FINAL **True**; finish `eos`; output tokens **23**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/29_number_format_D_1024_1.json), SHA-256 `f80d77207fc3db83670a9568844a790ef1497fad11c0ca3e859f7f7f44594bb4`.

Final-channel inspection:

```text
<FINAL>382269594.038000</FINAL>
```

## 31_number_format_D_2048_1

Primary status `wrong`; native score **0.0**; strict-valid FINAL **True**; finish `eos`; output tokens **23**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/31_number_format_D_2048_1.json), SHA-256 `07c6b0de4e0ecfc1f5bbb540bb87d4a6603a4a8dac8492624904eb6d01a0a9bb`.

Final-channel inspection:

```text
<FINAL>382269594.038000</FINAL>
```

## 34_letter_counting_R_1024_1

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/34_letter_counting_R_1024_1.json), SHA-256 `2a3b802a49c854cc61ce2407d4416d44c6c9a65a6277092fdbd3330eb9a046f8`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 36_graph_color_R_1024_1

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/36_graph_color_R_1024_1.json), SHA-256 `148db34f1a4382a82097897a1ace11d79089abae266c29e9a5c953a24721a36c`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 37_graph_color_D_1024_1

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **61**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/37_graph_color_D_1024_1.json), SHA-256 `66733e1ddd1c7f6c327ab9c3dedbe53d280cdcd7dc6011bb555b41d185784502`.

Final-channel inspection:

```text
{"0": 1, "1": 2, "2": 2, "3": 1, "4": 3, "5": 3, "6": 1, "7": 2, "8": 1, "9": 2}
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 38_graph_color_R_2048_1

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **2048**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/38_graph_color_R_2048_1.json), SHA-256 `903195606a49b947472466857e82555e18f3dd7d80b8b4d14a3ea19d3186b8eb`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 39_graph_color_D_2048_1

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `eos`; output tokens **61**. Flags: `['outer_wrapper_failure']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/39_graph_color_D_2048_1.json), SHA-256 `144b7e5aeecabbcaebbd07750764238cfc0ecf80b5f45264eb9011010d73c85f`.

Final-channel inspection:

```text
{"0": 1, "1": 2, "2": 2, "3": 1, "4": 3, "5": 3, "6": 1, "7": 2, "8": 1, "9": 2}
```

Separate **bare_native_payload_diagnostic**: unchanged native score **1.0**. Primary score remains **0.0**; this does not repair the deployed output or increase completion.

## 40_shortest_path_R_2048_1

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **2048**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/40_shortest_path_R_2048_1.json), SHA-256 `2714daab7815d0a7cda07e094b5bc4cc98bba03f98d2ddf95150619a589017ab`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 41_shortest_path_D_2048_1

Primary status `outer_wrapper_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **2048**. Flags: `['outer_wrapper_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/41_shortest_path_D_2048_1.json), SHA-256 `09852748ebb40a3e47c05ad80e18b87e2c844ec7246c1aae08cca899bf0e7cab`.

Final-channel inspection:

```text
<FINAL>right right down down left left left down down left left left left left left down down left left left left left left left down down left left left left left left left down down left left left left left left left down down left left left left l
[report excerpt shortened; full raw output retained]
 down down left left left left left left left down down left left left left left left left down down left left left left left left left down down left left left left left left left down down left left left left left left left down down left left left
```

No eligible unambiguous payload-only diagnostic is reported.

## 42_shortest_path_R_1024_1

Primary status `native_delimiter_failure`; native score **0.0**; strict-valid FINAL **False**; finish `cap`; output tokens **1024**. Flags: `['native_delimiter_failure', 'cap_without_valid_final']`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/42_shortest_path_R_1024_1.json), SHA-256 `e1bfeb09c6c9a434870ad25d1ffbcc57dcf542755bafe9eb1de02ebb5ec5cedc`.

No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.

## 43_shortest_path_D_1024_1

Primary status `wrong`; native score **0.0**; strict-valid FINAL **True**; finish `eos`; output tokens **20**. Flags: `[]`.
[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/43_shortest_path_D_1024_1.json), SHA-256 `645f9f566d4f54a0ed5f41309c4d9ebd35d47a09f41031f4f937b4eaaae447e3`.

Final-channel inspection:

```text
<FINAL>right right down down left left left down down left right left right</FINAL>
```
