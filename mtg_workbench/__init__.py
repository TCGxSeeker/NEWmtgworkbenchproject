"""Repository-root import shim for the src-layout package.

This lets root-level commands such as `python -m unittest discover -s tests`
import `mtg_workbench` without requiring a manual PYTHONPATH.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import extend_path


__path__ = extend_path(__path__, __name__)

_SRC_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "mtg_workbench"
if _SRC_PACKAGE.is_dir():
    _src_package = str(_SRC_PACKAGE)
    if _src_package not in __path__:
        __path__.append(_src_package)

__all__ = ["__version__"]
__version__ = "0.1.0"
