import sys
import os

from typing import List, Dict, Tuple

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


def _get_dists() -> Dict[str, str]:
    """Retruns a dict snapshotting the current state from dist names to their .dist-info absolute paths."""
    dist_infos = []
    for path in sys.path:
        if os.path.isdir(path):
            dist_infos += list(
                map(
                    lambda base_name: (base_name, path),
                    filter(lambda folder: "dist-info" in folder, os.listdir(path)),
                )
            )
    return dict(
        map(
            lambda dist_info_path: (
                dist_info_path[0].removesuffix(".dist-info"),
                f"{dist_info_path[1]}/{dist_info_path[0]}",
            ),
            dist_infos,
        )
    )


def _build_top_module_to_dist_map(
    dists: Dict[str, str] = None,
) -> Dict[str, Tuple[str, str]]:
    """Returns a dict mapping top-level module names to a tuple of (dist name, version).

    dists -- the given dict of the same format from _get_dists(). If not specified, we fetch from _get_dists()
    """
    top_module_to_dep = {}
    for dist_and_version, path in (dists or _get_dists()).items():
        dist, version = dist_and_version.split("-")
        with open(f"{path}/RECORD") as f:
            for line in f.readlines():
                source = line.strip().split(",")[0]
                if source.endswith(".py"):
                    top_module = source.split("/")[0]
                    top_module_to_dep.update({top_module: (dist, version)})
    return top_module_to_dep
