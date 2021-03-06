## Input data

### Genome

To run `ANANSE` on your sample(s), a matching genome and gene annotation is necessary. We recommand that you download your genome file with [genomepy](https://github.com/vanheeringen-lab/genomepy). Genomepy is a Python package with command-line interface to easily download and install genomes, generates associated files and more.

To install the genome with `genomepy` you can use this command, which will download both the `FASTA` file and the annotation `BED` file, and exports them to the PATH.

``` bash
# activate ananse environment
conda activate ananse

# install the hg38 genome
genomepy install hg38 UCSC -a

# or, alternatively, the version from Ensembl
genomepy install GRCh38.p13 Ensembl -a
```

You can then direct to the genome like so: `-g hg38`

If you wish to manually set the files required for ANANSE, create a folder containing:  

    * A genome FASTA file   

    * A BED12 file with genome annotation.  

!!! note  
    Some model organism gene bed12 files are included in ANANSE:  

    * [hg19](https://github.com/vanheeringen-lab/ANANSE/blob/master/ananse/db/hg19.genes.bed)  

    * [hg38](https://github.com/vanheeringen-lab/ANANSE/blob/master/ananse/db/hg38.genes.bed)  

    * [mm10](https://github.com/vanheeringen-lab/ANANSE/blob/master/ananse/db/mm10.gene.bed)  

    * [xt9.1](https://github.com/vanheeringen-lab/ANANSE/blob/master/ananse/db/xt9.1.gene.bed)  
    
    * [xt10.0](https://github.com/vanheeringen-lab/ANANSE/blob/master/ananse/db/xt10.0.gene.bed)  


You can then direct to the genome like so: `-g /path/to/genome.fa`

### Motif database

By default ANANSE uses a non-redundant, clustered database of known vertebrate motifs: `gimme.vertebrate.v5.0`. These motifs come from CIS-BP (http://cisbp.ccbr.utoronto.ca/) and other sources. [Large-scale benchmarks](https://www.biorxiv.org/content/10.1101/474403v1.full) using ChIP-seq peaks show that this database shows good performance and should be a good default choice. 

!!! warning
    If you would like to use your own motif database, please make sure your database include following two files: 1) **a motif file** and 2) **a motif2factors file**.
    The `motif` file should contain positional frequency matrices and should end with the `.pfm` extension. The `motif2factors` file should have the same name as  the `motif` file and end with `.motif2factors.txt` instead of `.pfm`.

#### Motif file

```    
# Comments are allowd
>GM.5.0.Sox.0001
0.7213	0.0793	0.1103	0.0891
0.9259	0.0072	0.0062	0.0607
0.0048	0.9203	0.0077	0.0672
0.9859	0.0030	0.0030	0.0081
0.9778	0.0043	0.0128	0.0051
0.1484	0.0050	0.0168	0.8299
```

#### Motif2factors file  

```
Motif	Factor	Evidence	Curated
GM.5.0.Sox.0001	SRY	JASPAR	Y
GM.5.0.Sox.0001	SOX9	Transfac	Y
GM.5.0.Sox.0001	Sox9	Transfac	N
GM.5.0.Sox.0001	SOX9	SELEX	Y
GM.5.0.Sox.0001	Sox9	SELEX	N
GM.5.0.Sox.0001	SOX13	ChIP-seq	Y
GM.5.0.Sox.0001	SOX9	ChIP-seq	Y
GM.5.0.Sox.0001	Sox9	ChIP-seq	N
GM.5.0.Sox.0001	SRY	SELEX	Y
```

!!! note  
    The default motif database (`gimme.vertebrate.v5.0`) from the [GimmeMotifs](https://github.com/vanheeringen-lab/gimmemotifs) package[^1] can be found here:  

    * [gimme.vertebrate.v5.0.pfm](https://github.com/vanheeringen-lab/gimmemotifs/blob/master/data/motif_databases/gimme.vertebrate.v5.0.pfm)  
    * [gimme.vertebrate.v5.0.motif2factors.txt](https://github.com/vanheeringen-lab/gimmemotifs/blob/master/data/motif_databases/gimme.vertebrate.v5.0.motif2factors.txt)

### Enhancer data

The enhancer data file that ANANSE needs as input should contain putative enhancer regions with an associated enhancer signal for the specific cell type or tissue. This signal can be any measure that is related to enhancer activity. We have used p300 or H3K27ac ChIP-seq signal. p300 ChIP-seq peaks can be used directly, however the H3K27ac signal is not specific enough. Peaks from a H3K27ac ChIP-seq experiment are too broad for the motif analysis. This means that you will have to use another source of data to determine the putative enhancer regions. For human data, we estblished a enhancer peak database. For other genome, we have used ATAC-seq peaks, but other data such as DNase I could also work.

In practice these are examples of approaches that will work: Use [STAR]()/[bwa]() or your tool of choice to map your `fastq` files to the genome. Use [MACS2](https://github.com/taoliu/MACS) or your tool of choice to identify the peaks. Then establish enhancer peak normalize it with `ananse enhancer` command.  


* For **H3K27ac ChIP-seq for human hg38** data. The `ananse enhancer` command will generate enhancer file based on built-in human enhancer database (200bp) and H3K27ac ChIP-seq intensity (2000bp).   

!!! tip "Example"
    `ananse enhancer -g hg38 -t H3K27ac -b KRT_H3K27ac.sorted.bam -p KRT_H3K27ac.broadPeak -o KRT_enhancer.bed`


* For **p300 ChIP-seq** data. The `ananse enhancer` command will generate enhancer file based on p300 ChIP-seq peak (200bp) and p300 ChIP-seq intensity (200bp).   

!!! tip "Example"
    `ananse enhancer -g hg19 -t p300 -b KRT_p300.sorted.bam -p KRT_p300.narrowPeak -o KRT_enhancer.bed`


* For **ATAC-seq and H3K27ac ChIP-seq** data. The `ananse enhancer` command will generate enhancer file based on ATAC-seq peak (200bp) and H3K27ac ChIP-seq intensity (2000bp).  

!!! tip "Example"
    `ananse enhancer -g hg19 -t ATAC -b KRT_H3K27ac.sorted.bam -p KRT_ATAC.narrowPeak -o KRT_enhancer.bed`



This is an example of an input BED file:

```
chr2	148881617	148881817	7
chr7	145997204	145997404	4
chr7	145997304	145997404	4
chr7	145997104	145997404	4
chr13	109424160	109424360	20
chr14	32484901	32485101	2

```

!!! note 
    You can find our example enhancer files at here: 

    * [FB_enhancer.bed](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/FB_enhancer.bed)  
    * [KRT_enhancer.bed](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/KRT_enhancer.bed)


### Expression data

The expression data normally comes from an RNA-seq experiment. We use the `TPM` score to represent the gene expression in ANANSE. In the expression input file, the 1st column (named as `target_id`) should contain the **gene name**, and the second column should be named `tpm`. At the moment TFs are coupled to motifs my HGNC symbol, so all gene identifiers should be the approved HGNC gene names.

This is an example of the input expression file:

```
target_id	tpm
A1BG	9.579771
A1CF	0.0223
A2M	0.25458
A2ML1	664.452
A3GALT2	0.147194
```

!!! note 
    You can find our example expression files here:  

    * [FB_rep1_TPM.txt](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/FB_rep1_TPM.txt)  
    * [FB_rep2_TPM.txt](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/FB_rep2_TPM.txt)  
    * [KRT_rep1_TPM.txt](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/KRT_rep1_TPM.txt)  
    * [KRT_rep2_TPM.txt](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/KRT_rep2_TPM.txt)  

### Differential expression data

The differential expression data normally comes from an RNA-seq experiment. This file can be created using, for instance, [DESeq2](https://bioconductor.org/packages/release/bioc/html/DESeq2.html). In the differential expression file, the 1st column (named as `resid`) should contain **gene name** (the HGNC symbol), the second column should be named as `log2FoldChange` which is **log2 FoldChange score** of gene, and the third column should be named as `padj`, which is the adjusted **p-value** of the differential gene expression test. 

This is an example of a differential expression input file:

```
resid	log2FoldChange	padj
ANPEP	7.44242618323665	0
CD24	-8.44520139575174	0
COL1A2	8.265875689393	0
COL6A1	7.41947749996406	0
COL6A2	9.62485194293185	0
COL6A3	11.0553152937569	0
DAB2	7.46610079411987	0
DMKN	-11.6435948368453	0
```
!!! warning
    The `log2FoldChange` should be a **positive number** if this gene is up regulated, and **negative number** if this gene is down regulated.

!!! note 
    You can find our example differential expression input file here:  

    * [FB2KRT_degenes.csv](https://github.com/vanheeringen-lab/ANANSE/blob/master/test/data/FB2KRT_degenes.csv)  

[^1]: van Heeringen, S.J., and Veenstra, G.J.C. (2010). GimmeMotifs: a de novo motif prediction pipeline for ChIP-sequencing experiments. Bioinformatics 27, 270-271.
[^2]: Kent, J., ENCODE DCC. (2014). kentUtils: Jim Kent command line bioinformatic utilities. Available from: https://github.com/ENCODE-DCC/kentUtils.
