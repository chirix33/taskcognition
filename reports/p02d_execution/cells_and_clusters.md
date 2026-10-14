# P02D v4 execution: all planned cells

Primary scores are unchanged. Dispatched includes consumed reservations before load; logged admission and retained records are separate. No missing draw is imputed.

| Family | Mode | Planned | Dispatched | Admitted | Retained | Unexecuted | Unscored consumed | Strict FINAL | Perfect | Partial scores | Tokens known |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| number_sorting | D | 16 | 16 | 16 | 16 | 0 | 0 | 4 | 4 | [] | 768 |
| number_sorting | R | 16 | 16 | 16 | 16 | 0 | 0 | 16 | 16 | [] | 14450 |
| number_format | D | 16 | 16 | 16 | 16 | 0 | 0 | 16 | 16 | [] | 412 |
| number_format | R | 16 | 16 | 16 | 16 | 0 | 0 | 16 | 16 | [] | 14299 |
| letter_counting | D | 16 | 16 | 16 | 16 | 0 | 0 | 16 | 3 | [] | 128 |
| letter_counting | R | 16 | 16 | 16 | 16 | 0 | 0 | 14 | 14 | [] | 13683 |
| graph_color | D | 16 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | [] | 976 |
| graph_color | R | 16 | 16 | 16 | 16 | 0 | 0 | 6 | 6 | [] | 29661 |
| shortest_path | D | 16 | 16 | 16 | 16 | 0 | 0 | 14 | 0 | [] | 4366 |
| shortest_path | R | 16 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | [] | 32768 |
| knights_knaves | D | 16 | 16 | 16 | 16 | 0 | 0 | 16 | 7 | [] | 296 |
| knights_knaves | R | 16 | 16 | 16 | 16 | 0 | 0 | 12 | 12 | [] | 17564 |

## Failure subtypes, score distributions and measured costs

Exact score/token/duration/memory lists, including unknowns, are in production_execution_report.json. Values below are direct summaries of those primary records.

| Family / mode | Native scores | Wrapper subtype counts | Failure flags | Timeouts | Output lengths | Worker seconds sum |
|---|---|---|---|---:|---|---:|
| number_sorting / D | [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0] | {"missing_both_tags": 12} | {"outer_wrapper_failure": 12} | 0 | [52, 32, 63, 45, 52, 32, 63, 45, 52, 32, 63, 45, 52, 32, 63, 45] | 521.950676 |
| number_sorting / R | [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] | {} | {} | 0 | [910, 680, 840, 1263, 1227, 892, 689, 1144, 1030, 622, 716, 1134, 1260, 563, 759, 721] | 1109.913904 |
| number_format / D | [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] | {} | {} | 0 | [28, 28, 23, 24, 28, 28, 23, 24, 28, 28, 23, 24, 28, 28, 23, 24] | 517.418170 |
| number_format / R | [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] | {} | {} | 0 | [548, 485, 580, 1603, 396, 930, 624, 764, 542, 1283, 988, 1052, 696, 689, 1745, 1374] | 1099.322674 |
| letter_counting / D | [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0] | {} | {} | 0 | [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8] | 510.797544 |
| letter_counting / R | [1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0] | {} | {"native_delimiter_failure": 2, "cap_without_valid_final": 2} | 0 | [743, 626, 2048, 757, 661, 575, 595, 982, 628, 449, 607, 867, 735, 766, 2048, 596] | 1088.957318 |
| graph_color / D | [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] | {"missing_both_tags": 16} | {"outer_wrapper_failure": 16} | 0 | [61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61] | 542.888893 |
| graph_color / R | [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0] | {"missing_close_tag": 1} | {"native_delimiter_failure": 9, "cap_without_valid_final": 10, "outer_wrapper_failure": 1} | 0 | [830, 2048, 2048, 2048, 1844, 2048, 2048, 2023, 1608, 2048, 2048, 2048, 839, 2048, 2048, 2037] | 1755.264514 |
| shortest_path / D | [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] | {"missing_close_tag": 2} | {"outer_wrapper_failure": 2, "cap_without_valid_final": 2} | 0 | [21, 19, 15, 14, 21, 26, 2048, 14, 2048, 20, 23, 14, 23, 23, 22, 15] | 695.971359 |
| shortest_path / R | [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] | {} | {"native_delimiter_failure": 16, "cap_without_valid_final": 16} | 0 | [2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048, 2048] | 1875.579931 |
| knights_knaves / D | [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0] | {} | {} | 0 | [18, 19, 20, 17, 18, 19, 20, 17, 18, 19, 20, 17, 18, 19, 20, 17] | 531.622942 |
| knights_knaves / R | [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0] | {} | {"native_delimiter_failure": 4, "cap_without_valid_final": 4} | 0 | [926, 2048, 537, 587, 909, 2048, 1111, 804, 626, 2048, 877, 562, 1066, 2048, 850, 517] | 1257.669482 |

## All 24 input clusters

Only complete K=4 D/R clusters receive targets. T_b/T_h/redraw/partial-decline values are existing-contract pipeline checks, not independent cross-pair samples or routing evidence. Full input identities and unrounded target values are in the JSON report.

| Family / index | Input ID prefix | D scores | R scores | D perfect | D/R sample variance | Complete K4 | Targets |
|---|---|---|---|---:|---|---|---|
| number_sorting / 0 | 0b18ad4b25042863 | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| number_sorting / 1 | bed4b15503bb7cee | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| number_sorting / 2 | aaf37f95311ad8c5 | [1.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 4 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 1.0, "mean_score_R": 1.0, "perfect_rate_D": 1.0, "perfect_rate_R": 1.0} |
| number_sorting / 3 | 4974aec214882645 | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| number_format / 0 | 65e79401a071f1e7 | [1.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 4 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 1.0, "mean_score_R": 1.0, "perfect_rate_D": 1.0, "perfect_rate_R": 1.0} |
| number_format / 1 | 454f382c1f601b36 | [1.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 4 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 1.0, "mean_score_R": 1.0, "perfect_rate_D": 1.0, "perfect_rate_R": 1.0} |
| number_format / 2 | 3e7bcec0872d4483 | [1.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 4 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 1.0, "mean_score_R": 1.0, "perfect_rate_D": 1.0, "perfect_rate_R": 1.0} |
| number_format / 3 | 836b15d78bb442b2 | [1.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 4 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 1.0, "mean_score_R": 1.0, "perfect_rate_D": 1.0, "perfect_rate_R": 1.0} |
| letter_counting / 0 | 883e1e30eea51db3 | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| letter_counting / 1 | d7dc610a978b638f | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| letter_counting / 2 | 55445bd2ec996797 | [0.0, 0.0, 0.0, 0.0] | [0.0, 1.0, 1.0, 0.0] | 0 | [0.0, 0.3333333333333333] | True | {"benefit": 0.5, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.5, "perfect_rate_D": 0.0, "perfect_rate_R": 0.5} |
| letter_counting / 3 | 401ed4d11e91c0d7 | [0.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 3 | [0.25, 0.0] | True | {"benefit": 0.25, "joint_spoilage": 0.0, "direct_redraw": 0.25, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.75, "mean_score_R": 1.0, "perfect_rate_D": 0.75, "perfect_rate_R": 1.0} |
| graph_color / 0 | 281fe48a734b2571 | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| graph_color / 1 | f200a01a171eb4e5 | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| graph_color / 2 | 8680a46bf75a99d9 | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| graph_color / 3 | b04603cfb7f55bc6 | [0.0, 0.0, 0.0, 0.0] | [0.0, 1.0, 0.0, 1.0] | 0 | [0.0, 0.3333333333333333] | True | {"benefit": 0.5, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.5, "perfect_rate_D": 0.0, "perfect_rate_R": 0.5} |
| shortest_path / 0 | f434ee436187a084 | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| shortest_path / 1 | d21984adaac8d34e | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| shortest_path / 2 | 76a1ecefabfe3941 | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| shortest_path / 3 | 041f5e754e6f2731 | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| knights_knaves / 0 | fa4be76e5463236f | [0.0, 0.0, 0.0, 0.0] | [1.0, 1.0, 1.0, 1.0] | 0 | [0.0, 0.0] | True | {"benefit": 1.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 1.0, "perfect_rate_D": 0.0, "perfect_rate_R": 1.0} |
| knights_knaves / 1 | b736b398e5e56350 | [0.0, 0.0, 0.0, 0.0] | [0.0, 0.0, 0.0, 0.0] | 0 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.0, "mean_score_R": 0.0, "perfect_rate_D": 0.0, "perfect_rate_R": 0.0} |
| knights_knaves / 2 | 430c39d7cb402c29 | [1.0, 0.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 3 | [0.25, 0.0] | True | {"benefit": 0.25, "joint_spoilage": 0.0, "direct_redraw": 0.25, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 0.75, "mean_score_R": 1.0, "perfect_rate_D": 0.75, "perfect_rate_R": 1.0} |
| knights_knaves / 3 | 9584691319ab68b0 | [1.0, 1.0, 1.0, 1.0] | [1.0, 1.0, 1.0, 1.0] | 4 | [0.0, 0.0] | True | {"benefit": 0.0, "joint_spoilage": 0.0, "direct_redraw": 0.0, "decline_010": 0.0, "decline_025": 0.0, "mean_score_D": 1.0, "mean_score_R": 1.0, "perfect_rate_D": 1.0, "perfect_rate_R": 1.0} |
