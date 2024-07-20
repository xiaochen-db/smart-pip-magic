import importlib
import sys


from typing import List, Dict, Tuple, Set

__all__ = ["get_imported_modules", "get_imported_3rd_party_modules"]


def get_imported_modules() -> List[str]:
    """Returns all imported modules."""
    return list(sys.modules.keys())


def get_imported_3rd_party_modules() -> Dict[str, Tuple[str, str]]:
    """Returns all 3rd-party imported modules and their associated (dist, version)"""
    result = {}
    module_to_dist = _build_module_to_dist_map()
    for mod in get_imported_modules():
        if mod in module_to_dist:
            dist, version = module_to_dist[mod]
            result.update({mod: (dist, version)})
    return result


def _get_dists() -> Set[str]:
    """Retruns a snapshot of the current available dist in form of '[name]-[version]'"""
    return set(
        map(
            lambda dist: f"{dist.name}-{dist.version}",
            importlib.metadata.distributions(),
        )
    )


def _build_module_to_dist_map(
    dists: Set[str] = None,
) -> Dict[str, Tuple[str, str]]:
    """Returns a dict mapping module names to a tuple of (dist name, version).

    dists -- the given dicts of the same format from _get_dists(). If not specified, we fetch from _get_dists()
    """
    module_to_dep = {}
    for dist_and_version in dists or _get_dists():
        dist, _, version = dist_and_version.rpartition("-")
        for file_path in importlib.metadata.Distribution.from_name(dist).files:
            file_path = str(file_path)
            mod = None
            if file_path.startswith(".."):
                continue
            if file_path.endswith("/__init__.py"):
                mod = file_path.removesuffix("/__init__.py").replace("/", ".")
            elif file_path.endswith(".py"):
                mod = file_path.removesuffix(".py").replace("/", ".")
            else:
                continue
            module_to_dep.update({mod: (dist, version)})
    return module_to_dep
