.. _Tools:

Modules and Tools on OSC
========================

On OSC there are a number of different ways to run a tool/app/executable/binary/etc.


.. code-block:: bash

    $ /fs/ess/PAS1117
    $ run app

1) Directly
2) Loading a module
3) Executing/running a Singularity container

The easiest way of illustrating this point is to use NCBI's BLAST+ set of tools. For example, if we want to compare our
set of proteins (myProteins.faa) against NCBI's non-redundant (nr) database, we need to load and run blastp
(protein-protein comparison).

Running Tools
-------------

Directly
~~~~~~~~

If you know the exact location of the blastp executable on the system, then you can call the program directly using the
"full path" to the executable:

.. code-block:: bash

    /fs/project/PAS1573/tools/ncbi-blast+/2.8.0+/bin/blastp -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv


Using Modules
~~~~~~~~~~~~~

Sometimes a tool requires other tools as dependencies or you might want to run a pipeline of tools, and you don't want
to remember the full path to every tool. Instead, you can build and/or load a module, which extends your $PATH (i.e.
what folders the system looks in to find executables) and modifies other system variables so that all your tools/dependencies
can be found.

.. code-block:: bash

    module load blast/2.8.0+
    blastp -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv

For this example, it seems like an extra line, but in a "real" data analysis pipeline, you can load a single module and
be able to run dozens of tools. Or, using the example above, what if you wanted to compare your sequence against multiple
NCBI databases?

.. code-block:: bash

    module load blast/2.8.0+
    blastn -query myNucleotides.fna -db nt --outfmt 6 -out myNucleotides-vs-NT.tsv
    blastx -query myNucleotides.fna -db nr --outfmt 6 -out myNucleotides-vs-NR.tsv
    blastp -query myProteins.fna -db nr --outfmt 6 -out myProteins-vs-NR.tsv
    rpsblast -query myProteins.fna -db CDD --outfmt 6 -out myProteins-vs-CDD.tsv

Instead of using long paths for every command, or loading a module for every BLAST+ tool individually, you can simply
load one module for the entire collection of BLAST+ tools. In reality, the BLAST+ module we loaded *does load* the
BLAST+ family, but it serves to illustrate this example. One module = many tools.

For a complete description of how to build your own modules, go to :ref:`buildingTools`.

Singularity containers
~~~~~~~~~~~~~~~~~~~~~~

For some tools, they might require dependencies that OSC won't install, or can't. These are often tools or libraries that
need to be installed system-wide. The problem is that oftentimes dependencies among tools can conflict, so OSC doesn't
want to install system-wide dependencies for Tool A that conflict with Tool B. Not only that, but they're installing
something that might affect all users on OSC. OSC tends to sidestep that situation entirely by choosing not to install these
often troublesome tools. So what do you do when there's a tool that needs to be installed but can't be?

Enter `Singularity <https://sylabs.io/singularity/>`_. Personally, this is the preferred method of running a tool for
the Sullivan lab. Singularity containers (we'll get to that in a second) are secure, single-file executables that can
be run on any system w/ Singularity installed. If you've heard of Docker, then Singularity is pretty similar, but offers
a more secure solution for bioinformatics-driven analyses. This is because Docker has a pesky privilege escalation problem,
where a Docker user can maliciously execute code from a Docker container and take control of the host system. As one can
imagine, this would be a problem in a shared HPC environment if a single user could intentionally/unintentionally take
down an entire cluster.

A Singularity container is basically an operating-system-in-a-file. It contains all the system libraries and dependencies
you need in order to run a tool. So if you can install the tool in linux (which covers the vast majority of bioinformatic
tools), then you can use Singularity to package it.

To run a Singularity container on OSC, you must first load Singularity and then you can execute the container.

.. code-block:: bash

    module load singularity/current
    singularity run blastp.simg -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv

There's a bunch of ways to run a container - but keep in mind that the container is treated just like any executable on
the system.

.. code-block:: bash

    module load singularity/current
    singularity run blastp.simg -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv
    singularity exec blastp.simg blastp -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv
    blastp.simg -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv

Notice in the last line you don't even need to call singularity? That's because the Singularity container is smart enough
to tell the system that it needs Singularity to execute it.

For a complete description of how to build your own modules, go to :ref:`buildingTools`.
