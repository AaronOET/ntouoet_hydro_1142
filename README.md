# Interactive Groundwater Head Profiles

Interactive Jupyter notebook widgets for visualising steady-state, one-dimensional
groundwater flow, based on analytical solutions from *Analytical Groundwater Modeling*
(Bakker & Post).

---

## Notebooks

### 1. Steady 1-D Flow — No Recharge

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AaronOET/ntouoet_hydro_1142/HEAD?urlpath=%2Fdoc%2Ftree%2FHEAD_interactive%2FHEAD_interactive.ipynb)

Located in [HEAD_interactive/](HEAD_interactive/)

Adjust the left (`h0`) and right (`hL`) boundary heads with sliders to see the
resulting linear head profile and saturated zone overlaid on a georeferenced
aquifer cross-section.

**Analytical solution:**

```
h(x) = h0 + (hL − h0) · x / L
```

---

### 2. Steady 1-D Flow — With Areal Recharge

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AaronOET/ntouoet_hydro_1142/HEAD?urlpath=%2Fdoc%2Ftree%2FHEAD_WITH_RECHARGE_interactive%2FHEAD_WITH_RECHARGE_interactive.ipynb)

Located in [HEAD_WITH_RECHARGE_interactive/](HEAD_WITH_RECHARGE_interactive/)

Adjust `h0`, `hL`, and the uniform areal recharge rate `N` to see the parabolic
head profile, the saturated zone, and the computed discharge into each boundary
river.

**Analytical solution:**

```
h(x)  = −N/(2T) · (x² − L·x) + (hL − h0) · x/L + h0
Qx(x) =  N·(x − L/2) − T·(hL − h0)/L
```

---

## Aquifer Parameters

| Symbol | Description | Default value |
|--------|-------------|---------------|
| `L`    | Aquifer length | 1000 m |
| `H`    | Saturated thickness | 10 m |
| `zb`   | Aquifer bottom elevation | −5 m |
| `k`    | Hydraulic conductivity | 10 m/d |
| `T = k·H` | Transmissivity | 100 m²/d |
| `N`    | Areal recharge rate | m/d (slider) |

---

## Repository Structure

```
ntouoet_hydro_1142/
├── HEAD_interactive/
│   ├── HEAD_interactive.ipynb       # Notebook (no recharge)
│   ├── head_interactive_widget.py   # Widget class
│   ├── figs/fig1.2.jpg              # Background cross-section image
│   └── RAS/georef1.tif              # Georeferenced GeoTIFF (auto-generated)
├── HEAD_WITH_RECHARGE_interactive/
│   ├── HEAD_WITH_RECHARGE_interactive.ipynb   # Notebook (with recharge)
│   ├── head_with_recharge_widget.py           # Widget class
│   ├── figs/fig1.2.jpg                        # Background cross-section image
│   └── RAS/georef1.tif                        # Georeferenced GeoTIFF (auto-generated)
└── requirements.txt
```

---

## Installation

It is recommended to use conda:

```bash
conda install numpy matplotlib rasterio ipywidgets
```

or with pip:

```bash
pip install -r requirements.txt
```

> **Note:** `ipywidgets` requires the notebook extension to be enabled.
> In JupyterLab this is bundled; in classic Notebook run:
> ```bash
> jupyter nbextension enable --py widgetsnbextension
> ```

---

## Citation

The analytical solutions, aquifer cross-section background images (`fig1.2.jpg`), and
conceptual framework used in these notebooks are based on:

> Bakker, M., & Post, V. (2022). *Analytical Groundwater Modeling: Theory and
> Applications using Python*. CRC Press / Taylor & Francis.
> ISBN 978-1-032-00982-1

The background images reproduced in the widgets are taken from Figure 1.2 of that
book and are used here for educational purposes.
