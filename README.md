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

1. The script appends the benchmark root `bin/` and `lib/` diretories to the environment `PATH` and
`LD_LIBRARY_PATH` variables.  This is needed due to the fact that this package installs everything
in the package root directory.

2. The script also sets the command that is used to launch an MPI job.  For many machines this
is just `mpirun`, but the actual command string should also contain any additional options needed
to run with the setting you need, such as setting the job size, etc.  By default, this environment
variable (called `MPIRUN`) is set to `mpirun.lsf` which is the command available on NCAR's Yellowstone
supercomputer.  However, for generic MPI installations, you may want to set this to something like 
`mpirun -n 16`.

We recommand that you edit the `init.sh` file according to your needs, and then initialize your environment with:

    . init.sh

To build and install the package software and its dependencies, just type:

    make

or

    make build

and the dependencies will be built in the `build/` directory and installed in the package
root directory.  (Python packages will be installed in a `virtualenv` environment called
`venv`.)

If you encounter any problems building and installing the software, you can look in the
appropriate subdirectory of the `build/` directory to diagnose the problem.  The build
makefile is `src/Makefile` and can be viewed to see how each dependency is built.

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

### Benchmark Tests

There are 10 tests that can be run.  For each test, there is a subdirectory within the `tests/`
directory.  The tests are as follows:

- `small`: This is a small demo test.  Use this test to check that your environment is set
correctly and that the benchmark suite was built correctly.  (Using 40 MPI processes on
NCAR's Geyser cluster, this test used a total of 1782 MB of memory with a maximum
use of 94 MB on any single process.  Data generation ran
in about 5 seconds, and the PyReshaper ran in about 11 seconds.)

- `atmfv1p0deg`: This tests a 1.0-degree finite-volume atmospheric-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 2745 MB of memory with a maximum
use of 121 MB on any single process.  Data generation ran 
in about 18 seconds, and the PyReshaper ran in about 81 seconds.)

- `atmse1p0deg`: This tests a 1.0-degree spectral-element atmospheric-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 8352 MB of memory with a maximum
use of 122 MB on any single process.  Data generation ran
in about 20 seconds, and the PyReshaper ran in about 78 seconds.)

- `lndse1p0deg`: This tests a 1.0-degree spectral-element land-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 2593 MB of memory with a maximum
use of 122 MB on any single process.  Data generation ran
in about 10 seconds, and the PyReshaper ran in about 255 seconds.)

- `ocn1p0deg`: This tests a 1.0-degree ocean-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 11829 MB of memory with a maximum
use of 167 MB on any single process.  Data generation ran
in about 85 seconds, and the PyReshaper ran in about 139 seconds.)

- `seaice1p0deg`: This tests a 1.0-degree sea-ice-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 2264 MB of memory with a maximum
use of 109 MB on any single process.  Data generation ran
in about 8 seconds, and the PyReshaper ran in about 83 seconds.)

- `atmse0p25deg`: This tests a 0.25-degree spectral-element atmospheric-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 236796 MB of memory with a maximum
use of 376 MB on any single process.  Data generation ran
in about 565 seconds, and the PyReshaper ran in about 591 seconds.)

- `lndse0p25deg`: This tests a 0.25-degree spectral-element land-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 34673 MB of memory with a maximum
use of 355 MB on any single process.  Data generation ran
in about 90 seconds, and the PyReshaper ran in about 195 seconds.)

- `ocn0p1deg`: This tests a 0.1-degree ocean-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 242194 MB of memory with a maximum
use of 2677 MB on any single process.  Data generation ran
in about 1190 seconds, and the PyReshaper ran in about 1755 seconds.)

- `seaice0p1deg`: This tests a 0.1-degree sea-ice-model-like dataset.  (Using
40 MPI processes on NCAR's Geyser cluster, this test used a total of 1780 MB of memory with a maximum
use of 333 MB on any single process.  Data generation ran
in about 310 seconds, and the PyReshaper ran in about 382 seconds.)

Data regarding each test, using NCAR's Geyser cluster, is described in the following table:

|--------------|--------------|-------------------|-------------------------|----------------------|---------------------|
| Test Name    | MPI Job Size | Total Memory Used | Memory Used per Process | Data Generation Time | PyReshaper Run Time | 
|--------------|--------------|-------------------|-------------------------|----------------------|---------------------|
| small        | 40 processes |                   |                         |                      |                     |
| atmfv1p0deg  | 40 processes |                   |                         |                      |                     |
| atmse1p0deg  | 40 processes |                   |                         |                      |                     |
| lndse1p0deg  | 40 processes |                   |                         |                      |                     |
| ocn1p0deg    | 40 processes |                   |                         |                      |                     |
| seaice1p0deg | 40 processes |                   |                         |                      |                     |
| atmse0p25deg | 40 processes |                   |                         |                      |                     |
| lndse0p25deg | 40 processes |                   |                         |                      |                     |
| ocn0p1deg    | 40 processes |                   |                         |                      |                     |
| seaice0p1deg | 40 processes |                   |                         |                      |                     |
|--------------|--------------|-------------------|-------------------------|----------------------|---------------------|


### Results

The results requested for this benchmark will be the contents of the `logs/` directory.  You
may tarball this directory up and send it to us as requested. 



Copyright 2017, University Corporation for Atmospheric Research
