import subprocess
from IPython import get_ipython
from imports.analyze import (
    _get_dists,
    _build_module_to_dist_map,
    get_imported_modules,
)


__all__ = ["pip"]


ip = get_ipython()

# Try to preserve the original %pip behavior into run_pip
try:
    run_pip = ip.magics_manager.magics["line"]["pip"]
except KeyError:
    # If %pip is not ever registered, create a default one using subprocess
    def run_pip(line):
        ret = subprocess.run(["pip"] + line.split(" "))
        if ret.returncode:
            print(
                f"Failed to run pip {line}. stdout: {ret.stdout} | stderr: {ret.stderr}"
            )
            return


BLUE = "\033[94m"
RESET = "\033[0m"


def pip(line):
    """Jupyter line magic %smart_pip"""

    dists_snapshot = _get_dists()

    run_pip(line)

    added_dists = _get_dists() - dists_snapshot
    if added_dists:
        affected_modules = _build_module_to_dist_map(added_dists).keys()
        imported_modules = set(get_imported_modules())
        modules_to_reimport = imported_modules & affected_modules
        if modules_to_reimport:
            print(
                f'{BLUE}Note: You should restart Python because the underlying files are updated for these imported modules: {", ".join(modules_to_reimport)}{RESET}'
            )


# Register the smart %pip line magic and override the orignal one
ip.magics_manager.register_function(pip)
