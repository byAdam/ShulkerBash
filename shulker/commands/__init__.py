from os.path import dirname, basename, isfile, join
import glob

## Get all .py files
modules = glob.glob(join(dirname(__file__), "*.py"))

## Set __all__ variable to all py files that arent this file
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]