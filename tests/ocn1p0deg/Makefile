################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/ocn1p0deg
#
#  TEST:  Faux ocean 1.0-degree dataset
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@echo "Running benchmark: $@"
	@echo "  Generating input data."
	@$(ACTIVATE) && $(MPIRUN) $(GENDATA) -p "$@." \
	-d 1,5,50,320,384 -v 30 -v 5,1,3 -v 20,3,4 -v 55,0,3,4 -v 55,0,2,3,4 -n 64 > \
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


