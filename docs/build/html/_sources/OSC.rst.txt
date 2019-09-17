.. _OSC:

OSC Introduction and Guide
===========================

This documentation is taken from a variety of resources, with a number of links and external resources available at the
end of this guide.

Remember, during our first week of the course we received an excellent overview of the
`Ohio Supercomputer Center (OSC) <https://www.osc.edu/>`_ from Dr. Kate Cahill of OSC. Please find her lecture on
`Carmen <https://carmen.osu.edu/#>`_ as a refresher.

Below is an *intro* into using OSC (using Dr. Cahill's slides as a guide) and should not serve as an all-encompassing
list. If you need that, please consult the links at the bottom.

Systems
-------

=======================     ======= =======
System                      Pitzer  Owens
-----------------------     ------- -------
Year                        2018    2016
Theoretical Performance     1200 TF 1600 TF
Nodes                       260     824
CPU cores                   10560   23392
Total Memory                70.6 Tb 120 Tb
Memory/Core                 > 5 Gb  > 5 Gb
=======================     ======= =======

Notice that Pitzer, though newer, has far fewer nodes (31%) and less than half the cores (45%). However, it has 75% the
theoretical performance. Why would that be? Turns out the CPUs are faster and there are more CPUs/node.

We won't be discussing Ruby, as it's not geared towards the analysis types we'll be working with.

Login Nodes
-----------

The login nodes are where you:

1) Submit jobs
2) Mange and edit files
3) Very small scale, interactive work

There is a 1 GB memory and 20 min CPU limit on login nodes. Why? That's all you should need! Login nodes **are not for
doing large scale jobs**!

Filesystems
-----------

There are a number of different filesystems available on OSC, each with a different purpose.

Home
^^^^

Where to store your files. This is backed up daily. Use $HOME to reference it.

Project
^^^^^^^

Available to project PIs by request. Shared by all users on a project. Backed up daily.

Our project is PAS1573. It should be available at /fs/scratch/PAS1573.

Scratch
^^^^^^^

Where to store large input or output files. This has faster I/O than the home or project directories. What does that
mean? It means reading and writing to the disk is faster. It's like downloading a large file from the internet verses
copying a file from one folder to another on your local machine. This is also *temporary* storage and is not backed up.
If you really need to keep a copy of data, copy/keep it in $HOME.

$TMPDIR
^^^^^^^

This is *local* (relative to the compute node) storage during job execution. There's about 1 TB available on Owens

Connecting to OSC
-----------------

From a Mac, Linux or UNIX-based machine:

.. code-block:: bash

    ssh userid@pitzer.osc.edu

Replace "pitzer" with "owens" for which system you wish to log into, and replace "userid" with your OSC userid, usually
osuXXXX.

From Windows:

Grab a free SSH client, like `PuTTY <https://www.putty.org/>`_. You'll need to set up the configuration to connect,
which is slightly more "difficult" than opening a terminal window and typing "ssh." However, once done. Login will be a
simple selection of which machine to log into.

**OR** you can login using `OSC's OnDemand <https://ondemand.osc.edu>`_.

If you need to connect to OSC and be able to use a X-based GUI, simply append "-X" flag after ssh (node: X is capitalized).

Transferring Data to/from OSC
-----------------------------

There are 3 main ways of transferring data to/from OSC, each with advantages or disadvantages.

OnDemand
^^^^^^^^

Login to OSC's OnDemand, navigate to "Files" and then drag-and-drop files (up to 5 GB) from your local computer to OSC.

SFTP/SCP
^^^^^^^^

To connect to OSC:

.. code-block:: bash

    sftp userid@sftp.osc.edu

Cyberduck
^^^^^^^^^

You can also download and setup `Cyberduck <https://cyberduck.io/?l=en>`_.



Batch Processing (i.e. submitting jobs)
---------------------------------------

"Where the real data processing gets done."

To create a job and submit it to OSC, the following steps are usually done (we'll break down the steps afterward):

1) Create a batch script
2) Submit the batch script as a job
3) Job gets queued
4) When resources become available (length of time you wait depends on how many resources you request), job starts/runs
5) Job finishes up, output is written

Creating a batch script
^^^^^^^^^^^^^^^^^^^^^^^

There are a minimum number of resources that must be specified in order for OSC to accept & run a job. First of all,
the job file (we're going to call it "ourJob.sh"):

.. code-block:: bash

    #PBS -N job_name
    #PBS -l walltime=1:00:00
    #PBS -l nodes=1:ppn=40
    #PBS -A PAS0000
    #PBS -j oe

    # Load modules
    module load blast/2.8.0+

    # Move to directory where job was submitted from
    cd $PBS_O_WORKDIR

    # Copy input data to the job node's local disk space
    cp query.fasta $TMPDIR

    # Change directory to node's local disk
    cd $TMPDIR

    # Execute the command
    blastn -query query.fasta -db nr -outfmt 6 -out results.tsv

    # Copy the results back to the directory where the job was submitted
    cp results.tsv $PBS_O_WORKDIR

Submitting the job
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    qsub ourJob.sh

Job gets queued
^^^^^^^^^^^^^^^

How to show the status:

.. code-block:: bash

    qstat -a jobid
    qstat -u username
    qstat -f jobid

How to delete a job:

.. code-block:: bash

    qdel jobid

When resources become available, job runs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Walltime limits:

* 168 hours for serial (single node) jobs
* 96 hours for parallel (multiple node) jobs

Per-user limits:

* 128 currently running jobs
* 2040 processor cores in use
* 1000 jobs in batch system (running + queued)

Per-group limits:

* 192 concurrently running jobs
* 2040 processor corers in use

**How long will you be waiting for a job to run?** It depends on many factors, such as how many other users are using
OSC, how many resources requested (nodes, cores, GPUs, software licenses), and if you (or your group!) are already using
(or requesting) a lot of resources.

Job finishes up, with results!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What does the output look like? *Besides* the output generated from the tool, the job will generate a couple more files.

They'll be at least a job_name.o1234567, which contains output printed to stdout, but *it may also* contain errors that
were written to stderr. The reason *both* of them would be in the output file is because the job file specified that
the output file should "join" the two: "#PBS -j oe" (i.e. join output + error)

Other cases
^^^^^^^^^^^

**Interactive batch jobs**: good for jobs that can't be run on the login nodes, or as debugging (when you need more
than 1 hour).

.. code-block:: bash

    qsub -I -l nodes=1:ppn=40 -l walltime=1:00:00 -m abe

Keep in mind that it might not be practical to wait for a job when the system load is high. If Pitzer or Owens is at
>95% capacity, expect to wait quite a few minutes.

You can also grab a debug node:

.. code-block:: bash

    qsub -I -l nodes=1:ppn=40 -q debug

Modules
-------

Modules modify environmental variables like $PATH and $MANPATH. By loading a module, you modify your $PATH and lets the
system find the tool you need.

.. code-block:: bash

    module load blast/2.8.0+

With blast loaded, you can now access blastn, blastp, blastx and all the other blast-family executables!

A few things to keep in mind with modules:

* Don't fully replace $PATH with a single folder, like "/fs/project/PAS0000/bin/" - it will cause essential system files
  to not be found. Instead, if you need to update your $PATH:

.. code-block:: bash

    export PATH=$HOME/bin:$PATH

Here, you're *extending* the $PATH variable to include the binaries/executables in $HOME/bin.

A short list to some module commands:

.. code-block:: bash

    module list

Will show you what modules are loaded. Upon login, you'll have several already loaded.

.. code-block:: bash

    module spider

Get a list of what modules are available. If you want to know details about a specific module, add the name of the module
to the command:

.. code-block:: bash

    module spider blast/2.8.0+

Load a module:

.. code-block:: bash

    module load blast/2.8.0+

Unload a module:

.. code-block:: bash

    module unload blast/2.8.0+

Load a different version of a module:

.. code-block:: bash

    module swap intel intel/13.1.3.192

Links
-----

`OSC Getting started guide <https://www.osc.edu/resources/getting_started>`_: a first stop for figuring out how to navigate
OSC and its resources.

`Kate Cahill's guide to OSC <https://khill42.github.io/OSC_IntroHPC/>`_: this is an excellent BEGINNERS guide to
high-performance computing (HPC) on the `Ohio Supercomputer Center (OSC) <https://www.osc.edu/>`_. This provides a
step-by-step guide to pretty much everything you need to know to get started. You'll learn, through the course, what is
the HPC, how to connect, how to use the scheduler (i.e. how to submit jobs), how to use the cluster efficiently, as well
as a basic guide to UNIX commands.


