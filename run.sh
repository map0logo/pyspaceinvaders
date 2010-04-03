#!/bin/sh
unset DYLD_LIBRARY_PATH  # fix Apple linker
exec python $* pyspaceinvaders.py
