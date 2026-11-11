import astropy.units as u

from ..setup.system_config import CanonicalUnits


def time_to_canonical(dim_time, cu: CanonicalUnits):
    """Convert a dimensional time to canonical time units

    Args:
        dim_time (astropy.units.Quantity):
            Time in any astropy time unit.
        cu (CanonicalUnits):
            Canonical units of the system. `time_days` must be set.

    Returns:
        canonical_time (float or numpy.ndarray):
            Time in canonical time units (TU).
    """
    return dim_time.to("day").value / cu.time_days


def time_to_dimensional(canonical_time, cu: CanonicalUnits):
    """Convert a canonical time to days

    Args:
        canonical_time (float or numpy.ndarray):
            Time in canonical time units (TU).
        cu (CanonicalUnits):
            Canonical units of the system. `time_days` must be set.

    Returns:
        dim_time (astropy.units.Quantity):
            Time in days.
    """
    return canonical_time * cu.time_days * u.day


def pos_to_canonical(dim_pos, cu: CanonicalUnits):
    """Convert a dimensional position to canonical distance units

    Args:
        dim_pos (astropy.units.Quantity):
            Position in any astropy length unit.
        cu (CanonicalUnits):
            Canonical units of the system.

    Returns:
        canonical_pos (float or numpy.ndarray):
            Position in canonical distance units (DU).
    """
    return dim_pos.to("m").value / cu.du_m


def pos_to_dimensional(canonical_pos, cu: CanonicalUnits):
    """Convert a canonical position to meters

    Args:
        canonical_pos (float or numpy.ndarray):
            Position in canonical distance units (DU).
        cu (CanonicalUnits):
            Canonical units of the system.

    Returns:
        dim_pos (astropy.units.Quantity):
            Position in meters.
    """
    return canonical_pos * cu.du_m * u.m


def vel_to_canonical(dim_vel, cu: CanonicalUnits):
    """Convert a dimensional velocity to canonical velocity units

    Args:
        dim_vel (astropy.units.Quantity):
            Velocity in any astropy velocity unit.
        cu (CanonicalUnits):
            Canonical units of the system. `time_days` must be set.

    Returns:
        canonical_vel (float or numpy.ndarray):
            Velocity in canonical velocity units (DU/TU).
    """
    dim_vel_mpd = dim_vel.to("m/d").value
    return (dim_vel_mpd / cu.du_m) * cu.time_days


def vel_to_dimensional(canonical_vel, cu: CanonicalUnits):
    """Convert a canonical velocity to meters per day

    Args:
        canonical_vel (float or numpy.ndarray):
            Velocity in canonical velocity units (DU/TU).
        cu (CanonicalUnits):
            Canonical units of the system. `time_days` must be set.

    Returns:
        dim_vel (astropy.units.Quantity):
            Velocity in meters per day.
    """
    return canonical_vel * cu.du_m / cu.time_days * (u.m / u.day)
