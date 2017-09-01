################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./tests/small
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

include ../Makefile.run_test

this = $(notdir $(shell pwd))

default: $(this)

$(this):
	@$(call run_test, "-d 10,100 -v 20,0,1 -n 12", "gendata.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log", "--testname $@ --runname $(RUNNAME) --hostname $(HOSTNAME)", "reshaper.$@.$(RUNNAME).$(HOSTNAME).$(shell date +%Y%m%d%H%M%S).log")
	
.PHONY:	$(this)


