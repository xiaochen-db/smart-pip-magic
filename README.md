# Smart pip magic
A alternative pip magic to jupyter's %pip. It shows if you need to restart python after %pip install based on if existing imported modules are affected. 

## Install
```
pip install smart-pip-magic
```
## Usage
Enable smart pip:
```
import smart_pip
%pip install [opts] [list of package specifications]
```

At the end of pip standard output, it will alert you if need to restart python and list all affected imported modules.


Add action hook to act on affected imported modules by the end of %pip install. If no such module is found, hooks are not invoked. 

```
import smart_pip
def hook(modules_whose_files_changed: Callable[[List[str]], None]) -> None:
    print('hook called on ' + str(modules_whose_files_changed))
smart_pip.add_reload_hook(hook)
```

## Testing
```
pip install .[dev]
pytest
```
