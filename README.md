# cs-server-runner


## installation
I suggest pyenv for running to avoid library conflicts, but you can do whatever

### pyenv
pyenv install: https://github.com/pyenv/pyenv#getting-pyenv
remember to update your bashrc, both for pyenv and pyenv-virtualenv

install python version
```
pyenv install 3.11.4
```

create virtual environment
```
pyenv virtualenv 3.11.4 cs-server-service
```

make sure you are in the project directory
then set local (`.python-version`) to virtual-env
```
pyenv local cs-server-service
```

if pyenv is setup correctly you should now be in the pyenv virtual environment and can install libraries freely
```
pyenv version
```

to setup with vscode or pycharm, change interpreter to 
```
~/.pyenv/versions/3.11.4/envs/cs-server-service-bin/python
```

### requirements
TODO
