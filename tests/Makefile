################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./Tests/
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

ifndef TSIZE
  export TSIZE := 16
endif

ifndef MPIRUN
  export MPIRUN := mpirun -n $(TSIZE)
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
export EXECRUN := $(PREFIX)/sbin/execrun.sh $(PREFIX)/sbin/runtest.py -d $(DEFLATE) -i input -o output 
export GENDATA := $(PREFIX)/sbin/gendata.py -o input
export ACTIVATE := source $(PREFIX)/venv/bin/activate

dirs = $(sort $(dir $(wildcard */)))
tests = $(dirs:%/=%)

default:

.PHONY:	logdir

logdir:
	@mkdir -p $(PREFIX)/logs

$(tests): logdir
	@$(MAKE) -C $@
	