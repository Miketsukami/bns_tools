# BnS tools

## Prerequisites

You should install python >= 3.7 to use this toolbox.

## animation.py

Tool that helps you to remove animations from your client.

Usage: `animation.py {remove,restore}`

You can provide settings in `Settings` class.

### Settings

* `BNS_ROOT` - path to your client installation

* `BACKUP_DIR` - path to your backup catalog
    
* `REMOVE_COMMON` - boolean flag: set True, if you want to remove common animations

* `REMOVE_SPECIALS` - list of tuples. First element of tuple is enum `Classes`, second is enum `Stages`
