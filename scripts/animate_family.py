import warnings
from pathlib import Path

import astropy.units as u
import matplotlib
import numpy as np
import spiceypy as spice
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d.art3d import Line3D
from scipy.optimize import root_scalar

from orbit_gen.setup.config import RunConfig
from orbit_gen.setup.system_config import CanonicalUnits, SystemConfig
from orbit_gen.utils import eom, units

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "orbit_config.yaml"
ANIMATION_DIR = ROOT / "animations"

MAX_ORBITS: int | None = None  # Animate at most this many orbits, evenly spaced
FRAMES_PER_ORBIT = 18
HOLD_FRAMES = 90  # Frames rotating the finished family at the end
FPS = 25  # Exact only if it divides 100 and is at most 50
DPI = 140
FIGSIZE = (8, 8)
COLORMAP = "viridis"
BG_COLOR = "black"
FG_COLOR = "white"

if 100 % FPS or FPS > 50:
    warnings.warn(
        f"FPS = {FPS} can't be stored exactly in a GIF, which uses whole hundredths "
        "of a second per frame. Use a divisor of 100 that is at most 50."
    )


def canonical_units(cfg: RunConfig) -> CanonicalUnits:
    """Canonical units of the configured system, computed the same way as Family

    Args:
        cfg (RunConfig):
            Run configuration providing the system and SPICE kernels.

    Returns:
        CanonicalUnits:
            Canonical distance and time units of the system.
    """
    for path in cfg.kernel_paths.values():
        spice.furnsh(str(path))

    system = cfg.system
    gm_primary = spice.bodvrd(system.primary, "GM", 1)[1][0]
    gm_secondary = spice.bodvrd(system.secondary, "GM", 1)[1][0]

    dist_km = system.canonical_units.dist_km
    time_seconds = np.sqrt(dist_km**3 / (gm_primary + gm_secondary))
    return CanonicalUnits(dist_km=dist_km, time_days=time_seconds / 86400)


def reference_points(system: SystemConfig, mu_star: float) -> dict[str, float]:
    """Positions of the collinear Lagrange points and the two bodies

    Finds L1, L2, and L3 as the roots of the x-acceleration of a particle at rest
    on the x-axis. All points lie on the x-axis (y = z = 0).

    Args:
        system (SystemConfig):
            CR3BP system, providing the body names.
        mu_star (float):
            CR3BP mass ratio.

    Returns:
        dict[str, float]:
            x-position of each point in canonical distance units (DU), keyed by
            name.
    """

    def ax_at_rest(x_rest: float) -> float:
        """x-acceleration of a particle at rest at (x_rest, 0, 0)."""
        return eom.crtbp_eom(0.0, [x_rest, 0.0, 0.0, 0.0, 0.0, 0.0], mu_star)[3]

    eps = 1e-8
    brackets = {
        "L1": (-mu_star + eps, 1 - mu_star - eps),
        "L2": (1 - mu_star + eps, 1 - mu_star + 3.0),
        "L3": (-mu_star - 3.0, -mu_star - eps),
    }
    points = {
        name: root_scalar(ax_at_rest, bracket=b).root for name, b in brackets.items()
    }
    points[system.primary] = -mu_star
    points[system.secondary] = 1 - mu_star
    return points


cfg = RunConfig.from_yaml(CONFIG_PATH)
cu = canonical_units(cfg)

if not cfg.output_path.exists():
    raise FileNotFoundError(
        f"Saved family at {cfg.output_path} does not exist. "
        "Please run scripts/generate_family.py to create it."
    )
data = np.load(cfg.output_path)
states = data["states"]
periods = data["periods"]
mu_star = float(data["mu_star"])

if MAX_ORBITS is not None and MAX_ORBITS < len(periods):
    idx = np.linspace(0, len(periods) - 1, MAX_ORBITS).round().astype(int)
    states, periods = states[idx], periods[idx]
n_orbits = len(periods)
periods_days = units.time_to_dimensional(periods, cu).to_value(u.day)

positions = []
reveal_ends = []
for i, (state, period) in enumerate(zip(states, periods)):
    orbit_states, times = eom.propagate([state[0], state[2], state[4], period], mu_star)
    positions.append(orbit_states[:, 0:3])
    # Number of points drawn at each reveal step, evenly spaced in time
    reveal_times = np.linspace(0, period, FRAMES_PER_ORBIT + 1)[1:]
    reveal_ends.append(np.searchsorted(times, reveal_times, side="right"))

    if cfg.verbose:
        print(f"Propagated orbit {i + 1}/{n_orbits}: {periods_days[i]:.4f} days")

# Cube centered on the family so all axes share one scale, padded 8% per side
all_positions = np.concatenate(positions)
center = (all_positions.min(axis=0) + all_positions.max(axis=0)) / 2
half_span = 0.58 * np.ptp(all_positions, axis=0).max()

# Skip the darkest end of the colormap so orbits stay visible
colors = matplotlib.colormaps[COLORMAP](0.35 + 0.65 * np.linspace(0, 1, n_orbits))
grid_color = (0.28, 0.28, 0.28)

# mplot3d reads its grid, axis line, and pane colors from rcParams on creation
plt.switch_backend("Agg")
with plt.rc_context(
    {
        "grid.color": grid_color,
        "grid.linewidth": 0.4,
        "axes.edgecolor": grid_color,
        "axes3d.xaxis.panecolor": (0, 0, 0, 0),
        "axes3d.yaxis.panecolor": (0, 0, 0, 0),
        "axes3d.zaxis.panecolor": (0, 0, 0, 0),
    }
):
    fig = plt.figure(figsize=FIGSIZE, facecolor=BG_COLOR)
    ax = fig.add_subplot(projection="3d")

fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=0.93)
fig.suptitle(cfg.ic.name.replace("_", " "), fontsize=12, color=FG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(center[0] - half_span, center[0] + half_span)
ax.set_ylim(center[1] - half_span, center[1] + half_span)
ax.set_zlim(center[2] - half_span, center[2] + half_span)
ax.set_box_aspect((1, 1, 1))
ax.set_xlabel("x [DU]", color=FG_COLOR)
ax.set_ylabel("y [DU]", color=FG_COLOR)
ax.set_zlabel("z [DU]", color=FG_COLOR)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_tick_params(colors=FG_COLOR, labelsize=8)

theta, phi = np.meshgrid(np.linspace(0, 2 * np.pi, 25), np.linspace(0, np.pi, 13))
unit_sphere = np.array(
    [np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)]
)

for name, x_ref in reference_points(cfg.system, mu_star).items():
    if np.all(np.abs(np.array([x_ref, 0.0, 0.0]) - center) <= half_span):
        ax.plot([x_ref], [0.0], [0.0], marker="+", color=FG_COLOR, ms=10, mew=1.5)
        ax.text(x_ref, 0.0, 0.0, f"  {name}", fontsize=8, color=FG_COLOR)

        if name in (cfg.system.primary, cfg.system.secondary):
            radius_km = spice.bodvrd(name, "RADII", 3)[1][0]
            radius = units.pos_to_canonical(radius_km * u.km, cu)
            x, y, z = radius * unit_sphere
            ax.plot_surface(x_ref + x, y, z, color=FG_COLOR, alpha=0.25, linewidth=0)

lines = [Line3D([], [], [], color=color, linewidth=2.8) for color in colors]
head = Line3D(
    [], [], [], marker="o", color=FG_COLOR, markersize=5, mec=BG_COLOR, mew=0.7
)
for line in [*lines, head]:
    ax.add_line(line)
hud = ax.text2D(
    0.02,
    0.96,
    "",
    transform=ax.transAxes,
    fontsize=8,
    family="monospace",
    color=FG_COLOR,
)


def update(frame: int) -> None:
    """Draw one animation frame

    Orbits before the active one are drawn in full and dimmed, the active orbit is
    drawn up to the current reveal step, and the camera rotates every frame.

    Args:
        frame (int):
            Frame index.
    """
    ax.view_init(elev=20, azim=-60 + 0.6 * frame)
    active, step = divmod(frame, FRAMES_PER_ORBIT)

    for line, r in zip(lines[:active], positions):
        line.set_data_3d(r[:, 0], r[:, 1], r[:, 2])
        line.set_alpha(0.65)
        line.set_linewidth(1.5)

    if active < n_orbits:
        r = positions[active][: reveal_ends[active][step]]
        lines[active].set_data_3d(r[:, 0], r[:, 1], r[:, 2])
        head.set_data_3d(r[-1:, 0], r[-1:, 1], r[-1:, 2])
        hud.set_text(
            f"orbit {active + 1}/{n_orbits}\n"
            f"period = {periods_days[active]:.3f} days"
        )
    else:
        head.set_data_3d([], [], [])
        hud.set_text(f"orbit {n_orbits}/{n_orbits} (complete)")


n_frames = n_orbits * FRAMES_PER_ORBIT + HOLD_FRAMES
if cfg.verbose:
    print(f"Rendering {n_frames} frames...")

ANIMATION_DIR.mkdir(parents=True, exist_ok=True)
output_path = ANIMATION_DIR / f"{cfg.ic.name}.gif"
anim = FuncAnimation(fig, update, frames=n_frames)
anim.save(output_path, writer=PillowWriter(fps=FPS), dpi=DPI)

print(f"Saved animation to {output_path}")
