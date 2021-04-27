.. _processing_viral:

End-to-End Processing of a Viral Metagenome
===========================================



For this dataset, we'll be **fully** processing `SRX4071230 <https://www.ncbi.nlm.nih.gov/sra/ERR594369>`_, a peat
metagenome with 14.1M reads. The SRA Run is ERR594369, which will be important when downloading the data from SRA.

This will include (nearly) all steps and *most* of the results returned from the command line. Clearly, some outputs
can't be nicely placed here, but are available (as links to files) or in the M8194 project directory.

Everything here uses Singularity. All of the singularity images are located at:

**/users/PAS1117/osu9664/eMicro-Apps/**

So you must prepend each \*.img, \*.simg or \*.sif Singularity container w/ this path OR link them (see :ref:`UNIX_LINUX`).

Downloading the data
--------------------

The first thing we need to do is grab the data from the SRA. You can do this a few ways, either through navigating the
NCBI+SRA websites, or directly using their SRA Toolkit.

.. code-block:: bash

    # Move to project directory
    $ cd /fs/project/PAS1573/week7_processing
    # Load modules necessary
    $ module load singularity
    $ singularity run SRA_Toolkit.sif fasterq-dump -e 4 -p --split-files ERR594369
    join   :|-------------------------------------------------- 100.00%
    concat :|-------------------------------------------------- 100.00%
    spots read      : 37,151,587
    reads read      : 74,303,174
    reads written   : 74,303,174

In the example above, we used *fasterq-dump*, which is designated to download two paired end read files in fastq format.
We also specified 4 threads (-e 4) so it would run a little faster. There should be *two* output files: ERR594369_1.fastq
and ERR594369_2.fastq. fasterq-dump won't compress the files for you, so you'll have to do this after the download completes.


Read Quality Control
--------------------

We will be using either `BBDuk <https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/>`_ or
`Trimmomatic <http://www.usadellab.org/cms/?page=trimmomatic>`_ to process our input reads. *You only need to select one*.
We'll be using both for examples, but typically stick with one and use it.

.. code-block:: bash

    $ singularity run Trimmomatic-0.36.0.img PE ERR594369_1.fastq ERR594369_2.fastq ERR594369_1_t_paired.fastq.gz ERR594369_1_t_unpaired.fastq.gz ERR594369_2_t_paired.fastq.gz ERR594369_2_t_unpaired.fastq.gz ILLUMINACLIP:/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10:2 LEADING:3 TRAILING:3 MINLEN:36
    TrimmomaticPE: Started with arguments:
     ERR594369_1.fastq ERR594369_2.fastq ERR594369_1_t_paired.fastq.gz ERR594369_1_t_unpaired.fastq.gz ERR594369_2_t_paired.fastq.gz ERR594369_2_t_unpaired.fastq.gz ILLUMINACLIP:/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10:2 LEADING:3 TRAILING:3 MINLEN:36
    Using PrefixPair: 'TACACTCTTTCCCTACACGACGCTCTTCCGATCT' and 'GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT'
    ILLUMINACLIP: Using 1 prefix pairs, 0 forward/reverse sequences, 0 forward only sequences, 0 reverse only sequences
    Quality encoding detected as phred33
    Input Read Pairs: 37151587 Both Surviving: 36444033 (98.10%) Forward Only Surviving: 632370 (1.70%) Reverse Only Surviving: 67275 (0.18%) Dropped: 7909 (0.02%)
    TrimmomaticPE: Completed successfully

For Trimmomatic, the defaults work pretty well. Note the location of the IlluminaClip - it's already "in" the Singularity
file. If you have your own custom primers/adapters, you'll need to add your sequences or create your own primer and adapter
file.

Next, BBDuk. BBDuk is usually done in 2-3 steps, with 1st being an adapter trimming step, and 2nd with the removal of
low quality sequences. You can do both steps in a single command, but doing so in two steps allows us to see what was
removed during each.

.. code-block:: bash

    $ BBTools-38.69.sif bbduk.sh in1=ERR594369_1.fastq.gz in2=ERR594369_2.fastq.gz out1=ERR594369_1_t.fastq.gz out2=ERR594369_2_t.fastq.gz ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    java -ea -Xmx50052m -Xms50052m -cp /bbmap/current/ jgi.BBDuk in1=ERR594369_1.fastq.gz in2=ERR594369_2.fastq.gz out1=ERR594369_1_t.fastq.gz out2=ERR594369_2_t.fastq.gz ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    Executing jgi.BBDuk [in1=ERR594369_1.fastq.gz, in2=ERR594369_2.fastq.gz, out1=ERR594369_1_t.fastq.gz, out2=ERR594369_2_t.fastq.gz, ref=/bbmap/resources/adapters.fa, ktrim=r, k=23, mink=11, hdist=1, tpe, tbo]
    Version 38.69

    maskMiddle was disabled because useShortKmers=true
    0.021 seconds.
    Initial:
    Memory: max=50733m, total=50733m, free=49894m, used=839m

    Added 217135 kmers; time: 	0.328 seconds.
    Memory: max=50733m, total=50733m, free=48774m, used=1959m

    Input is being processed as paired
    Started output streams:	0.094 seconds.
    Processing time:   		1157.764 seconds.

    Input:                  	74303174 reads 		7164049847 bases.
    KTrimmed:               	480321 reads (0.65%) 	11406582 bases (0.16%)
    Trimmed by overlap:     	262843 reads (0.35%) 	1383411 bases (0.02%)
    Total Removed:          	3298 reads (0.00%) 	12789993 bases (0.18%)
    Result:                 	74299876 reads (100.00%) 	7151259854 bases (99.82%)

    Time:                         	1158.188 seconds.
    Reads Processed:      74303k 	64.15k reads/sec
    Bases Processed:       7164m 	6.19m bases/sec

.. code-block:: bash

    $ BBTools-38.69.sif bbduk.sh in1=ERR594369_1_t.fastq.gz in2=ERR594369_2_t.fastq.gz qtrim=rl trimq=10 out1=ERR594369_1_t_qc.fastq.gz out2=ERR594369_2_t_qc.fastq.gz
    java -ea -Xmx50160m -Xms50160m -cp /bbmap/current/ jgi.BBDuk in1=ERR594369_1_t.fastq.gz in2=ERR594369_2_t.fastq.gz qtrim=rl trimq=10 out1=ERR594369_1_t_qc.fastq.gz out2=ERR594369_2_t_qc.fastq.gz
    Executing jgi.BBDuk [in1=ERR594369_1_t.fastq.gz, in2=ERR594369_2_t.fastq.gz, qtrim=rl, trimq=10, out1=ERR594369_1_t_qc.fastq.gz, out2=ERR594369_2_t_qc.fastq.gz]
    Version 38.69

    0.021 seconds.
    Initial:
    Memory: max=50843m, total=50843m, free=50001m, used=842m

    Input is being processed as paired
    Started output streams:	0.109 seconds.
    Processing time:   		346.964 seconds.

    Input:                  	74299876 reads 		7151259854 bases.
    QTrimmed:               	238190 reads (0.32%) 	2587818 bases (0.04%)
    Total Removed:          	3352 reads (0.00%) 	2587818 bases (0.04%)
    Result:                 	74296524 reads (100.00%) 	7148672036 bases (99.96%)

    Time:                         	347.075 seconds.
    Reads Processed:      74299k 	214.07k reads/sec
    Bases Processed:       7151m 	20.60m bases/sec

How does the quality check out?

Read Quality Control (Visualizing)
----------------------------------

Here, we've already loaded singularity (above) and moved to the project directory. In this example, I'm going to run
FastQC on all of the input files (2), the results from Trimmomatic (4) and the adapter trimmed (2) and quality filtered
(2) read *pairs* of BBDuk.

.. code-block:: bash

    $ FastQC-0.11.8.sif ERR594369_1_t_paired.fastq.gz ERR594369_1_t_unpaired.fastq.gz ERR594369_2_t_paired.fastq.gz ERR594369_2_t_unpaired.fastq.gz ERR594369_1_t.fastq ERR594369_2_t.fastq.gz ERR594369_1_t_qc.fastq.gz ERR594369_2_t_qc.fastq
    Started analysis of ERR594369_1_t_paired.fastq.gz
    Approx 5% complete for ERR594369_1_t_paired.fastq.gz
    Approx 10% complete for ERR594369_1_t_paired.fastq.gz
    Approx 15% complete for ERR594369_1_t_paired.fastq.gz
    Approx 20% complete for ERR594369_1_t_paired.fastq.gz
    Approx 25% complete for ERR594369_1_t_paired.fastq.gz
    Approx 30% complete for ERR594369_1_t_paired.fastq.gz
    Approx 35% complete for ERR594369_1_t_paired.fastq.gz
    Approx 40% complete for ERR594369_1_t_paired.fastq.gz
    Approx 45% complete for ERR594369_1_t_paired.fastq.gz
    Approx 50% complete for ERR594369_1_t_paired.fastq.gz
    Approx 55% complete for ERR594369_1_t_paired.fastq.gz
    Approx 60% complete for ERR594369_1_t_paired.fastq.gz
    Approx 65% complete for ERR594369_1_t_paired.fastq.gz
    Approx 70% complete for ERR594369_1_t_paired.fastq.gz
    Approx 75% complete for ERR594369_1_t_paired.fastq.gz
    Approx 80% complete for ERR594369_1_t_paired.fastq.gz
    Approx 85% complete for ERR594369_1_t_paired.fastq.gz
    Approx 90% complete for ERR594369_1_t_paired.fastq.gz
    Approx 95% complete for ERR594369_1_t_paired.fastq.gz
    Analysis complete for ERR594369_1_t_paired.fastq.gz

I've omitted the lengthy 5% increments for all 10 files. Basically, FastQC will process each file individually and
deposit the results in <filename>_fastqc.zip and <filename>_fastqc.html.

Next, we'll want to visually summarize these results using MultiQC. I'm running MultiQC in the directory with all the
FastQC results, so I'm using "." to specify "the current directory" on the command line.

.. code-block:: bash

    $ singularity run MultiQC-1.7.sif .
    [INFO   ]         multiqc : This is MultiQC v1.7
    [INFO   ]         multiqc : Template    : default
    [INFO   ]         multiqc : Searching '.'
    [INFO   ]          fastqc : Found 10 reports
    [INFO   ]         multiqc : Compressing plot data
    [INFO   ]         multiqc : Report      : multiqc_report.html
    [INFO   ]         multiqc : Data        : multiqc_data
    [INFO   ]         multiqc : MultiQC complete

Once that's done, the resulting directory should look like:

.. code-block:: bash

    $ ls -lh
    # Original input data
    ERR594369_1_fastqc.zip
    ERR594369_2_fastqc.zip
    # Trimmomatic results. Paired reads surviving (2) + unpaired reads (mate pair didn't make it) surviving (2)
    ERR594369_1_t_paired_fastqc.zip
    ERR594369_1_t_unpaired_fastqc.zip
    ERR594369_2_t_paired_fastqc.zip
    ERR594369_2_t_unpaired_fastqc.zip
    # BBDuk adapter trimming results. BBDuk will only return paired reads with the parameters we specified
    ERR594369_1_t_fastqc.zip
    ERR594369_2_t_fastqc.zip
    # BBDuk quality trimming results, using the trimming results (above) as input
    ERR594369_1_t_qc_fastqc.zip
    ERR594369_2_t_qc_fastqc.zip
    # MultiQC report and data
    multiqc_report.html
    multiqc_data

I've added comments to the command (above). *Normally*, this would NOT be in the output, but I'm commenting here to break
down what files came from where.

Assembly
--------

Assembly isn't for the faint of heart. It can be frustrating and it can fail for a lot of reasons, often due to insufficient
memory or due to the dataset complexity. There's only so much you can do.

However, our example dataset will finish on OSC within a few hours. Below is the bash script that can be submitted to OSC
that should assemble your data.

*This will run SPAdes on the Trimmomatic-cleaned reads, alternatives are below*.

.. code-block:: bash

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -t 24:00:00
    #SBATCH -n 48
    #SBATCH -J SPAdes
    #SBATCH --partition=hugemem

    # Load the SPAdes module or the singularity version
    # module use /fs/project/PAS1117/modulefiles  # Uncomment if wanting to use modules
    # module load spades/3.15.2 # Uncomment if wanting to use modules

    module load singularity

    # Directories
    projectDir="/fs/project/PAS1117/viral_ecogenomics_pipeline/"
    readsDir="${projectDir}/read_trimming/trimmomatic/"
    spadesLoc="/users/PAS1117/osu9664/eMicro-Apps/SPAdes-3.13.0.sif"
    outputDir="${projectDir}/assemblies/SPAdes_with_Trimmomatic"

    # General Options, can't use --careful with --meta
    genOpts="--meta -k 21,33,55,77,99,121"  # Paired end, 1 pair only
    runOpts="-t 48 -m 124"  # Match to job request. This is 48 cores and 744 GB memory (a node on Owens = 128 GB)

    # Whare are the reads we'll need?
    forReads="${readsDir}/ERR594369_1_t_paired.fastq.gz"
    revReads="${readsDir}/ERR594369_2_t_paired.fastq.gz"

    # spadesRun="spades.py ${genOpts} ${runOpts}"  # Because we loaded the module, the system knows where to look

    # Now that we have our parameters and input files, we can put everything together
    spadesCmd="singularity run ${spadesLoc} ${genOpts} ${runOpts}"
    spadesCmd="${spadesCmd} --pe1-1 ${forReads} --pe1-2 ${revReads}"

    # I always like to know what command was actually sent to SPAdes
    # -o will send the output of SPAdes to the assembly directory, defined above
    echo "${spadesCmd} -o ${outputDir}"

    ${spadesCmd} -o ${outputDir}

    # Uncomment the lines below if using module
    # spadesRun="${spadesRun} --pe1-1 ${pe1f} --pe1-2 ${pe1r}"

    # echo "${spadesRun} -o ${outputDir}"
    # ${spadesRun} -o "${outputDir}"


Submit using:

.. code-block:: bash

    $ sbatch SPAdes_Trimmomatic.sh

Please see the OSC guide for how this job script was created. Since I'm familiar with the sample background (sample
complexity, microbes, relative sequencing depth) and the SPAdes assembler for this sample, I can guess at how long to
request for the job. I requested 24 hours and a full large memory node (48 cores, and set SPAdes -t 48). It used to be
that at the end of the run, OSC would let you know the resources you used, but sadly, they do not (or I haven't figured
out how to automatically get it). Instead, we can use "sacct" to figure out what resources were used.

For this job:

.. code-block:: bash

    $ sacct -j 3917921 --format "CPUTime,MaxRSS,Elapsed"
       CPUTime     MaxRSS    Elapsed
    ---------- ---------- ----------
    6-14:06:24  54310312K   03:17:38

The job required ~54 GB and ~3.25 hours. We can't do anything about the GB requested, as asking for 48 cores will give
you *at least* a large memory node. We could request 60 GB of memory, but OSC will still charge you for the whole node.

And now, what if we wanted to use a different assembler, let's say MEGAHIT?

.. code-block:: bash

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -t 24:00:00
    #SBATCH -n 48
    #SBATCH -J MEGAHIT
    #SBATCH --partition=hugemem

    # Load the SPAdes module or the singularity version
    # module use /fs/project/PAS1117/modulefiles  # Uncomment if wanting to use modules
    # module load spades/3.15.2 # Uncomment if wanting to use modules

    module load singularity

    # Directories
    projectDir="/fs/project/PAS1117/viral_ecogenomics_pipeline/"
    readsDir="${projectDir}/read_trimming/trimmomatic/"
    megahitLoc="/users/PAS1117/osu9664/eMicro-Apps/MEGAHIT-1.2.8.sif"
    outputDir="${projectDir}/assemblies/MEGAHIT_with_Trimmomatic"

    # Assembling with MEGAHIT, so setting up parameters
    genOpts="--k-list 21,41,61,81,99"  # K-mer selection is a PhD itself...
    runOpts="-t 48 -m 0.9"  # Match to job request, 40 cores and 90% of memory

    # Whare are the reads we'll need?
    forReads="${readsDir}/ERR594369_1_t_paired.fastq.gz"
    revReads="${readsDir}/ERR594369_2_t_paired.fastq.gz"

    # Now that we have our parameters and input files, we can put everything together
    megahitCmd="${megahitLoc} ${genOpts} ${runOpts}"
    megahitCmd="${megahitCmd} -1 ${forReads} -2 ${revReads}"

    echo "${megahitCmd} -o ${outputDir}"

    ${megahitCmd} -o ${outputDir}

Notice how I only changed a few lines, as when we switched from using Trimmomatic to BBDuk cleaned reads. The lines that
were changed:

 * megahitLoc="/users/PAS1117/osu9664/eMicro-Apps/MEGAHIT-1.2.8.sif"
 * outputDir="${projectDir}/assemblies/MEGAHIT_with_Trimmomatic"
 * genOpts="--k-list 21,41,61,81,99"
 * runOpts="-t 48 -m 0.9"  # Match to job request, 48 cores and 90% of memory
 * megahitCmd="${megahitLoc} ${genOpts} ${runOpts}"
 * megahitCmd="${megahitCmd} -1 ${forReads} -2 ${revReads}"

The location of the assembler changed, as did the output directory. Also, because we're using a different assembler with
different parameters/arguments, we need to change those as well.

Submit!

And resources used:

.. code-block:: bash

    $ sacct -j 3929590 --format "CPUTime,MaxRSS,Elapsed,TotalCPU"
       CPUTime     MaxRSS    Elapsed   TotalCPU
    ---------- ---------- ---------- ----------
    1-09:32:00   5723168K   00:41:55 1-01:08:22

That took 41 minutes and used ~5.7 GB. That's... quite a bit faster and significantly less memory.


Identifying Viruses
-------------------

The next step is to identify which contigs are viral, and which are not.

There are many, many tools (now in 2021) to identify. *For now*, we'll focus on just using VirSorter 1.

NOTE: As this guide continues to expand, we'll add in more analyses to flesh out this content.

.. code-block:: bash

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -t 24:00:00
    #SBATCH -n 40
    #SBATCH -J VirSorter

    # Load the VirSorter module or the singularity version
    # module use /fs/project/PAS1117/modulefiles
    # module load virsorter/1.1.0

    module use singularity

    projectDir="/fs/project/PAS1117/viral_ecogenomics_pipeline/"
    spadesOutput="${projectDir}/assemblies/SPAdes_with_Trimmomatic"

    cd projectDir

    Filter_by_SeqLength.py "{spadesOutput}/contigs.fasta 5000 contigs.5k.fasta

    projectDir="/fs/project/PAS1117/viral_ecogenomics_pipeline/"

    VirSorter-1.0.5.img -f contigs.5k.fasta --db 2 --wdir VirSorter --ncpu 40 --data-dir /fs/project/PAS1117/modules/virsorter/1.1.0/databases/virsorter-data/

    # Or if using the module, uncomment the below
    wrapper_phage_contigs_sorter_iPlant.pl -f contigs.5k.fasta --db 2 --wdir VirSorter --ncpu 40 --data-dir /fs/project/PAS1117/modules/virsorter/1.1.0/databases/virsorter-data/


If you noticed, we first filtered the SPAdes contigs to 5k. Why? VirSorter doesn't tend to perform as well on smaller contigs,
as there's not as much information to work with. Alternatively, you could also use DeepVirFinder and combine the two
results.

And how long did the job take?

.. code-block:: bash

    $ sacct -j 3919608 --format "CPUTime,MaxRSS,Elapsed,TotalCPU"
       CPUTime     MaxRSS    Elapsed   TotalCPU
    ---------- ---------- ---------- ----------
    6-14:16:00   9013112K   03:57:24   23:24:18

Four hours, using 9 GB. Looks like the next time I run VirSorter on 5193 contigs I can probably shorten it!

Let's combine the highest confidence virsorter categories (1-2, 4-5) and see how many viral genomes it predicted:

.. code-block:: bash

    $ projectDir=/fs/project/PAS1117/viral_ecogenomics_pipeline/
    $ virsorterDir=$projectDir/VirSorter/Predicted_viral_sequences/

    $ cat $virsorterDir/VIRSorter_cat-1.fasta $virsorterDir/VIRSorter_cat-2.fasta $virsorterDir/VIRSorter_prophages_cat-4.fasta $virsorterDir/VIRSorter_prophages_cat-5.fasta > VirSorter_cat1245.fasta

    $ grep -c ">" VirSorter_cat1245.fasta
    5193

There's 5193 predicted viruses!


Checking the Quality with CheckV
--------------------------------

Now we'd like to check to see what the quality of the VirSorter-predicted putative viral genomes are. For this, we can
use CheckV - an awesome tool developed only a couple of years ago. Before then, viral ecology researchers didn't have
much to go on regarding what the "quality" of their viruses were. Sure, they might be confident that it's a viral genome,
but there wasn't an established method to define it.

.. code-block:: bash

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -t 1:00:00
    #SBATCH -n 40
    #SBATCH -J CheckV

    module load singularity

    # Directories
    projectDir="/fs/project/PAS1117/viral_ecogenomics_pipeline/"
    checkv="/users/PAS1117/osu9664/eMicro-Apps/CheckV-2020.04.27.sif"

    input_fp="${projectDir}/VirSorter_cat1245.fasta"
    output_dir="${projectDir}/CheckV_output"

    # Other checkV variables
    min_contig_len=2000
    min_tr_len=20
    max_tr_count=5
    max_tr_dust=20.0

    $checkv contamination -t 40 ${input_fp} ${output_dir}

    $checkv completeness -t 40 ${input_fp} ${output_dir} -t 40

    trim="--min_contig_len ${min_contig_len} --min_tr_len ${min_tr_len} --max_tr_count ${min_tr_len} --max_tr_dust ${max_tr_dust}"
    $checkv terminal_repeats $trim ${input_fp} ${output_dir}

    $checkv quality_summary ${input_fp} ${output_dir}


Once that's finished, let's look at the output files generated in the ${output_dir}:

.. code-block:: bash

    cleaned_contigs.fna
    contamination.tsv
    completeness.tsv
    tmp
    terminal_repeats.tsv
    quality_summary.tsv

Each file corresponds to each of the CheckV steps, plus a tmp/ directory and cleaned_contigs.fna.

And what does the top of the quality look like?

contig_id	contig_length	checkv_quality	miuvig_quality	completeness	contamination	prophage	terminicomments
VIRSorter_NODE_44_length_103345_cov_0_397294-cat_1	103345	Medium-quality	Genome-fragment	54.08	0.0	No	NA
VIRSorter_NODE_79_length_76634_cov_0_488273-cat_1	76634	Low-quality	Genome-fragment	43.73	0.0	No	NA
VIRSorter_NODE_98_length_66506_cov_0_281883-cat_1	66506	Low-quality	Genome-fragment	35.83	0.0	No	NA
VIRSorter_NODE_106_length_63961_cov_0_327190-cat_1	63961	Low-quality	Genome-fragment	34.13	0.0	No	NA
VIRSorter_NODE_136_length_55559_cov_0_526740-cat_1	55559	Low-quality	Genome-fragment	33.26	0.0	No	NA
VIRSorter_NODE_145_length_52574_cov_0_529166-cat_1	52574	Low-quality	Genome-fragment	24.52	0.0	No	NA
VIRSorter_NODE_146_length_52536_cov_1_173084-cat_1	52536	High-quality	High-quality	134.39	0.0	No	NA	Warning: completeness >110%. Estimate may be unreliable.
VIRSorter_NODE_169_length_48035_cov_0_841226-cat_1	48035	Low-quality	Genome-fragment	25.42	0.0	No	NA
VIRSorter_NODE_173_length_47685_cov_0_177258-cat_1	47685	Low-quality	Genome-fragment	27.08	0.0	No	NA

From the results of CheckV, it looks like we have:

810 Low-quality
24 Medium-quality
17 High-quality
68 Not-determined

Not too bad. Since this is only one dataset, we're probably not going to be able to generate very long, high-quality
genomes.


Preparing for vConTACT2 and Running vConTACT2
---------------------------------------------

vConTACT2 is a tool to classify viral genomes. But first, we need to get the input files setup. In the script below,
we'll run prodigal first - to generate proteins - and then use an accessory function to prepare vConTACT2 files.

.. code-block:: bash

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -t 4:00:00
    #SBATCH -n 48
    #SBATCH -J vConTACT2
    #SBATCH --partition=hugemem

    module load singularity
    module use /fs/project/PAS1117/modulefiles
    module load singularityImages

    # Directories
    projectDir="/fs/project/PAS1117/viral_ecogenomics_pipeline/"
    vcontact2Loc="/users/PAS1117/osu9664/eMicro-Apps/vConTACT2-0.9.20.sif"
    outputDir="${projectDir}/vConTACT2_Output"

    prodigal -i VirSorter_cat1245.fasta -p meta -a VirSorter_cat1245.faa -o VirSorter_cat1245.prodigal

    vContact-Gene2Contig-1.0.0.img -p VirSorter_cat1245.faa -o VirSorter_cat1245_proteins.csv -s Prodigal-FAA

    vConTACT2-0.9.20.sif --pcs-mode MCL --vcs-mode ClusterONE --threads 48 --raw-proteins VirSorter_cat1245.faa --rel-mode Diamond --proteins-fp VirSorter_cat1245_proteins.csv --db 'ProkaryoticViralRefSeq201-Merged' --c1-bin /usr/local/bin/cluster_one-1.0.jar --output-dir $outputDir


And with that, we've gone from raw, environmental viral metagenome data (downloaded from the SRA). We've QC'd, assembled, 
identified viral genomes, checked their quality, and then got a bit of classification. Just like with the Microbial 
Ecology pipeline, we're only two steps away from a published manuscript!

