################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/ocn0p1deg
#
#  TEST:  Faux ocean 0.1-degree dataset
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@echo "Running benchmark: $@"
	@echo "  Generating input data."
	@$(ACTIVATE) && $(MPIRUN) $(GENDATA) -p "$@." \
	-d 1,60,2400,3600 -v 30 -v 20,2,3 -v 20,0,2,3 -v 10,0,1,2,3 -n 120 > \
	gendata.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@if [ ! -d output ]; then mkdir output; fi
	@echo "  Running test."
	@$(ACTIVATE) && $(MPIRUN) $(EXECRUN) -p "$@." \
	--testname $@  --runname $(RUNNAME) --hostname $(HOSTNAME) > \
	reshaper.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@echo "  Copying logfiles."
	@cp *.log $(PREFIX)/logs/
	@echo "  Done."
	@echo
	
.PHONY:	$(this)


