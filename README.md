# Smart pip magic
A alternative pip magic to jupyter's %pip. It shows if you need to restart python after %smart_pip install based on if existing imported modules are affected. 

## Install
```
pip install smart-pip-magic
```
## Usage
```
import smart_pip

%smart_pip install [opts] [list of package specifications]
```
