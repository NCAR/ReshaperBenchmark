################################################################################
#
#  Makefile for ASAP Benchmark Utilities: Externals-Source Level
#
################################################################################

export PREFIX := $(abspath .)
export PYTHONUSERBASE := $(PREFIX)
export PYTHONVER := $(shell python -c "import sys; print 'python{0}.{1}'.format(*sys.version_info[:2])")

HLINE1 := "---------------------------------------------------------------------"
HLINE2 := "====================================================================="

PYRESHAPER  := PyReshaper-iobackend
PYAVERAGER  := pyAverager-0.9.4
ASAPTOOLS   := ASAPPyTools-0.5.5
PYNIO       := PyNIO-1.4.1p2
NETCDF4PY   := netcdf4-python-1.2.3.1rel
ORDEREDDICT := ordereddict-1.1
MPI4PY      := mpi4py-1.3.1
NUMPY       := numpy-1.10.2
VIRTUALENV  := virtualenv-14.0.6
SETUPTOOLS  := setuptools-20.2.2
NETCDF      := netcdf-4.4.0
HDF5        := hdf5-1.8.16
ZLIB        := zlib-1.2.8
JPEG        := jpeg-6b
PNG         := libpng-1.6.21

ifndef PYTHON
  PYTHON := python
endif

all: pyreshaper pyaverager

pyaverager: build asaptools Nio
	@HAS_PYAVERAGER=`source $(PREFIX)/venv/bin/activate && python -c "import pyaverager" 2> /dev/null; echo $$?`; \
	if [ $$HAS_PYAVERAGER -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(PYAVERAGER) ]; then \
			tar -xmzf ../source/$(PYAVERAGER).tar.gz; \
		fi; \
		cd $(PYAVERAGER) && \
		source $(PREFIX)/venv/bin/activate && \
		python setup.py install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

pyreshaper: build asaptools Nio netcdf4python
	@HAS_PYRESHAPER=`source $(PREFIX)/venv/bin/activate && python -c "import pyreshaper" 2> /dev/null; echo $$?`; \
	if [ $$HAS_PYRESHAPER -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(PYRESHAPER) ]; then \
			tar -xmzf ../source/$(PYRESHAPER).tar.gz; \
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
		cd build; \
		if [ ! -d $(ASAPTOOLS) ]; then \
			tar -xmzf ../source/$(ASAPTOOLS).tar.gz; \
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
		cd build; \
		if [ ! -d $(NETCDF4PY) ]; then \
			tar -xmzf ../source/$(NETCDF4PY).tar.gz; \
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
	
Nio: build numpy netcdf
	@HAS_NIO=`source $(PREFIX)/venv/bin/activate && python -c "import Nio" 2> /dev/null; echo $$?`; \
	if [ $$HAS_NIO -ne 0 ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(PYNIO) ]; then \
			tar -xmzf ../source/$(PYNIO).tar.gz; \
		fi; \
		cd $(PYNIO) && \
		source $(PREFIX)/venv/bin/activate && \
		HAS_OPENDAP=0 HAS_SZIP=0 HAS_NETCDF4=1 HAS_HDF5=1 \
		HDF5_PREFIX=$(PREFIX) NETCDF4_PREFIX=$(PREFIX) \
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
		cd build; \
		if [ ! -d $(ORDEREDDICT) ]; then \
			tar -xmzf ../source/$(ORDEREDDICT).tar.gz; \
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
		cd build; \
		if [ ! -d $(MPI4PY) ]; then \
			tar -xmzf ../source/$(MPI4PY).tar.gz; \
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
		cd build; \
		if [ ! -d $(NUMPY) ]; then \
			tar -xmzf ../source/$(NUMPY).tar.gz; \
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
		cd build; \
		if [ ! -d $(SETUPTOOLS) ]; then \
			tar -xmzf ../source/$(SETUPTOOLS).tar.gz; \
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
	@cd build; \
	if [ ! -d $(VIRTUALENV) ]; then \
		tar -xmzf ../source/$(VIRTUALENV).tar.gz; \
	fi
	@cd build/$(VIRTUALENV) && $(PYTHON) setup.py install --user --prefix=
	@if [ ! -d $(PREFIX)/venv ]; then \
		bin/virtualenv --no-pip --no-wheel --no-setuptools $(PREFIX)/venv; \
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
	@if [ ! -s lib/libnetcdf.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		export LD_LIBRARY_PATH=$(PREFIX)/lib:$$LD_LIBRARY_PATH; \
		if [ ! -d $(NETCDF) ]; then \
			tar -xmzf ../source/$(NETCDF).tar.gz && \
			cd $(NETCDF) && \
			CPPFLAGS=-I$(PREFIX)/include LDFLAGS=-L$(PREFIX)/lib \
			./configure --prefix=$(PREFIX) --disable-dap; \
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

hdf5: build zlib
	@if [ ! -s lib/libhdf5.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(HDF5) ]; then \
			tar -xmzf ../source/$(HDF5).tar.gz && \
			cd $(HDF5) && \
			./configure --prefix=$(PREFIX) --with-zlib=$(PREFIX); \
			cd ..; \
		fi; \
		cd $(HDF5) && \
		$(MAKE) && \
		$(MAKE) install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

zlib: build
	@if [ ! -s lib/libz.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(ZLIB) ]; then \
			tar -xmzf ../source/$(ZLIB).tar.gz && \
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

jpeg: build zlib 
	@if [ ! -s lib/libjpeg.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(JPEG) ]; then \
			tar -xmzf ../source/$(JPEG).tar.gz && \
			cd $(JPEG) && \
			./configure --prefix=$(PREFIX); \
			mkdir -p man/man1; \
			cd ..; \
		fi; \
		cd $(JPEG) && \
		$(MAKE) && \
		$(MAKE) install-lib; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

png: build
	@if [ ! -s lib/libpng.a ]; then \
		echo; \
		echo $(HLINE2); \
		echo "Now building: $@"; \
		echo; \
		cd build; \
		if [ ! -d $(PNG) ]; then \
			tar -xmzf ../source/$(PNG).tar.gz && \
			cd $(PNG) && \
			./configure --prefix=$(PREFIX); \
			cd ..; \
		fi; \
		cd $(PNG) && \
		$(MAKE) && \
		$(MAKE) install; \
	fi
	@echo $(HLINE1)
	@echo "Installed: $@"
	@echo $(HLINE1)

.PHONY:	clean list build

build:
	@if [ ! -d build ]; then \
		echo "Creating build directory."; \
		mkdir build; \
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

