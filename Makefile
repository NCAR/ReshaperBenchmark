################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

export PREFIX := $(abspath .)
export PYTHONUSERBASE := $(PREFIX)
export PYTHONVER := $(shell python -c "import sys; print 'python{0}.{1}'.format(*sys.version_info[:2])")

all: build

.PHONY:	allclean clean list build

tests: build
	@echo "Running benchmarking tests."
	@$(MAKE) -C tests
 
build:
	@echo "Building source and dependencies."
	@$(MAKE) -C src

list:
	@echo "Available Targets:"
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

clean:
	rm -rf $(PREFIX)/build

allclean:	clean
	rm -rf $(PREFIX)/bin $(PREFIX)/include $(PREFIX)/lib $(PREFIX)/share $(PREFIX)/man $(PREFIX)/venv

