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

ifndef INPUT_ROOT
  export INPUT_ROOT := $(PREFIX)/tests
endif

ifndef OUTPUT_ROOT
  export OUTPUT_ROOT := $(PREFIX)/tests
endif

ifeq ($(BACKEND),nio)
  export FULLBACKEND := Nio
else
  export FULLBACKEND := netCDF4
endif

export HOSTNAME := $(shell hostname -s)
export EXECRUN := $(PREFIX)/sbin/execrun.sh $(PREFIX)/sbin/runtest.py -b $(FULLBACKEND) -d $(DEFLATE)
export GENDATA := $(PREFIX)/sbin/gendata.py
export ACTIVATE := source $(PREFIX)/venv/bin/activate
export CHECK := $(PREFIX)/sbin/checktest.py
export POST := $(PREFIX)/sbin/posttest.py

tdirs = $(sort $(dir $(wildcard */)))
tests = $(tdirs:%/=%)

default:

.PHONY:	logdir

logdir:
	@mkdir -p $(PREFIX)/logs

$(tests): logdir
	@cd $@ && \
	echo "Running benchmark: $@" && \
	echo "  Generating input data." && \
	source ./arguments.sh && \
	$(ACTIVATE) && $(MPIRUN) $(GENDATA) -o $(INPUT_ROOT)/$@/input -p "$@." $$GENARGS > \
	gendata.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log && \
	if [ ! -d $(OUTPUT_ROOT)/$@/output ]; then mkdir -p $(OUTPUT_ROOT)/$@/output; fi && \
	echo "  Running test." && \
	RUNLOG=reshaper.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log && \
	$(ACTIVATE) && $(MPIRUN) $(EXECRUN) -i $(INPUT_ROOT)/$@/input -o $(OUTPUT_ROOT)/$@/output -p "$@." --testname $@ --runname $(RUNNAME) --hostname $(HOSTNAME) > $$RUNLOG && \
	$(ACTIVATE) && $(CHECK) -o $(OUTPUT_ROOT)/$@/output -p "$@." $$GENARGS && \
	$(ACTIVATE) && $(POST) $$RUNLOG && \
	echo "  Copying logfiles." && \
	cp *.log $(PREFIX)/logs/ && \
	echo "  Done." && \
	unset GENARGS RUNLOG && \
	echo

cleantests:
	rm -rf */*.log
	rm -rf */*.s2s
	rm -rf $(INPUT_ROOT)/*/input
	rm -rf $(OUTPUT_ROOT)/*/output
	