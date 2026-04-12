"""
Steady 1-D Flow with Areal Recharge — Interactive Head Profile

Usage:
    Run in a Jupyter-compatible environment (JupyterLab, VS Code interactive, etc.):
        %matplotlib inline
        from head_with_recharge_widget import HeadWithRechargeWidget
        app = HeadWithRechargeWidget()
        app.show()
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.errors import NotGeoreferencedWarning
from rasterio.plot import show
import ipywidgets as widgets
from IPython.display import display


class HeadWithRechargeWidget:
    def __init__(
        self,
        image_path: str = "figs/fig1.2.jpg",
        georef_path: str = "RAS/georef1.tif",
        L: float = 1000,
        H: float = 10,
        zb: float = -5,
        k: float = 10,
    ):
        """
        Parameters
        ----------
        image_path  : path to the background cross-section image
        georef_path : path where the georeferenced GeoTIFF is written / read
        L           : aquifer length (m)
        H           : saturated thickness (m)
        zb          : aquifer bottom elevation (m)
        k           : hydraulic conductivity (m/d)
        """
        self.image_path = image_path
        self.georef_path = georef_path

        # Fixed aquifer parameters
        self.L = L
        self.H = H
        self.zb = zb
        self.k = k
        self.T = k * H          # transmissivity, m²/d
        self.x = np.linspace(0, L, 200)

        self._setup_georaster()
        self._build_controls()

    # ------------------------------------------------------------------ #
    #  GEORASTER SETUP
    # ------------------------------------------------------------------ #
    def _setup_georaster(self):
        """Georeference the background image once and cache as a GeoTIFF."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", NotGeoreferencedWarning)
            unref = rasterio.open(self.image_path)

        point1 = rasterio.control.GroundControlPoint(col=58,  row=44,  x=0,    y=5)
        point2 = rasterio.control.GroundControlPoint(col=58,  row=151, x=0,    y=-5)
        point3 = rasterio.control.GroundControlPoint(col=497, row=151, x=1000, y=-5)
        transform = rasterio.transform.from_gcps([point1, point2, point3])

        with rasterio.open(
            self.georef_path, "w",
            driver="GTiff",
            height=unref.read(1).shape[0],
            width=unref.read(1).shape[1],
            count=3,
            dtype=unref.read(1).dtype,
            crs=rasterio.crs.CRS.from_epsg(4326),
            transform=transform,
        ) as dst:
            dst.write(unref.read(1), 1)
            dst.write(unref.read(2), 2)
            dst.write(unref.read(3), 3)

        self.georaster = rasterio.open(self.georef_path)

    # ------------------------------------------------------------------ #
    #  CONTROLS
    # ------------------------------------------------------------------ #
    def _build_controls(self):
        slider_kw = dict(
            style={"description_width": "80px"},
            layout=widgets.Layout(width="400px"),
            continuous_update=False,
        )
        self.slider_h0 = widgets.FloatSlider(
            value=6.0, min=-4.0, max=9.0, step=0.1,
            description="h0 (m):",
            **slider_kw,
        )
        self.slider_hL = widgets.FloatSlider(
            value=4.0, min=-4.0, max=9.0, step=0.1,
            description="hL (m):",
            **slider_kw,
        )
        self.slider_N = widgets.FloatSlider(
            value=0.001, min=0.0, max=0.005, step=0.0001,
            description="N (m/d):",
            readout_format=".4f",
            **slider_kw,
        )

        self.ui = widgets.VBox([
            widgets.HTML("<b>Boundary Conditions &amp; Recharge</b>"),
            self.slider_h0,
            self.slider_hL,
            self.slider_N,
        ])

        self.out = widgets.interactive_output(
            self._plot_head,
            {"h0": self.slider_h0, "hL": self.slider_hL, "N": self.slider_N},
        )

    # ------------------------------------------------------------------ #
    #  PLOT
    # ------------------------------------------------------------------ #
    def _plot_head(self, h0: float, hL: float, N: float):
        """Analytical solution callback invoked by interactive_output."""
        x, L, T, zb = self.x, self.L, self.T, self.zb

        # Parabolic head profile with areal recharge
        h  = -N / (2 * T) * (x**2 - L * x) + (hL - h0) * x / L + h0
        Qx =  N * (x - L / 2) - T * (hL - h0) / L

        fig, ax = plt.subplots(figsize=(12, 6))
        show(self.georaster, ax=ax)

        ax.fill_between(x, h, zb, color="C1", alpha=0.5, label="Saturated zone")
        ax.plot(
            x, h, color="C1", linewidth=2,
            label=f"Head (h0={h0:.2f} m, hL={hL:.2f} m, N={N:.4f} m/d)",
        )

        ax.set_aspect(20)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("Elevation (m)")
        ax.set_title("Steady 1-D Flow with Areal Recharge")
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

        # Discharge annotations
        q_left  = -Qx[0]
        q_right =  Qx[-1]
        ax.annotate(
            f"Q into left river\n{q_left:.3f} m²/d",
            xy=(0, h[0]), xytext=(60, h[0] + 0.6),
            fontsize=8, color="C0",
            arrowprops=dict(arrowstyle="->", color="C0", lw=1.2),
        )
        ax.annotate(
            f"Q into right river\n{q_right:.3f} m²/d",
            xy=(L, h[-1]), xytext=(L - 200, h[-1] + 0.6),
            fontsize=8, color="C2",
            arrowprops=dict(arrowstyle="->", color="C2", lw=1.2),
        )

        fig.subplots_adjust(right=0.86)
        plt.show()

    # ------------------------------------------------------------------ #
    #  PUBLIC
    # ------------------------------------------------------------------ #
    def show(self):
        """Display the interactive widget."""
        display(self.ui, self.out)
