.. _processing_microbe:

End-to-End Processing of a Microbial Metagenome
===============================================

For this dataset, we'll be **fully** processing `SRX4071230 <https://www.ncbi.nlm.nih.gov/sra/SRX4071230>`_, a peat
metagenome with 14.1M reads. The SRA Run is SRR7151490, which will be important when downloading the data from SRA.

This will include (nearly) all steps and *most* of the results returned from the command line. Clearly, some outputs
can't be nicely placed here, but are available (as links to files) or in the M8194 project directory.

Everything here uses Singularity. All of the singularity images are located at:

**/users/PAS1117/osu9664/eMicro-Apps/**

So you must prepend each \*.img, \*.simg or \*.sif Singularity container w/ this path OR link them (see :ref:`UNIX_LINUX`).

Downloading the data
--------------------

We need to grab the data from the SRA.

.. code-block:: bash

    # Move to project directory
    $ cd /fs/project/PAS1573/week7_processing
    # Load modules necessary
    $ module load singularity
    $ singularity run SRA_Toolkit.sif fasterq-dump –e 4 SRR7151490
    spots read      : 14,145,898
    reads read      : 28,291,796
    reads written   : 28,291,796

In the example above, we used *fasterq-dump*, which is designated to download two paired end read files in fastq format.
We also specified 4 threads (-e 4) so it would run a little faster. There should be *two* output files: SRR7151490_1.fastq
and SRR7151490_2.fastq. fasterq-dump won't compress the files for you, so you'll have to do this after the download completes.

Read Quality Control
--------------------

We will be using either `BBDuk <https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbduk-guide/>`_ or
`Trimmomatic <http://www.usadellab.org/cms/?page=trimmomatic>`_ to process our input reads. *You only need to select one*.
We'll be using both for examples, but typically stick with one and use it.

.. code-block:: bash

    $ singularity run Trimmomatic-0.36.0.img PE SRR7151490_1.fastq SRR7151490_2.fastq SRR7151490_1_t_paired.fastq.gz SRR7151490_1_t_unpaired.fastq.gz SRR7151490_2_t_paired.fastq.gz SRR7151490_2_t_unpaired.fastq.gz ILLUMINACLIP:/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10:2 LEADING:3 TRAILING:3 MINLEN:36
    TrimmomaticPE: Started with arguments:
    SRR7151490_1.fastq SRR7151490_2.fastq SRR7151490_1_t_paired.fastq.gz SRR7151490_1_t_unpaired.fastq.gz SRR7151490_2_t_paired.fastq.gz SRR7151490_2_t_unpaired.fastq.gz ILLUMINACLIP:/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10:2 LEADING:3 TRAILING:3 MINLEN:36
    Using PrefixPair: 'TACACTCTTTCCCTACACGACGCTCTTCCGATCT' and 'GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT'
    ILLUMINACLIP: Using 1 prefix pairs, 0 forward/reverse sequences, 0 forward only sequences, 0 reverse only sequences
    Quality encoding detected as phred33
    Input Read Pairs: 14145898 Both Surviving: 13356639 (94.42%) Forward Only Surviving: 705239 (4.99%) Reverse Only Surviving: 64641 (0.46%) Dropped: 19379 (0.14%)
    TrimmomaticPE: Completed successfully

    real	11m0.811s
    user	11m43.109s
    sys	0m12.327s

For Trimmomatic, the defaults work pretty well. Note the location of the IlluminaClip - it's already "in" the Singularity
file. If you have your own custom primers/adapters, you'll need to add your sequences or create your own primer and adapter
file.

Next, BBDuk. BBDuk is usually done in 2-3 steps, with 1st being an adapter trimming step, and 2nd with the removal of
low quality sequences.

.. code-block:: bash

    $ singularity run BBTools-38.69.sif bbduk.sh in1=SRR7151490_1.fastq in2=SRR7151490_2.fastq out1=SRR7151490_1_t.fastq out2=SRR71514902_t.fastq ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    java -ea -Xmx58304m -Xms58304m -cp /bbmap/current/ jgi.BBDuk in1=SRR7151490_1.fastq in2=SRR7151490_2.fastq out1=SRR7151490_1_t.fastq out2=SRR71514902_t.fastq ref=/bbmap/resources/adapters.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo
    Executing jgi.BBDuk [in1=SRR7151490_1.fastq, in2=SRR7151490_2.fastq, out1=SRR7151490_1_t.fastq, out2=SRR71514902_t.fastq, ref=/bbmap/resources/adapters.fa, ktrim=r, k=23, mink=11, hdist=1, tpe, tbo]
    Version 38.69

    maskMiddle was disabled because useShortKmers=true
    0.022 seconds.
    Initial:
    Memory: max=61136m, total=61136m, free=61102m, used=34m

    Added 217135 kmers; time: 	0.064 seconds.
    Memory: max=61136m, total=61136m, free=61027m, used=109m

    Input is being processed as paired
    Started output streams:	0.027 seconds.
    Processing time:   		22.848 seconds.

    Input:                  	28291796 reads 		2857471396 bases.
    KTrimmed:               	66418 reads (0.23%) 	2072372 bases (0.07%)
    Trimmed by overlap:     	7444 reads (0.03%) 	81230 bases (0.00%)
    Total Removed:          	12460 reads (0.04%) 	2153602 bases (0.08%)
    Result:                 	28279336 reads (99.96%) 	2855317794 bases (99.92%)

    Time:                         	22.942 seconds.
    Reads Processed:      28291k 	1233.19k reads/sec
    Bases Processed:       2857m 	124.55m bases/sec

    real	0m25.604s
    user	3m38.195s
    sys	0m8.344s

.. code-block:: bash

    $ singularity run BBTools-38.69.sif bbduk.sh in1=SRR7151490_1_t.fastq in2=SRR71514902_t.fastq qtrim=rl trimq=10 out1=SRR7151490_1_t_qc.fastq out2=SRR7151490_2_t_qc.fastq
    java -ea -Xmx58304m -Xms58304m -cp /bbmap/current/ jgi.BBDuk in1=SRR7151490_1_t.fastq in2=SRR71514902_t.fastq qtrim=rl trimq=10 out1=SRR7151490_1_t_qc.fastq out2=SRR7151490_2_t_qc.fastq
    Executing jgi.BBDuk [in1=SRR7151490_1_t.fastq, in2=SRR71514902_t.fastq, qtrim=rl, trimq=10, out1=SRR7151490_1_t_qc.fastq, out2=SRR7151490_2_t_qc.fastq]
    Version 38.69

    0.024 seconds.
    Initial:
    Memory: max=61136m, total=61136m, free=61102m, used=34m

    Input is being processed as paired
    Started output streams:	0.021 seconds.
    Processing time:   		7.409 seconds.

    Input:                  	28279336 reads 		2855317794 bases.
    QTrimmed:               	4386431 reads (15.51%) 	183780487 bases (6.44%)
    Total Removed:          	837690 reads (2.96%) 	183780487 bases (6.44%)
    Result:                 	27441646 reads (97.04%) 	2671537307 bases (93.56%)

    Time:                         	7.431 seconds.
    Reads Processed:      28279k 	3805.70k reads/sec
    Bases Processed:       2855m 	384.26m bases/sec

    real	0m8.023s
    user	0m39.299s
    sys	0m7.407s

BBDuk completed in 25+8 seconds, Trimmomatic in 11 minutes. Certainly a performance difference. How does the quality
check out?

Read Quality Control (Visualizing)
----------------------------------

Here, we've already loaded singularity (above) and moved to the project directory. In this example, I'm going to run
FastQC on all of the input files (2), the results from Trimmomatic (4) and the adapter trimmed (2) and quality filtered
(2) read *pairs* of BBDuk.

.. code-block:: bash

    $ singularity run FastQC-0.11.8.sif SRR7151490_1.fastq SRR7151490_2.fastq SRR7151490_1_t_paired.fastq SRR7151490_1_t_unpaired.fastq SRR7151490_2_t_paired.fastq SRR7151490_2_t_unpaired.fastq SRR7151490_1_t.fastq SRR7151490_1_t_qc.fastq SRR7151490_2_t.fastq SRR7151490_2_t_qc.fastq
    Started analysis of SRR7151490_1.fastq
    Approx 5% complete for SRR7151490_1.fastq
    Approx 10% complete for SRR7151490_1.fastq
    Approx 15% complete for SRR7151490_1.fastq
    …
    …
    Approx 95% complete for SRR7151490_1.fastq
    Analysis complete for SRR7151490_1.fastq

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
    SRR7151490_1_fastqc.zip
    SRR7151490_2_fastqc.zip
    # Trimmomatic results. Paired reads surviving (2) + unpaired reads (mate pair didn't make it) surviving (2)
    SRR7151490_1_t_paired_fastqc.zip
    SRR7151490_1_t_unpaired_fastqc.zip
    SRR7151490_2_t_paired_fastqc.zip
    SRR7151490_2_t_unpaired_fastqc.zip
    # BBDuk adapter trimming results. BBDuk will only return paired reads with the parameters we specified
    SRR7151490_1_t_fastqc.zip
    SRR7151490_2_t_fastqc.zip
    # BBDuk quality trimming results, using the trimming results (above) as input
    SRR7151490_1_t_qc_fastqc.zip
    SRR7151490_2_t_qc_fastqc.zip
    # MultiQC report and data
    multiqc_report.html
    multiqc_data

I've added comments to the command (above). *Normally*, this would NOT be in the output, but I'm commenting here to break
down what files came from where.

Let's look at the results:

(will be inserting results page shortly)

Assembly
--------

Assembly isn't for the faint of heart. It can be frustrating and it can fail for a lot of reasons, often due to insufficient
memory or due to the dataset complexity. There's only so much you can do.

However, our example dataset will finish on OSC within a few hours. Below is the bash script that can be submitted to OSC
that should assemble your data.

*This will run SPAdes on the Trimmomatic-cleaned reads, alternatives are below*.

.. code-block:: bash

    #PBS -l walltime=12:00:00
    #PBS -l nodes=1:ppn=40
    #PBS -N SPAdes_SRR7151490_Trimmomatic
    #PBS -A PAS1573
    #PBS -S /bin/bash
    #PBS -j oe
    #PBS -m ae

    # Load modules that we'll need
    module load singularity

    # Set variables for this script - it makes it easier to refer to later on
    # Some get confused by this, but in the long run it'll save a lot of typing

    # Root/core directories
    projectDir="/fs/project/PAS1573/week7_processing/"
    readsDir="${projectDir}/trimmed_trimmomatic/"
    spadesLoc="/users/PAS1117/osu9664/eMicro-Apps/SPAdes-3.13.0.sif"
    outputDir="${projectDir}/assemblies/SPAdes_with_Trimmomatic"

    # Whare are the reads we'll need?
    forReads="${readsDir}/SRR7151490_1_t_paired.fastq.gz"
    revReads="${readsDir}/SRR7151490_2_t_paired.fastq.gz"

    # Assembling with SPAdes, so setting up parameters
    genOpts="--meta -k 21,33,55,77"  # Paired end, 1 pair only
    runOpts="-t 40 -m 190"  # Match to job request, 40 cores and ~192 GB of memory

    # Now that we have our parameters and input files, we can put everything together
    spadesCmd="singularity run ${spadesLoc} ${genOpts} ${runOpts}"
    spadesCmd="${spadesCmd} --pe1-1 ${forReads} --pe1-2 ${revReads}"

    # I always like to know what command was actually sent to SPAdes
    # -o will send the output of SPAdes to the assembly directory, defined above
    echo "${spadesCmd} -o ${outputDir}"

    ${spadesCmd} -o ${outputDir}

Submit using:

.. code-block:: bash

    qsub spades_assembly_trimmomatic_reads.sh

Please see the OSC guide for how this job script was created. Since I'm familiar with the sample background (sample
complexity, microbes, relative sequencing depth) and the SPAdes assembler for this sample, I can guess at how long to
request for the job. I requested 12 hours and a full node (ppn=40 cores, and set SPAdes -t 40). At the end of the run,
OSC will let you know what kind of resources you actually used. For this job:

 * resources_used.vmem=41783760kb
 * resources_used.walltime=10:37:21

The job required ~42 GB and ~10.5 hours. We can't do anything about the GB requested, as asking for 40 cores will give
you the whole (192 GB) node. We could request 50 GB of memory, but OSC will still charge you for the whole node.

But what if we didn't want to use Trimmomatic? Let's use the BBDuk-cleaned reads, generated earlier? Instead of
copying-and-pasting the whole bash script, i'll only highlight the changes:

readsDir="${projectDir}/trimmed_trimmomatic/" --> readsDir="${projectDir}/trimmed_bbduk/"

outputDir="${projectDir}/assemblies/SPAdes_with_Trimmomatic" --> outputDir="${projectDir}/assemblies/SPAdes_with_BBDuk"

forReads="${readsDir}/SRR7151490_1_t_paired.fastq.gz" --> forReads="${readsDir}/SRR7151490_1_t_qc.fastq"

revReads="${readsDir}/SRR7151490_2_t_paired.fastq.gz" --> revReads="${readsDir}/SRR7151490_2_t_qc.fastq"

And that's it! Submit that to OSC!

What resources were used?

 * resources_used.vmem=42275192kb
 * resources_used.walltime=10:28:35

About the same amount of resources. It makes sense since our reads were trimmed a tiny amount and there wasn't much
difference between them anyway.

And now, what if we wanted to use a different assembler, let's say MEGAHIT?

.. code-block:: bash

    #PBS -l walltime=2:00:00
    #PBS -l nodes=1:ppn=40
    #PBS -N METAHIT_SRR7151490_Trimmomatic
    #PBS -A PAS1573
    #PBS -S /bin/bash
    #PBS -j oe
    #PBS -m ae

    # Load modules that we'll need
    module load singularity

    # Root/core directories
    projectDir="/fs/project/PAS1573/week7_processing/"
    readsDir="${projectDir}/trimmed_trimmomatic/"
    megahitLoc="/users/PAS1117/osu9664/eMicro-Apps/MEGAHIT-1.2.8.sif"
    outputDir="${projectDir}/assemblies/MEGAHIT_with_Trimmomatic"

    # Whare are the reads we'll need?
    forReads="${readsDir}/SRR7151490_1_t_paired.fastq.gz"
    revReads="${readsDir}/SRR7151490_2_t_paired.fastq.gz"

    # Assembling with MEGAHIT, so setting up parameters
    genOpts="--k-list 21,41,61,81,99"  # K-mer selection is a PhD itself...
    runOpts="-t 40 -m 0.9"  # Match to job request, 40 cores and 90% of memory

    # Now that we have our parameters and input files, we can put everything together
    megahitCmd="singularity run ${megahitLoc} ${genOpts} ${runOpts}"
    megahitCmd="${megahitCmd} -1 ${forReads} -2 ${revReads}"

    # I always like to know what command was actually sent to SPAdes
    # -o will send the output of SPAdes to the assembly directory, defined above
    echo "${megahitCmd} -o ${outputDir}"

    ${megahitCmd} -o ${outputDir}

Notice how I only changed a few lines, as when we switched from using Trimmomatic to BBDuk cleaned reads. The lines that
were changed:

 * megahitLoc="/users/PAS1117/osu9664/eMicro-Apps/MEGAHIT-1.2.8.sif"
 * outputDir="${projectDir}/assemblies/MEGAHIT_with_Trimmomatic"
 * genOpts="--k-list 21,41,61,81,99"
 * runOpts="-t 40 -m 0.9"  # Match to job request, 40 cores and 90% of memory
 * megahitCmd="singularity run ${megahitLoc} ${genOpts} ${runOpts}"
 * megahitCmd="${megahitCmd} -1 ${forReads} -2 ${revReads}"

The location of the assembler changed, as did the output directory. Also, because we're using a different assembler with
different parameters/arguments, we need to change those as well.

Submit!

* resources_used.vmem=7302672kb
* resources_used.walltime=00:20:29

Wow. 20 minutes and 7 GB of memory. More on this later...

And finally, IDBA-UD. Oh wait, IDBA-UD wants fasta-formatted sequences. We need to make a small change.

.. code-block:: bash

    $ singularity exec /users/PAS1117/osu9664/eMicro-Apps/IDBA-UD-1.1.3.sif fq2fa --merge --filter SRR7151490_1_t_paired.fastq SRR7151490_2_t_paired.fastq SRR7151490_t_paired.fasta

    real	1m9.317s
    user	1m3.504s
    sys	0m4.836s

We just converted our gzip-decompressed fastq files into fasta. Now we can submit. Let's use BBDuk reads this time.

.. code-block:: bash

    #PBS -l walltime=2:00:00
    #PBS -l nodes=1:ppn=40
    #PBS -N IDBA_UD_SRR7151490_BBDuk
    #PBS -A PAS1573
    #PBS -S /bin/bash
    #PBS -j oe
    #PBS -m ae

    # Load modules that we'll need
    module load singularity

    # Root/core directories
    projectDir="/fs/project/PAS1573/week7_processing/"
    readsDir="${projectDir}/trimmed_bbduk/"
    idbaLoc="/users/PAS1117/osu9664/eMicro-Apps/IDBA-UD-1.1.3.sif"
    outputDir="${projectDir}/assemblies/IDBA_UD_with_BBDuk"

    # Whare are the reads we'll need?
    bothReads="${readsDir}/SRR7151490_t_paired.fasta"

    # Assembling with IDBA-UD, so setting up parameters
    runOpts="--num_threads 40"

    idbaCmd="singularity run ${idbaLoc} ${runOpts}"
    idbaCmd="${idbaCmd} -r ${bothReads}"

    echo "${idbaCmd} -o ${outputDir}"

    ${idbaCmd} -o ${outputDir}

And resources used:

* resources_used.vmem=56120080kb
* resources_used.walltime=01:29:35

Binning
-------

Tune in next week for the next exciting adventure in microbial metagenome processing!
