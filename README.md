# Smart pip magic
A alternative pip magic to jupyter's %pip. It shows if you need to restart python after %pip install based on if existing imported modules are affected. 

## Install
```
pip install smart-pip-magic
```
## Usage
```
import smart_pip

%pip install [opts] [list of package specifications]
```

At the end of pip standard output, it will alert you if need to restart python and list all affected imported modules.
