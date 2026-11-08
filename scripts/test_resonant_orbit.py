from pathlib import Path
import matplotlib.pyplot as plt

from orbit_gen.family import Family
from orbit_gen.setup.config import RunConfig

CONFIG_PATH = Path(__file__).resolve().parent.parent / "orbit_config.yaml"

cfg = RunConfig.from_yaml(CONFIG_PATH)
family = Family(cfg)

# Select only the first orbit
orbit = family.orbits[0]

orbit.propagate()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Convert time to days
times_days = orbit.times * (
    orbit.period_days / orbit.period
)

# Plot each 27-day interval separately
for i in range(5):
    mask = (times_days >= i*27.2) & (times_days <= (i+1)*27.2)

    ax.plot(
        orbit.states[mask, 0],
        orbit.states[mask, 1],
        orbit.states[mask, 2],
        label=f"Cycle {i+1}"
    )

ax.set_xlabel("X [DU]")
ax.set_ylabel("Y [DU]")
ax.set_zlabel("Z [DU]")
ax.legend()

plt.show()