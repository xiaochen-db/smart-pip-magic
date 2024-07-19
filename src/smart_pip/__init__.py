from IPython.core.magic import register_line_magic
import subprocess
from imports import get_imported_modules
from imports.analyze import _get_dists, _build_top_module_to_dep_map

from typing import Dict


def _dict_diff(d1, d2) -> Dict[str, any]:
    keys1 = set(d1.keys())
    keys2 = set(d2.keys())

    added = keys2 - keys1
    removed = keys1 - keys2
    modified = {k: (d1[k], d2[k]) for k in keys1 & keys2 if d1[k] != d2[k]}

    if not (added or removed or modified):
        return {}

    return {
        "added": {k: d2[k] for k in added},
        "removed": {k: d1[k] for k in removed},
        "modified": modified,
    }


@register_line_magic
def smart_pip(line):
    dists_snapshot = _get_dists()
    ret = subprocess.run(["pip"] + line.split(" "))
    if ret.returncode:
        print(f"Failed to run pip {line}. stdout: {ret.stdout} | stderr: {ret.stderr}")

    dists_delta = _dict_diff(dists_snapshot, _get_dists())

    if "added" in dists_delta:
        affected_modules = _build_top_module_to_dep_map(dists_delta["added"]).keys()
        imported_modules = set(get_imported_modules())
        modules_to_reimport = imported_modules & affected_modules
        if modules_to_reimport:
            return f'You should restart Python because the underlying files are updated for these dependencies: {','.join(modules_to_reimport)}'
    return ""
