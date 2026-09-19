#!/usr/bin/env python3
"""Design-stage calculations for the TaskCognition fixed-family audit.

These are deterministic planning calculations, not study results.
"""
from math import ceil, exp, log, sqrt

ALPHA = 0.10
GAMMA = 0.05
N = 450
FAMILIES = 6


def ceil_multiple(x: float, m: int) -> int:
    return m * ceil(x / m)


def kl_bernoulli(q: float, p: float) -> float:
    if not (0 <= q <= 1 and 0 < p < 1):
        raise ValueError((q, p))
    left = 0.0 if q == 0 else q * log(q / p)
    right = 0.0 if q == 1 else (1 - q) * log((1 - q) / (1 - p))
    return left + right


def bisect_kl_lower_threshold(n: int, p: float, gamma: float) -> float:
    """Largest q<p satisfying n*KL(q||p) >= log(1/gamma), boundary value."""
    target = log(1 / gamma) / n
    lo, hi = 0.0, p
    if kl_bernoulli(lo, p) < target:
        return float("nan")  # even q=0 cannot reject
    for _ in range(200):
        mid = (lo + hi) / 2
        # KL decreases as q rises from 0 toward p.
        if kl_bernoulli(mid, p) >= target:
            lo = mid
        else:
            hi = mid
    return lo


sum_w2 = 1 / N  # six equal families, 75 each => every row weight is 1/450
r_z = sqrt(log(1 / GAMMA) / (2 * N))  # Z width is 1
r_b = r_z
r_delta = 2 * r_z  # Delta range [-1,1], width 2

print(f"n={N}, alpha={ALPHA}, gamma={GAMMA}")
print(f"sum(w_i^2)={sum_w2:.12f}")
print(f"Hoeffding r_Z=r_B={r_z:.12f}")
print(f"Hoeffding r_Delta={r_delta:.12f}")
print(f"minimum Bhat for any Z-pass (even Rhat=0): {r_z/ALPHA:.12f}")
print("\nObserved-ratio ceiling for Z-pass, Rhat <= alpha-r_Z/Bhat:")
for b in [0.30, 0.40, 0.50, 0.60, 0.75, 1.00]:
    print(f"  Bhat={b:.2f}: Rhat <= {ALPHA-r_z/b:.6f}")

print("\nSymmetric-Hoeffding n needed merely for mean margin B*(alpha-R) to exceed r_Z:")
for b in [0.30, 0.40, 0.50, 0.75, 1.00]:
    for risk in [0.00, 0.02, 0.05, 0.08]:
        margin = b * (ALPHA - risk)
        raw = log(1 / GAMMA) / (2 * margin * margin)
        print(f"  B={b:.2f}, R={risk:.2f}: raw={raw:.3f}, equal-family n={ceil_multiple(raw, FAMILIES)}")

qcrit = bisect_kl_lower_threshold(N, ALPHA, GAMMA)
zcrit = qcrit - ALPHA
print("\nKL-Hoeffding lower-tail audit for X=Z+alpha in [0,1]:")
print(f"  critical Xbar at n={N}: {qcrit:.12f}")
print(f"  equivalent critical Zhat: {zcrit:.12f}")
print(f"  minimum Bhat for zero observed spoilage: {-zcrit/ALPHA:.12f}")
print("  Point-at-alternative p-bounds and n thresholds (power must still be simulated):")
for b in [0.30, 0.40, 0.50, 0.60, 0.75, 1.00]:
    for risk in [0.00, 0.02, 0.05, 0.08]:
        z = b * (risk - ALPHA)
        x = ALPHA + z
        if x >= ALPHA:
            pbound = 1.0
            raw_n = float("inf")
            n6 = None
        else:
            d = kl_bernoulli(x, ALPHA)
            pbound = exp(-N * d)
            raw_n = log(1 / GAMMA) / d
            n6 = ceil_multiple(raw_n, FAMILIES)
        print(f"  B={b:.2f}, R={risk:.2f}: X={x:.4f}, p450={pbound:.6g}, raw_n={raw_n:.3f}, equal-family n={n6}")

cost_crit = bisect_kl_lower_threshold(N, 0.50, GAMMA)
# Upper-tail threshold is symmetric around one half.
delta_x_crit = 1 - cost_crit
delta_crit = 2 * delta_x_crit - 1
print("\nOther KL-Hoeffding thresholds at n=450:")
print(f"  midpoint normalized cost: observed cost must be <= {cost_crit:.12f}")
print(f"  zero-margin score noninferiority: observed Delta must be >= {delta_crit:.12f}")
print(f"  ideal zero-spoilage joint window (p_D=1, no gate cost): route/B in [{-zcrit/ALPHA:.6f}, {cost_crit:.6f}]")

# Sufficient 80% power under a second symmetric Hoeffding step for the original audit.
kappa = 0.20
print("\nConservative n sufficient for >=80% pass probability under symmetric-Hoeffding analysis:")
coef = (sqrt(log(1 / GAMMA)) + sqrt(log(1 / kappa))) ** 2 / 2
for b in [0.30, 0.50, 0.75, 1.00]:
    for risk in [0.00, 0.05]:
        margin = b * (ALPHA - risk)
        raw = coef / (margin * margin)
        print(f"  B={b:.2f}, R={risk:.2f}: raw={raw:.3f}, equal-family n={ceil_multiple(raw, FAMILIES)}")

print("\nMidpoint-cost implication under constant c_R-c_D>0:")
print("  E[g] <= 0.5 - C_gate/(c_R-c_D), hence B=E[g p_D] <= E[g] < 0.5 if gate cost is positive.")
print("  Since the n=450 symmetric audit needs Bhat >= 0.5769 even at zero observed spoilage, pass is structurally impossible in that idealized cost model.")

print("\nFinite-sample cost UCB under a midpoint budget, after normalizing c_D=0, c_R=1:")
print(f"  r_C={r_z:.12f} because the cost range has width 1.")
print(f"  With zero gate cost, pass requires observed routing rate <= {0.5-r_z:.12f}.")
print(f"  Yet zero-spoilage Z-pass requires observed Bhat >= {r_z/ALPHA:.12f} and Bhat<=routing rate.")
print("  Therefore no candidate can pass both cost and Z under this normalization at n=450.")

n_joint_raw = 2 * log(1 / GAMMA) / (ALPHA * ALPHA)
print("\nNecessary n for any joint pass under a midpoint budget and zero gate cost:")
print("  Need r <= alpha/(2*(1+alpha)) from r/alpha <= 0.5-r.")
print(f"  raw n >= {n_joint_raw*(1+ALPHA)**2:.3f}; equal-family n >= {ceil_multiple(n_joint_raw*(1+ALPHA)**2, FAMILIES)}.")
print("  Positive gate cost, nonzero true spoilage, cost heterogeneity, score LCB, and b_min can only make feasibility harder.")

def eb_radius(sample_variance: float, width: float = 1.0) -> float:
    """Maurer-Pontil Thm. 11, expressed on the original scale."""
    v_scaled = sample_variance / (width * width)
    return width * (sqrt(2 * v_scaled * log(2 / GAMMA) / N)
                    + 7 * log(2 / GAMMA) / (3 * (N - 1)))

print("\nEmpirical-Bernstein illustration at n=450 (idealized g in {0,1}, p_D=1, zero spoilage):")
feasible_q = []
for selected in range(N + 1):
    q = selected / N
    # Finite-sample variance s^2 for two-point rows with exactly selected ones.
    var_g = (N / (N - 1)) * q * (1 - q) if N > 1 else 0.0
    r_cost_eb = eb_radius(var_g, 1.0)
    r_z_eb = eb_radius((ALPHA ** 2) * var_g, 1.0)  # Z has known full range width 1
    if -ALPHA * q + r_z_eb <= 0 and q + r_cost_eb <= 0.5:
        feasible_q.append(q)
if feasible_q:
    print(f"  joint pass routing interval on the 1/450 grid: [{min(feasible_q):.6f}, {max(feasible_q):.6f}]")
else:
    print("  no joint pass routing interval")
print(f"  zero-variance EB radius for a unit-width statistic: {eb_radius(0.0, 1.0):.12f}")
print(f"  zero-variance EB radius for Delta in [-1,1]: {eb_radius(0.0, 2.0):.12f}")
