[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/isaacksdata/dictionary-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/isaacksdata/dictionary-tools)
![unit tests](https://github.com/isaacksdata/dictionary-tools/actions/workflows/unit_tests.yml/badge.svg)
[![DeepSource](https://app.deepsource.com/gh/isaacksdata/dictionary-tools.svg/?label=active+issues&show_trend=true&token=VPCHdTjz3W_pzGOGCfPp9Xvs)](https://app.deepsource.com/gh/isaacksdata/dictionary-tools/?ref=repository-badge)
[![DeepSource](https://app.deepsource.com/gh/isaacksdata/dictionary-tools.svg/?label=resolved+issues&show_trend=true&token=VPCHdTjz3W_pzGOGCfPp9Xvs)](https://app.deepsource.com/gh/isaacksdata/dictionary-tools/?ref=repository-badge)

# Dictionary Tools  

Documentation -> https://isaacksdata.github.io/dictionary-tools/

## Dictionary Structure  

This repo includes tools for understanding the structure of a dictionary data structure.   
For example, you might want to know what types the keys and values are, or how many elements an iterable has.   


## CommentedDict  

This repo also has the CommentedDict data type. This is a sub class of collections.UserDict which allows 
a comment to be added to describe the dictionary.   
The commentedDict is can also handle CommentedKeys and CommentedValues which allow comments to be added for 
individual key:value pairs.   