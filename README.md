# ReshaperBenchmark

## An I/O Benchmark based on the NCAR PyReshaper Utility

### Benchmarking Suite 

This benchmark suite requires a C compiler, `make`, an installed implementation of MPI, and
Python version 2.7.  All of the other necessary dependencies are included in the `src/`
directory of this package, and they will be built with default build options as part of this
benchmark's installation process.

After downloading and unpacking this benchmark package, you should see the following files and
directories:

    README.md        - this file
    LICENSE.rst      - the license for this benchmark
    Makefile         - the makefile used for building and running this benchmark
    init.sh.template - a template environment initialization script
    sbin/            - directory where useful scripts for running the benchmark are located
    src/             - directory where all dependencies are contained (as source tarballs)
    tests/           - directory where all benchmark tests will be run

In addition to these files and directories, other directories will be created during installation.
These include:

    bin/     - binary installation directory for the benchmark's dependencies
    build/   - directory where all dependencies will be built
    include/ - include directory for the benchmark's dependencies
    lib/     - library directory for the benchmark's dependencies
    logs/    - directory where all benchmark test logs will be placed
    share/   - shared resource directory for the benchmark's dependencies
    venv/    - virtualenv environment directory where Python dependencies will be installed

Everything about this benchmark is controlled via the makefile, so you should not need to enter
into any of these directories for any reason other than to check that things are okay or to 
diagnose and fix problems.  (Hopefully, you will not have any problems!)

### Installation

This benchmark does not install any software outside of the benchmark package root directory.
(The root directory of this benchmark package will be the prefix for all source installations.)

Before building and installing, you may need to set the proper environment variables for the
software to build and run properly.  This can be done by modifying the `init.sh.template` script
for your machine.  Very little in this script may need to change for your machine, but the
critical things done in this script are:

1. The script appends the benchmark root `bin/` and `lib/` diretories to the environment `PATH` and
`LD_LIBRARY_PATH` variables.  This is needed due to the fact that this package installs everything
in the package root directory.
2. The script 

Assuming you have necessary dependencies installed (`make`, a C compiler, MPI, and Python 2.7),
you should be able to build and install the benchmarking package software with:

    make build

or just simply:

    make



To run these benchmarks, you will need Python 2.7, an implementation of MPI, and
a C compiler.  Before building the benchmark and dependencies, you may need to
make changes to the environment settings found in the `init.sh.template` file.
We suggest that you make a copy of this template file (e.g., init.sh), make 
changes to fit your environment, and initialize the environment by typing:

    . init.sh

or whatever you named the copy.

Then, to build the toolsuite, just type:

    make build

All other dependencies are included with this benchmark package as tarballs in
the src directory.  These dependencies will be build with default settings.  If
any of these packages fail to build, their build directories will be located in
the `build` directory, and you will be able to diagnose any build problems as you
encounter them.

Once the dependencies are built, you can run all of the tests by typing:

    make alltests

Or you may run each tests one by one.


Copyright 2017, University Corporation for Atmospheric Research
