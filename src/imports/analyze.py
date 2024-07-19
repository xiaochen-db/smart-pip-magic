import sys
import os

from typing import List, Dict, Tuple

__all__ = ["get_imported_modules", "get_imported_depdencies"]


def get_imported_modules() -> List[str]:
    return list(sys.modules.keys())


def get_imported_depdencies() -> Dict[str, any]:
    result = {}
    top_module_to_dep = _build_top_module_to_dep_map()
    for mod in get_imported_modules():
        if mod in top_module_to_dep:
            dep, version = top_module_to_dep[mod]
            result.update({mod: (dep, version)})
    return result


def _get_dists() -> Dict[str, str]:
    site_package_path = list(
        filter(lambda p: "site-packages" in p or "dist-packages" in p, sys.path)
    )[0]
    dist_info_folders = list(
        filter(lambda folder: "dist-info" in folder, os.listdir(site_package_path))
    )
    return dict(
        map(
            lambda folder: (
                folder.removesuffix(".dist-info"),
                f"{site_package_path}/{folder}",
            ),
            dist_info_folders,
        )
    )


def _build_top_module_to_dep_map(
    dists: Dict[str, str] = None,
) -> Dict[str, Tuple[str, str]]:
    top_module_to_dep = {}
    for dep_version, path in (dists or _get_dists()).items():
        dep, version = dep_version.split("-")
        with open(f"{path}/RECORD") as f:
            for line in f.readlines():
                source = line.strip().split(",")[0]
                if source.endswith(".py"):
                    top_module = source.split("/")[0]
                    top_module_to_dep.update({top_module: (dep, version)})
    return top_module_to_dep
