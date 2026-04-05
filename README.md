# 🔬 B.Sc. Physics Practicals — Tri-Chandra Multiple Campus

**Department of Physics | B.Sc. III Year | Tribhuvan University | 2082**  
**Author:** Nabin Pandey | `nabin.795401@trc.tu.edu.np`  
**LinkedIn:** [nabinpandey1661](https://np.linkedin.com/in/nabinpandey1661)

---

This repository contains **clean, reproducible Python analyses** of physics laboratory experiments, built for portfolio use (Masters/PhD applications). Each practical includes:

- ✅ Weighted least-squares fitting with proper error propagation
- ✅ Publication-quality figures
- ✅ Jupyter notebooks with full theory, derivations, and discussion
- ✅ Standalone `.py` scripts

---

## 📂 Structure

```
physics-practicals/
│
├── practical3_gm_absorption/
│   ├── practical3_absorption.py       ← standalone script
│   ├── practical3_absorption.ipynb    ← full Jupyter notebook
│   ├── absorption_data.csv            ← raw data
│   └── practical3_figure.png          ← output figure
│
└── README.md
```

---

## Practical 3 — Linear Absorption Coefficient (µ)

**Instrument:** Geiger-Müller (GM) Counter  
**Objective:** Determine the linear absorption coefficient µ of radiation through a material.

### Physics

The Beer-Lambert exponential attenuation law:

$$N(x) = N_0 \cdot e^{-\mu x}$$

Linearised:

$$\ln N(x) = \ln N_0 - \mu \cdot x$$

GM counts follow **Poisson statistics** → σ_N = √N → σ_lnN = 1/√N.  
We use **Weighted Least Squares (WLS)** to account for heteroscedastic errors.

### Results

| Quantity | Value |
|---|---|
| µ (linear attenuation coefficient) | **1.5392 ± 0.0327 cm⁻¹** |
| N₀ (initial count rate) | **1042.5 ± 23.5** |
| R² | **0.9996** |
| χ²_reduced | **0.094** |
| Mean free path λ = 1/µ | **≈ 0.65 cm** |

### Figure

![Practical 3 Figure](practical3_gm_absorption/practical3_figure.png)

---

## 🛠 Requirements

```bash
pip install numpy pandas matplotlib scipy
```

Run any practical:
```bash
python practical3_absorption.py
```

Or open in Jupyter:
```bash
jupyter notebook practical3_absorption.ipynb
```

---

*More practicals (including Practical 24 — Natural Background Radiation & Gaussian Statistics) coming soon.*
