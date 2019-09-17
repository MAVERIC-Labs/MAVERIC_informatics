.. _Tools:

#########################
Modules and Tools on OSC
#########################

On OSC there are a number of different ways to run a tool/app/executable/binary/etc.

1) Directly
2) Loading a module
3) Executing/running a Singularity container

The easiest way of illustrating this point is to use NCBI's BLAST+ set of tools. For example, if we want to compare our
set of proteins (myProteins.faa) against NCBI's non-redundant (nr) database, we need to load and run blastp
(protein-protein comparison).

*************
Running Tools
*************

Directly
********

If you know the exact location of the blastp executable on the system, then you can call the program directly using the
"full path" to the executable:

.. code-block:: bash

    /fs/project/PAS1573/tools/ncbi-blast+/2.8.0+/bin/blastp -query myProteins.faa -db nr --outfmt 6 -out myProteins-vs-NR.tsv


Using Modules
*************

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
**********************

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


Available Environmental Microbiology ("eMicro") Apps and Tools
##############################################################

Below is a list and description of the apps available to anyone on OSC. Please keep in mind that this list is not 100%
comprehensive and *does not* detail the methods underlying the tool. Where possible, citations have been included so users
can read the original source's documentation and theory.

Some of this documentation is lifted from the `iVirus project <https://ivirus.readthedocs.io/en/latest/>`_ to avoid
reinventing the wheel. Every effort is being made to ensure that **both** locations are up-to-date with the latest tools
and literature.

**Keep in mind that none of these apps/tools should be run on the login nodes. Please create a job script and submit it or incur OSC's wrath!**

Quality Control
===============

Generally speaking, quality control (QC) is a technique applied to to [most commonly] raw read data. This ensures that
the data going into the assembly (common next step) is of high quality. Poor read quality can result in mis- or
incorrectly assembled sequences. Most frequently, read data QC involves trimming reads according to their quality
scores. Although some assemblers do not require QC’d reads, we highly recommend it!

Trimmomatic
-----------

**Reference**: Bolger, A. M., Lohse, M., & Usadel, B. (2014). Trimmomatic: A flexible trimmer for Illumina Sequence Data. Bioinformatics, btu170.

**Short description**: Identifies adapter sequences in raw sequencing reads and quality filters

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Trimmomatic-0.36.0.img PE -phred33 input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36


Assembly
========

gsAssembler (aka Newbler)
-------------------------

**Reference**: Genivaldo, GZ; Silva, Bas E; Dutilh, David; Matthews, Keri; Elkins, Robert; Schmieder, Elizabeth A;
Dinsdale, Robert A Edwards. "Combining de novo and reference-guided assembly with scaffold_builder". Source Code
Biomed Central. 8 (23). doi:10.1186/1751-0473-8-23.

**Short description**: De novo assembly based on overlap-layout-consensus

**Notes on use**: 454 Life Sciences was purchased by Roche in 2007 and shut down in 2013. There haven't been **any**
updates for the software since then, making it an increasingly aging tool.

**Singularity use**: We provide several versions of the tool on OSC, but please use the latest version unless you have a
good reason otherwise (i.e. reproducing previous results). These are 2.3 and 2.5.

.. code-block:: bash

    module load singularity/current
    singularity run Newbler-2.9.img -o output_dir /path/to/sff/file

The singularity container *does contain* the mapper, but for all intents and purposes, the tool uses runAssembly.

SPAdes
------

**Reference**: Bankevich A., Nurk S., Antipov D., Gurevich A., Dvorkin M., Kulikov A. S., Lesin V., Nikolenko S.,
Pham S., Prjibelski A., Pyshkin A., Sirotkin A., Vyahhi N., Tesler G., Alekseyev M. A., Pevzner P. A. SPAdes: A New
Genome Assembly Algorithm and Its Applications to Single-Cell Sequencing. Journal of Computational Biology, 2012

**Short description**: SPAdes – St. Petersburg genome assembler – is an assembly toolkit containing various assembly
pipelines

**Notes on use**: SPAdes, as with many de Bruijn assemblers, can consume incredibly amounts of memory. In the context
of viral metagenomics, it's been known to use 2-3, and upwards of 6 TB of memory (and more if you give it more data!).
There are multiple implementations on OSC using different runtimes and memory allocations.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run SPAdes-3.13.1.simg

IDBA-UD
-------

**Reference**: Peng, Y., et al. (2010) IDBA- A Practical Iterative de Bruijn Graph De Novo Assembler. RECOMB. Lisbon.

Peng, Y., et al. (2012) IDBA-UD: a de novo assembler for single-cell and metagenomic sequencing data with highly uneven
depth, Bioinformatics, 28, 1420-1428.

**Short description**: IDBA-UD is a iterative De Bruijn Graph De Novo Assembler for Short Reads Sequencing data with
Highly Uneven Sequencing Depth. It is an extension of IDBA algorithm.

**Long description**: IDBA-UD is a iterative De Bruijn Graph De Novo Assembler for Short Reads Sequencing data with
Highly Uneven Sequencing Depth. It is an extension of IDBA algorithm. IDBA-UD also iterates from small k to a large k.
In each iteration, short and low-depth contigs are removed iteratively with cutoff threshold from low to high to reduce
the errors in low-depth and high-depth regions. Paired-end reads are aligned to contigs and assembled locally to
generate some missing k-mers in low-depth regions. With these technologies, IDBA-UD can iterate k value of de Bruijn
graph to a very large value with less gaps and less branches to form long contigs in both low-depth and high-depth
regions. (taken from website)

**Singularity use**:

Forthcoming!

Trinity
-------

**Reference**: Grabherr MG, Haas BJ, Yassour M, Levin JZ, Thompson DA, Amit I, Adiconis X, Fan L, Raychowdhury R, Zeng
Q, Chen Z, Mauceli E, Hacohen N, Gnirke A, Rhind N, di Palma F, Birren BW, Nusbaum C, Lindblad-Toh K, Friedman N, Regev
A. Full-length transcriptome assembly from RNA-seq data without a reference genome. Nat Biotechnol. 2011
May 15;29(7):644-52. doi: 10.1038/nbt.1883. PubMed PMID: 21572440.

**Short description**: Trinity assembles transcript sequences from Illumina RNA-Seq data.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Trinity-2.4.0.img


Gene Callers
============

FragGeneScan
------------

**Reference**: Mina Rho, Haixu Tang, and Yuzhen Ye. FragGeneScan: Predicting Genes in Short and Error-prone Reads. Nucl. Acids Res., 2010 doi: 10.1093/nar/gkq747

**Short description**: FragGeneScan is an application for finding (fragmented) genes in short reads

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run FragGeneScan-1.30.0.img

Prodigal
--------

**Reference**: Hyatt, D. Prodigal (2.6.3) [Software]. Available at https://github.com/hyattpd/Prodigal

**Short description**: Fast, reliable protein-coding gene prediction for prokaryotic genomes.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Prodigal-2.6.3.img -i metagenome.fna -o coords.gbk -a proteins.faa -p anon

MetaGeneAnnotator ("MGA")
-------------------------

**Reference**: Noguchi, H., Taniguchi, T., & Itoh, T. (2008). MetaGeneAnnotator: Detecting Species-Specific Patterns of
Ribosomal Binding Site for Precise Gene Prediction in Anonymous Prokaryotic and Phage Genomes. DNA Research, 15(6),
387–396. https://doi.org/10.1093/dnares/dsn027

**Short description**: MetaGeneAnnotator is a gene-finding program for prokaryote and phage

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run MetaGeneAnnotator-1.1.0.img


Annotation and Analyses
=======================

Prokka
------

**Reference**: Seemann T. Prokka: rapid prokaryotic genome annotation Bioinformatics 2014 Jul 15;30(14):2068-9.
PMID:24642063

**Short description**: Prokka is a software tool to annotate bacterial, archaeal and viral genomes quickly and produce
standards-compliant output files

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Prokka-1.12.0.img


Diamond
-------

**Reference**: B. Buchfink, Xie C., D. Huson, "Fast and sensitive protein alignment using DIAMOND", Nature Methods 12,
59-60 (2015)

**Short description**: DIAMOND is a sequence aligner for protein and translated DNA searches, designed for high
performance analysis of big sequence data.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Diamond-0.9.10.img

CAT
---

**Reference**: https://github.com/dutilh/CAT

**Short description**: Contig Annotation Tool (CAT) is a pipeline for the taxonomic classification of long DNA sequences
 and metagenome assembled genomes (MAGs/bins) of both known and (highly) unknown microorganisms, as generated by
 contemporary metagenomics studies.

**Other notes**: There are two versions of CAT. A pre-4.x version ("1.0.0") and a post 4.x version ("4.3.3"). The new one
is superior in all aspects, except database setup. The paths provided will not work unless you have the appropriate
databases installed.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run CAT-4.3.3.simg contigs -c {contigs fasta} -d 2019-03-31_CAT_database -t 2019-03-31_taxonomy

Viral Analyses
==============

"Consider something viral in your research" - F. Rohwer

VIRSorter
---------

**Reference**: Roux S, Enault F, Hurwitz BL, Sullivan MB. (2015) VirSorter: mining viral signal from microbial genomic
data. PeerJ 3:e985 https://doi.org/10.7717/peerj.985

**Short description**: Identify viral contigs in a microbial metagenomes

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run VirSorter-1.0.5.img

vConTACT
--------

vConTACT is a suite a tools that classify contigs/genomes based on their shared gene content. v1 "requires"
3 tools, whereas v2 (below) only requires 2.

**Reference**: Bolduc B, Jang H Bin, Doulcier G, You Z, Roux S, Sullivan MB. (2017). vConTACT: an iVirus tool to
classify double-stranded DNA viruses that infect Archaea and Bacteria. PeerJ 5: e3243.

**Short description**: Guilt-by-contig-association automatic classification of viral contigs

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run vContact-Gene2Contig-1.0.0.img
    singularity run vContact_PCs-0.1.60.img
    singularity run vContact-1.60.0.img

More forthcoming!!!

vConTACT2
---------

**Reference**: Bin Jang, H., Bolduc, B., Zablocki, O., Kuhn, J. H., Roux, S., Adriaenssens, E. M., …
Sullivan, M. B. (2019). Taxonomic assignment of uncultivated prokaryotic virus genomes is enabled by
gene-sharing networks. Nature Biotechnology. https://doi.org/10.1038/s41587-019-0100-8

**Short description**: Guilt-by-contig-association automatic classification of viral contigs

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run vConTACT2-0.9.9.simg


