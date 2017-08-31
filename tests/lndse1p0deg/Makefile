################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/lndse1p0deg
#
#  TEST:  Faux land-model 1.0-degree spectral-element dataset
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@echo "Running benchmark: $@"
	@echo "  Generating input data."
	@$(ACTIVATE) && $(MPIRUN) $(GENDATA) -p "$@." \
	-d 1,15,48600 -v 290,0,2 -v 5,1,2 -v 5,0,1,2 -n 120 > \
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


