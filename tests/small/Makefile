################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/small
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@GENARGS="-d 10,100 -v 20,0,1 -n 12"
	@GENLOG="gendata.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log"
	@RUNARGS="--testname $@  --runname $(RUNNAME) --hostname $(HOSTNAME)"
	@RUNLOG="reshaper.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log"
	@$(call run_test,$@,2,3,4,5)
	
.PHONY:	$(this)


