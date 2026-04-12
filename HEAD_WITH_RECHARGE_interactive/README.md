# Steady 1-D Flow with Areal Recharge — Interactive Head Profile
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AaronOET/ntouoet_hydro_1142/HEAD?urlpath=%2Fdoc%2Ftree%2FHEAD_WITH_RECHARGE_interactive%2FHEAD_WITH_RECHARGE_interactive.ipynb)

Interactive visualisation of a steady-state, one-dimensional groundwater head profile
with areal recharge, overlaid on a georeferenced cross-section image.
Based on **Chapter 1** of *Analytical Groundwater Modeling* (Bakker & Post).

## Physics

For steady 1-D flow with constant transmissivity and uniform areal recharge, the head
follows a parabolic profile:

```
h(x) = -N/(2T) · (x² - L·x) + (hL - h0) · x/L + h0
```

The horizontal discharge at any cross-section is:

```
Qx(x) = N·(x - L/2) - T·(hL - h0)/L
```

| Symbol | Description | Value |
|--------|-------------|-------|
| `L`    | Aquifer length | 1000 m |
| `H`    | Saturated thickness | 10 m |
| `zb`   | Aquifer bottom elevation | −5 m |
| `k`    | Hydraulic conductivity | 10 m/d |
| `T`    | Transmissivity (`k · H`) | 100 m²/d |
| `N`    | Areal recharge rate | m/d (slider) |

## Usage

Open `HEAD_WITH_RECHARGE_interactive.ipynb` and run all cells:

```python
%matplotlib inline
from head_with_recharge_widget import HeadWithRechargeWidget

app = HeadWithRechargeWidget()
app.show()
```

Use the **h0**, **hL**, and **N** sliders to set the left and right boundary heads and
the recharge rate. The plot updates to show the parabolic head profile, the saturated
zone, and the discharge into each boundary river, all overlaid on the cross-section
background image.

## Files

```
HEAD_WITH_RECHARGE_interactive.ipynb   # Notebook — import and run the widget
head_with_recharge_widget.py           # Widget class (all major code lives here)
figs/
    fig1.2.jpg                         # Source cross-section image (unreferenced)
RAS/
    georef1.tif                        # Georeferenced GeoTIFF written on first run
```

## Requirements

```
numpy
matplotlib
rasterio
ipywidgets
```

Install with conda (recommended):

```bash
conda install numpy matplotlib rasterio ipywidgets
```

or with pip:

```bash
pip install numpy matplotlib rasterio ipywidgets
```

> **Note:** `ipywidgets` also requires the notebook extension to be enabled.
> In JupyterLab this is bundled; in classic Notebook run
> `jupyter nbextension enable --py widgetsnbextension`.
