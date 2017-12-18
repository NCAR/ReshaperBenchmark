# ReshaperBenchmark

## An I/O Benchmark based on the NCAR PyReshaper Utility

### Benchmarking Suite 

This benchmark suite requires a C compiler, `make`, an installed implementation of MPI, and
Python version 2.7.  All of the other necessary dependencies are included in the `src/`
directory of this package, and they will be built with default build options as part of this
benchmark's installation process.

After downloading and unpacking this benchmark package, you should see the following files and
directories:

    README.md   - this file
    LICENSE.rst - the license for this benchmark
    Makefile    - the makefile used for building and running this benchmark
    init.sh     - a template environment initialization script
    sbin/       - directory where useful scripts for running the benchmark are located
    src/        - directory where all dependencies are contained (as source tarballs)
    tests/      - directory where all benchmark tests will be run

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
software to build and run properly.  This can be done by modifying the `init.sh` script
for your machine.  Very little in this script may need to change for your machine, but the
critical things done in this script are:

1. The script appends the benchmark root `bin/` and `lib/` directories to the environment `PATH` and
`LD_LIBRARY_PATH` variables, reespectively.  This is needed due to the fact that this package installs
everything in the package root directory.

2. The script also sets the command that is used to launch an MPI job.  For many machines this
is just `mpirun -n N`, where `N` is the number of MPI tasks needed for the job.  By default, this environment
variable (called `MPIRUN`) is set to `mpirun.lsf` which is the command available on NCAR's Yellowstone
supercomputer.  However, for generic MPI installations, you may want to set this to something like 
`mpirun -n N`, where `N` is the number of MPI tasks needed for the job.  Other alternatives might be
`mpiexec -n N` or `mpirun_mpt` or `aprun -n N`, all depending on the MPI environment on the machine 
you are running.

We recommand that you edit the `init.sh` file according to your needs, and then initialize your environment with:

    . init.sh

To build and install the package software and its dependencies, just type:

    make

or

    make build

and the dependencies will be built in the `build/` directory and installed in the package
root directory.  (Python packages will be installed in a `virtualenv` environment called
`venv`.)  Note that you can control the compiler used to build the dependencies with the `CC` and `CXX`
environment variables (for the C and C++ compilers, respectively), like so:

    CC=icc CXX=icpc make build

If you encounter any problems building and installing the software, you can look in the
appropriate subdirectory of the `build/` directory to diagnose the problem.  The build
makefile is `src/Makefile` and can be viewed to see how each dependency is built.  If you need
to reconfigure and rebuild an individual package because the default configuration will not
work on your system, this is how (and where) you would do it.

This package is designed to build all of the necessary dependencies (except python and MPI) with default
configurations, so that comparison between runs on different systems is more of an "apples-to-apples"
comparison.  However, there are times that can arise (such as if default configuration cannot build
on the given system, or if idealized timing conditions might be desired instead of default timings)
when you might want to use packages already installed on your system.  When this is the case,
you can set the `USE_SYSTEM_PACKAGES` environment variable to change the way that the packages
are built.  When the `USE_SYSTEM_PACKAGES` variable is set, the benchmark tool will create the
virtual environment using the `--system_site_packages` flag, making the available system-installed
Python packages availing from within the virtual environment itself.  Hence, if your system already
has an install of `netcdf4-python`, for example, you can use this flag to prevent the rebuilding 
and installing of `netcdf4`, `hdf5`, and the `netcdf4-python` packages and their dependencies.

### Running the Benchmarks

Once the package and its dependencies have been built, you can run all of the tests with:

    make alltests

This will run all of the tests found in subdirectories of the `tests/` directory.  To get
a list of all of the tests that can be run, just type:

    make help

Each test can be run individually with the command:

    make testname

where `testname` is the name of the individual test you want to run.

When a test is run, the procedure for the run is as follows:

1. The data for the test is generated.  This can be almost as long as the test in some cases.
On NCAR's Geyser DAV cluster, with 40 MPI processes, the largest test takes roughly 
13 minutes to generate the test data.  Data generation is done in parallel, and the parallel
data generation script is run with command set by the `MPIRUN` environment variable.

2. The PyReshaper tool is run with the generated input.  This step is also run with the command
set by the `MPIRUN` environment variable.  The largest run takes roughly 60 minutes to run with
40 MPI processors on NCAR's Geyser DAV cluster.

3. The data generation and PyReshaper log files are copied to the `logs/` directory.

If a test fails, and you need to modify environment variables to to get it to rerun, you may
want to run `make cleantests` before rerunning the next test.  This will erase the contents of
the test directories (including all data).  Or, you may just want to delete all log files still
remaining in the `tests/` subdirectories.

### Benchmark Tests

There are 10 tests that can be run.  For each test, there is a subdirectory within the `tests/`
directory.  The tests are as follows:

- `small`: This is a small demo test.  Use this test to check that your environment is set
correctly and that the benchmark suite was built correctly.

- `atmfv1p0deg`: This tests a 1.0-degree finite-volume atmospheric-model-like dataset.

- `atmse1p0deg`: This tests a 1.0-degree spectral-element atmospheric-model-like dataset.

- `lndse1p0deg`: This tests a 1.0-degree spectral-element land-model-like dataset.

- `ocn1p0deg`: This tests a 1.0-degree ocean-model-like dataset.

- `seaice1p0deg`: This tests a 1.0-degree sea-ice-model-like dataset.

- `atmse0p25deg`: This tests a 0.25-degree spectral-element atmospheric-model-like dataset.

- `lndse0p25deg`: This tests a 0.25-degree spectral-element land-model-like dataset.

- `ocn0p1deg`: This tests a 0.1-degree ocean-model-like dataset.

- `seaice0p1deg`: This tests a 0.1-degree sea-ice-model-like dataset.

Data regarding each test, using a *single node* on NCAR's Geyser cluster, is described in the following table:

| Test Name    | MPI Job Size | Maximum Single-Process Memory Use | Data Generation Time | PyReshaper Run Time | PyReshaper Throughput | Data Volume |
|--------------|-------------:|----------------------------------:|---------------------:|--------------------:|----------------------:|------------:|
| small        | 40 procs     | 43 MB                             | 1 sec                | 1 sec               | 1 MB/sec              | 1 MB        |
| atmfv1p0deg  | 40 procs     | 70 MB                             | 31 sec               | 107 sec             | 256 MB/sec            | 27338 MB    |
| atmse1p0deg  | 40 procs     | 70 MB                             | 35 sec               | 136 sec             | 237 MB/sec            | 32086 MB    |
| lndse1p0deg  | 40 procs     | 70 MB                             | 15 sec               | 555 sec             | 22 MB/sec             | 12331 MB    |
| ocn1p0deg    | 40 procs     | 98 MB                             | 157 sec              | 252 sec             | 631 MB/sec            | 158816 MB   |
| seaice1p0deg | 40 procs     | 58 MB                             | 12 sec               | 147 sec             | 59 MB/sec             | 8626 MB     |
| atmse0p25deg | 40 procs     | 212 MB                            | 1041 sec             | 1042 sec            | 1060 MB/sec           | 1104653 MB  |
| lndse0p25deg | 40 procs     | 209 MB                            | 153 sec              | 273 sec             | 648 MB/sec            | 176674 MB   |
| ocn0p1deg    | 40 procs     | 3577 MB                           | 2338 sec             | 3456 sec            | 715 MB/sec            | 2471925 MB  |
| seaice0p1deg | 40 procs     | 346 MB                            | 591 sec              | 563 sec             | 1077 MB/sec           | 606451 MB   |

### Results

The results requested for this benchmark will be the contents of the `logs/` directory.  You
may tarball this directory up and send it to us as requested. 

---

Copyright 2017, University Corporation for Atmospheric Research
