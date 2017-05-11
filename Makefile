################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

export PREFIX := $(abspath .)
export PYTHONUSERBASE := $(PREFIX)
export PYTHONVER := $(shell python -c "import sys; print 'python{0}.{1}'.format(*sys.version_info[:2])")

all: build

.PHONY: build cleanbuild cleanbuildall cleantestdata list tests

tests:
	@IS_BUILT=`source $(PREFIX)/venv/bin/activate && python -c "import pyreshaper" 2> /dev/null; echo $$?`; \
	if [ $$IS_BUILT -ne 0 ]; then \
		echo "Run 'make' before 'make tests'."; \
		exit 1; \
	fi
	@echo "Running benchmarking tests."
	@echo
	@$(MAKE) -C tests
 
build:
	@echo "Building source and dependencies."
	@echo
	@$(MAKE) -C src

list:
	@echo "Available Targets:"
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

cleanbuild:
	rm -rf $(PREFIX)/build

cleanbuildall: cleanbuild
	rm -rf $(PREFIX)/bin $(PREFIX)/include $(PREFIX)/lib $(PREFIX)/share $(PREFIX)/man $(PREFIX)/venv

cleantestdata:
	rm -rf $(PREFIX)/tests/*/input $(PREFIX)/tests/*/output

