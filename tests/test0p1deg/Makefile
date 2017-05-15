################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/test0p1deg
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@echo "Running benchmark: $@"
	@echo "  Generating input data."
	@$(ACTIVATE) && $(MPIRUN) $(GENDATA) -p "$@." \
	-d 1,1800,3600,100 -v 10,0,1,2 -v 10,0,1,2,3 -n 120 > \
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


