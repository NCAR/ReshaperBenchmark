################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

default: all

all: small 

small:
	@echo "Running benchmark: $@"
	$(MPIRUN) $(PREFIX)/sbin/gendata.py -o input
	@if [ ! -d output ]; then mkdir output; fi
	@$(ACTIVATE) && \
	$(MPIRUN) $(EXECRUN) > $(shell echo $@).$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@echo "  Copying logfile."
	@cp *.log $(PREFIX)/logs/
	@echo "  Done."
	@echo
	
.PHONY:	small


