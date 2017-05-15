################################################################################
#
#  Makefile for the NCAR PyReshaper Benchmark - ./
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

export SHELL := $(shell which bash)
export PREFIX := $(abspath .)
export PYTHONUSERBASE := $(PREFIX)
export PYTHONVER := $(shell python -c "import sys; print 'python{0}.{1}'.format(*sys.version_info[:2])")

default: build

tdirs = $(sort $(dir $(wildcard tests/*/.)))
tests = $(tdirs:tests/%/=%)

alltests: $(tests)

$(tests): build
	@IS_BUILT=`source $(PREFIX)/venv/bin/activate && python -c "import pyreshaper" 2> /dev/null; echo $$?`; \
	if [ $$IS_BUILT -ne 0 ]; then \
		echo "Run 'make' before 'make test'."; \
		exit 1; \
	fi
	@echo "Running benchmarking tests."
	@echo
	@$(MAKE) -C tests $@
 
build:
	@echo "Building source and dependencies."
	@echo
	@$(MAKE) -C src

.PHONY: help clean

help:
	@echo "To run these benchmarks, you will need Python 2.7, an implementation of MPI, and"
	@echo "a C compiler.  Before building the benchmark and dependencies, you may need to"
	@echo "make changes to the environment settings found in the init.sh.template file."
	@echo "We suggest that you make a copy of this template file (e.g., init.sh), make "
	@echo "changes to fit your environment, and initialize the environment by typing:"
	@echo
	@echo "    . init.sh"
	@echo
	@echo "or whatever you named the copy."
	@echo
	@echo "Then, to build the toolsuite, just type:"
	@echo
	@echo "    make build"
	@echo
	@echo "All other dependencies are included with this benchmark package as tarballs in"
	@echo "the src directory.  These dependencies will be build with default settings.  If"
	@echo "any of these packages fail to build, their build directories will be located in"
	@echo "the build directory, and you will be able to diagnose the build problems as you"
	@echo "encounter them."
	@echo
	@echo "Once the dependencies are built, you can run all of the tests by typing:"
	@echo 
	@echo "    make alltests"
	@echo
	@echo "Or you may run each tests one by one."
	@echo
	@echo "Available Targets:"
	@echo
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

clean:
	rm -rf tests/*/*.log
	rm -rf tests/*/*.s2s
	rm -rf tests/*/input
	rm -rf tests/*/output
