#!/bin/sh
# COPYRIGHT 2017, University Corporation for Atmospheric Research

# If desired, set the location of the output and input root data directories
#export INPUT_ROOT=`pwd`
#export OUTPUT_ROOT=`pwd`

# For convenience, we set the number of MPI processes we use here.
#
# NOTE: This is not needed.  It is only used in the RUNNAME string
#       and in the MPIRUN command string, both specified below.
#       This value is the maximum number of processes that can be
#       run on the NCAR Geyser DAV cluster, so we recommend this (40)
#       as the number of processes you use.

export NPROCS=40

# This is the command that will preface any test script that runs in parallel.
#
# NOTE: In this example, we set the size of the MPI environment in this
#       command, but your environment and MPI launcher may be different.
#       The size of the job should be set according to your environment's needs.

# On Yellowstone...
export MPIRUN="mpirun.lsf"

# On Cheyenne...
#export MPIRUN="mpiexec_mpt -n $NPROCS"

# On a generic MPI machine...
#export MPIRUN="mpirun -n $NPROCS"

# Include any MPI environment flags necessary for these runs here
#
# NOTE: You may not need this, but this MPI benchmark, in some tests, can have
#       MPI processes that are idle for a long time.  These MPI environment
#       variables are needed on NCAR's Geyser DAV cluster to prevent timeout
#       due to inactivity, among other things.

export MP_TIMEOUT=14400
export MP_PULSE=1800
export MP_DEBUG_NOTIMEOUT=yes

# Whether to capture strace results during tests (default to no strace results)
# If strace is enabled (STRACE=1), the timing of the tests will be affected.
# Therefore, if strace is enabled, you should reflect this fact in the RUNNAME
# (below).  Timing results should not be run with strace enabled.
#
# WARNING:  On some systems, or with some MPI implementations, strace will
#           not capture statistics between MPI_Init and MPI_Finalize!  You
#           may need to modify your MPIRUN command to allow strace to work
#           as expected.

export STRACE=0

# Whether to output test files with compression enabled.  This will affect
# timing if enabled (DEFLATE>0).  Therefore, if the DEFLATE value is changed, you
# should reflect this fact in the RUNNAME (below).  We recommend keeping compression
# disabled (DEFLATE=0).

export DEFLATE=0

# This is a name to give these runs (can be anything, just no "." or spaces).  This
# name will be included in the name of the log-files, so try to make your name
# unique.  We recommend including in this name the settings you used for this
# run (e.g., the number of processors, the compression/deflate setting, the
# strace setting, etc.).

HOSTNAME=`hostname`
export RUNNAME=$HOSTNAME-N$NPROCS-D$DEFLATE-S$STRACE

# Append benchmark directories to PATH or LD_LIBRARY_PATH, if necessary.  You should
# not need to change anything below this line.

CWD=`pwd`

NEEDS_BINDIR=`echo $PATH | grep -q "$CWD/bin"; echo $?`
if [ $NEEDS_BINDIR -ne 0 ]; then
	export PATH=$CWD/bin:$PATH
fi

NEEDS_LIBDIR=`echo $LD_LIBRARY_PATH | grep -q "$CWD/lib"; echo $?`
if [ $NEEDS_LIBDIR -ne 0 ]; then
	export LD_LIBRARY_PATH=$CWD/lib:$LD_LIBRARY_PATH
fi
