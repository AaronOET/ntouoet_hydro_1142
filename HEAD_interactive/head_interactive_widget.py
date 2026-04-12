"""
Steady 1-D Flow — Interactive Head Profile Widget

Visualises a linear head profile over a georeferenced background image
using ipywidgets and matplotlib/rasterio.

Usage (Jupyter / VS Code Interactive):
    %matplotlib inline
    from head_interactive_widget import HeadInteractiveWidget
    app = HeadInteractiveWidget()
    app.show()
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.errors import NotGeoreferencedWarning
from rasterio.plot import show as rasterio_show
import ipywidgets as widgets
from IPython.display import display


class HeadInteractiveWidget:
    # Fixed aquifer parameters
    L  = 1000   # aquifer length, m
    H  = 10     # saturated thickness, m
    zb = -5     # aquifer bottom elevation, m
    k  = 10     # hydraulic conductivity, m/d
    n  = 0.3    # porosity, -

    def __init__(
        self,
        image_path: str = "figs/fig1.2.jpg",
        output_path: str = "RAS/georef1.tif",
    ):
        self.image_path  = image_path
        self.output_path = output_path
        self.T = self.k * self.H          # transmissivity, m²/d
        self.x = np.linspace(0, self.L, 100)

        self._setup_raster()
        self._build_controls()

    # ------------------------------------------------------------------ #
    #  RASTER SETUP
    # ------------------------------------------------------------------ #
    def _setup_raster(self):
        """Georeference the background image and open the result."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", NotGeoreferencedWarning)
            unref = rasterio.open(self.image_path)

        point1 = rasterio.control.GroundControlPoint(col=58,  row=44,  x=0,    y=5)
        point2 = rasterio.control.GroundControlPoint(col=58,  row=151, x=0,    y=-5)
        point3 = rasterio.control.GroundControlPoint(col=497, row=151, x=1000, y=-5)
        transformation = rasterio.transform.from_gcps([point1, point2, point3])

        with rasterio.open(
            self.output_path, "w",
            driver="GTiff",
            height=unref.read(1).shape[0],
            width=unref.read(1).shape[1],
            count=3,
            dtype=unref.read(1).dtype,
            crs=rasterio.crs.CRS.from_epsg(4326),
            transform=transformation,
        ) as dst:
            dst.write(unref.read(1), 1)
            dst.write(unref.read(2), 2)
            dst.write(unref.read(3), 3)

        self.geo_raster = rasterio.open(self.output_path)

    # ------------------------------------------------------------------ #
    #  CONTROLS
    # ------------------------------------------------------------------ #
    def _build_controls(self):
        """Create sliders and wire up the interactive output."""
        slider_layout = widgets.Layout(width="400px")
        style = {"description_width": "80px"}

        self.slider_h0 = widgets.FloatSlider(
            value=6.0, min=-4.0, max=9.0, step=0.1,
            description="h0 (m):",
            style=style,
            layout=slider_layout,
            continuous_update=False,
        )
        self.slider_hL = widgets.FloatSlider(
            value=4.0, min=-4.0, max=9.0, step=0.1,
            description="hL (m):",
            style=style,
            layout=slider_layout,
            continuous_update=False,
        )

        self.ui = widgets.VBox([
            widgets.HTML("<b>Boundary Conditions</b>"),
            self.slider_h0,
            self.slider_hL,
        ])
        self.out = widgets.interactive_output(
            self._plot_head,
            {"h0": self.slider_h0, "hL": self.slider_hL},
        )

    # ------------------------------------------------------------------ #
    #  PLOT
    # ------------------------------------------------------------------ #
    def _plot_head(self, h0: float, hL: float):
        """Render the head profile for the given boundary conditions."""
        h = (hL - h0) * self.x / self.L + h0   # linear head profile

        fig, ax = plt.subplots(1, figsize=(12, 6))
        rasterio_show(self.geo_raster, ax=ax)

        ax.fill_between(self.x, h, self.zb, color="C1", alpha=0.5, label="Saturated zone")
        ax.plot(
            self.x, h,
            color="C1", linewidth=2,
            label=f"Head (h0={h0:.2f} m, hL={hL:.2f} m)",
        )

        ax.set_aspect(20)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("Elevation (m)")
        ax.set_title("Steady 1-D Flow with Constant Transmissivity")
        ax.legend(
            loc="upper left",
            bbox_to_anchor=(1.01, 1.0),
            borderaxespad=0.0,
            frameon=True,
            facecolor="white",
            framealpha=0.9,
            edgecolor="0.3",
        )
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(top=False, right=False)

        fig.subplots_adjust(right=0.86)
        plt.show()

    # ------------------------------------------------------------------ #
    #  PUBLIC
    # ------------------------------------------------------------------ #
    def show(self):
        """Display the widget."""
        display(self.ui, self.out)
