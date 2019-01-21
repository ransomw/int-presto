#! /bin/sh

export PYTHONPATH=server:test:$PYTHONPATH

python -m unittest pi_test
