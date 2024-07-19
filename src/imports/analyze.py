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
    top_module_to_dist = _build_top_module_to_dist_map()
    for mod in get_imported_modules():
        if mod in top_module_to_dist:
            dist, version = top_module_to_dist[mod]
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


def _build_top_module_to_dist_map(
    dists: Set[str] = None,
) -> Dict[str, Tuple[str, str]]:
    """Returns a dict mapping top-level module names to a tuple of (dist name, version).

    dists -- the given dicts of the same format from _get_dists(). If not specified, we fetch from _get_dists()
    """
    top_module_to_dep = {}
    for dist_and_version in dists or _get_dists():
        dist, version = dist_and_version.split("-")
        for file_path in importlib.metadata.Distribution.from_name(dist).files:
            file_path = str(file_path)
            if file_path.endswith(".py"):
                top_module = file_path.split("/")[0]
                top_module_to_dep.update({top_module: (dist, version)})
    return top_module_to_dep
