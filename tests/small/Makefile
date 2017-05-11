################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/small
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

default: all

all: small

small:
	@echo "Running benchmark: $@"
	@echo "  Generating input data."
	@$(ACTIVATE) && \
	$(MPIRUN) $(GENDATA) -p $@ > gendata.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@if [ ! -d output ]; then mkdir output; fi
	@echo "  Running test."
	$(ACTIVATE) && \
	$(MPIRUN) $(EXECRUN) > reshaper.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@echo "  Copying logfiles."
	@cp *.log $(PREFIX)/logs/
	@echo "  Done."
	@echo
	
.PHONY:	small


