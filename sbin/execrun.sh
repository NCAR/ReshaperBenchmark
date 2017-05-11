#!/bin/sh
if [ $STRACE -ne 0 ]; then
	BASENAME=$(basename $PWD)
	TIMESTAMP=$(date +%Y%m%d%H%M%S)	
	STRACELOG=$BASENAME.$RUNNAME.$HOSTNAME.$TIMESTAMP.$$.strace
	CMD="strace -tt -T -o $STRACELOG $@"
else
	CMD="$@"
fi

exec $CMD
