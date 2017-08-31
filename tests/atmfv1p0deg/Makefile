################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/atmfv1p0deg
#
#  TEST:  Faux atmospheric 1.0-degree finite-volume dataset
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@echo "Running benchmark: $@"
	@echo "  Generating input data."
	@GENARGS="-d 1,25,192,288 -v 80,0,2,3 -v 40,0,1,2,3 -n 120"
	@GENLOG=gendata.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@$(ACTIVATE) && $(MPIRUN) $(GENDATA) -p "$@." $$GENARGS > $$GENLOG
	@if [ ! -d output ]; then mkdir output; fi
	@echo "  Running test."
	@RUNARGS="--testname $@  --runname $(RUNNAME) --hostname $(HOSTNAME)"
	@RUNLOG=reshaper.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log
	@$(ACTIVATE) && $(MPIRUN) $(EXECRUN) -p "$@." $$RUNARGS > $$RUNLOG
	@$(ACTIVATE) && $(CHECK) -p "$@." $$GENARGS
	@$(ACTIVATE) && $(POST) -l $$RUNLOG
	@echo "  Copying logfiles."
	@cp *.log $(PREFIX)/logs/
	@echo "  Done."
	@echo
	
.PHONY:	$(this)


