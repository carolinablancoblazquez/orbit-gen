from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from platformdirs import user_cache_dir


@dataclass(frozen=True)
class KernelSpec:
    """A NAIF SPICE kernel file and its download URL

    Attributes:
        filename (str):
            Name of the kernel file in the cache directory
        url (str):
            URL the kernel is downloaded from

    """

    filename: str
    url: str


REQUIRED_KERNELS: tuple[KernelSpec, ...] = (
    KernelSpec(
        filename="naif0012.tls",
        url="https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    ),
    KernelSpec(
        filename="gm_de440.tpc",
        url="https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de440.tpc",
    ),
    KernelSpec(
        filename="pck00011.tpc",
        url="https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc",
    ),
)


def cache_dir() -> Path:
    """Return the kernel cache directory, creating it if needed

    Returns:
        direc (pathlib.Path):
            The `kernels` folder inside the platformdirs user cache directory for
            orbit-gen.
    """
    direc = Path(user_cache_dir("orbit-gen")) / "kernels"
    direc.mkdir(parents=True, exist_ok=True)
    return direc


def ensure_kernel(spec: KernelSpec) -> Path:
    """Return the cached path of a kernel, downloading it first if missing or empty

    Args:
        spec (KernelSpec):
            Kernel to look up or download.

    Returns:
        dest (pathlib.Path):
            Path of the kernel file in the cache directory.

    Raises:
        RuntimeError:
            If the download fails.
    """
    cache = cache_dir()
    dest = cache / spec.filename

    if dest.exists() and dest.stat().st_size > 0:
        return dest

    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with urlopen(spec.url, timeout=30) as resp, open(tmp, "wb") as f:
            f.write(resp.read())
    except URLError as e:
        raise RuntimeError(
            f"Failed to download {spec.filename} from {spec.url}: {e}"
        ) from e
    tmp.rename(dest)
    return dest


def ensure_kernels() -> dict[str, Path]:
    """Ensure all REQUIRED_KERNELS are cached, downloading any that are missing

    Returns:
        kernel_paths (dict[str, pathlib.Path]):
            Cached path of each required kernel, keyed by filename.
    """
    return {spec.filename: ensure_kernel(spec) for spec in REQUIRED_KERNELS}
