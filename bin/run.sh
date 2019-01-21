#! /bin/sh

export PYTHONPATH=server:$PYTHONPATH

python bin/init.py $*
