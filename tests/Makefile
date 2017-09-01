################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./Tests/
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

ifndef NPROCS
  export NPROCS := 40
endif

ifndef MPIRUN
  export MPIRUN := mpirun -n $(NPROCS)
endif

ifndef STRACE
  export STRACE := 0
endif

ifndef DEFLATE
  export DEFLATE := 0
endif

ifndef HOSTNAME
  export HOSTNAME := $(shell hostname)
endif

ifndef BACKEND
  export BACKEND := nc4
endif

ifndef RUNNAME
  export RUNNAME := $(HOSTNAME)-$(BACKEND)-N$(NPROCS)-D$(DEFLATE)-S$(STRACE)
endif

ifeq ($(BACKEND),nio)
  export FULLBACKEND := Nio
else
  export FULLBACKEND := netCDF4
endif

export HOSTNAME := $(shell hostname -s)
export EXECRUN := $(PREFIX)/sbin/execrun.sh $(PREFIX)/sbin/runtest.py -b $(FULLBACKEND) -d $(DEFLATE) -i input -o output 
export GENDATA := $(PREFIX)/sbin/gendata.py -o input
export ACTIVATE := source $(PREFIX)/venv/bin/activate
export CHECK := $(PREFIX)/sbin/checktest.py -o output
export POST := $(PREFIX)/sbin/posttest.py

dirs = $(sort $(dir $(wildcard */)))
tests = $(dirs:%/=%)

default:

.PHONY:	logdir

logdir:
	@mkdir -p $(PREFIX)/logs

$(tests): logdir
	include ./$@.test
	echo "Running benchmark: $@"
	echo "  Generating input data."
	$(ACTIVATE) && $(MPIRUN) $(GENDATA) -p "$@" $(GENARGS) > $(GENLOG)
	if [ ! -d output ]; then mkdir output; fi
	echo "  Running test."
	$(ACTIVATE) && $(MPIRUN) $(EXECRUN) -p "$@" $(RUNARGS) > $(RUNLOG)
	$(ACTIVATE) && $(CHECK) -p "$@" $(GENARGS)
	$(ACTIVATE) && $(POST) -l $(RUNLOG)
	echo "  Copying logfiles."
	cp *.log $(PREFIX)/logs/
	echo "  Done."
	echo
