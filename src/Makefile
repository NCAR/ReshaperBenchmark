################################################################################
#
#  Makefile for ASAP Benchmark Utilities: Externals-Source Level
#
# COPYRIGHT 2017, University Corporation for Atmospheric Research
################################################################################

export PREFIX := $(abspath ..)
export PYTHONUSERBASE := $(PREFIX)
export PYTHONVER := $(shell python -c "import sys; print 'python{0}.{1}'.format(*sys.version_info[:2])")

HLINE1 := "---------------------------------------------------------------------"
HLINE2 := "====================================================================="

PYRESHAPER  := PyReshaper-1.0.1
ASAPTOOLS   := ASAPPyTools-0.6.0
NETCDF4PY   := netcdf4-python-1.2.3.1rel
ORDEREDDICT := ordereddict-1.1
MPI4PY      := mpi4py-1.3.1
NUMPY       := numpy-1.10.2
VIRTUALENV  := virtualenv-14.0.6
SETUPTOOLS  := setuptools-20.2.2
NETCDF      := netcdf-4.4.0
HDF5        := hdf5-1.8.16
ZLIB        := zlib-1.2.11
SZIP        := szip-2.1.1

ifndef PYTHON
  PYTHON := python
endif

all: pyreshaper

pyreshaper: build asaptools netcdf4python
	@HAS_PYRESHAPER=`source $(PREFIX)/venv/bin/activate && python -c "import pyreshaper" 2> /dev/null; echo $$?`; \
	if [ $$HAS_PYRESHAPER -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(PYRESHAPER) ]; then \
			tar -xmzf $(PREFIX)/src/$(PYRESHAPER).tar.gz; \
		fi; \
		cd $(PYRESHAPER) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

asaptools: build mpi4py
	@HAS_ASAPTOOLS=`source $(PREFIX)/venv/bin/activate && python -c "import asaptools" 2> /dev/null; echo $$?`; \
	if [ $$HAS_ASAPTOOLS -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(ASAPTOOLS) ]; then \
			tar -xmzf $(PREFIX)/src/$(ASAPTOOLS).tar.gz; \
		fi; \
		cd $(ASAPTOOLS) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

netcdf4python: build numpy ordereddict netcdf
	@HAS_NETCDF4PY=`source $(PREFIX)/venv/bin/activate && python -c "import netCDF4" 2> /dev/null; echo $$?`; \
	if [ $$HAS_NETCDF4PY -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(NETCDF4PY) ]; then \
			tar -xmzf $(PREFIX)/src/$(NETCDF4PY).tar.gz; \
		fi; \
		cd $(NETCDF4PY) && \
		source $(PREFIX)/venv/bin/activate && \
		export PATH=$(PREFIX)/bin:$$PATH && \
		python setup.py build && \
		python setup.py install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

ordereddict: build virtualenv
	@HAS_ORDEREDDICT=`source $(PREFIX)/venv/bin/activate && python -c "from collections import OrderedDict" 2> /dev/null; echo $$?`; \
	if [ $$HAS_ORDEREDDICT -ne 0 ]; then \
		HAS_ORDEREDDICT=`source $(PREFIX)/venv/bin/activate && python -c "from ordereddict import OrderedDict" 2> /dev/null; echo $$?`; \
	fi; \
	if [ $$HAS_ORDEREDDICT -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(ORDEREDDICT) ]; then \
			tar -xmzf $(PREFIX)/src/$(ORDEREDDICT).tar.gz; \
		fi; \
		cd $(ORDEREDDICT) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py build install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)
	
mpi4py: build numpy
	@HAS_MPI4PY=`source $(PREFIX)/venv/bin/activate && python -c "import mpi4py" 2> /dev/null; echo $$?`; \
	if [ $$HAS_MPI4PY -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(MPI4PY) ]; then \
			tar -xmzf $(PREFIX)/src/$(MPI4PY).tar.gz; \
		fi; \
		cd $(MPI4PY) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py build install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

numpy: build setuptools
	@HAS_NUMPY=`source $(PREFIX)/venv/bin/activate && python -c "import numpy" 2> /dev/null; echo $$?`; \
	if [ $$HAS_NUMPY -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(NUMPY) ]; then \
			tar -xmzf $(PREFIX)/src/$(NUMPY).tar.gz; \
		fi; \
		cd $(NUMPY) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py build -j 4 install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

setuptools: build virtualenv
	@HAS_SETUPTOOLS=`source $(PREFIX)/venv/bin/activate && python -c "import setuptools" 2> /dev/null; echo $$?`; \
	if [ $$HAS_SETUPTOOLS -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(SETUPTOOLS) ]; then \
			tar -xmzf $(PREFIX)/src/$(SETUPTOOLS).tar.gz; \
		fi; \
		cd $(SETUPTOOLS) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

virtualenv: build sitepkgs python
ifeq ($(wildcard $(PREFIX)/venv),)
	@echo
	@echo $(HLINE2)
	@echo "Now building: $@"
	@echo
	@cd $(PREFIX)/build; \
	if [ ! -d $(VIRTUALENV) ]; then \
		tar -xmzf $(PREFIX)/src/$(VIRTUALENV).tar.gz; \
	fi
	@cd $(PREFIX)/build/$(VIRTUALENV) && $(PYTHON) setup.py install --user --prefix=
	@if [ ! -d $(PREFIX)/venv ]; then \
		$(PREFIX)/bin/virtualenv --no-pip --no-wheel --no-setuptools $(PREFIX)/venv; \
	fi
endif
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

python:
	@which $(PYTHON)
	@echo
	@echo $(HLINE2)
	@echo "Checking Python Version"
	@echo
	$(PYTHON) --version
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

netcdf:	build hdf5
	@if [ ! -s $$PREFIX/lib/libnetcdf.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		export LD_LIBRARY_PATH=$(PREFIX)/lib:$$LD_LIBRARY_PATH; \
		if [ ! -d $(NETCDF) ]; then \
			tar -xmzf $(PREFIX)/src/$(NETCDF).tar.gz && \
			cd $(NETCDF) && \
			CPPFLAGS=-I$(PREFIX)/include LDFLAGS=-L$(PREFIX)/lib \
			./configure --enable-netcdf-4 --prefix=$(PREFIX) --disable-dap; \
			cd ..; \
		fi; \
		cd $(NETCDF) && \
		$(MAKE) && \
		$(MAKE) install || \
		$(MAKE) install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

hdf5: build szip zlib
	@if [ ! -s $$PREFIX/lib/libhdf5.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(HDF5) ]; then \
			tar -xmzf $(PREFIX)/src/$(HDF5).tar.gz && \
			cd $(HDF5) && \
			./configure --prefix=$(PREFIX) --with-zlib=$(PREFIX) --with-szlib=$(PREFIX); \
			cd ..; \
		fi; \
		cd $(HDF5) && \
		$(MAKE) && \
		$(MAKE) install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

szip: build
	@if [ ! -s $$PREFIX/lib/libsz.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(SZIP) ]; then \
			tar -xmzf $(PREFIX)/src/$(SZIP).tar.gz && \
			cd $(SZIP) && \
			./configure --prefix=$(PREFIX); \
			cd ..; \
		fi; \
		cd $(SZIP) && \
		$(MAKE) && \
		$(MAKE) install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

zlib: build
	@if [ ! -s $$PREFIX/lib/libz.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd $(PREFIX)/build; \
		if [ ! -d $(ZLIB) ]; then \
			tar -xmzf $(PREFIX)/src/$(ZLIB).tar.gz && \
			cd $(ZLIB) && \
			./configure --prefix=$(PREFIX); \
			cd ..; \
		fi; \
		cd $(ZLIB) && \
		$(MAKE) && \
		$(MAKE) install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)
	

.PHONY:	clean list build

build:
	@if [ ! -d $$PREFIX/build ]; then \
		echo "Creating build directory."; \
		mkdir $$PREFIX/build; \
	else \
		echo "Build directory already exists."; \
	fi

sitepkgs:
	@if [ ! -d $$PREFIX/lib/$$PYTHONVER/site-packages ]; then \
		mkdir -p $$PREFIX/lib/$$PYTHONVER/site-packages; \
	fi

list:
	@echo "Available Targets:"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

clean:
	rm -rf build

allclean:	clean
	rm -rf bin include lib share man venv

