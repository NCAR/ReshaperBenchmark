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

.PHONY: help build cleanall cleantests cleanbuild

help:
	@echo "To run these benchmarks, you will need Python 2.7, an implementation of MPI, and"
	@echo "a C compiler.  Before building the benchmark suite and its and dependencies, you"
	@echo "may need to make changes to the environment settings found in the init.sh file."
	@echo "We suggest that you edit this file to make changes to fit your environment, and"
	@echo "initialize the environment by typing:"
	@echo
	@echo "    . init.sh"
	@echo
	@echo "on the command line."
	@echo
	@echo "To build the benchmark suite, just type:"
	@echo
	@echo "    make"
	@echo
	@echo "or"
	@echo
	@echo "    make build"
	@echo
	@echo "All other dependencies are included with this benchmark package as tarballs in"
	@echo "the src/ directory.  These dependencies will be built with default settings.  If"
	@echo "any of these packages fail to build, their build directories will be located in"
	@echo "the build/ directory, and you will be able to diagnose the build problems as you"
	@echo "encounter them.  Assuming all dependencies build, they will be installed in the"
	@echo "root directory of this benchmark package."
	@echo
	@echo "Once the dependencies are built, you can run all of the tests by typing:"
	@echo 
	@echo "    make alltests"
	@echo
	@echo "Or you may run each test individually."
	@echo
	@echo "Available Test Targets:"
	@echo
	@for test in $(tests) ; do \
	echo "    $$test" ; \
	done

cleantests:
	rm -rf tests/*/*.log
	rm -rf tests/*/*.s2s
	rm -rf tests/*/input
	rm -rf tests/*/output

cleanbuild:
	rm -rf build

cleanall: cleanbuild
	rm -rf bin venv lib include share
