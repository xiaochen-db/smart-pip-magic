from IPython.core.magic import register_line_magic
import subprocess
from imports.analyze import (
    _get_dists,
    _build_module_to_dist_map,
    get_imported_modules,
)


__all__ = ["pip"]


@register_line_magic
def pip(line):
    """Jupyter line magic %smart_pip"""

    dists_snapshot = _get_dists()
    ret = subprocess.run(["pip"] + line.split(" "))
    if ret.returncode:
        print(f"Failed to run pip {line}. stdout: {ret.stdout} | stderr: {ret.stderr}")
        return

    added_dists = _get_dists() - dists_snapshot
    if added_dists:
        affected_modules = _build_module_to_dist_map(added_dists).keys()
        imported_modules = set(get_imported_modules())
        modules_to_reimport = imported_modules & affected_modules
        if modules_to_reimport:
            print(
                f'You should restart Python because the underlying files are updated for these imported modules: {", ".join(modules_to_reimport)}'
            )
