import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Higher-quality defaults for all figures
DEFAULT_DPI = 300
plt.rcParams["figure.dpi"] = 100  # on-screen/preview only; savefig uses DEFAULT_DPI explicitly
plt.rcParams["font.size"] = 10
plt.rcParams["axes.linewidth"] = 0.8


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def _grid_shape(n):
    if n <= 0:
        raise ValueError("n must be greater than 0")
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return rows, cols


def _make_axes(n, figsize_per_plot=(5, 4), sharey=False, sharex=False):
    rows, cols = _grid_shape(n)
    fig, axes = plt.subplots(
        rows, cols,
        figsize=(figsize_per_plot[0] * cols, figsize_per_plot[1] * rows),
        squeeze=False,
        sharey=sharey,
        sharex=sharex,
    )
    return fig, list(axes.flat)


# ---------------------------------------------------------------------------
# Histograms
# ---------------------------------------------------------------------------

def plot_histograms(results, save_path=None, bins=30, density=True):
    """
    Plot the distribution of generated values.

    density=True (default) normalizes each histogram to a probability
    density, so generators with very different sample counts per bin
    (e.g. non_coprime collapsing into fewer distinct values) are still
    comparable on the same y-scale. Set density=False for raw counts.
    """
    if not results:
        return

    fig, axes = _make_axes(len(results), sharey=density)

    for ax, (name, values) in zip(axes, results.items()):
        if max(values, default=0) > 1 or min(values, default=0) < 0:
            raise ValueError(f"{name}: expected normalized values in [0,1)")

        ax.hist(
            values, bins=bins, range=(0, 1), density=density,
            color="steelblue", edgecolor="black", linewidth=0.4,
        )
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Generated value")
        ax.set_ylabel("Density" if density else "Frequency")
        ax.set_xlim(0, 1)
        ax.grid(axis="y", alpha=0.2)

        if density:
            ax.axhline(1.0, color="red", linewidth=0.7, linestyle="--", alpha=0.6)

    _finish(fig, axes, len(results), save_path, suptitle="Value Distribution")


# ---------------------------------------------------------------------------
# Lag scatter plots
# ---------------------------------------------------------------------------

def plot_lag_scatter(results, lag=1, save_path=None, point_size=1.5):
    if not results:
        return
    if lag <= 0:
        raise ValueError("lag must be greater than 0")

    fig, axes = _make_axes(len(results), sharey=True, sharex=True)

    for ax, (name, values) in zip(axes, results.items()):
        if len(values) <= lag:
            ax.text(0.5, 0.5, "Not enough data", ha="center", va="center",
                     transform=ax.transAxes)
        else:
            ax.scatter(
                values[:-lag], values[lag:],
                s=point_size, alpha=0.35, color="darkorange", edgecolors="none",
                rasterized=True,  # keeps file size sane at high dpi with many points
            )
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Value at n")
        ax.set_ylabel(f"Value at n + {lag}")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.grid(alpha=0.2)

    _finish(fig, axes, len(results), save_path,
            suptitle=f"Lag-{lag} Correlation: x[n] vs x[n + {lag}]")


# ---------------------------------------------------------------------------
# 3D lag scatter (for RANDU-style plane structure)
# ---------------------------------------------------------------------------

def plot_lag_scatter_3d(results, save_path=None, point_size=2, elev=20, azim=45):
    """
    Plot (x[n], x[n+1], x[n+2]) triples in 3D.

    Some generators (notably RANDU) look fine in 2D lag plots but collapse
    onto a small number of parallel planes when viewed in 3D. Rotate elev/
    azim if the planes aren't visible from the default angle.
    """
    if not results:
        return

    n = len(results)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    fig = plt.figure(figsize=(5.5 * cols, 5 * rows))

    for i, (name, values) in enumerate(results.items(), start=1):
        ax = fig.add_subplot(rows, cols, i, projection="3d")
        if len(values) <= 2:
            ax.text2D(0.5, 0.5, "Not enough data", ha="center", va="center",
                        transform=ax.transAxes)
            continue
        ax.scatter(
            values[:-2], values[1:-1], values[2:],
            s=point_size, alpha=0.5, color="crimson", edgecolors="none",
            rasterized=True,
        )
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.set_xlabel("x[n]", fontsize=8)
        ax.set_ylabel("x[n+1]", fontsize=8)
        ax.set_zlabel("x[n+2]", fontsize=8)
        ax.view_init(elev=elev, azim=azim)
        ax.tick_params(labelsize=7)

    fig.suptitle("3D Lag Structure: (x[n], x[n+1], x[n+2])", fontsize=16, fontweight="bold")
    fig.tight_layout(rect=(0.02, 0.02, 0.98, 0.95))

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=DEFAULT_DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)
    else:
        plt.show()


# ---------------------------------------------------------------------------
# Sequence plots
# ---------------------------------------------------------------------------

def plot_sequence(results, n=200, save_path=None, autoscale_y=True):
    """
    Plot the first n generated values.

    autoscale_y=True (default) lets each subplot use its own y-range,
    so slow-mixing generators (e.g. near-identity multiplier LCGs, whose
    values barely move over n samples) are actually visible instead of
    flatlining against a shared [0,1] axis.
    """
    if not results:
        return
    if n <= 0:
        raise ValueError("n must be greater than 0")

    fig, axes = _make_axes(len(results), sharey=not autoscale_y)

    for ax, (name, values) in zip(axes, results.items()):
        displayed = values[:n]
        ax.plot(displayed, linewidth=0.9, color="seagreen")
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Sample index")
        ax.set_ylabel("Generated value")
        if not autoscale_y:
            ax.set_ylim(0, 1)
        ax.grid(alpha=0.2)

    _finish(fig, axes, len(results), save_path, suptitle=f"Generated Sequence (first {n} values)")


# ---------------------------------------------------------------------------
# Figure finishing / saving
# ---------------------------------------------------------------------------

def _finish(fig, axes, n_used, save_path, suptitle=None):
    for ax in axes[n_used:]:
        ax.axis("off")

    if suptitle:
        fig.suptitle(suptitle, fontsize=16, fontweight="bold", y=0.995)

    fig.tight_layout(rect=(0.02, 0.02, 0.98, 0.95))

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=DEFAULT_DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)
    else:
        plt.show()
