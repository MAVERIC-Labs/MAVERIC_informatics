.. _eMicroApps:

Available Environmental Microbiology ("eMicro") Apps and Tools
==============================================================

Below is a list and description of the apps available to anyone on OSC. Please keep in mind that this list is not 100%
comprehensive and *does not* detail the methods underlying the tool. Where possible, citations have been included so users
can read the original source's documentation and theory.

**Always check for the latest versions of Singularity containers and modules!**

Some of this documentation is lifted from the `iVirus project <https://ivirus.readthedocs.io/en/latest/>`_ to avoid
reinventing the wheel. Every effort is being made to ensure that **both** locations are up-to-date with the latest tools
and literature.

**All of the eMicro singularity images are located at:**
/users/PAS1117/osu9664/eMicro-Apps/

**Additionally, Microbial Informatics students can also find additional images at:**
/fs/project/PAS1573/sif/

**Members of the Sullivan Lab can find apptainer containers at:**
/fs/ess/PAS1117/modules/singularity/

You must provide full paths to each image/container, or link them  (see :ref:`UNIX_LINUX`).

**Example**:

.. code-block:: bash

    $ module load singularity/current
    $ singularity run /users/PAS1117/osu9664/eMicro-Apps/Prokka-1.12.0.img -h
    # Alternatively
    $ singularity run /fs/project/PAS1573/sif/fastqc_0.11.9--hdfd78af_1.sif

Alternatively, if you do not want to type out the full paths each time you run the container, you'll want to add the
 container location to your PATH.

.. code-block:: bash

    $ export PATH=/users/PAS1117/osu9664/eMicro-Apps/:$PATH
    $ Prokka-1.12.0.img -h
    # OR, alternatively
    $ export PATH=/fs/project/PAS1573/sif/:$PATH
    $ fastqc_0.11.9--hdfd78af_1.sif

**Keep in mind that NONE of these apps/tools should be run on the login nodes. Please create a job script and submit it
or incur OSC's wrath!**

Also to note: There are several cases where these tools have been used in the `CyVerse cyberinfrastructure <https://www.cyverse.org/>`_.
For these, there is a `protocols.io <https://www.protocols.io/>`_ link. We're continually developing these protocols and
trying to keep them up to date (though if it's not broke and a current version, it'll likely not be updated), so always
make sure it's the latest version.

**For Sullivan lab members, also included are OSC module system, to use:**

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles  # Load Sullivan lab's modules
    module load Prokka/1.13
    # OR
    module load Prokka/1.14.6
    prokka -h


Quality Control [of Reads] and Read Mapping
--------------------------------------------

Generally speaking, quality control (QC) is a technique applied to to [most commonly] raw read data. This ensures that
the data going into the assembly (common next step) is of high quality. Poor read quality can result in mis- or
incorrectly assembled sequences. Most frequently, read data QC involves trimming reads according to their quality
scores. Although some assemblers do not require QC’d reads, we highly recommend it!

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

**Apptainer use**:

.. code-block:: bash

    module load apptainer/current
    apptainer run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.97.sif

    # For PAS1117
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    BBTools-38.97.sif


BBDuk (in the BBTools package)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Website**: https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/

**Short description**: “Duk” stands for Decontamination Using Kmers. BBDuk was developed to combine most common
data-quality-related trimming, filtering, and masking operations into a single high-performance tool. It is capable of
quality-trimming and filtering, adapter-trimming, contaminant-filtering via kmer matching, sequence masking,
GC-filtering, length filtering, entropy-filtering, format conversion, histogram generation, subsampling, quality-score
recalibration, kmer cardinality estimation, and various other operations in a single pass.

**Apptainer use**:

.. code-block:: bash

    module load apptainer/current
    # Just adapter trimming
    apptainer run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif bbduk.sh in1=<input-pair1> in2=<input-pair2> out1=<trimmed-pair1> out2=<trimmed-pair2> ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    # Just quality filtering
    apptainer run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif bbduk.sh in1=<trimmed-pair1> in2=<trimmed-pair2> qtrim=rl trimq=10 out1=<trimmed-and-quality-pair1> out2=<trimmed-and-quality-pair2>

Alternatively, run them both at the same time!

.. code-block:: bash

    # Adapter and quality filtering *at the same time*
    apptainer run /users/PAS1117/osu9664/eMicro-Apps/BBTools-38.69.sif bbduk.sh in1=<input-pair1> in2=<input-pair2> out1=<qc-trimmed-pair1> out2=<qc-trimmed-pair2> ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo trimq=10 qtrim=rl minlength=35


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


bcftools
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


Cramino
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


Dorado
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


GOTTCHA2
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


Guppy
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


Kraken2
~~~~~~~

**Website**: https://github.com/DerrickWood/kraken2

**Website**: https://ccb.jhu.edu/software/kraken2/

**Manual**: https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown

**Reference**: Wood, D. E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. Genome Biol. 20, 257
(2019). https://doi.org/10.1186/s13059-019-1891-0

**Short description**: Kraken 2 is the newest version of Kraken, a taxonomic classification system using exact
k-mer matches to achieve high accuracy and fast classification speeds. This classifier matches each k-mer within a
query sequence to the lowest common ancestor (LCA) of all genomes containing the given k-mer. The k-mer assignments
inform the classification algorithm

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Kraken-2.1.2.sif

    # To run against the standard database  # For PAS1573
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Kraken-2.1.2.sif --db /fs/project/PAS1573/modules/sequence_dbs/kraken2_dbs/standard --gzip-compressed --paired --classified-out Reads_R#.fastq.gz Reads_1.fastq.gz Reads_2.fastq.gz > kraken2_results

    # To run against the standard database  # For PAS1117
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Kraken-2.1.2.sif --db /fs/project/PAS1117/modules/sequence_dbs/kraken2_dbs/standard --gzip-compressed --paired --classified-out Reads_R#.fastq.gz Reads_1.fastq.gz Reads_2.fastq.gz > kraken2_results

Note: Please check the kraken2_dbs folder for additional databases!


MetaPhlAn
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


NanoFilt
~~~~~~~~

**Website**: https://github.com/wdecoster/nanofilt

**Short Description**: Filtering and trimming of long read sequencing data.

**Reference**: De Coster, W., D’Hert, S., Schultz, D. T., Cruts, M. & Van Broeckhoven, C. NanoPack: visualizing and
processing long-read sequencing data. Bioinformatics 34, 2666–2669 (2018). https://doi.org/10.1093/bioinformatics/bty149

**Singularity Use**:

Forthcoming...

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Nanofilt/2.8.0


NanoStat
~~~~~~~~

**Website**: https://github.com/wdecoster/nanostat

**Short Description**: Calculate various statistics from a long read sequencing dataset in fastq, bam or albacore sequencing summary format.

**Reference**: De Coster, W., D’Hert, S., Schultz, D. T., Cruts, M. & Van Broeckhoven, C. NanoPack: visualizing and
processing long-read sequencing data. Bioinformatics 34, 2666–2669 (2018). https://doi.org/10.1093/bioinformatics/bty149

**Singularity Use**:

Forthcoming...

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load Nanostat/1.6.0
    

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


Pydamage
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


Read2RefMapper
~~~~~~~~~~~~~~

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


QUAST/MetaQUAST
~~~~~~~~~~~~~~~

**Website**: http://quast.sourceforge.net/

**Manual**: http://cab.cc.spbu.ru/quast/manual.html

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

.. code-block:: bash

    export SIF=/fs/project/PAS1573/sif

    # QUAST
    $SIF/quast.py contigs_1.fasta contigs_2.fasta --threads 48

    # MetaQUAST
    $SIF/metaquast.py contigs_1.fasta contigs_2.fasta ... --threads 48

    # MetaQUAST can optionally be run with a list of reference genomes
    $SIF/metaquast.py contigs_1.fasta contigs_2.fasta ... -r reference_1,reference_2,reference_3,... --threads 48

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load quast/4.5


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


Samtools
~~~~~~~~

**Website**: http://www.htslib.org/

**Reference**: Danecek, P. et al. Twelve years of SAMtools and BCFtools. Gigascience 10, 1–4 (2021).

**Short description**: Samtools is a suite of programs for interacting with high-throughput sequencing data

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load samtools/1.10


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


Salmon
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MEGAHIT-1.2.8.sif --k-list 21,41,61,81,99 -t <threads> -m 0.9 -1 <for-reads> -2 <rev-reads> -o <output-dir> --presets meta-sensitive (or meta-large for complex metagenomes like soils or oceans)


MeGAMerge
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


MetaQUAST
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


MIRA
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


PriceTI
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SPAdes-3.15.5.sif

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load spades/3.15.2


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Trinity-2.9.0.sif


Velvet
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


Binning
-------

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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DAS_Tool-1.1.1.sif

    # You can test the installation (if you've git cloned the repository!)
    git clone https://github.com/cmks/DAS_Tool.git
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DAS_Tool-1.1.1.sif -i DAS_Tool/sample_data/sample.human.gut_concoct_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_maxbin2_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_metabat_scaffolds2bin.tsv,DAS_Tool/sample_data/sample.human.gut_tetraESOM_scaffolds2bin.tsv -l concoct,maxbin,metabat,tetraESOM -c DAS_Tool/sample_data/sample.human.gut_contigs.fa --search_engine diamond -o DASToolTestRun --write_bins


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load DAS_Tool


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
    singularity run MaxBin2-2.2.6.sif

    # Download test data
    wget -O 20x.scaffold https://downloads.jbei.org/data/microbial_communities/MaxBin/getfile.php?20x.scaffold
    wget -O 20x.abund https://downloads.jbei.org/data/microbial_communities/MaxBin/getfile.php?20x.abund

    # Run MaxBin2
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MaxBin2-2.2.6.sif -contig 20x.scaffold -abund 20x.abund -out 20x.out -thread 4

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MaxBin/2.2.6


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


MetaCC
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


metaTOR
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


VAMB
~~~~

**Website**: https://github.com/RasmussenLab/vamb

**Reference**: Nissen, J. N. et al. Improved metagenome binning and assembly using deep variational autoencoders. Nat. Biotechnol. 39, 555–560 (2021).

**Short description**: Vamb is a metagenomic binner which feeds sequence composition information from a contig catalogue and
co-abundance information from BAM files into a variational autoencoder and clusters the latent representation.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    VAMB-3.0.2.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/VAMB-3.0.2.sif


Gene Callers
------------

CRT
~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


FragGeneScan
~~~~~~~~~~~~

**Reference**: Mina Rho, Haixu Tang, and Yuzhen Ye. FragGeneScan: Predicting Genes in Short and Error-prone Reads. Nucl. Acids Res., 2010 doi: 10.1093/nar/gkq747

**Short description**: FragGeneScan is an application for finding (fragmented) genes in short reads

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/FragGeneScan-1.30.0.img

GeneMarkS
~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


MetaGeneMark2
~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


RNAmmer
~~~~~~~

**Website**: https://services.healthtech.dtu.dk/service.php?RNAmmer-1.2

**Reference**: Lagesen, K. et al. RNAmmer: consistent and rapid annotation of ribosomal RNA genes. Nucleic Acids Res. 35, 3100–3108 (2007).

**Short description**: The RNAmmer 1.2 server predicts 5s/8s, 16s/18s, and 23s/28s ribosomal RNA in full genome sequences.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    RNAmmer-1.2.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/RNAmmer-1.2.sif


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


Annotation and Analyses
-----------------------

This is a catch-all category that doesn't fit with the other sections.


Bakta
~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


BamM
~~~~

**Website**: http://ecogenomics.github.io/BamM/

**Short description**: Metagenomics-focused BAM file manipulation

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BamM-1.7.0.sif

**Note**: This is no longer actively maintained. CoverM is a direct replacement.


BLAST+
~~~~~~

**Website**:

**Reference**:

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load blast/2.8.1+


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


CheckM2
~~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CoverM-0.6.1.sif genome --genome-fasta-directory <path-to-bins> -x fna --coupled <reads1.fastq> <reads2.fastq> --output-format sparse --min-read-percent-identity .95 --min-read-aligned-percent .75 --min-covered-fraction .75 > coverage_table.csv


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


DRAM
~~~~

**Website**: https://github.com/shafferm/DRAM

**Short description**: DRAM (Distilled and Refined Annotation of MAGs [Metagenome Assembled Genomes]) is a tool for
annotating metagenomic assembled genomes and VIRSorter identified viral contigs. DRAM annotates MAGs and viral contigs
using KEGG (if provided by the user), UniRef90, [PFAM (https://pfam.xfam.org/), dbCAN, RefSeq viral, VOGDB and the
MEROPS peptidase database as well as custom user databases. DRAM is ran in two stages. Additionally viral contigs are
further analyzed to identify potential AMGs. This is done via assigning an auxilary score and flags representing the
likelihood that a gene is metabolic and viral. The auxiliary score represents the confidence that a gene is viral in
origin based on surrounding genes.

**Module use**: (This is always the most up-to-date version, barring the Wrighton lab's constant updates!)

.. code-block:: bash

    # For PAS1117
    module use /fs/project/PAS1117/modulefiles
    module load DRAM

    DRAM.py annotate -i '<path-to-bins>/*.fa' -o annotation
    DRAM.py distill -i annotation/annotations.tsv -o distill --trna_path annotation/trnas.tsv --rrna_path annotation/rrnas.tsv

    # For PAS1573
    export PATH=/fs/ess/PAS1573/modules/DRAM-1.4.0/bin:$PATH
    DRAM.py annotate -i '<path-to-bins>/*.fa' -o annotation
    DRAM.py distill -i annotation/annotations.tsv -o distill --trna_path annotation/trnas.tsv --rrna_path annotation/rrnas.tsv

**Singularity use**

Unfortunately, due to the size of the database, this is not currently possible. While we work on a solution, please use
the module version!


dRep
~~~~

**Website**: https://github.com/MrOlm/drep

**Website**: https://drep.readthedocs.io/en/master/

**Short description**: dRep is a python program for rapidly comparing large numbers of genomes. dRep can also
"de-replicate" a genome set by identifying groups of highly similar genomes and choosing the best representative genome
for each genome set.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/dRep-2.3.2.sif

    # You can test the installation
    singularity run /users/PAS1117/osu9664/eMicro-Apps/dRep-2.3.2.sif bonus testDir --check_dependencies

    # More rigorously check
    git clone https://github.com/MrOlm/drep.git
    cd drep/tests
    singularity run /users/PAS1117/osu9664/eMicro-Apps/dRep-2.3.2.sif dereplicate output_dir -g genomes/*

    # For genome de-replication
    dRep.sif dereplicate outout_directory -g path/to/genomes/*.fasta

    # To compare genomes
    dRep.sif compare output_directory -g path/to/genomes/*.fasta


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load dRep/2.4.2


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


HMMsearch
~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


KEGGcharter
~~~~~~

**Website**: Coming soon!

**Reference**: Coming soon!

**Short description**: Coming soon!

**Singularity use**:

.. code-block:: bash
    
    Coming soon!


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


PROSITE
~~~~~~~

**Website**:

**Reference**:

**Short description**:

**Singularity use**:

.. code-block:: bash

    module load PROSITE/1.86
    ps_scan.pl <rest-of-command>


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


ViennaRNA
~~~~~~~~~

**Website**: https://www.tbi.univie.ac.at/RNA/index.html

**Reference**: Lorenz, R. et al. ViennaRNA Package 2.0. Algorithms Mol. Biol. 6, 26 (2011).

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load ViennaRNA/2.4.14


MetaPop
~~~~~~~

**Website**: https://github.com/metaGmetapop/metapop/

**Reference**: Coming soon!

**Short description**: MetaPop is a pipeline designed to facilitate the processing of sets of short read data mapped
to reference genomes with the twin aims of calculating sample-level diversity metrics such as abundance, population
diversity, and similarity across multiple samples, and assessing within-species diversity through the assessment of
nucleotide polymorphisms and amino acid substitutions. To further facilitate understanding, the pipeline also produces
graphical summaries of its results.

**Singularity use**:

.. code-block:: bash

    # Load singularity
    module load singularity

    # Set variables
    threads=40

    # Inputs
    input_contigs=data_dir/individual_fasta_dir/
    input_coverage=data_dir/counts.txt
    bam_dir=data_dir/BAMs

    singularity run /users/PAS1117/osu9664/eMicro-Apps/MetaPop-0.35.sif -i $bam_dir -r $input_contigs --threads $threads -o $out_dir -n $input_coverage

MetaPop requires:

 * input_contigs: a directory of fasta files representing the contigs/genomes - EACH genome must be its own FASTA file
 * bam_dir: a directory containing BAM alignment files of reads against the contigs/genomes
 * input_coverage: a tab-delimited file with the BAM filename (*without* the .bam extension) and the bp of that dataset
 * out_dir: where to place the output files

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load MetaPop/latest

    python $(which metapop_main.py) -i $bam_dir -r $input_contigs --threads $threads -o $out_dir -n $input_coverage


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


SingleM
~~~~~~~

**Website**: https://github.com/wwood/singlem

**Short description**: SingleM is a tool to find the abundances of discrete operational taxonomic units (OTUs) directly
from shotgun metagenome data, without heavy reliance on reference sequence databases. It is able to differentiate
closely related species even if those species are from lineages new to science.

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SingleM-0.13.2.sif

    # Generate OTU table from RAW metagenomic data
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SingleM-0.13.2.sif pipe --sequences my_sequences.fastq.gz --otu_table otu_table.csv --threads <threads>

    # Summarize OTU table in Krona plot
    singularity run /users/PAS1117/osu9664/eMicro-Apps/SingleM-0.13.2.sif summarise --input_otu_tables otu_table.csv --krona krona_plot.html

There are a lot more options are customization than is presented here. Check the documentation for more information.
Remember, anything after "singlem" in a command can be copy-and-pasted after the "SingleM-0.13.2.sif" in the above examples.


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


Virus Analyses
--------------

"Consider something viral in your research" - Forest Rohwer

Cenote-Taker2
~~~~~~~~~~~~~

**Website**: https://github.com/mtisza1/Cenote-Taker2

**Reference**: Tisza, M. J., Belford, A. K., Domínguez-Huerta, G., Bolduc, B. & Buck, C. B. Cenote-Taker 2 democratizes virus discovery and sequence annotation. Virus Evol. 7, 1–12 (2021). doi:10.1093/ve/veaa100

**Short description**: Cenote-Taker 2 is a dual function bioinformatics tool. On the one hand, Cenote-Taker 2
discovers/predicts virus sequences from any kind of genome or metagenomic assembly. Second, virus sequences/genomes
are annotated with a variety of sequences features, genes, and taxonomy. Either the discovery or the the annotation
module can be used independently.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    Cenote-Taker2-2.1.3_osc.sif --contigs <contigs> --run_title <run title> --template_file <template file>

**Notes**: There is an *extensive* list of parameters for Cenote-Taker2 and their values. Call them with "--help".

**Notes**: There is currently no eMicro equivalent, mainly due to the size of the required databases. We're working
to fix this issue.

For those who want to repeat the "defaults" of the CyVerse app:

.. code-block:: bash

    module load singularity/current
    singularity run /fs/project/PAS1117/modules/singularity/Cenote-Taker2-2.1.3_osc.sif --contigs testcontigs_DNA_ct2.fasta --run_title run_title --template_file 010226_6435_template.sbt --prune_prophage True --cpu 68 --mem 92 -am False --minimum_length_circular 1000 --minimum_length_linear 1000 --virus_domain_db standard --lin_minimum_hallmark_genes 1 --circ_minimum_hallmark_genes 1 --enforce_start_codon False --hhsuite_tool hhblits --isolation_source unknown --Environmental_sample False --molecule_type DNA --data_source original --filter_out_plasmids False --orf-within-orf False


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
    CheckV-0.8.1.sif --help

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CheckV-0.8.1.sif


CheckV Clustering
~~~~~~~~~~~~~~~~~~

This uses two scripts *already available* in CheckV to deduplicate/dereplicate sequence data.

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
    CheckV-0.8.1-ClusterONLY.sif -i <input-fasta> -t <threads> -o <output-dir> --min-ani <min_ani> --min-qcov <min_query_coverage> --min-tcov <min_target_coverage>

    # For eMicro and PAS1573
    singularity run CheckV-0.8.1-ClusterONLY.sif -i <input-fasta> -t <threads> -o <output-dir>

    # For additional help
    CheckV-0.8.1-ClusterONLY.sif --help


**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load blast/2.11.0+
    module load CheckV/2021.02.03
    module load python/biopython3

    CheckV-Deduplication.py -i <input-fasta> -t <threads> -o <output-dir> --min-ani <min_ani> --min-qcov <min_query_coverage> --min-tcov <min_target_coverage>


**Notes**: 206K viral contigs can be dereplicated to 52K in 1 hr 30 min


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

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    /users/PAS1117/osu9664/eMicro-Apps/DeepVirFinder.simg --help


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


IVA
~~~

**Website**: https://sanger-pathogens.github.io/iva/

**Reference**: Hunt, M., Gall, A., Ong, S. H., Brener, J., Ferns, B., Goulder, P., … Otto, T. D. (2015). IVA: Accurate
de novo assembly of RNA virus genomes. Bioinformatics, 31(14), 2374–2376. https://doi.org/10.1093/bioinformatics/btv120

**Short description**: IVA is a de novo assembler designed to assemble virus genomes that have no repeat sequences,
using Illumina read pairs sequenced from mixed populations at extremely high and variable depth.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load IVA

    iva -f <forward-reads.fastq> -r <reverse-reads.fastq> <output-dir>

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/IVA-1.0.9.sif

    # You can test the installation
    singularity run /users/PAS1117/osu9664/eMicro-Apps/IVA-1.0.9.sif --test outdir

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

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MARVEL-0.1.simg


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
    module load PhageTerm/4.0.0

Note: PhageTerm is installed under numerous versions. Ensure you're using the version you think you're using.


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
    singularity run /users/PAS1117/osu9664/eMicro-Apps/vConTACT2-0.11.1.sif

.. code-block:: bash

    # For PAS1117 users
    module load singularity/current
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    singularity run vConTACT2-0.11.1.sif

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

.. code-block:: bash

    module load singularity/current

    # For eMicro and PAS1573
    VIBRANT_DATA_PATH=/users/PAS1117/osu9664/eMicro-Apps/vibrant_dbs/20231102  # Optional
    singularity run /users/PAS1117/osu9664/eMicro-Apps/VIBRANT-1.2.1.sif -i <input-fasta> -folder <output-dir>

    # If VIBRANT_DATA_PATH is not specified, then you will need to specify -d /users/PAS1117/osu9664/eMicro-Apps/vibrant_dbs/20231102

    # For PAS1117
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    VIBRANT-1.2.1.sif -i <input-fasta> -i <input-fasta> -folder <output-dir>


Note: There may be numerous DeprecationWarning. They can be safely ignored.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load VIBRANT/1.1.0
    # OR
    module load VIBRANT/1.2.1

ViralCC
~~~~~~~

**Website**: https://github.com/dyxstat/ViralCC.git

**Reference**: Du, Y., Fuhrman, J. A. & Sun, F. ViralCC retrieves complete viral genomes and virus-host pairs from
metagenomic Hi-C data. Nat Commun 14, 502 (2023). https://doi.org/10.1038/s41467-023-35945-y

**Short description**: ViralCC is a new open-source metagenomic Hi-C-based binning pipeline to recover high-quality
viral genomes. ViralCC not only considers the Hi-C interaction graph, but also puts forward a novel host proximity
graph of viral contigs as a complementary source of information to the remarkably sparse Hi-C interaction map. The
two graphs are then integrated together, followed by the Leiden graph clustering using the integrative graph to
generate draft viral genomes.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load ViralCC/1.0.0
    ViralCC pipeline -v <virus-contigs-FASTA> <sorted-BAM> <virus-contigs-CSV> <output-directory>


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


VIRIDIC
~~~~~~~

**Website**: http://rhea.icbm.uni-oldenburg.de/VIRIDIC/

**Reference**:  Moraru, C., Varsani, A. & Kropinski, A. M. VIRIDIC — A Novel Tool to Calculate the Intergenomic
Similarities of Viruses 12, 1268 (2020).

**Short description**:

**Module use**:

.. code-block:: bash

    cp /fs/project/PAS1117/modules/viridic_v1.0_r3.6/* <current-directory>
    ./viridic.bash projdir=<output-dir> in=<fasta-file>


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


VPF-Tools
~~~~~~~~~

**Website**: https://github.com/biocom-uib/vpf-tools

**Reference**: Pons, J. C. et al. VPF-Class: taxonomic assignment and host prediction of uncultivated viruses based on
viral protein families. Bioinformatics 1–9 (2021). doi:10.1093/bioinformatics/btab026

**Short description**:

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles


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


Miscellaneous
-------------

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


KronaTools
~~~~~~~~~~~

**Website**: https://github.com/marbl/Krona/tree/master/KronaTools

**Manual**: https://github.com/marbl/Krona/wiki/KronaTools

**Reference**: Ondov BD, Bergman NH, and Phillippy AM. Interactive metagenomic visualization in a Web browser.
BMC Bioinformatics. 2011 Sep 30; 12(1):385.

**Short description**: Krona Tools is a set of scripts to create Krona charts from several Bioinformatics tools as
well as from text and XML files.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load KronaTools/2.8
    # There are a large number of kt* tools available, see the documentation for a full list
    ktImportTaxonomy --help


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

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For eMicro users
    singularity run /users/PAS1117/osu9664/eMicro-Apps/CD-HIT-4.8.1.sif

By default, the Singularity/Apptainer container uses the "cd-hit" program. If you want to use the other cd-hit tools,
use *exec*

.. code-block:: bash

    singularity exec /users/PAS1117/osu9664/eMicro-Apps/cd-hit
    singularity exec /users/PAS1117/osu9664/eMicro-Apps/cd-hit-2d
    singularity exec /users/PAS1117/osu9664/eMicro-Apps/cd-hit-est
    singularity exec /users/PAS1117/osu9664/eMicro-Apps/cd-hit-454
    singularity exec /users/PAS1117/osu9664/eMicro-Apps/cd-hit-dup
    ...


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

**Singularity use**:

.. code-block:: bash

    module load singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/WIsH-1.0.0.sif

iPHoP
~~~~~

**Website**: https://bitbucket.org/srouxjgi/iphop

**Reference**: Roux, S., Camargo, A.P., Coutinho, F.H., Dabdoub, S.M., Dutilh, B.E., Nayfach, S. and Tritt, A., 2023. iPHoP: An integrated machine learning framework to maximize host prediction for metagenome-derived viruses of archaea and bacteria. PLoS biology, 21(4), p.e3002083. https://doi.org/10.1371/journal.pbio.3002083.

**Short description**: iPHoP stands for **i**\ntegrated **P**\hage **H**o\st **P**\rediction. It is an automated
command-line pipeline for predicting host genus of novel bacteriophages and archaeoviruses based on their genome sequences.

**Module use**:

.. code-block:: bash

    module use /fs/project/PAS1117/modulefiles
    module load iPHoP/1.0.0

    # Taken from the website
    # Download test file
    wget https://bitbucket.org/srouxjgi/iphop/raw/7319bbb6d3c4a8dac5e4bd613847c40ad99e8a73/test/test_input_phages.fna

    # Run with TEST database
    iphop predict --fa_file test_input_phages.fna --db_dir $DB_TEST --out_dir iphop_test_results

    # Alternatively, run with FULL database
    iphop predict --fa_file test_input_phages.fna --db_dir $DB --out_dir iphop_test_results
    ### Welcome to iPHoP ###
    Looks like everything is now set up, we will first clean up the input file, and then we will start the host prediction steps themselves
    [1/1/Run] Running blastn against genomes...
    [1/3/Run] Get relevant blast matches...
    [2/1/Run] Running blastn against CRISPR...
    [2/2/Run] Get relevant crispr matches...
    [3/1/Run] Running WIsH...
    [3/2/Run] Get relevant WIsH hits...
    [4/1/Run] Running VHM s2 similarities...
    [4/2/Run] Get relevant VHM hits...
    [5/1/Run] Running PHP...
    [5/2/Run] Get relevant PHP hits...
    [6/1/Run] Running RaFAH...
    [6/2/Run] Get relevant RaFAH scores...
    [6.1/1/Run] Running Diamond comparison to RaFAH references...
    [5/2/Run] Get AAI distance to RaFAH refs...
    write
    [7] Aggregating all results and formatting for TensorFlow...

    ...
    ...
    ...

    [9/1.1] Preparing data for aggregated score ...
    [9/1.2] Run classifier for aggregated score ...
    [INFO kernel.cc:1153] Loading model from path
    [INFO decision_forest.cc:617] Model loaded with 500 root(s), 689556 node(s), and 30 input feature(s).
    [INFO abstract_model.cc:1063] Engine "RandomForestOptPred" built
    [INFO kernel.cc:1001] Use fast generic engine
    [9/2] Combining all results (Blast, CRISPR, iPHoP, and RaFAH) in a single file: iphop_test_results_2nd/Wdir/All_combined_scores.csv
    [10/1] Preparing the detailed output...
    [10/2] Preparing the iPHoP-only result file, linking viruses to individual genomes (iphop_test_results_2nd/Host_prediction_to_genome_m90.csv) ...
    [10/3] Preparing the combined iPHoP / RaFAH output summarized at the genus rank (iphop_test_results_2nd/Host_prediction_to_genus_m90.csv) ...

**Notes**: Both a $DB and $TB_TEST system variable exist, depending on if you're testing your dataset, or you wish to run
the full database.


**Singularity use**: (Experimental!)

.. code-block:: bash

    module use singularity/current
    singularity run /users/PAS1117/osu9664/eMicro-Apps/iPHoP-1.1.0.sif

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

BAMM
~~~~

**Website**: http://bamm-project.org/index.html

**Website**: https://github.com/macroevolution/bamm

**Reference**: Rabosky, D. L. Automatic Detection of Key Innovations, Rate Shifts, and Diversity-Dependence on
Phylogenetic Trees. PLoS One 9, e89543 (2014).

**Short description**: BAMM (Bayesian analysis of macroevolutionary mixtures) is a program for modeling complex dynamics of speciation, extinction, and trait evolution on phylogenetic trees. The program is oriented entirely towards detecting and quantifying heterogeneity in evolutionary rates.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    BAMM-2.5.0.sif --help

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BAMM-2.5.0.sif


Astral
~~~~~~

**Website**: https://github.com/smirarab/ASTRAL

**Reference**: Zhang, C., Rabiee, M., Sayyari, E. & Mirarab, S. ASTRAL-III: polynomial time species tree reconstruction
from partially resolved gene trees. BMC Bioinformatics 19, 153 (2018).

**Short description**: ASTRAL is a tool for estimating an unrooted species tree given a set of unrooted gene trees.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    Astral-5.7.8.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Astral-5.7.8.sif


Seq-Gen
~~~~~~~

**Website**: http://tree.bio.ed.ac.uk/software/seqgen/

**Website**: https://github.com/rambaut/Seq-Gen

**Reference**:

**Short description**: Seq-Gen is a program that will simulate the evolution of nucleotide or amino acid sequences along a phylogeny, using common models of the substitution process.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    Seq-Gen-1.3.4.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/Seq-Gen-1.3.4.sif


BioKIT
~~~~~~~

**Website**: https://github.com/JLSteenwyk/BioKIT

**Reference**: Steenwyk, J. L. et al. BioKIT: a versatile toolkit for processing and analyzing diverse types of
sequence data. Genetics iyac079 (2022) doi:10.1093/genetics/iyac079.

**Short description**: BioKIT is a UNIX shell toolkit for processing molecular sequence data.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    BioKIT-0.0.9.sif -h

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/BioKIT-0.0.9.sif -h


MIGRATE
~~~~~~~

**Website**:

**Reference**: Beerli, P., Ashki, H., Mashayekhi, S. & Palczewski, M. Population divergence time estimation using
individual lineage label switching. G3 Genes|Genomes|Genetics 12, (2022).

**Short description**: Migrate estimates effective population sizes,past migration rates between n population assuming
a migration matrix model with asymmetric migration rates and different subpopulation sizes, and population divergences or admixture. Migrate uses Bayesian inference to jointly estimate all parameters.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    MIGRATE-5.0.4.sif -help

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MIGRATE-5.0.4.sif -help

**Note**: Though built with threads, this is a non-MPI version.


DELINEATE
~~~~~~~~~

**Website**: https://github.com/jeetsukumaran/delineate

**Reference**: Sukumaran, J., Holder, M. T. & Knowles, L. L. Incorporating the speciation process into species
delimitation. PLOS Comput. Biol. 17, e1008924 (2021).

**Short description**: DELINEATE is an approach to species delimitation that incorporates an extended model of
speciation to discriminate between population isolation and speciation boundaries in genomic structure. Given a tree of
population lineages inferred under the classical "censored coalescent" (Rannala and Yang, 2003; Yang and Rannala 2010),
now more commonly known as the "multipecies coalescent" or MSC (Degnan and Rosenberg, 2009), this package will
calculate the probabilities of different organizations of the population lineages into species under the Protracted
Birth Death model of (Etienne et al, 2012)

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    DELINEATE-1.2.2.sif delineate-estimate --help

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DELINEATE-1.2.2.sif delineate-estimate --help

    # To run summarize
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DELINEATE-1.2.2.sif delineate-summarize --help

**Note**: To successfully run the singularity container, you must specify *delineate-estimate* or *delineate-summarize*


RANGER-DTL
~~~~~~~~~~

**Website**: https://compbio.engr.uconn.edu/software/RANGER-DTL/

**Reference**: Bansal, M. S., Kellis, M., Kordi, M. & Kundu, S. RANGER-DTL 2.0: rigorous reconstruction of gene-family
evolution by duplication, transfer and loss. Bioinformatics 34, 3214–3216 (2018).

**Short description**: RANGER-DTL 2.0 (short for Rapid ANalysis of Gene family Evolution using Reconciliation-DTL)
is a software package for inferring gene family evolution by speciation, gene duplication, horizontal gene transfer,
and gene loss. The software takes as input a gene tree (rooted or unrooted) and a rooted species tree and reconciles
the two by postulating speciation, duplication, transfer, and loss events.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    RANGER-DTL-2.0.sif <name-of-program>

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/RANGER-DTL-2.0.sif <name-of-program>

**Note**: RANGER-DTL consists of a suite of programs, such as OptRoot, Ranger-DTL, OptResolutions-DTL, and others. Please
check out the manual for additional information.


MAMMaL
~~~~~~

**Website**:

**Reference**:

**Short description**: (M)ultinomial (A)pproximate (M)ixture (Ma)ximum (L)ikelihood. The main program mammal takes as
input a number of classes, a sequence file and a tree and outputs estimated frequencies for classes using the methods
described in Susko, Lincker and Roger (2018).

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    MAMMaL-1.1.3.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/MAMMaL-1.1.3.sif

**Note**:


PAUP*
~~~~~~

**Website**: http://paup.phylosolutions.com/

**Reference**: Swofford, D. L. 2003. PAUP\*. Phylogenetic Analysis Using Parsimony (\*and Other Methods). Version 4. Sinauer Associates, Sunderland, Massachusetts.

**Short description**: Phylogenetic Analysis Using Parsimony \*and other methods

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    PAUP-4a168.sif --help

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/PAUP-4a168.sif --help


TICR
~~~~~~

**Website**: https://github.com/nstenz/TICR

**Reference**: Stenz, N. W. M., Larget, B., Baum, D. A. & Ané, C. Exploring Tree-Like and Non-Tree-Like Patterns
Using Genome Sequences: An Example Using the Inbreeding Plant Species Arabidopsis thaliana (L.) Heynh. Syst. Biol. 64, 809–823 (2015).

**Short description**: These scripts can be utilized to perform highly parallelized concordance analyses on any given
alignment, with a particular focus on very large datasets which may include dozens of taxa and may span entire
chromosomes or genomes.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    TICR.sif <name-of-program>

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/TICR.sif <name-of-program>

ExpressBetaDiversity
~~~~~~~~~~~~~~~~~~~~

**Website**: https://github.com/dparks1134/ExpressBetaDiversity

**Reference**: Parks, D. H. & Beiko, R. G. Measures of phylogenetic differentiation provide
robust and complementary insights into microbial communities. ISME J. 7, 173–183 (2013).

**Short description**: Open-source software implementing the phylogenetic β-diversity measures.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    EBD-1.0.10.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/EBD-1.0.10.sif

Note: Many users may find one of the EBD scripts useful: convertToEBD.py, which is used to convert from Unifrac/QIIME
file formats to an EBD format.

.. code-block:: bash

    module load singularity/current
    singularity exec /users/PAS1117/osu9664/eMicro-Apps/EBD-1.0.10.sif convertToEBD.py --help

DeePhage
~~~~~~~~

**Website**: https://github.com/shufangwu/DeePhage

**Reference**: Shufang Wu, Zhencheng Fang, Jie Tan, Mo Li, Congmin Xu, and Huaiqiu Zhu. DeePhage:
distinguish temperate phage-derived and virulent phage-derived sequence in metavirome data using deep learning.

**Short description**: DeePhage is designed to identify metavirome sequences as temperate
phage-derived and virulent phage-derived sequences. The program calculate a score reflecting the
likelihood of each input fragment as temperate phage-derived and virulent phage-derived sequences.

**Singularity use**:

.. code-block:: bash

    module load singularity/current

    # For PAS1117 users
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages
    DeePhage.sif

    # For eMicro
    singularity run /users/PAS1117/osu9664/eMicro-Apps/DeePhage.sif

    # To run with GPU enabled
    module load singularity
    module load cuda
    singularity run --nv /users/PAS1117/osu9664/eMicro-Apps/DeePhage.sif example.fna deephage_results.csv

For CUDA, ensure that you request a GPU-enabled node with "#SBATCH --gpus-per-node=1"
