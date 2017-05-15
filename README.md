# ReshaperBenchmark
I/O Benchmark based on the PyReshaper Utility

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
