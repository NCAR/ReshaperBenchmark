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

2. The script also sets the command that is used to launch an MPI job.  For many machines this
is just `mpirun`, but the actual command string should also contain any additional options needed
to run with the setting you need, such as setting the job size, etc.  By default, this environment
variable (called `MPIRUN`) is set to `mpirun -n 16`.

We recommand that you make a copy of the template initialization script:

    cp init.sh.template init.sh

edit this file according to your needs, and then initialize your environment with:

    . init.sh

or similar, depending on what you named the script.

To build and install the package software and its dependencies, just type:

    make build

or

    make

and the dependencies will be built in the `build/` directory and installed in the package
root directory.  (Python packages will be installed in a `virtualenv` environment called
`venv`.)

If you encounter any problems building and installing the software, you can look in the
appropriate subdirectory of the `build/` directory to diagnose the problem.  The build
makefile is `src/Makefile` and can be viewed to see how each dependency is built.

### Running the Benchmark

Once the package and its dependencies have been built, you can run all of the tests with:

    make alltests

This will run all of the tests found in subdirectories of the `tests/` directory.  To get
a list of all of the tests that can be run, just type:

    make help

Each test can be run individually with the command:

    make testname

where `testname` is the name of the individual test you want to run.

When a test is run, the procedure for the run is as follows:

1. The data for the test is generated.  This can almost as long as the test in some cases.
On NCAR's Geyser DAV cluster, with 40 MPI processes, the largest test takes roughly 
20 minutes to generate the test data.  Data generation is done in parallel, and the parallel
data generation script is run with command set by the `MPIRUN` environment variable.

2. The PyReshaper tool is run with the generated input.  This step is also run with the command
set by the `MPIRUN` environment variable.  The largest run takes roughly 30 minutes to run with
40 MPI processors on NCAR's Geyser DAV cluster.

3. The data generation and PyReshaper log files are copied to the `logs/` directory.

If a test fails, and you need to modify environment variables to to get it to rerun, you may
want to run `make cleantests` before rerunning the next test.  This will erase the contents of
the test directories (including all data).  Or, you may just want to delete all log files still
remaining in the `tests/` subdirectories.

### Results

The results requested for this benchmark will be the contents of the `logs/` directory.  You
may tarball this directory up and send it to us as requested. 



Copyright 2017, University Corporation for Atmospheric Research
