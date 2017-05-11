################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

ifndef MPIRUN
  export MPIRUN := $(shell which mpirun) -n 16
endif

ifndef RUNNAME
  export RUNNAME := default
endif

ifndef STRACE
  export STRACE := 0
endif

ifndef DEFLATE
  export DEFLATE := 0
endif

export HOSTNAME := $(shell hostname -s)
export EXECRUN := $(PREFIX)/sbin/execrun.sh $(PREFIX)/sbin/runtest.py
export ACTIVATE := source $(PREFIX)/venv/bin/activate

default: all

all: small	

.PHONY:	small

small:
	@$(MAKE) -C small
