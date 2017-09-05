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

Data regarding each test, using NCAR's Geyser cluster, is described in the following table:

| Test Name    | MPI Job Size | Total Memory Used | Memory Used per Process | Data Generation Time | PyReshaper Run Time | PyReshaper Throughput |
|--------------|-------------:|------------------:|------------------------:|---------------------:|--------------------:|----------------------:|
| small        | 40 procs     | 1788 MB           | 91 MB                   | 0.16 sec             | 1 sec               | 0.18 MB/sec           |
| atmfv1p0deg  | 40 procs     | 2745 MB           | 123 MB                  | 17 sec               | 130 sec             | 211 MB/sec            |
| atmse1p0deg  | 40 procs     | 8352 MB           | 126 MB                  | 31 sec               | 130 sec             | 247 MB/sec            |
| lndse1p0deg  | 40 procs     | 2593 MB           | 123 MB                  | 13 sec               | 519 sec             | 23.8 MB/sec           |
| ocn1p0deg    | 40 procs     | 11829 MB          | 178 MB                  | 68 sec               | 152 sec             | 1044 MB/sec           |
| seaice1p0deg | 40 procs     | 2264 MB           | 113 MB                  | 4 sec                | 117 sec             | 74.0 MB/sec           |
| atmse0p25deg | 40 procs     | 236796 MB         | 376 MB                  | 342 sec              | 510 sec             | 2167 MB/sec           |
| lndse0p25deg | 40 procs     | 34673 MB          | 372 MB                  | 75 sec               | 238 sec             | 742 MB/sec            |
| ocn0p1deg    | 40 procs     | 242194 MB         | 2677 MB                 | 774 sec              | 3472 sec            | 712 MB/sec            |
| seaice0p1deg | 40 procs     | 1780 MB           | 335 MB                  | 168 sec              | 250 sec             | 2423 MB/sec           |

### Results

The results requested for this benchmark will be the contents of the `logs/` directory.  You
may tarball this directory up and send it to us as requested. 

---

Copyright 2017, University Corporation for Atmospheric Research
