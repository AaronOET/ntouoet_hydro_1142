# Steady 1-D Flow — Interactive Head Profile
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AaronOET/ntouoet_hydro_1142/HEAD?urlpath=%2Fdoc%2Ftree%2FHEAD_interactive%2FHEAD_interactive.ipynb)

Interactive visualisation of a steady-state, one-dimensional groundwater head profile
over a georeferenced cross-section image.
Based on **Chapter 1** of *Analytical Groundwater Modeling* (Bakker & Post).

## Physics

For steady 1-D flow with constant transmissivity and no recharge, the head varies
linearly between the two boundary heads:

```
h(x) = h0 + (hL - h0) · x / L
```

| Symbol | Description | Value |
|--------|-------------|-------|
| `L`    | Aquifer length | 1000 m |
| `H`    | Saturated thickness | 10 m |
| `zb`   | Aquifer bottom elevation | −5 m |
| `k`    | Hydraulic conductivity | 10 m/d |
| `T`    | Transmissivity (`k · H`) | 100 m²/d |
| `n`    | Porosity | 0.3 |

## Usage

Open `HEAD_interactive.ipynb` and run all cells:

```python
%matplotlib inline
from head_interactive_widget import HeadInteractiveWidget

app = HeadInteractiveWidget()
app.show()
```

Use the **h0** and **hL** sliders to set the left and right boundary heads.
The plot updates to show the linear head profile and the saturated zone overlaid
on the cross-section background image.

## Files

```
HEAD_interactive.ipynb       # Notebook — import and run the widget
head_interactive_widget.py   # Widget class (all major code lives here)
figs/
    fig1.2.jpg               # Source cross-section image (unreferenced)
RAS/
    georef1.tif              # Georeferenced GeoTIFF written on first run
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