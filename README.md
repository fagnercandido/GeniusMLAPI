# GeniusMLAPI
PyPI package to use Genius.
## Getting Started
#### Dependencies
You need Python 3.7 or later to use **geniusmlapi**. You can find it at [python.org](https://www.python.org/).
You also need setuptools, wheel and twine packages, which is available from [PyPI](https://pypi.org). If you have pip, just run:
```
pip install setuptools
pip install wheel
pip install twine
```
#### Installation
Clone this repo to your local machine using:
```
git clone https://github.com/fagnercandido/GeniusMLAPI
```
## Features
- File structure for PyPI packages
- Setup with package informations
- License example

## Running
```
pip install geniusmlapi
```

And then

```
from geniusmlapi import gml
```

Finally:
```
genius = gml.GeniusLM(ACCESS_TOKEN)
songs = genius.search('my search')
dataframe = genius.get_dataframe(songs)
dataframe.head()
```




