.. _eMicroApps:

Available Environmental Microbiology ("eMicro") Apps and Tools
==============================================================

Below is a list and description of the apps available to anyone on OSC. Please keep in mind that this list is not 100%
comprehensive and *does not* detail the methods underlying the tool. Where possible, citations have been included so users
can read the original source's documentation and theory.

Some of this documentation is lifted from the `iVirus project <https://ivirus.readthedocs.io/en/latest/>`_ to avoid
reinventing the wheel. Every effort is being made to ensure that **both** locations are up-to-date with the latest tools
and literature.

**One last thing to note: All of the singularity images are located at:**

/users/PAS1117/osu9664/eMicro-Apps/

So you must prepend each \*.img, \*.simg or \*.sif Singularity container w/ this path OR link them (see :ref:`UNIX_LINUX`).

**Example**:

.. code-block:: bash

    module load singularity/current
    singularity run Prokka-1.12.0.img -h

**should be**

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Prokka-1.12.0.img -h

**Keep in mind that NONE of these apps/tools should be run on the login nodes. Please create a job script and submit it
or incur OSC's wrath!**

Also to note: There are several cases where these tools have been used in the `CyVerse cyberinfrastructure <https://www.cyverse.org/>`_.
For these, there is a `protocols.io <https://www.protocols.io/>`_ link. We're continually developing these protocols and
trying to keep them up to date (though if it's not broke and a current version, it'll likely not be updated), so always
make sure it's the latest version.

**For Sullivan lab members, also included are OSC's module system, to use:**

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles  # Load Sullivan lab's modules
    module load Prokka/1.13
    prokka -h


Quality Control (Reads)
-----------------------

Generally speaking, quality control (QC) is a technique applied to to [most commonly] raw read data. This ensures that
the data going into the assembly (common next step) is of high quality. Poor read quality can result in mis- or
incorrectly assembled sequences. Most frequently, read data QC involves trimming reads according to their quality
scores. Although some assemblers do not require QC’d reads, we highly recommend it!

Trimmomatic
~~~~~~~~~~~

**Reference**: Bolger, A. M., Lohse, M., & Usadel, B. (2014). Trimmomatic: A flexible trimmer for Illumina Sequence Data. Bioinformatics, btu170.

**Short description**: Identifies adapter sequences in raw sequencing reads and quality filters

**Protocols.io**: `Trimmomatic on CyVerse <https://dx.doi.org/10.17504/protocols.io.gvybw7w>`_

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Trimmomatic-0.36.0.img PE -phred33 input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load trimmomatic/0.36-sulli
    trimmomatic PE -phred33 input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

**Notes**: Trimmomatic is a java jar file, and *normally* needs to be executed with "java -jar trimmomatic.jar [commands]",
but a tiny bash script has been written to automate this, which is why you can call "trimmomatic" without the java component.


BBTools
~~~~~~~

**Reference**: http://sourceforge.net/projects/bbmap/

**Reference** (BBMerge): Bushnell, B., Rood, J., & Singer, E. (2017). BBMerge – Accurate paired shotgun read merging
via overlap. PLOS ONE, 12(10), e0185056. https://doi.org/10.1371/journal.pone.0185056

**Short description**: BBTools is a suite of fast, multithreaded bioinformatics tools designed for analysis of DNA and
RNA sequence data. BBTools can handle common sequencing file formats such as fastq, fasta, sam, scarf, fasta+qual,
compressed or raw, with autodetection of quality encoding and interleaving.

**Note**: This is SEVERAL tools, BBDuk (discussed below) is just one of them. We'll be working on detailing this here,
but in the meantime, any tool available on https://jgi.doe.gov/data-and-tools/bbtools/ is available through this image.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run BBTools-38.69.sif

BBDuk
~~~~~

**Website**: https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/

**Short description**: “Duk” stands for Decontamination Using Kmers. BBDuk was developed to combine most common
data-quality-related trimming, filtering, and masking operations into a single high-performance tool. It is capable of
quality-trimming and filtering, adapter-trimming, contaminant-filtering via kmer matching, sequence masking,
GC-filtering, length filtering, entropy-filtering, format conversion, histogram generation, subsampling, quality-score
recalibration, kmer cardinality estimation, and various other operations in a single pass.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    # Just adapter trimming
    singularity run BBTools-38.69.sif bbduk.sh in1=<input-pair1> in2=<input-pair2> out1=<trimmed-pair1> out2=<trimmed-pair2> ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    # Just quality filtering
    singularity run BBTools-38.69.sif bbduk.sh in1=<trimmed-pair1> in2=<trimmed-pair2> qtrim=rl trimq=10 out1=<trimmed-and-quality-pair1> out2=<trimmed-and-quality-pair2>
    # Adapter and quality filtering
    singularity run BBTools-38.69.sif bbduk.sh in1=<input-pair1> in2=<input-pair2> out1=<qc-trimmed-pair1> out2=<qc-trimmed-pair2> ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo trimq=10 qtrim=rl minlength=35


MultiQC
~~~~~~~

**Website**: https://multiqc.info/

**Reference**: Ewels, P., Magnusson, M., Lundin, S., & Käller, M. (2016). MultiQC: Summarize analysis results for
multiple tools and samples in a single report. Bioinformatics, 32(19), 3047–3048. https://doi.org/10.1093/bioinformatics/btw354

**Short description**: MultiQC searches a given directory for analysis logs and compiles a HTML report. It's a general
use tool, perfect for summarising the output from numerous bioinformatics tools

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run MultiQC-1.7.sif

Assembly
--------

gsAssembler (aka Newbler)
~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~

**Reference**: Bankevich A., Nurk S., Antipov D., Gurevich A., Dvorkin M., Kulikov A. S., Lesin V., Nikolenko S.,
Pham S., Prjibelski A., Pyshkin A., Sirotkin A., Vyahhi N., Tesler G., Alekseyev M. A., Pevzner P. A. SPAdes: A New
Genome Assembly Algorithm and Its Applications to Single-Cell Sequencing. Journal of Computational Biology, 2012

**Short description**: SPAdes – St. Petersburg genome assembler – is an assembly toolkit containing various assembly
pipelines

**Protocols.io**: `Running SPAdes on CyVerse <https://dx.doi.org/10.17504/protocols.io.ewrbfd6>`_

**Notes on use**: SPAdes, as with many de Bruijn assemblers, can consume incredibly amounts of memory. In the context
of viral metagenomics, it's been known to use 2-3, and upwards of 6 TB of memory (and more if you give it more data!).
There are multiple implementations on OSC using different runtimes and memory allocations.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run SPAdes-3.13.0.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load spades/3.13.1


IDBA-UD
~~~~~~~

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

.. code-block:: bash

    singularity run IDBA-UD-1.1.3.sif --num_threads <threads> -r <reads-in-fasta-format> -o <output-dir>

Trinity
~~~~~~~

**Reference**: Grabherr MG, Haas BJ, Yassour M, Levin JZ, Thompson DA, Amit I, Adiconis X, Fan L, Raychowdhury R, Zeng
Q, Chen Z, Mauceli E, Hacohen N, Gnirke A, Rhind N, di Palma F, Birren BW, Nusbaum C, Lindblad-Toh K, Friedman N, Regev
A. Full-length transcriptome assembly from RNA-seq data without a reference genome. Nat Biotechnol. 2011
May 15;29(7):644-52. doi: 10.1038/nbt.1883. PubMed PMID: 21572440.

**Short description**: Trinity assembles transcript sequences from Illumina RNA-Seq data.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Trinity-2.4.0.img

MEGAHIT
~~~~~~~

**Reference**: Li, D., Liu, C. M., Luo, R., Sadakane, K., & Lam, T. W. (2014). MEGAHIT: An ultra-fast single-node
solution for large and complex metagenomics assembly via succinct de Bruijn graph. Bioinformatics, 31(10), 1674–1676.
https://doi.org/10.1093/bioinformatics/btv033

**Short description**: MEGAHIT is an ultra-fast and memory-efficient NGS assembler. It is optimized for metagenomes,
but also works well on generic single genome assembly (small or mammalian size) and single-cell assembly.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run MEGAHIT-1.2.8.sif --k-list 21,41,61,81,99 -t <threads> -m 0.9 -1 <for-reads> -2 <rev-reads> -o <output-dir>

Binning
-------

MetaBAT2
~~~~~~~~

**Reference**: https://bitbucket.org/berkeleylab/metabat

**Reference**: Kang, D. D., Froula, J., Egan, R., & Wang, Z. (2015). MetaBAT, an efficient tool for accurately
reconstructing single genomes from complex microbial communities. PeerJ, 3(8), e1165. https://doi.org/10.7717/peerj.1165

**Short description**: A robust statistical framework for reconstructing genomes from metagenomic data

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run MetaBAT2-2.14.sif

    # Download test data (instructions from https://bitbucket.org/berkeleylab/metabat/wiki/Best%20Binning%20Practices)
    wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Files/BestPractices/V2/CASE1/assembly.fa.gz
    wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Files/BestPractices/V2/CASE1/depth.txt

    # Run MetaBAT2
    singularity run MetaBAT2-2.14.sif -i assembly.fa.gz -a depth.txt -o resA1/bin -v

MaxBin2
~~~~~~~

**Website**: https://downloads.jbei.org/data/microbial_communities/MaxBin/MaxBin.html

**Website (alt)**: https://sourceforge.net/projects/maxbin/

**Reference** (MaxBin1): Wu, Y.-W., Tang, Y.-H., Tringe, S. G., Simmons, B. A., & Singer, S. W. (2014). MaxBin: an
automated binning method to recover individual genomes from metagenomes using an expectation-maximization algorithm.
Microbiome, 2(1), 26. https://doi.org/10.1186/2049-2618-2-26

**Reference** (MaxBin2): Yu-Wei Wu, Blake A. Simmons, Steven W. Singer, MaxBin 2.0: an automated binning algorithm to
recover genomes from multiple metagenomic datasets, Bioinformatics, Volume 32, Issue 4, 15 February 2016, Pages 605–607,
https://doi.org/10.1093/bioinformatics/btv638

**Short description**: MaxBin2 is the next-generation of MaxBin () that supports multiple samples at the same time.
MaxBin is a software for binning assembled metagenomic sequences based on an Expectation-Maximization algorithm. Users
could understand the underlying bins (genomes) of the microbes in their metagenomes by simply providing assembled
metagenomic sequences and the reads coverage information or sequencing reads. For users' convenience MaxBin will report
genome-related statistics, including estimated completeness, GC content and genome size in the binning summary page.
Users could use MEGAN or similar software on MaxBin bins to find out the taxonomy of each bin after the binning process
is finished.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run MaxBin2.sif

    # Download test data
    wget -O 20x.scaffold https://downloads.jbei.org/data/microbial_communities/MaxBin/getfile.php?20x.scaffold
    wget -O 20x.abund https://downloads.jbei.org/data/microbial_communities/MaxBin/getfile.php?20x.abund

    # Run MaxBin2
    singularity run MaxBin2.sif -contig 20x.scaffold -abund 20x.abund -out 20x.out -thread 4

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MaxBin/2.2.6

CONCOCT
~~~~~~~

**Website**: https://concoct.readthedocs.io/en/latest/

**Reference**: Alneberg, J., Bjarnason, B. S., de Bruijn, I., Schirmer, M., Quick, J., Ijaz, U. Z., … Quince, C. (2013).
 CONCOCT: Clustering cONtigs on COverage and ComposiTion, 1–28. Retrieved from http://arxiv.org/abs/1312.4038

**Short description**: CONCOCT “bins” metagenomic contigs. Metagenomic binning is the process of clustering sequences
into clusters corresponding to operational taxonomic units of some level.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run CONCOCT.sif


MetaWRAP
~~~~~~~~

**Website**: https://github.com/bxlab/metaWRAP

**Reference**: Uritskiy, G. V., DiRuggiero, J., & Taylor, J. (2018). MetaWRAP—a flexible pipeline for genome-resolved
metagenomic data analysis. Microbiome, 6(1), 158. https://doi.org/10.1186/s40168-018-0541-1

**Short description**: MetaWRAP aims to be an easy-to-use metagenomic wrapper suite that accomplishes the core tasks of
metagenomic analysis from start to finish: read quality control, assembly, visualization, taxonomic profiling, extracting
draft genomes (binning), and functional annotation. Additionally, metaWRAP takes bin extraction and analysis to the
next level (see module overview below). While there is no single best approach for processing metagenomic data,
metaWRAP is meant to be a fast and simple approach before you delve deeper into parameterization of your analysis.
MetaWRAP can be applied to a variety of environments, including gut, water, and soil microbiomes (see metaWRAP paper
for benchmarks). Each individual module of metaWRAP is a standalone program, which means you can use only the modules
you are interested in for your data.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load metaWRAP

DAS_Tool
~~~~~~~~

**Website**: https://github.com/cmks/DAS_Tool

**Reference**: Sieber, C. M. K., Probst, A. J., Sharrar, A., Thomas, B. C., Hess, M., Tringe, S. G., & Banfield,
 J. F. (2018). Recovery of genomes from metagenomes via a dereplication, aggregation and scoring strategy. Nature
 Microbiology, 3(7), 836–843. https://doi.org/10.1038/s41564-018-0171-1

**Short description**: DAS Tool is an automated method that integrates the results of a flexible number of binning
algorithms to calculate an optimized, non-redundant set of bins from a single assembly.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run DAS_Tool.sif

    # You can test the installation
    git clone https://github.com/cmks/DAS_Tool.git
    singularity run DAS_Tool.sif -i DAS_Tool/sample_data/sample.human.gut_concoct_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_maxbin2_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_metabat_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_tetraESOM_scaffolds2bin.tsv -l concoct,maxbin,metabat,tetraESOM -c DAS_Tool/sample_data/sample.human.gut_contigs.fa --search_engine diamond -o DASToolTestRun


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load DAS_Tool


Gene Callers
------------

FragGeneScan
~~~~~~~~~~~~

**Reference**: Mina Rho, Haixu Tang, and Yuzhen Ye. FragGeneScan: Predicting Genes in Short and Error-prone Reads. Nucl. Acids Res., 2010 doi: 10.1093/nar/gkq747

**Short description**: FragGeneScan is an application for finding (fragmented) genes in short reads

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run FragGeneScan-1.30.0.img

Prodigal
~~~~~~~~

**Reference**: Hyatt, D. Prodigal (2.6.3) [Software]. Available at https://github.com/hyattpd/Prodigal

**Short description**: Fast, reliable protein-coding gene prediction for prokaryotic genomes.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Prodigal-2.6.3.img -i metagenome.fna -o coords.gbk -a proteins.faa -p anon

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load prodigal/2.6.3
    prodigal -i metagenome.fna -o coords.gbk -a proteins.faa -p anon


MetaGeneAnnotator ("MGA")
~~~~~~~~~~~~~~~~~~~~~~~~~

**Reference**: Noguchi, H., Taniguchi, T., & Itoh, T. (2008). MetaGeneAnnotator: Detecting Species-Specific Patterns of
Ribosomal Binding Site for Precise Gene Prediction in Anonymous Prokaryotic and Phage Genomes. DNA Research, 15(6),
387–396. https://doi.org/10.1093/dnares/dsn027

**Short description**: MetaGeneAnnotator is a gene-finding program for prokaryote and phage

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run MetaGeneAnnotator-1.1.0.img


Annotation and Analyses
-----------------------

This is a catch-all category that doesn't fit with the other sections.

Prokka
~~~~~~

**Reference**: Seemann T. Prokka: rapid prokaryotic genome annotation Bioinformatics 2014 Jul 15;30(14):2068-9.
PMID:24642063

**Short description**: Prokka is a software tool to annotate bacterial, archaeal and viral genomes quickly and produce
standards-compliant output files

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Prokka-1.12.0.img

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Prokka/1.13

Diamond
~~~~~~~

**Reference**: B. Buchfink, Xie C., D. Huson, "Fast and sensitive protein alignment using DIAMOND", Nature Methods 12,
59-60 (2015)

**Short description**: DIAMOND is a sequence aligner for protein and translated DNA searches, designed for high
performance analysis of big sequence data.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Diamond-0.9.10.img

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load diamond/0.9.24

CAT
~~~

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

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load CAT/4.3.3

Centrifuge
~~~~~~~~~~

**Website**: http://www.ccb.jhu.edu/software/centrifuge

**Reference**: Kim, D., Song, L., Breitwieser, F. P., & Salzberg, S. L. (2016). Centrifuge: rapid and sensitive
classification of metagenomic sequences. Genome Research, 26(12), 1721–1729. https://doi.org/10.1101/gr.210641.116

**Short description**: [Centrifuge] is a novel microbial classification engine that enables rapid, accurate and
sensitive labeling of reads and quantification of species on desktop computers. The system uses a novel indexing
scheme based on the Burrows-Wheeler transform (BWT) and the Ferragina-Manzini (FM) index, optimized specifically for
the metagenomic classification problem. Centrifuge requires a relatively small index (4.7 GB for all complete bacterial
and viral genomes plus the human genome) and classifies sequences at very high speed, allowing it to process the
millions of reads from a typical high-throughput DNA sequencing run within a few minutes. Together these advances
enable timely and accurate analysis of large metagenomics data sets on conventional desktop computers

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run Centrifuge-X.sif

(more forthcoming!)

VSEARCH
~~~~~~~

**Website**:https://github.com/torognes/vsearch

**Reference**: Rognes, T., Flouri, T., Nichols, B., Quince, C., & Mahé, F. (2016). VSEARCH: a versatile open source
tool for metagenomics. PeerJ, 4(10), e2584. https://doi.org/10.7717/peerj.2584

**Short description**: VSEARCH is a fast, accurate and full-fledged alternative to USEARCH. It's free, isn't limited to
32-bit, but is only for nucleotide, not protein work. VSEARCH is “more accurate than USEARCH when performing searching,
clustering, chimera detection and subsampling, while on a par with USEARCH for paired-ends read merging. VSEARCH is
slower than USEARCH when performing clustering and chimera detection, but significantly faster when performing
paired-end reads merging and dereplication.” (Rognes et al, 2016. PeerJ)

Long story short: it's a free alternative to USEARCH's 64-bit version. USEARCH does have a free 32-bit version, but that
limits the available system memory to 4 GB, hardly sufficient to do large-scale metagenomic analyses.


**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run VSEARCH-2.14.1.sif

**Note**: VSEARCH has **a lot** of options. So. Many.

CheckM
~~~~~~

**Website**: https://github.com/Ecogenomics/CheckM

**Reference**: Parks DH, Imelfort M, Skennerton CT, Hugenholtz P, Tyson GW. 2015. CheckM: assessing the quality of
microbial genomes recovered from isolates, single cells, and metagenomes. Genome Research, 25: 1043–1055.

**Short description**: CheckM provides a set of tools for assessing the quality of genomes recovered from isolates,
single cells, or metagenomes. It provides robust estimates of genome completeness and contamination by using collocated
sets of genes that are ubiquitous and single-copy within a phylogenetic lineage.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run CheckM-1.0.18.sif


BamM
~~~~

**Website**: http://ecogenomics.github.io/BamM/

**Short description**: Metagenomics-focused BAM file manipulation

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run BamM-1.7.0.sif

**Note**: This is no longer actively maintained. CoverM is a direct replacement.

CoverM
~~~~~~

**Website**: https://github.com/wwood/CoverM

**Short description**: CoverM aims to be a configurable, easy to use and fast DNA read coverage and relative abundance
calculator focused on metagenomics applications. CoverM calculates coverage of genomes/MAGs (coverm genome) or
individual contigs (coverm contig). Calculating coverage by read mapping, its input can either be BAM files sorted by
reference, or raw reads and reference FASTA sequences.

Forthcoming!


Viral Analyses
--------------

"Consider something viral in your research" - F. Rohwer

VIRSorter
~~~~~~~~~

**Reference**: Roux S, Enault F, Hurwitz BL, Sullivan MB. (2015) VirSorter: mining viral signal from microbial genomic
data. PeerJ 3:e985 https://doi.org/10.7717/peerj.985

**Short description**: Identify viral contigs in a microbial metagenomes

**Protocols.io**: `VIRSorter on CyVerse <https://dx.doi.org/10.17504/protocols.io.eyjbfun>`_

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run VirSorter-1.0.5.img

vConTACT2
~~~~~~~~~

vConTACT2 is a tool designed to classify viruses based on their shared gene content. It is *intended for* archaeal and
bacterial viruses. It *can* work for *some* eukaryotic viruses, but may utterly fail *or* totally work - regardless -
it hasn't been vetted or tested for use with them.

**Reference (V2)**: Bin Jang, H., Bolduc, B., Zablocki, O., Kuhn, J. H., Roux, S., Adriaenssens, E. M., …
Sullivan, M. B. (2019). Taxonomic assignment of uncultivated prokaryotic virus genomes is enabled by
gene-sharing networks. Nature Biotechnology. https://doi.org/10.1038/s41587-019-0100-8

**Reference (Theory)**: Bolduc B, Jang H Bin, Doulcier G, You Z, Roux S, Sullivan MB. (2017). vConTACT: an iVirus tool
to classify double-stranded DNA viruses that infect Archaea and Bacteria. PeerJ 5: e3243.

**Protocols.io**: `Running vConTACT2 on VIRSorter output in CyVerse <https://dx.doi.org/10.17504/protocols.io.x5xfq7n>`_

**Short description**: Guilt-by-contig-association automatic classification of viral contigs

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run vConTACT2-0.9.9.sif


IVA
~~~

**Website**: https://sanger-pathogens.github.io/iva/

**Reference**: Hunt, M., Gall, A., Ong, S. H., Brener, J., Ferns, B., Goulder, P., … Otto, T. D. (2015). IVA: Accurate
de novo assembly of RNA virus genomes. Bioinformatics, 31(14), 2374–2376. https://doi.org/10.1093/bioinformatics/btv120

**Short description**: IVA is a de novo assembler designed to assemble virus genomes that have no repeat sequences,
using Illumina read pairs sequenced from mixed populations at extremely high and variable depth.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run IVA-1.0.9.sif

    # You can test the installation
    singularity run IVA-1.0.9.sif --test outdir

PhageTerm
~~~~~~~~~

**Website**: https://sourceforge.net/projects/phageterm/

**Reference**: Garneau, J. R., Depardieu, F., Fortier, L.-C., Bikard, D., & Monot, M. (2017). PhageTerm: a tool for
fast and accurate determination of phage termini and packaging mechanism using next-generation sequencing data.
Scientific Reports, 7(1), 8292. https://doi.org/10.1038/s41598-017-07910-5

**Short description**:  Here, we developed a theoretical and statistical framework to analyze DNA termini and phage
packaging mechanisms using next-generation sequencing data. PhageTerm was validated on a set of phages with
well-established packaging mechanisms representative of the termini diversity: 5’cos (lambda), 3’cos (HK97), pac (P1),
headful without a pac site (T4), DTR (T7) and host fragment (Mu). In addition, we determined the termini of 9
Clostridium difficile phages and 5 phages whose sequences where retrieved from the sequence read archive (SRA)

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run PhageTerm-1.0.12.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PhageTerm/1.0.11

