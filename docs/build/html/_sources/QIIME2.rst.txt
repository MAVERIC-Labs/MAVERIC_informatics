.. _QIIME2:

QIIME2
======

Nearly all of this documentation is taken directly from lecture and text guides from class. QIIME2 instructions to
process the "moving pictures" dataset are from Instructor Shareef's guide found on `Carmen <https://carmen.osu.edu/#>`_.
If you'd like to read up more about this dataset, they can be found `here <https://genomebiology.biomedcentral.com/articles/10.1186/gb-2011-12-5-r50>`_.

Before beginning, you'll want to copy the two examples files from the project directory (/fs/project/PAS1573) on scratch to
 your home directory!

Sequencing data: /fs/project/PAS1573/week3_16S/qiime2/moving_pictures/single_end

Metadata: /fs/project/PAS1573/week3_16S/qiime2/moving_pictures/mp_sample_metadata.tsv

Please check out the OSC/linux intro if you have any questions/need help for how to copy files from one location to another.

Data Import
-----------

We start by importing our single end sequencing data into a QIIME2-compatible format, the \*.qza.

.. code-block:: bash

    qiime tools import --type EMPSingleEndSequences --input-path data/single_end/ --output-path emp-single-end-sequences.qza

Remember, QIIME2 thinks in terms of methods --> artifacts, which in this case is EMPSingleEndSequences, and visualizers
(not shown here, yet), in visualizations.

Demultiplexing
--------------

Next we'll demultiplex the sequences

.. code-block:: bash

    qiime demux emp-single --i-seqs emp-single-end-sequences.qza --m-barcodes-file sample_metadata.tsv --m-barcodes-column barcode-sequence --o-per-sample-sequences demux.qza --o-error-correction-details demux-details.qza

You should generate two files:

Saved SampleData[SequencesWithQuality] to: demux.qza

Saved ErrorCorrectionDetails to: demux-details.qza

After demultiplexing, we need to summarize the data to see what we got!

Summarize
---------

.. code-block:: bash

    qiime demux summarize --i-data demux.qza --o-visualization demux.qzv

Notice how we now have a \*.qzv file? This is QIIME2's **v**\ isualization file that can be uploaded to the
`QIIME2 view page <https://view.qiime2.org/>`_. Go ahead and try it and see what happens.

Quality Control and Creating the Feature Table
----------------------------------------------

Sequence quality control and feature table construction

.. code-block:: bash

    qiime quality-filter q-score --i-demux demux.qza --o-filtered-sequences demux-filtered.qza --o-filter-stats demux-filter-stats.qza

Saved SampleData[SequencesWithQuality] to: demux-filtered.qza

Saved QualityFilterStats to: demux-filter-stats.qza

Next we're going to use deblur to clean up our 16S data.

.. code-block:: bash

    qiime deblur denoise-16S --i-demultiplexed-seqs demux-filtered.qza --p-trim-length 120 --o-representative-sequences rep-seqs-deblur.qza --o-table tble-deblur.qza --p-sample-stats --o-stats deblur-stats.qza

Saved FeatureTable[Frequency] to: table-deblur.qza

Saved FeatureData[Sequence] to: rep-seqs-deblur.qza

Saved DeblurStats to: deblur-stats.qza

FeatureTable and FeatureData summaries

.. code-block:: bash

    qiime feature-table summarize --i-table table-deblur.qza --o-visualization table-deblur.qzv --m-sample-metadata-file mp_sample_metadata.tsv

Saved Visualization to: table-deblur.qzv

.. code-block:: bash

    qiime feature-table tabulate-seqs --i-data rep-seqs-deblur.qza --o-visualization rep-seqs-deblur.qzv

Saved Visualization to: rep-seqs-deblur.qzv

Generate a tree for phylogenetic diversity analyses

.. code-block:: bash

    qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs-deblur.qza --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza

Saved FeatureData[AlignedSequence] to: aligned-rep-seqs.qza

Saved FeatureData[AlignedSequence] to: masked-aligned-rep-seqs.qza

Saved Phylogeny[Unrooted] to: unrooted-tree.qza

Saved Phylogeny[Rooted] to: rooted-tree.qza

Alpha and Beta Diversity Analyses
---------------------------------

Alpha diversity can be measured in a few ways. QIIME2 supports many of these. The ones we'll be looking at are:

* Shannon's diversity index
* Observed OTUs
* Faith's phylogenetic diversity
* Evenness

For Beta diversity:

* Jaccard distance
* Bray-Curtise distance
* unweighted UniFrac distance
* weighted UniFrac distance

.. code-block:: bash

    qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table-deblur.qza --p-sampling-depth 850 --m-metadata-file mp_sample_metadata.tsv --output-dir core-metrics-results-850

Saved FeatureTable[Frequency] to: core-metrics-results-850/rarefied_table.qza

Saved SampleData[AlphaDiversity] % Properties('phylogenetic') to: core-metrics-results-850/faith_pd_vector.qza

Saved SampleData[AlphaDiversity] to: core-metrics-results-850/observed_otus_vector.qza

Saved SampleData[AlphaDiversity] to: core-metrics-results-850/shannon_vector.qza

Saved SampleData[AlphaDiversity] to: core-metrics-results-850/evenness_vector.qza

Saved DistanceMatrix % Properties('phylogenetic') to: core-metrics-results-850/unweighted_unifrac_distance_matrix.qza

Saved DistanceMatrix % Properties('phylogenetic') to: core-metrics-results-850/weighted_unifrac_distance_matrix.qza

Saved DistanceMatrix to: core-metrics-results-850/jaccard_distance_matrix.qza

Saved DistanceMatrix to: core-metrics-results-850/bray_curtis_distance_matrix.qza

Saved PCoAResults to: core-metrics-results-850/unweighted_unifrac_pcoa_results.qza

Saved PCoAResults to: core-metrics-results-850/weighted_unifrac_pcoa_results.qza

Saved PCoAResults to: core-metrics-results-850/jaccard_pcoa_results.qza

Saved PCoAResults to: core-metrics-results-850/bray_curtis_pcoa_results.qza

Saved Visualization to: core-metrics-results-850/unweighted_unifrac_emperor.qzv

Saved Visualization to: core-metrics-results-850/weighted_unifrac_emperor.qzv

Saved Visualization to: core-metrics-results-850/jaccard_emperor.qzv

Saved Visualization to: core-metrics-results-850/bray_curtis_emperor.qzv

Wow. That was a lot of outputs. Always been aware of **what** you're looking at. The filename has what kind of analysis
was performed, but it's up to you to figure out what it means!

.. code-block:: bash

    qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/faith_pd_vector.qza --m-metadata-file mp_sample_metadata.tsv --o-visualization core-metrics-results/faith_pd_group-significance.qzv

Saved Visualization to: core-metrics-results-741/faith_pd_group-significance.qzv

.. code-block:: bash

    qiime diversity alpha-group-significance --i-alpha-diversity core-metrics-results/evenness_vector.qza --m-metadata-file mp_sample_metadata.tsv --o-visualization core-metrics-results/evenness-group-significance.qzv

Saved Visualization to: core-metrics-results/evenness-group-significance.qzv

Next we're going to look at beta diversity, looking to compare different metadata.

Body site

.. code-block:: bash

    qiime diversity beta-group-significance --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza --m-metadata-file mp_sample_metadata.tsv --m-metadata-column body-site --o-visualization core-metrics-results/unweighted_unifrac-body-site-sig.qzv --p-pairwise

Saved Visualization to: core-metrics-results/unweighted_unifrac-body-site-sig.qzv

Subject

.. code-block:: bash

    qiime diversity beta-group-significance --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza --m-metadata-file mp_sample_metadata.tsv --m-metadata-column subject --o-visualization core-metrics-results/unweighted_unifrac-subject-sig.qzv --p-pairwise

Saved Visualization to: core-metrics-results/unweighted_unifrac-subject-sig.qzv

Longitudinal

.. code-block:: bash

    qiime emperor plot --i-pcoa core-metrics-results/unweighted_unifrac_pcoa_results.qza --m-metadata-file mp_sample_metadata.tsv --p-custom-axes days-since-experiment-start --o-visualization core-metrics-results/unweighted_unifrac-emperor-dses.qzv

Saved Visualization to: core-metrics-results/unweighted_unifrac-emperor-dses.qzv

Alpha rarefaction

.. code-block:: bash

    qiime diversity alpha-rarefaction --i-table table-deblur.qza --i-phylogeny rooted-tree.qza --p-max-depth 4000 --m-metadata-file mp_sample_metadata.tsv --o-visualization alpha-rarefaction.qzv

Assign taxonomy

.. code-block:: bash

    qiime feature-classifier classify-sklearn --i-classifier /fs/project/PAS1573/week3_16S/qiime2/gg-13-8-99-515-806-nb-classifier.qza --i-reads rep-seqs-deblur.qza --o-classification taxonomy-deblur.qza

Saved FeatureData[Taxonomy] to: taxonomy-deblur.qza

.. code-block:: bash

    qiime metadata tabulate --m-input-file taxonomy-deblur.qza--o-visualization taxonomy.qzv

Saved Visualization to: taxonomy.qzv

.. code-block:: bash

    qiime taxa barplot --i-table table-deblur.qza --i-taxonomy taxonomy-deblur.qza --m-metadata-file mp_sample_metadata.tsv --o-visualization taxa-bar-plots.qzv

Saved Visualization to: taxa-bar-plots.qzv

