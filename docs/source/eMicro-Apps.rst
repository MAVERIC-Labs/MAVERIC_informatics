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
    # OR
    module load Prokka/1.14.6
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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Trimmomatic-0.36.0.img PE -phred33 input_forward.fq.gz input_reverse.fq.gz output_forward_paired.fq.gz output_forward_unpaired.fq.gz output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

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

**Short description**: BBTools is a suite of fast, multi-threaded bioinformatics tools designed for analysis of DNA and
RNA sequence data. BBTools can handle common sequencing file formats such as fastq, fasta, sam, scarf, fasta+qual,
compressed or raw, with autodetection of quality encoding and interleaving.

**Note**: This is SEVERAL tools, BBDuk (discussed below) is just one of them. We'll be working on detailing this here,
but in the meantime, any tool available on https://jgi.doe.gov/data-and-tools/bbtools/ is available through this image.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif

BBDuk (in the BBTools package)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif bbduk.sh in1=<input-pair1> in2=<input-pair2> out1=<trimmed-pair1> out2=<trimmed-pair2> ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    # Just quality filtering
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif bbduk.sh in1=<trimmed-pair1> in2=<trimmed-pair2> qtrim=rl trimq=10 out1=<trimmed-and-quality-pair1> out2=<trimmed-and-quality-pair2>

Alternatively, run them both at the same time!

.. code-block:: bash

    # Adapter and quality filtering *at the same time*
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif bbduk.sh in1=<input-pair1> in2=<input-pair2> out1=<qc-trimmed-pair1> out2=<qc-trimmed-pair2> ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo trimq=10 qtrim=rl minlength=35

FastQC
~~~~~~~

**Website**: https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

**Short description**: FastQC aims to provide a simple way to do some quality control checks on raw sequence data
coming from high throughput sequencing pipelines. It provides a modular set of analyses which you can use to give a
quick impression of whether your data has any problems of which you should be aware before doing any further analysis.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/FastQC-0.11.8.sif <input-fastq-file>

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load fastqc/0.11.5

**Module use (directly from OSC)**:

.. code-block:: bash

    module load fastqc/0.11.8


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MultiQC-1.7.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MultiQC


QUAST/MetaQUAST
~~~~~~~~~~~~~~~

**Website**: http://quast.sourceforge.net/

**Short Description**: The project aim is to create easy-to-use tools for genome assemblies evaluation and comparison.

**Reference**: Gurevich, A., Saveliev, V., Vyahhi, N., & Tesler, G. (2013). QUAST: Quality assessment tool for genome
assemblies. Bioinformatics, 29(8), 1072–1075. https://doi.org/10.1093/bioinformatics/btt086

**Reference (using v4.x)**: Mikheenko, A., Valin, G., Prjibelski, A., Saveliev, V., & Gurevich, A. (2016). Icarus:
Visualizer for de novo assembly evaluation. Bioinformatics, 32(21), 3321–3323.
https://doi.org/10.1093/bioinformatics/btw379

**Reference (using v5.x)**: Mikheenko, A., Prjibelski, A., Saveliev, V., Antipov, D., & Gurevich, A. (2018). Versatile
genome assembly evaluation with QUAST-LG. Bioinformatics, 34(13), i142–i150.
https://doi.org/10.1093/bioinformatics/bty266

**Singularity use**:

Forthcoming!

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load quast/4.5

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Newbler-2.9.img -o output_dir /path/to/sff/file

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SPAdes-3.13.0.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load spades/3.15.2


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

    singularity run /users/PAS1117/osu9664/eMicro-Apps/IDBA-UD-1.1.3.sif --num_threads <threads> -r <reads-in-fasta-format> -o <output-dir>

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Trinity-2.4.0.img

MEGAHIT
~~~~~~~

**Reference**: Li, D., Liu, C. M., Luo, R., Sadakane, K., & Lam, T. W. (2014). MEGAHIT: An ultra-fast single-node
solution for large and complex metagenomics assembly via succinct de Bruijn graph. Bioinformatics, 31(10), 1674–1676.
https://doi.org/10.1093/bioinformatics/btv033

**Short description**: MEGAHIT is an ultra-fast and memory-efficient NGS assembler. It is optimized for metagenomes,
but also works well on generic single genome assembly (small or mammalian size) and single-cell assembly.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MEGAHIT/1.2.9

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MEGAHIT-1.2.8.sif --k-list 21,41,61,81,99 -t <threads> -m 0.9 -1 <for-reads> -2 <rev-reads> -o <output-dir>

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MetaBAT2-2.14.sif

    # Download test data (instructions from https://bitbucket.org/berkeleylab/metabat/wiki/Best%20Binning%20Practices)
    wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Files/BestPractices/V2/CASE1/assembly.fa.gz
    wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Files/BestPractices/V2/CASE1/depth.txt

    # Run MetaBAT2
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MetaBAT2-2.14.sif -i assembly.fa.gz -a depth.txt -o resA1/bin -v

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MaxBin2.sif -contig 20x.scaffold -abund 20x.abund -out 20x.out -thread 4

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CONCOCT-1.1.0.sif

See :ref:`processing_microbe` for a more detailed explanation on usage.


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DAS_Tool.sif

    # You can test the installation (if you've git cloned the repository!)
    git clone https://github.com/cmks/DAS_Tool.git
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DAS_Tool.sif -i DAS_Tool/sample_data/sample.human.gut_concoct_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_maxbin2_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_metabat_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_tetraESOM_scaffolds2bin.tsv -l concoct,maxbin,metabat,tetraESOM -c DAS_Tool/sample_data/sample.human.gut_contigs.fa --search_engine diamond -o DASToolTestRun


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load DAS_Tool

UniteM
~~~~~~

**Website**: https://github.com/dparks1134/UniteM

**Reference**: https://github.com/dparks1134/UniteM (cite the repository)

**Short description**: UniteM is a software toolkit implementing different ensemble binning strategies for producing a
non-redundant set of bins from the output of multiple binning methods.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load uniteM


Gene Callers
------------

FragGeneScan
~~~~~~~~~~~~

**Reference**: Mina Rho, Haixu Tang, and Yuzhen Ye. FragGeneScan: Predicting Genes in Short and Error-prone Reads. Nucl. Acids Res., 2010 doi: 10.1093/nar/gkq747

**Short description**: FragGeneScan is an application for finding (fragmented) genes in short reads

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/FragGeneScan-1.30.0.img

Prodigal
~~~~~~~~

**Reference**: Hyatt, D. Prodigal (2.6.3) [Software]. Available at https://github.com/hyattpd/Prodigal

**Short description**: Fast, reliable protein-coding gene prediction for prokaryotic genomes.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Prodigal-2.6.3.img -i metagenome.fna -o coords.gbk -a proteins.faa -p anon

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MetaGeneAnnotator-1.1.0.img

MetaGeneMark
~~~~~~~~~~~~

**Website**:

**Reference**: Zhu, W., Lomsadze, A. & Borodovsky, M. Ab initio gene identification in metagenomic sequences.
Nucleic Acids Res. 38, 1–15 (2010).

**Short description**: ORF prediction...

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MetaGeneMark/3.38

    gmhmmp <rest-of-command>


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Prokka-1.12.0.img

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Diamond-0.9.26.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load diamond/0.9.24

    # OR
    module load diamond/ 2.0.5

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CAT-4.3.3.simg contigs -c {contigs fasta} -d 2019-03-31_CAT_database -t 2019-03-31_taxonomy

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Centrifuge-X.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load centrifuge/1.0.3

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/VSEARCH-2.14.1.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load vsearch/2.6.0

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CheckM-1.0.18.sif


Clust
~~~~~

**Website**: https://github.com/baselabujamous/clust

**Reference**: Abu-Jamous, B., & Kelly, S. (2018). Clust: automatic extraction of optimal co-expressed gene clusters
from gene expression data. Genome Biology, 19(1), 172. https://doi.org/10.1186/s13059-018-1536-8

**Short description**: Clust is a fully automated method for identification of clusters (groups) of genes that are
consistently co-expressed (well-correlated) in one or more heterogeneous datasets from one or multiple species.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/clust-1.8.9.img data_path -o output_directory [...]

Please do read the extensive documentation on the Clust github page.


BamM
~~~~

**Website**: http://ecogenomics.github.io/BamM/

**Short description**: Metagenomics-focused BAM file manipulation

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BamM-1.7.0.sif

**Note**: This is no longer actively maintained. CoverM is a direct replacement.

CoverM
~~~~~~

**Website**: https://github.com/wwood/CoverM

**Short description**: CoverM aims to be a configurable, easy to use and fast DNA read coverage and relative abundance
calculator focused on metagenomics applications. CoverM calculates coverage of genomes/MAGs (coverm genome) or
individual contigs (coverm contig). Calculating coverage by read mapping, its input can either be BAM files sorted by
reference, or raw reads and reference FASTA sequences.

**Singularity use**:

For a directory of genome bins (each fasta file is a bin, all files having the "fna" extension) and the original fastq
files used in the assembly...

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CoverM-0.2.0-alpha7.sif genome --genome-fasta-directory <path-to-bins> -x fna --coupled <reads1.fastq> <reads2.fastq> --output-format sparse --min-read-percent-identity .95 --min-read-aligned-percent .75 --min-covered-fraction .75 > coverage_table.csv

Alternatively, if you want to ...


SingleM
~~~~~~~

**Website**: https://github.com/wwood/singlem

**Short description**: SingleM is a tool to find the abundances of discrete operational taxonomic units (OTUs) directly
from shotgun metagenome data, without heavy reliance on reference sequence databases. It is able to differentiate
closely related species even if those species are from lineages new to science.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SingleM-0.8.1.img

    # Generate OTU table from RAW metagenomic data
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SingleM-0.8.1.img pipe --sequences my_sequences.fastq.gz --otu_table otu_table.csv --threads <threads>

    # Summarize OTU table in Krona plot
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SingleM-0.8.1.img summarise --input_otu_tables otu_table.csv --krona krona_plot.html

There are a lot more options are customization than is presented here. Check the documentation for more information.
Remember, anything after "singlem" in a command can be copy-and-pasted after the "SingleM.img" in the above examples.

The latest version is 0.13.0. This will be updated alongside GraftM.

GraftM
~~~~~~~

**Website**: https://github.com/geronimp/graftM

**Reference**: Boyd, J. A., Woodcroft, B. J., & Tyson, G. W. (2018). GraftM: a tool for scalable, phylogenetically
informed classification of genes within metagenomes. Nucleic Acids Research, 46(10), e59–e59.
https://doi.org/10.1093/nar/gky174

**Short description**: GraftM is a tool for finding genes of interest in metagenomes, metatranscriptomes, and whole
 genomes. Using modular gene packages, GraftM will search the provided sequences using hmmsearch (HMMER) and place the
 identified sequences into a pre-constructed phylogenetic tree. The provides fast, phylogenetically informed community
 profiles and genome annotations.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/GraftM-0.10.1.img

The latest version is 0.13.1. This will be updated.

Read2RefMapper
^^^^^^^^^^^^^^

**Website**: https://bitbucket.org/bolduc/docker-read2refmapper

**Protocols.io**: `Read2Ref on CyVerse <https://dx.doi.org/10.17504/protocols.io.gv2bw8e>`_

**CyVerse App**: https://de.cyverse.org/de/?type=apps&app-id=Read2RefMapper-1.1.0u3&system-id=agave

**Short description**: Read2RefMapper is a python-wrapper for a number of scripts and tools that allow for filtering
coverage of BAM files against a reference dataset. It filters reads matching reference sequences for those references
that are not covered over a specified threshold length, as well as alignment identity and alignment coverage. It is
designed to be used in conjunction with Docker-BatchBowtie.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Read2RefMapper-1.1.1.simg --dir ${readsDir} --metagenome-sizes reads2refmapper_mysample.csv --num-threads 40 --coverages coverage_table.csv --cov_filter 70 --percent-id 0.95 --percent-aln 0.75 --coverage-mode tpmean --output-fmt png --dpi 300 --log read2refmapper.log

ClusterGenomes
~~~~~~~~~~~~~~

**Website**: https://bitbucket.org/MAVERICLab/stampede-clustergenomes/

**Short description**: ClusterGenomes is a nucmer-based tool designed to cluster viral genomes. It can handle circular
and short sequences with high accuracy.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # Dereplicate
    singularity run /users/PAS1117/osu9664/eMicro-Apps/ClusterGenomes-1.1.3.img -f <input-viral-genomes.fasta> -c <coverage> -i <identity> -o <output-directory>

Note: Both coverage and identity are 0 - 100, *not* 0.0 - 1.0.

dRep
^^^^

**Website**: https://github.com/MrOlm/drep

**Website**: https://drep.readthedocs.io/en/master/

**Short description**: dRep is a python program for rapidly comparing large numbers of genomes. dRep can also
"de-replicate" a genome set by identifying groups of highly similar genomes and choosing the best representative genome
for each genome set.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/dRep.sif

    # You can test the installation
    singularity run /users/PAS1117/osu9664/eMicro-Apps/dRep.sif bonus testDir --check_dependencies

    # More rigorously check
    git clone https://github.com/MrOlm/drep.git
    cd drep/tests
    singularity run /users/PAS1117/osu9664/eMicro-Apps/dRep.sif dereplicate output_dir -g genomes/*

    # For genome de-replication
    dRep.sif dereplicate outout_directory -g path/to/genomes/*.fasta

    # To compare genomes
    dRep.sif compare output_directory -g path/to/genomes/*.fasta


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load dRep/2.4.2


DRAM
^^^^

**Website**: https://github.com/shafferm/DRAM

**Short description**: DRAM (Distilled and Refined Annotation of MAGs [Metagenome Assembled Genomes]) is a tool for
annotating metagenomic assembled genomes and VIRSorter identified viral contigs. DRAM annotates MAGs and viral contigs
using KEGG (if provided by the user), UniRef90, [PFAM (https://pfam.xfam.org/), dbCAN, RefSeq viral, VOGDB and the
MEROPS peptidase database as well as custom user databases. DRAM is ran in two stages. Additionally viral contigs are
further analyzed to identify potential AMGs. This is done via assigning an auxilary score and flags representing the
likelihood that a gene is metabolic and viral. The auxiliary score represents the confidence that a gene is viral in
origin based on surrounding genes.

**PAS1573 use**: (This is now an out-of-date version but these commands will still work!)

.. code-block:: bash

    export PATH=/fs/project/PAS1573/week10_pathways/DRAM/bin/:$PATH
    DRAM.py annotate -i '<path-to-bins>/*.fasta' -o dram_annotations
    DRAM.py summarize_genomes -i dram_annotations/annotations.tsv -o dram_results --rrna_path dram_annotations/rrnas.tsv

You'll notice that the command to run the tool is different, this is because of the challenge in using Singularity to
encapsulate the package + databases.

**Module use**: (This is always the most up-to-date version, barring the Wrighton lab's constant updates!)

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load DRAM

    DRAM.py annotate -i '<path-to-bins>/*.fa' -o annotation
    DRAM.py distill -i annotation/annotations.tsv -o distill --trna_path annotation/trnas.tsv --rrna_path annotation/rrnas.tsv


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/VirSorter-1.0.5.img

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/vConTACT2-0.9.9.sif

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/IVA-1.0.9.sif

    # You can test the installation
    singularity run /users/PAS1117/osu9664/eMicro-Apps/IVA-1.0.9.sif --test outdir

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/PhageTerm-1.0.12.sif
    # OR
    singularity run /users/PAS1117/osu9664/eMicro-Apps/PhageTerm-3.1.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PhageTerm/1.0.11
    # OR
    module load PhageTerm/3.1.0

MetaPhinder
~~~~~~~~~~~

**Website**: https://github.com/vanessajurtz/MetaPhinder

**Reference**: Jurtz, V. I., Villarroel, J., Lund, O., Voldby Larsen, M., & Nielsen, M. (2016). MetaPhinder—Identifying
Bacteriophage Sequences in Metagenomic Data Sets. PLOS ONE, 11(9), e0163111. https://doi.org/10.1371/journal.pone.0163111

**Short description**: Here we present MetaPhinder, a method to identify assembled genomic fragments (i.e.contigs) of
phage origin in metagenomic data sets. The method is based on a comparison to a database of whole genome bacteriophage
sequences, integrating hits to multiple genomes to accomodate for the mosaic genome structure of many bacteriophages.
The method is demonstrated to out-perform both BLAST methods based on single hits and methods based on k-mer comparisons.


**Singularity use**:

coming soon...

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MetaPhinder

    MetaPhinder.py -i <input-file> -o <directory> -d $BLAST_DB/ALL_140821_hr -b /fs/project/PAS1117/modules/MetaPhinder/bin/

Note: MetaPhinder's help states that -o is a FILE, but specifying anything other than a directory (to be created)
generates one of several errors (one is often: "Command line argument error"). Specifying a non-existent directory is
the only way to avoid errors.

PHANOTATE
~~~~~~~~~

**Website**: https://github.com/deprekate/PHANOTATE

**Reference**:

**Short description**: PHANOTATE is a tool to annotate phage genomes. It uses the assumption that non-coding bases in
a phage genome is disadvantageous, and then populates a weighted graph to find the optimal path through the six frames
of the DNA where open reading frames are beneficial paths, while gaps and overlaps are penalized paths.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PHANOTATE/1.4.0

    phanotate.py --help

VIBRANT
~~~~~~~

**Website**: https://github.com/AnantharamanLab/VIBRANT

**Reference**: Kieft, K., Zhou, Z., and Anantharaman, K. (2019). VIBRANT: Automated recovery, annotation and curation
of microbial viruses, and evaluation of virome function from genomic sequences. BioRxiv 855387.

**Short description**: VIBRANT is a tool for automated recovery and annotation of bacterial and archaeal viruses,
determination of genome completeness, and characterization of virome function from metagenomic assemblies. VIBRANT uses
neural networks of protein annotation signatures and genomic features to maximize identification of highly diverse
partial or complete viral genomes as well as excise integrated proviruses.

**Singularity use**:

coming soon...

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load VIBRANT/1.1.0
    # OR
    module load VIBRANT/1.2.1

DRAM-v
~~~~~~

**Website**: https://github.com/shafferm/DRAM

**Short description**: DRAM (Distilled and Refined Annotation of MAGs [Metagenome Assembled Genomes]) is a tool for
annotating metagenomic assembled genomes and VIRSorter identified viral contigs. DRAM annotates MAGs and viral contigs
using KEGG (if provided by the user), UniRef90, [PFAM (https://pfam.xfam.org/), dbCAN, RefSeq viral, VOGDB and the
MEROPS peptidase database as well as custom user databases. DRAM is ran in two stages. Additionally viral contigs are
further analyzed to identify potential AMGs. This is done via assigning an auxilary score and flags representing the
likelihood that a gene is metabolic and viral. The auxiliary score represents the confidence that a gene is viral in
origin based on surrounding genes.

**PAS1573 use**: (This version is now out-of-date but these commands will still work)

.. code-block:: bash

    export PATH=/fs/project/PAS1573/week10_pathways/DRAM/bin/:$PATH
    # --skip_uniref if want faster, although, less sensitive results
    DRAM-v.py annotate -i <path-to-VIRSorter_cat_contigs.fasta> --virsorter_affi_contigs <path-to-VIRSorter-VIRSorter_affi-contigs.tab> --output_dir DRAMv_annotate --threads 40
    # optionally, --rrna_path dram_annotations/rrnas.tsv
    DRAM-v.py distill -i DRAMv_annotate/annotations.tsv -o DRAMv_summarize

You'll notice that the command to run the tool is different, this is because of the challenge in using Singularity to
encapsulate the package + databases.

**Module use**: (This is always the most up-to-date version, barring the Wrighton lab's constant updates!)

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load DRAM

    DRAM-v.py annotate -i VIRSorter_cat1245.fasta -v VIRSorter_affi-contigs.tab -o viral_annotation
    DRAM-v.py distill -i viral_annotation/annotations.tsv -o viral_annotation/distilled

ViralRecall
~~~~~~~~~~~

**Website**: https://github.com/faylward/viralrecall

**Reference**: Aylward, F. O. & Moniruzzaman, M. ViralRecall-A Flexible Command-Line Tool for the Detection of Giant
Virus Signatures in ’Omic Data. Viruses 13, 15–17 (2021).

**Short description**: ViralRecall is a flexible command-line tool for detecting signatures of giant viruses (NCLDV)
in genomic data. Version 2 has been updated to focus more on NCLDV compared to version 1, but the original options are still available.


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Treemmer/Treemmer

    python viralrecall.py -i examples/arm29B.fna -p test_outdir -t 2 -f


PropagAtE
~~~~~~~~~

**Website**: https://github.com/AnantharamanLab/PropagAtE

**Reference**: Kieft, K. & Anantharaman, K. Deciphering active prophages from metagenomes. bioRxiv 2021.01.29.428894
(2021). doi:10.1101/2021.01.29.428894

**Short description**: PropagAtE (Prophage Activity Estimator) uses genomic coordinates of integrated prophage sequences
 and short sequencing reads to estimate if a given prophage was in the lysogenic (dormant) or lytic (active) stage of
 infection. Prophages are designated according to a genomic/scaffold coordinate file, either manually generated by the
 user or taken directly from a VIBRANT (at least v1.2.1) output. The prophage:host read coverage ratio and corresponding
 effect size are used to estimate if the prophage was actively replicating its genome (significantly more prophage
 genome copies than host copies). PropagAtE is customizable to take in complete genomes or metagenomic scaffolds along
 with raw Illumina (short) reads, or instead take pre-aligned data files (sam or bam format). Threshold values are
 customizable but PropagAtE outputs clear “active” versus “dormant” estimations of given prophages with associated statistics.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PropagAtE/1.0.0

    PropagAtE_run.py --help


VPF-Tools
~~~~~~~~~

**Website**: https://github.com/biocom-uib/vpf-tools

**Reference**: Pons, J. C. et al. VPF-Class: taxonomic assignment and host prediction of uncultivated viruses based on
viral protein families. Bioinformatics 1–9 (2021). doi:10.1093/bioinformatics/btab026

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles


CheckV
~~~~~~

**Website**: https://bitbucket.org/berkeleylab/checkv

**Reference**: Nayfach, S. et al. CheckV assesses the quality and completeness of metagenome-assembled viral genomes.
Nat. Biotechnol. (2020). doi:10.1038/s41587-020-00774-7

**Short description**: CheckV is a fully automated command-line pipeline for assessing the quality of single-contig
viral genomes, including identification of host contamination for integrated proviruses, estimating completeness for
genome fragments, and identification of closed genomes.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    CheckV-2020.04.27.sif --help

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CheckV-2020.04.27.sif

Phigaro
~~~~~~~

**Website**: https://github.com/bobeobibo/phigaro

**Reference**: Starikova, E. V. et al. Phigaro: high-throughput prophage sequence annotation. Bioinformatics 36,
3882–3884 (2020).

**Short description**: Phigaro is a standalone command-line application that is able to detect prophage regions
taking raw genome and metagenome assemblies as an input. It also produces dynamic annotated “prophage genome maps” and
marks possible transposon insertion spots inside prophages. It is applicable for mining prophage regions from large
metagenomic datasets.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load phigaro/2.2.3

    phigaro -f <fasta-input> -o <output-file> -p --not-open -c $config

Note: $config is an environmental variable set to a specific file which information about the database locations

GRAViTy
~~~~~~~

**Website**: https://github.com/PAiewsakun/GRAViTy

**Reference**: Aiewsakun, P. & Simmonds, P. The genomic underpinnings of eukaryotic virus taxonomy: Creating a
sequence-based framework for family-level virus classification. Microbiome 6, 1–24 (2018).

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load GRAViTy


Phylogenetics
-------------

Treemmer
~~~~~~~~

**Website**: https://github.com/fmenardo/Treemmer

**Reference**: Menardo, F. et al. Treemmer: a tool to reduce large phylogenetic datasets with minimal loss of
diversity. BMC Bioinformatics 19, 164 (2018).

**Short description**: Treemmer, a simple tool to evaluate the redundancy of phylogenetic trees and reduce their
complexity by eliminating leaves that contribute the least to the tree diversity.


**Singularity use**:

coming soon...

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Treemmer/Treemmer

    Treemmer_v0.3.py --help


BALi-Phy
~~~~~~~~

**Website**: http://www.bali-phy.org/

**Reference**: 1. Redelings, B. D. Bali-Phy version 3: Model-based co-estimation of alignment and phylogeny.
Bioinformatics 2–4 (2021). doi:10.1093/bioinformatics/btab129

**Short description**: BAli-Phy is software by Ben Redelings that estimates multiple sequence alignments and
evolutionary trees from DNA, amino acid, or codon sequences. It uses likelihood-based evolutionary models of
substitutions and insertions and deletions to place gaps. It has been used in published analyses on data sets up
to 117 taxa.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run BALi-Phy-3.6.0.sif

TIM
~~~

**Website**: https://github.com/RomainBlancMathieu/TIM

**Reference**:

**Short description**: TIM detects and maps interactions between organisms onto a phylogenetic tree of a target group
of organisms. Interactions are predicted from a species co-occurence-based network (such as one generated by FlashWeave).

TIM assumes that evolutionarily related organisms (refer to as query) interact with evolutionary related organisms
(subject) (The reciprocal is not true).

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load TIM/TIM
    cp -r /fs/project/PAS1117/modules/TIM/TIM . && cd TIM
    main.py Picornavirales.nwk connections.txt POS
    downstream.py

Phylorank
~~~~~~~~~

**Website**: https://github.com/dparks1134/PhyloRank

**Reference**: https://github.com/dparks1134/PhyloRank (cite the github page)

**Short description**: PhyloRank provides functionality for calculating the relative evolutionary divergence (RED) of
taxa in a tree and for finding the best placement of taxonomic labels in a tree.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Phylorank


GTDB-Tk
~~~~~~~

**Website**: https://github.com/Ecogenomics/GtdbTk

**Reference**: Chaumeil, P.-A., Mussig, A. J., Hugenholtz, P. & Parks, D. H. GTDB-Tk: a toolkit to classify genomes
with the Genome Taxonomy Database. Bioinformatics 36, 1925–1927 (2019).

**Short description**: GTDB-Tk is a software toolkit for assigning objective taxonomic classifications to bacterial and
archaeal genomes based on the Genome Database Taxonomy GTDB. It is designed to work with recent advances that allow
hundreds or thousands of metagenome-assembled genomes (MAGs) to be obtained directly from environmental samples. It
can also be applied to isolate and single-cell genomes.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load GTDB-Tk

IQ-Tree
~~~~~~~~~

**Website**: https://github.com/Cibiv/IQ-TREE

**Reference**: Nguyen, L.-T., Schmidt, H. A., von Haeseler, A. & Minh, B. Q. IQ-TREE: A Fast and Effective Stochastic
Algorithm for Estimating Maximum-Likelihood Phylogenies. Mol. Biol. Evol. 32, 268–274 (2015).

**Short description**: The IQ-TREE software was created as the successor of IQPNNI and TREE-PUZZLE (thus the name
IQ-TREE). IQ-TREE was motivated by the rapid accumulation of phylogenomic data, leading to a need for efficient
phylogenomic software that can handle a large amount of data and provide more complex models of sequence evolution.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load IQ-TREE/2.0-rc1


Rascal
~~~~~~

**Website**: ftp://ftp-igbmc.u-strasbg.fr/pub/RASCAL (no longer available?)

**Reference**: Thompson, J. D., Thierry, J. C. & Poch, O. RASCAL: Rapid scanning and correction of multiple sequence
alignments. Bioinformatics 19, 1155–1161 (2003).

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load IQ-TREE/2.0-rc1

PhyML
~~~~~

**Website**: http://www.atgc-montpellier.fr/phyml/, https://github.com/stephaneguindon/phyml

**Reference**: Guindon, S. et al. New Algorithms and Methods to Estimate Maximum-Likelihood Phylogenies: Assessing the
Performance of PhyML 3.0. Syst. Biol. 59, 307–321 (2010).

**Short description**: PhyML is a software package that uses modern statistical approaches to analyse alignments of
nucleotide or amino acid sequences in a phylogenetic framework. The main tool in this package builds phylogenies
under the maximum likelihood criterion. It implements a large number of substitution models coupled to efficient
options to search the space of phylogenetic tree topologies. PhyTime is another tool in the PhyML package that
focuses on divergence date estimation in a Bayesian setting. The main strengths of PhyTime lies in its ability to
accommodate for uncertrainty in the placement of fossil calibration and the use of realistic models of rate variation
along the tree. Finally, PhyREX fits the spatial-Lambda-Fleming-Viot model to geo-referenced genetic data. This model
is similar to the structured coalescent but assumes that individuals are distributed along a spatial continuum rather
than discrete demes. PhyREX can be used to estimate population densities and rates of dispersal. Its output can be
processed by treeannotator (from the BEAST package) as well as SPREAD.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PhyML/3.1

MAFFT
~~~~~

**Website**: https://github.com/GSLBiotech/mafft

**Reference**: Katoh, K. & Standley, D. M. MAFFT Multiple Sequence Alignment Software Version 7: Improvements in
Performance and Usability. Mol. Biol. Evol. 30, 772–780 (2013).

**Reference** (original): Katoh, K. MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier
transform. Nucleic Acids Res. 30, 3059–3066 (2002).

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load mafft/7.429

Miscellaneous
-------------

SRA Toolkit
~~~~~~~~~~~

**Website**: https://www.ncbi.nlm.nih.gov/sra/docs/toolkitsoft/

**Website 2**: https://github.com/ncbi/sra-tools/wiki

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SRA_Toolkit.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load sratoolkit/2.10.7


Entrez Direct
~~~~~~~~~~~~~~

**Website**: https://www.ncbi.nlm.nih.gov/books/NBK179288/

**Short Description**: Entrez Direct (EDirect) provides access to the NCBI's suite of interconnected databases
(publication, sequence, structure, gene, variation, expression, etc.) from a Unix terminal window. Search terms
are entered as command-line arguments. Individual operations are connected with Unix pipes to allow construction of
multi-step queries. Selected records can then be retrieved in a variety of formats.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Entrez-Direct


ViennaRNA
~~~~~~~~~

**Website**: https://www.tbi.univie.ac.at/RNA/index.html

**Reference**: Lorenz, R. et al. ViennaRNA Package 2.0. Algorithms Mol. Biol. 6, 26 (2011).

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load ViennaRNA/2.4.14








ViPTreeGen
~~~~~~~~~~

**Website**: https://github.com/yosuken/ViPTreeGen

**Reference**: Nishimura, Y. et al. ViPTree: the viral proteomic tree server. Bioinformatics 1–2 (2017).
doi:10.1093/bioinformatics/btx157

**Short description**: ViPTreeGen is a tool for automated generation of viral "proteomic tree" by computing genome-wide
sequence similarities based on tBLASTx results. The original proteomic tree (i.e., "the Phage Proteomic Tree”) was
developed by Rohwer and Edwards, 2002. A proteomic tree is a dendrogram that reveals global genomic similarity
relationships between tens, hundreds, or thousands of viruses. It has been shown that viral groups identified in a
proteomic tree well correspond to established viral taxonomies. The proteomic tree approach is effective to investigate
genomes of newly sequenced viruses as well as those identified in metagenomes.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles

    ViPTreeGen --help




VIRIDIC
~~~~~~~

**Website**: https://github.com/yosuken/ViPTreeGen

**Reference**:  Moraru, C., Varsani, A. & Kropinski, A. M. VIRIDIC — A Novel Tool to Calculate the Intergenomic
Similarities of Viruses 12, 1268 (2020).

**Short description**:

**Module use**:

.. code-block:: bash

    cp /fs/project/PAS1117/modules/viridic_v1.0_r3.6/* <current-directory>
    ./viridic.bash projdir=<output-dir> in=<fasta-file>


Clinker
~~~~~~~

**Website**: https://github.com/gamcil/clinker

**Reference**: Gilchrist, C. L. M. & Chooi, Y.-H. clinker &amp; clustermap.js: automatic generation of gene cluster
comparison figures. Bioinformatics (2021). doi:10.1093/bioinformatics/btab007

**Short description**: Gene cluster comparison figure generator - clinker is a pipeline for easily generating
publication-quality gene cluster comparison figures.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Clinker/Clinker
    clinker --help


SortMeRNA
~~~~~~~~~

**Website**: https://github.com/biocore/sortmerna

**Reference**: Kopylova, E., Noé, L. & Touzet, H. SortMeRNA: fast and accurate filtering of ribosomal RNAs in
metatranscriptomic data. Bioinformatics 28, 3211–3217 (2012).

**Short description**: SortMeRNA is a local sequence alignment tool for filtering, mapping and clustering.

The core algorithm is based on approximate seeds and allows for sensitive analysis of NGS reads. The main application
of SortMeRNA is filtering rRNA from metatranscriptomic data. SortMeRNA takes as input files of reads (fasta, fastq,
fasta.gz, fastq.gz) and one or multiple rRNA database file(s), and sorts apart aligned and rejected reads into two
files. Additional applications include clustering and taxonomy assignation available through QIIME v1.9.1. SortMeRNA
works with Illumina, Ion Torrent and PacBio data, and can produce SAM and BLAST-like alignments.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load SortMeRNA/4.2.0

    sortmerna -h

SAMBAMBA
~~~~~~~~

**Website**: https://github.com/lomereiter/sambamba

**Reference**:

**Short description**: Sambamba is a high performance highly parallel robust and fast tool (and library), written in
the D programming language, for working with SAM and BAM files. Because of its efficiency Sambamba is an important
work horse running in many sequencing centres around the world today.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load SAMBAMBA/0.7.1


SpClust
~~~~~~~

**Website**: https://github.com/johnymatar/SpCLUST

**Reference**:

**Short description**: SpCLUST is a package for divergent nucleotide sequences clustering. Contrarely to traditional
clustering methods that focuses on the speed of clustering highly similar sequences, SpCLUST uses a Machine Learning
Gaussian Mixture Model and targets the clustering accuracy of divergent sequences with the best possible speed. The
current version of SpCLUST uses Edgar, R.C.'s MUSCLE module (www.drive5.com) for sequences alignment.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    singularity run SpCLUST.sif mpispclust -in test.fasta -out mpispclust_results.txt -alignMode fast -mdist BLOSUM62 -seqtype Amino
    # OR
    mpiexec -n 4 SpCLUST.sif spclust -in test.fasta -out spclust_results.txt -alignMode fast -mdist BLOSUM62 -seqtype Amino


PROSITE
~~~~~~~

**Website**:

**Reference**:

**Short description**:

**Singularity use**:

.. code-block:: bash

    module load PROSITE/1.86
    ps_scan.pl <rest-of-command>


HH-Suite
~~~~~~~~

**Website**: https://github.com/soedinglab/hh-suite

**Reference**: Steinegger, M. et al. HH-suite3 for fast remote homology detection and deep protein annotation.
BMC Bioinformatics 20, 473 (2019).

**Short description**: The HH-suite is an open-source software package for sensitive protein sequence searching based
on the pairwise alignment of hidden Markov models (HMMs).

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load hhsuite/3.2.0


MetaCHIP
~~~~~~~~

**Website**: https://github.com/songweizhi/MetaCHIP

**Reference**: Song, W., Wemheuer, B., Zhang, S., Steensen, K. & Thomas, T. MetaCHIP: community-level horizontal gene
transfer identification through the combination of best-match and phylogenetic approaches. Microbiome 7, 36 (2019).

**Short description**: MetaCHIP is a pipeline for reference-independent HGT identification at the community level.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MetaCHIP


SuperCRUNCH
~~~~~~~~~~~

**Website**: https://github.com/dportik/SuperCRUNCH

**Reference**: Portik, D. M. & Wiens, J. J. SuperCRUNCH: A bioinformatics toolkit for creating and manipulating
supermatrices and other large phylogenetic datasets. Methods Ecol. Evol. 11, 763–772 (2020).

**Short description**: SuperCRUNCH is a python toolkit for creating and working with phylogenetic datasets.
SuperCRUNCH can be run using any set of sequence data, as long as sequences are in fasta format with standard naming
conventions

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load SuperCRUNCH



Nonpareil
~~~~~~~~~

**Website**: http://enve-omics.ce.gatech.edu/nonpareil/, https://github.com/lmrodriguezr/nonpareil

**Reference**: Rodriguez-R, L. M., Gunturu, S., Tiedje, J. M., Cole, J. R. & Konstantinidis, K. T. Nonpareil 3:
Fast Estimation of Metagenomic Coverage and Sequence Diversity. mSystems 3, 1–9 (2018).

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Nonpareil


VG-Flow
~~~~~~~

**Website**: https://bitbucket.org/jbaaijens/vg-flow

**Reference**:

**Short description**: VG-Flow uses a de novo approach that enables full-length haplotype reconstruction from
pre-assembled contigs of complex mixed samples.

**Importance notice**: This requires a FREE Gurobi academic license: https://user.gurobi.com/download/licenses/free-academic

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages

    # If you haven't YET installed a license key
    vg-flow.sif grbgetkey <long-license-key-that-was-generated-at-sign-up>

    # Create the variation graph
    vg-flow.sif build_graph_msga.py -f example/forward.fastq -r example/reverse.fastq -c example/input.fasta -vg vg -t 4

    # Build the haplotypes
    vg-flow.sif vg-flow.py -m 10 -c 20 node_abundance.txt contig_graph.final.gfa

**Note**: This was installed prior to tool updates


PEAR
~~~~~

**Website**: https://cme.h-its.org/exelixis/web/software/pear/

**Reference**:

**Short description**: PEAR is an ultrafast, memory-efficient and highly accurate pair-end read merger. It is fully
parallelized and can run with as low as just a few kilobytes of memory.

PEAR evaluates all possible paired-end read overlaps and without requiring the target fragment size as input.
In addition, it implements a statistical test for minimizing false-positive results. Together with a highly optimized
implementation, it can merge millions of paired end reads within a couple of minutes on a standard desktop computer.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PEAR/0.9.11


SAVAGE
~~~~~~

**Website**: https://bitbucket.org/jbaaijens/savage

**Reference**: Baaijens, J. A., El Aabidine, A. Z., Rivals, E. & Schönhuth, A. De novo assembly of viral quasispecies
using overlap graphs. Genome Res. 27, 835–848 (2017).

**Short description**: SAVAGE is a computational tool for reconstructing individual haplotypes of intra-host virus
strains (a viral quasispecies) without the need for a high quality reference genome. SAVAGE makes use of either
FM-index based data structures or ad-hoc consensus reference sequence for constructing overlap graphs from patient
sample data. In this overlap graph, nodes represent reads and/or contigs, while edges reflect that two reads/contigs,
based on sound statistical considerations, represent identical haplotypic sequence. Following an iterative scheme, a
new overlap assembly algorithm that is based on the enumeration of statistically well-calibrated groups of
reads/contigs then efficiently reconstructs the individual haplotypes from this overlap graph.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load SAVAGE








Bioscripts-2.7 and Bioscripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Website**: https://github.com/christophertbrown/bioscripts27, https://github.com/christophertbrown/bioscripts

**Reference**:

**Short description**: Useful scripts for working with genomics and sequencing data

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load bioscripts/bioscripts27
    # OR
    module load bioscripts/bioscripts3


InterProScan
~~~~~~~~~~~~

**Website**: https://github.com/ebi-pf-team/interproscan

**Reference**: Quevillon, E. et al. InterProScan: protein domains identifier. Nucleic Acids Res. 33, W116–W120 (2005).

**Short description**: InterPro is a database which integrates together predictive information about proteins’
function from a number of partner resources, giving an overview of the families that a protein belongs to and the
domains and sites it contains.

Users who have novel nucleotide or protein sequences that they wish to functionally characterise can use the software
package InterProScan to run the scanning algorithms from the InterPro database in an integrated way. Sequences are
submitted in FASTA format. Matches are then calculated against all of the required member database’s signatures and
the results are then output in a variety of formats.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load InterProScan/5.36-75.0

    interproscan.sh <rest-of-command>





IVA
~~~

**Website**: https://sanger-pathogens.github.io/iva/

**Reference**: 1. Hunt, M. et al. IVA: Accurate de novo assembly of RNA virus genomes. Bioinformatics 31, 2374–2376
(2015).

**Short description**: IVA is a de novo assembler designed to assemble virus genomes that have no repeat sequences,
using Illumina read pairs sequenced from mixed populations at extremely high and variable depth.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load IVA

    iva -f <forward-reads.fastq> -r <reverse-reads.fastq> <output-dir>


ExaBayes
~~~~~~~~

**Website**: https://sanger-pathogens.github.io/iva/

**Reference**: Aberer, A. J., Kobert, K. & Stamatakis, A. Exabayes: Massively parallel bayesian tree inference for the
whole-genome era. Mol. Biol. Evol. 31, 2553–2556 (2014).

**Short description**: ExaBayes is a software package for Bayesian phylogenetic tree inference. It is particularly
suitable for large-scale analyses on computer clusters.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load exa-bayes/1.4.1


PAML
~~~~

**Website**: http://abacus.gene.ucl.ac.uk/software/paml.html

**Reference**: Yang, Z. PAML 4: Phylogenetic Analysis by Maximum Likelihood. Mol. Biol. Evol. 24, 1586–1591 (2007).

**Short description**: PAMLis a package of programs for phylogenetic analyses of DNA and protein sequences using
maximum likelihood (ML). The programs may be used to compare and test phylogenetic trees, but their main strengths
lie in the rich repertoire of evolutionary models implemented, which can be used to estimate parameters in models of
sequence evolution and to test interesting biological hypotheses. Uses of the programs include estimation of synonymous
and nonsynonymous rates (dN and dS) between two protein-coding DNA sequences, inference of positive Darwinian
selection through phylogenetic comparison of protein-coding genes, reconstruction of ancestral genes and proteins for
molecular restoration studies of extinct life forms, combined analysis of heterogeneous data sets from multiple gene
loci, and estimation of species divergence times incorporating uncertainties in fossil calibrations

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PAML


BEAST2
~~~~~~

**Website**: https://github.com/CompEvol/beast2, http://www.beast2.org/

**Reference**: Bouckaert, R. et al. BEAST 2.5: An advanced software platform for Bayesian evolutionary analysis.
PLOS Comput. Biol. 15, e1006650 (2019).

**Short description**: BEAST is a cross-platform program for Bayesian inference using MCMC of molecular sequences. It
is entirely orientated towards rooted, time-measured phylogenies inferred using strict or relaxed molecular clock
models. It can be used as a method of reconstructing phylogenies but is also a framework for testing evolutionary
hypotheses without conditioning on a single tree topology. BEAST uses MCMC to average over tree space, so that each
tree is weighted proportional to its posterior probability. We include a simple to use user-interface program for
setting up standard analyses and a suit of programs for analysing the results.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load BEAST2


RevBayes
~~~~~~~~

**Website**: https://revbayes.github.io/

**Reference**: Höhna, S. et al. RevBayes: Bayesian Phylogenetic Inference Using Graphical Models and an Interactive
Model-Specification Language. Syst. Biol. 65, 726–736 (2016).

**Short description**: RevBayes provides an interactive environment for statistical computation in phylogenetics. It
is primarily intended for modeling, simulation, and Bayesian inference in evolutionary biology, particularly
phylogenetics. However, the environment is quite general and can be useful for many complex modeling tasks.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load RevBayes


MARVEL
~~~~~~

**Website**: https://github.com/LaboratorioBioinformatica/MARVEL

**Reference**: Amgarten, D., Braga, L. P. P., da Silva, A. M. & Setubal, J. C. MARVEL, a Tool for Prediction of
Bacteriophage Sequences in Metagenomic Bins. Front. Genet. 9, 1–8 (2018).

**Short description**: MARVEL is a tool for recovery of draft phage genomes from whole community shotgun metagenomic
sequencing data.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MARVEL/0.2


MMSeqs2
~~~~~~~

**Website**: https://github.com/soedinglab/MMseqs2

**Reference**: Steinegger, M. & Söding, J. MMseqs2 enables sensitive protein sequence searching for the analysis of
massive data sets. Nat. Biotechnol. 35, 2–4 (2017).

**Short description**: MMseqs2 (Many-against-Many sequence searching) is a software suite to search and cluster huge
protein and nucleotide sequence sets. MMseqs2 is open source GPL-licensed software implemented in C++ for Linux,
MacOS, and (as beta version, via cygwin) Windows. The software is designed to run on multiple cores and servers and
exhibits very good scalability. MMseqs2 can run 10000 times faster than BLAST. At 100 times its speed it achieves
almost the same sensitivity. It can perform profile searches with the same sensitivity as PSI-BLAST at over 400 times
its speed.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MMseqs2


DeepVirFinder
~~~~~~~~~~~~~

**Website**: https://github.com/jessieren/DeepVirFinder

**Reference**: Ren, J. et al. Identifying viruses from metagenomic data by deep learning. (2018).

**Short description**: DeepVirFinder predicts viral sequences using deep learning method. The method has good
prediction accuracy for short viral sequences, so it can be used to predict sequences from the metagenomic data.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load DeepVirFinder


CD-HIT
~~~~~~

**Website**: https://github.com/weizhongli/cdhit, http://cd-hit.org

**Reference**: Fu, L., Niu, B., Zhu, Z., Wu, S. & Li, W. CD-HIT: accelerated for clustering the next-generation
sequencing data. Bioinformatics 28, 3150–3152 (2012).

**Short description**: CD-HIT is a very widely used program for clustering and comparing protein or nucleotide sequences

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load cdhit/4.6.1




BLAST+
~~~~~~

**Website**:

**Reference**:

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load blast/2.8.1+



Clust
~~~~~~

**Website**: https://github.com/BaselAbujamous/clust

**Reference**: Abu-Jamous, B. & Kelly, S. Clust: automatic extraction of optimal co-expressed gene clusters from gene
expression data. Genome Biol. 19, 172 (2018).

**Short description**: Optimised consensus clustering of one or more heterogeneous datasets.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load clust/1.8.9

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    clust-1.8.9.img --help



ViromeScan
~~~~~~~~~~

**Website**: http://sourceforge.net/projects/viromescan/

**Reference**: Rampelli, S. et al. ViromeScan: a new tool for metagenomic viral community profiling. BMC Genomics 17,
165 (2016).

**Short description**: Tool for metagenomic viral community profiling

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load viromescan
    module load bowtie2/2.3.4.1
    module load blast/2.4.0+

    viromescan


Bowtie2
~~~~~~~

**Website**: http://bowtie-bio.sourceforge.net/bowtie2/index.shtml

**Reference**: Langmead, B. & Salzberg, S. L. Fast gapped-read alignment with Bowtie 2. Nat. Methods 9, 357–9 (2012).

**Short description**: Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long
reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and
particularly good at aligning to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM
Index to keep its memory footprint small: for the human genome, its memory footprint is typically around 3.2 GB.
Bowtie 2 supports gapped, local, and paired-end alignment modes.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load bowtie2/2.4.1

Note: We have A LOT of bowtie2 versions, be aware that they may be updated more frequently than this site!


Jellyfish
~~~~~~~~~

**Website**: http://www.genome.umd.edu/jellyfish.html

**Reference**: Marcais, G. & Kingsford, C. A fast, lock-free approach for efficient parallel counting of occurrences
of k-mers. Bioinformatics 27, 764–770 (2011).

**Short description**: Jellyfish is a tool for fast, memory-efficient counting of k-mers in DNA. A k-mer is a
substring of length k, and counting the occurrences of all such substrings is a central step in many analyses of
DNA sequence. JELLYFISH can count k-mers quickly by using an efficient encoding of a hash table and by exploiting
the "compare-and-swap" CPU instruction to increase parallelism.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load jellyfish/2.2.10


WIsH
~~~~

**Website**: https://github.com/soedinglab/WIsH

**Reference**: Galiez, C., Siebert, M., Enault, F., Vincent, J. & Söding, J. WIsH: Who is the host? Predicting
prokaryotic hosts from metagenomic phage contigs. Bioinformatics 1–2 (2017). doi:10.1093/bioinformatics/btx383

**Short description**: WIsH can identify bacterial hosts from metagenomic data, keeping good accuracy even on smaller
contigs.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load WiSH

    # Taken from the website
    WIsH -c build -g prokaryoteGenomesDir -m modelDir
    WIsH -c predict -g phageContigsDir -m modelDir -r outputResultDir -b 1



PICRUSt
~~~~~~~

**Website**: https://github.com/picrust/picrust, http://picrust.github.io/picrust/index.html

**Reference**: Langille, M. G. I. et al. Predictive functional profiling of microbial communities using 16S
rRNA marker gene sequences. Nat. Biotechnol. 31, 814–821 (2013).

**Short description**: PICRUSt (pronounced “pie crust”) is a bioinformatics software package designed to predict metagenome functional content from marker gene (e.g., 16S rRNA) surveys and full genomes.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load PICRUSt/1.1.3



RDP Classifier
~~~~~~~~~~~~~~

**Website**: https://github.com/rdpstaff/classifier, https://rdp.cme.msu.edu/classifier/classifier.jsp

**Reference**: Wang, Q., Garrity, G. M., Tiedje, J. M. & Cole, J. R. Naïve Bayesian Classifier for Rapid Assignment of
rRNA Sequences into the New Bacterial Taxonomy. Appl. Environ. Microbiol. 73, 5261–5267 (2007).

**Short description**: The RDP Classifier is a naive Bayesian classifier which was developed to provide rapid taxonomic
placement based on rRNA sequence data. The RDP Classifier can rapidly and accurately classify bacterial and archaeal
16s rRNA sequences, and Fungal LSU sequences. It provides taxonomic assignments from domain to genus, with confidence
estimates for each assignment. The RDP Classifier likely can be adapted to additional phylogenetically coherent
bacterial taxonomies.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load rdp_classifier/2.3


ProtTest
~~~~~~~~

**Website**: https://github.com/ddarriba/prottest3

**Reference**: Darriba, D., Taboada, G. L., Doallo, R. & Posada, D. ProtTest 3: fast selection of best-fit models of
protein evolution. Bioinformatics 27, 1164–1165 (2011).

**Short description**: ProtTest is a bioinformatic tool for the selection of best-fit models of aminoacid replacement
for the data at hand. ProtTest makes this selection by finding the model in the candidate list with the smallest
Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC) score or Decision Theory Criterion (DT).
At the same time, ProtTest obtains model-averaged estimates of different parameters (including a model-averaged
phylogenetic tree) and calculates their importance(Posada and Buckley 2004). ProtTest differs from its nucleotide
analog jModeltest (Posada 2008) in that it does not include likelihood ratio tests, as not all models included in
ProtTest are nested.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load prottest/3.4.2


MINCED
~~~~~~

**Website**: https://github.com/ctSkennerton/minced

**Reference**: 1. Bland, C. et al. CRISPR Recognition Tool (CRT): a tool for automatic detection of clustered
regularly interspaced palindromic repeats. BMC Bioinformatics 8, 209 (2007).

**Short description**: MinCED is a program to find Clustered Regularly Interspaced Short Palindromic Repeats (CRISPRs)
in full genomes or environmental datasets such as assembled contigs from metagenomes. Iff you want to identify CRISPRs
in raw short read data, in the size range of 100-200bp try using Crass (https://github.com/ctskennerton/Crass) MinCED
runs from the command-line and was derived from CRT (http://www.room220.com/crt/)

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load minced/1.0.0

MASH
~~~~

**Website**: https://github.com/marbl/Mash

**Reference**: Ondov, B. D. et al. Mash: fast genome and metagenome distance estimation using MinHash. Genome
Biol. 17, 132 (2016).

**Short description**: Fast genome and metagenome distance estimation using MinHash

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MASH/1.1.1


MUMmer
~~~~~~

**Website**: http://mummer.sourceforge.net/

**Reference**: Kurtz, S. et al. Versatile and open software for comparing large genomes. Genome Biol. 5, 12 (2004).

**Short description**: MUMmer is a system for rapidly aligning entire genomes, whether in complete or draft form. For
example, MUMmer 3.0 can find all 20-basepair or longer exact matches between a pair of 5-megabase genomes in 13.7
seconds, using 78 MB of memory, on a 2.4 GHz Linux desktop computer. MUMmer can also align incomplete genomes; it can
easily handle the 100s or 1000s of contigs from a shotgun sequencing project, and will align them to another set of
contigs or a genome using the NUCmer program included with the system. If the species are too divergent for a DNA
sequence alignment to detect similarity, then the PROmer program can generate alignments based upon the six-frame
translations of both input sequences

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MUMmer/3.23


HMMER3
~~~~~~

**Website**: http://hmmer.org/

**Reference**: Eddy, S. R. Accelerated Profile HMM Searches. PLoS Comput. Biol. 7, e1002195 (2011).

**Short description**: HMMER is used for searching sequence databases for sequence homologs, and for making sequence
alignments. It implements methods using probabilistic models called profile hidden Markov models (profile HMMs).

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load hmmer3/3.1b2


MUSCLE
~~~~~~

**Website**: http://www.drive5.com/muscle/

**Reference**: Edgar, R. C. MUSCLE: multiple sequence alignment with high accuracy and high throughput. Nucleic Acid Res. 32, 1792–1797 (2004).

**Short description**: MUSCLE is one of the best-performing multiple alignment programs according to published
benchmark tests, with accuracy and speed that are consistently better than CLUSTALW. MUSCLE can align hundreds of
sequences in seconds.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load muscle/3.8.31


tRNA-Scan SE
~~~~~~~~~~~~

**Website**: https://github.com/UCSC-LoweLab/tRNAscan-SE

**Reference**: Lowe, T. M. & Eddy, S. R. tRNAscan-SE: A Program for Improved Detection of Transfer RNA Genes in
Genomic Sequence. Nucleic Acids Res. 25, 0955–0964 (1997).

**Short description**: We describe a program, tRNAscan-SE, which identifies 99–100% of transfer RNA genes in DNA
sequence while giving less than one false positive per 15 gigabases.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load tRNAscan-SE/1.23


Samtools
~~~~~~~~

**Website**: http://www.htslib.org/

**Reference**: Danecek, P. et al. Twelve years of SAMtools and BCFtools. Gigascience 10, 1–4 (2021).

**Short description**: Samtools is a suite of programs for interacting with high-throughput sequencing data

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load samtools/1.10


BWA
~~~

**Website**: https://github.com/lh3/bwa

**Reference**: Li, H. & Durbin, R. Fast and accurate short read alignment with Burrows-Wheeler transform.
Bioinformatics 25, 1754–60 (2009).

**Short description**: BWA is a software package for mapping DNA sequences against a large reference genome, such as
the human genome. It consists of three algorithms: BWA-backtrack, BWA-SW and BWA-MEM. The first algorithm is designed
for Illumina sequence reads up to 100bp, while the rest two for longer sequences ranged from 70bp to a few megabases.
BWA-MEM and BWA-SW share similar features such as the support of long reads and chimeric alignment, but BWA-MEM,
which is the latest, is generally recommended as it is faster and more accurate. BWA-MEM also has better performance
than BWA-backtrack for 70-100bp Illumina reads.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load bwa/0.7.17-r1198


MCL
~~~

**Website**: https://micans.org/mcl/

**Reference**: Enright, a J., Van Dongen, S. & Ouzounis, C. a. An efficient algorithm for large-scale detection of
protein families. Nucleic Acids Res. 30, 1575–84 (2002).

**Short description**: The MCL algorithm is short for the Markov Cluster Algorithm, a fast and scalable unsupervised
cluster algorithm for graphs (also known as networks) based on simulation of (stochastic) flow in graphs.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load mcl/14.137




# ClustalOmega/1.2.4/ module
# EMBOSS
# mason
$ RASCAL module
# Crux-Toolkit
# MrBayes
# PriceTI
# igraph
# spades-cleaner
# MIDAS module
# Salmon, dependency? of Trinity

# Velvet

# JAGS... hmmm
# PlasFlow... hmmm

# ANIcalculator

# PfamScan