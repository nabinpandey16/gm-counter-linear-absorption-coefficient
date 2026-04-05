"""
================================================================================
Practical 3 — Linear Absorption Coefficient (µ) of Radiation
Tri-Chandra Multiple Campus | Dept. of Physics | B.Sc. III Year | 2082

Instrument : Geiger-Müller (GM) Counter
Objective  : Determine the linear absorption coefficient µ of radiation
             passing through a material, and draw the best-fit line.

Physics background
------------------
When monochromatic radiation passes through an absorber of thickness x,
the transmitted intensity follows the Beer-Lambert (exponential attenuation) law:

        N(x) = N₀ · exp(−µx)

Taking the natural log:

        ln N(x) = ln N₀  −  µ · x

This is linear in x — so a plot of ln(N) vs x gives a straight line
with slope = −µ  and  intercept = ln(N₀).

Statistical note
----------------
Since GM counts follow Poisson statistics, the uncertainty in N counts is √N.
The propagated uncertainty in ln(N) is therefore  σ_ln(N) = √N / N = 1/√N.
We use weighted least squares to account for this heteroscedasticity.

Author : Nabin Pandey | nabin.795401@trc.tu.edu.np
================================================================================
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import linregress
import warnings
warnings.filterwarnings('ignore')

# ── 1. DATA ───────────────────────────────────────────────────────────────────
# GM counter readings at different absorber thicknesses
# count_error = √(counts)  [Poisson statistics]
raw = {
    'thickness_mm': [0,  2,   4,   6,   8,   10,  12,  14,  16, 18, 20],
    'counts'      : [1053, 768, 551, 412, 305, 218, 165, 121, 94, 66, 48],
    'count_error' : [32.45, 27.71, 23.47, 20.30, 17.46,
                     14.76, 12.85, 11.00,  9.70,  8.12, 6.93],
}

df = pd.DataFrame(raw)
df['thickness_cm'] = df['thickness_mm'] / 10.0          # SI: cm
df['ln_counts']    = np.log(df['counts'])                # linearise
df['ln_error']     = df['count_error'] / df['counts']    # error propagation: σ_lnN

x    = df['thickness_cm'].values
y    = df['ln_counts'].values
yerr = df['ln_error'].values

# ── 2. WEIGHTED LEAST-SQUARES BEST FIT ───────────────────────────────────────
# Minimises Σ wᵢ (yᵢ − a·xᵢ − b)²   where  wᵢ = 1/σᵢ²
w    = 1.0 / yerr**2
Sw   = np.sum(w);           Swx  = np.sum(w * x)
Swy  = np.sum(w * y);       Swxx = np.sum(w * x**2)
Swxy = np.sum(w * x * y)

D    = Sw * Swxx - Swx**2

a_w  = (Sw * Swxy  - Swx * Swy)  / D     # slope  = −µ
b_w  = (Swxx * Swy - Swx * Swxy) / D     # intercept = ln N₀

da_w = np.sqrt(Sw   / D)                 # uncertainty in slope
db_w = np.sqrt(Swxx / D)                 # uncertainty in intercept

mu     = -a_w                            # linear attenuation coefficient (cm⁻¹)
mu_err =  da_w
N0     =  np.exp(b_w)
N0_err =  N0 * db_w                      # propagated error

# ── 3. GOODNESS OF FIT ───────────────────────────────────────────────────────
_, _, r_value, p_value, _ = linregress(x, y)   # for R²
y_pred    = a_w * x + b_w
residuals = y - y_pred
chi2_val  = np.sum((residuals / yerr)**2)
dof       = len(x) - 2
chi2_red  = chi2_val / dof

# ── 4. PRINT RESULTS ─────────────────────────────────────────────────────────
print("=" * 64)
print("  EXPERIMENT 3 — LINEAR ABSORPTION COEFFICIENT")
print("  Tri-Chandra Multiple Campus | B.Sc. III Year | 2082")
print("=" * 64)
print(f"\n  Fitted slope (a)     = {a_w:.4f} ± {da_w:.4f} cm⁻¹")
print(f"  Intercept (ln N₀)    = {b_w:.4f} ± {db_w:.4f}")
print(f"\n  ┌─────────────────────────────────────────────────┐")
print(f"  │  µ (attenuation coeff.) = {mu:.4f} ± {mu_err:.4f} cm⁻¹  │")
print(f"  │  N₀ (initial counts)   = {N0:.2f} ± {N0_err:.2f}        │")
print(f"  └─────────────────────────────────────────────────┘")
print(f"\n  Goodness of fit")
print(f"    R²              = {r_value**2:.6f}")
print(f"    χ²_reduced      = {chi2_red:.4f}  (dof = {dof})")
print(f"    p-value (OLS)   = {p_value:.2e}")
print("=" * 64)

# ── 5. TABLE ─────────────────────────────────────────────────────────────────
df['ln_fit']   = a_w * x + b_w
df['residual'] = residuals

print("\n  DATA TABLE")
print(f"  {'x(mm)':>6}  {'N':>6}  {'σ_N':>6}  {'lnN':>7}  {'σ_lnN':>7}  "
      f"{'ln(fit)':>8}  {'resid':>7}")
print("  " + "-"*58)
for _, row in df.iterrows():
    print(f"  {row['thickness_mm']:>6.1f}  {row['counts']:>6.0f}  "
          f"{row['count_error']:>6.2f}  {row['ln_counts']:>7.4f}  "
          f"{row['ln_error']:>7.4f}  {row['ln_fit']:>8.4f}  "
          f"{row['residual']:>7.4f}")
print()

# ── 6. FIGURE ────────────────────────────────────────────────────────────────
x_fit  = np.linspace(0, 2.1, 400)
y_fit  = a_w * x_fit + b_w
N_fit  = np.exp(b_w) * np.exp(a_w * x_fit)

# Colour palette — dark academic / physics-lab aesthetic
BG      = '#0d1117'
PANEL   = '#161b22'
BORDER  = '#30363d'
GRID    = '#21262d'
BLUE    = '#58a6ff'
ORANGE  = '#f0883e'
GREEN   = '#56d364'
PURPLE  = '#bc8cff'
MUTED   = '#8b949e'
WHITE   = '#e6edf3'

fig = plt.figure(figsize=(14, 9), facecolor=BG)
gs  = gridspec.GridSpec(2, 2, figure=fig,
                        hspace=0.45, wspace=0.38,
                        left=0.09, right=0.95, top=0.91, bottom=0.09)

def style_ax(ax, title=''):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_edgecolor(BORDER)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.grid(True, color=GRID, linewidth=0.7, linestyle='--', alpha=0.8)
    if title:
        ax.set_title(title, color=WHITE, fontsize=11, fontweight='bold', pad=8)

# ── Panel 1 (top span): ln(N) vs x  — primary best-fit plot ─────────────────
ax1 = fig.add_subplot(gs[0, :])
ax1.errorbar(x, y, yerr=yerr,
             fmt='o', color=BLUE, ecolor=GREEN,
             capsize=4, capthick=1.3, markersize=7,
             linewidth=0, label='ln(N)  with propagated errors', zorder=5)
ax1.plot(x_fit, y_fit, color=ORANGE, linewidth=2.3,
         label=f'Weighted best fit: y = ({a_w:.4f}±{da_w:.4f})x + {b_w:.4f}', zorder=4)
ax1.fill_between(x_fit,
                 (a_w - da_w)*x_fit + (b_w - db_w),
                 (a_w + da_w)*x_fit + (b_w + db_w),
                 color=ORANGE, alpha=0.12, label='Uncertainty band (±σ)')

ann = (f'µ = {mu:.4f} ± {mu_err:.4f} cm⁻¹\n'
       f'N₀ = {N0:.1f} ± {N0_err:.1f}\n'
       f'R² = {r_value**2:.6f}\n'
       f'χ²_red = {chi2_red:.3f}   (dof = {dof})')
ax1.text(0.98, 0.96, ann, transform=ax1.transAxes,
         fontsize=9.5, va='top', ha='right',
         color=WHITE, fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#21262d',
                   edgecolor=ORANGE, alpha=0.92))

ax1.set_xlabel('Absorber Thickness  x  (cm)', fontsize=10)
ax1.set_ylabel('ln(N)  —  Natural log of counts', fontsize=10)
style_ax(ax1, 'Linearised Absorption: ln(N) vs x  |  Best Fit by Weighted Least Squares')
leg = ax1.legend(fontsize=9, facecolor=PANEL, edgecolor=BORDER)
for t in leg.get_texts():
    t.set_color(WHITE)

# ── Panel 2 (bottom-left): N vs x — exponential decay ───────────────────────
ax2 = fig.add_subplot(gs[1, 0])
ax2.errorbar(df['thickness_mm'], df['counts'], yerr=df['count_error'],
             fmt='s', color=BLUE, ecolor=GREEN, capsize=3, markersize=6,
             zorder=5, label='Observed counts')
ax2.plot(x_fit * 10, N_fit, color=ORANGE, lw=2,
         label='N₀·exp(−µx)', zorder=4)
ax2.set_xlabel('Absorber Thickness  (mm)', fontsize=9)
ax2.set_ylabel('Count rate  N', fontsize=9)
style_ax(ax2, 'Exponential Attenuation  N(x)')
leg2 = ax2.legend(fontsize=8.5, facecolor=PANEL, edgecolor=BORDER)
for t in leg2.get_texts():
    t.set_color(WHITE)

# ── Panel 3 (bottom-right): Residuals ────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 1])
ax3.errorbar(x, residuals, yerr=yerr,
             fmt='D', color=PURPLE, ecolor=GREEN,
             capsize=3, markersize=6, zorder=5, label='Residuals Δln(N)')
ax3.axhline(0, color=ORANGE, lw=1.5, linestyle='--', label='Zero line')
ax3.fill_between(x, -yerr, yerr, color=ORANGE, alpha=0.08, label='±1σ envelope')
ax3.set_xlabel('Absorber Thickness  x  (cm)', fontsize=9)
ax3.set_ylabel('Residual  Δln(N)', fontsize=9)
style_ax(ax3, 'Fit Residuals  (random scatter → good fit)')
leg3 = ax3.legend(fontsize=8.5, facecolor=PANEL, edgecolor=BORDER)
for t in leg3.get_texts():
    t.set_color(WHITE)

# ── Supertitle & footer ───────────────────────────────────────────────────────
fig.suptitle('Experiment 3 — Linear Absorption Coefficient (µ) via GM Counter',
             fontsize=14, fontweight='bold', color=WHITE, y=0.975)
fig.text(0.5, 0.003,
         'Tri-Chandra Multiple Campus · Department of Physics · B.Sc. III Year · 2082',
         ha='center', fontsize=8.5, color=MUTED)

fig.savefig('practical3_figure.png', dpi=180, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print("  Figure saved → practical3_figure.png")
print()
