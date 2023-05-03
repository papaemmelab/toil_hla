# Toil HLA

A toil wrapper that runs several HLA typing tools for Class I and Class II.

## Tools

| Tool Name        | Repository                                                             |
| ---------------- | ---------------------------------------------------------------------- | 
| Lilac            | https://github.com/hartwigmedical/hmftools/blob/master/lilac/README.md | 
| HLAscan          | https://github.com/SyntekabioTools/HLAscan                             | 
| arcasHLA         | https://github.com/RabadanLab/arcasHLA                                 | 
| seq2HLA          | https://github.com/TRON-Bioinformatics/seq2HLA                         |

## Installing

After cloning the repo, create a virtual environment and run:

        # install package
        cd /path/to/repo && pip install .

## Usage

The main command for this package is:

        toil_hla [TOIL-OPTIONS] [PIPELINE-OPTIONS]

This can be executed sequentially as follows:

1. Single machine mode

        toil_hla {OUTDIR}/jobstore \
            --stats \
            --disableCaching \
            --disableChaining \
            --rotatingLogging \
            --writeLogs {OUTDIR}/logs_toil \
            --logFile {OUTDIR}/head_job.toil \
            --statePollingWait 30 \
            --maxLocalJobs 500 \
            --outdir {OUTDIR} \
            --reference /path/to/reference/gr37.fasta \
            --normal-dna tests/data/test_DNA.bam \
            --normal-dna-id test_DNA \
            --tumor-rna /work/isabl/home/domenicd/tests/hla/test_files/test_RNA.bam \
            --tumor-rna-id test_RNA \
            --lilac-resource-dir /path/to/lilac/reference/immune \
            --lilac-img /path/to/lilac/run/script \
            --hlascan-tool /path/to/hlascan/hla_scan_r_v2.1.4 \
            --hlascan-resource-dir /path/to/hlascan/db/HLA-ALL.IMGT \
            --arcashla-img /path/to/arcasHLA/run/script \
            --seq2hla-img /path/to/seq2hla/run/script

2. To run in parallel on a high performance computing cluster add:

            --batchSystem custom_lsf

The Docker images used for testing can be pulled from here:

https://hub.docker.com/repository/docker/ddomenico/hmftools
https://hub.docker.com/repository/docker/ddomenico/arcashla
https://hub.docker.com/repository/docker/ddomenico/seq2hla

*NOTE:* Testing was done with singularity which can pull images from Dockerhub and build as *.sif or *.simg

The format of the /path/to/{TOOL}/run/script should look like one of these two implementations:

1. Singularity

        #!/bin/bash
        singularity exec --workdir {WORKDIR} --bind /local/system:/local/system hmftools.sif "$@"

2. Docker

        #!/bin/bash
        docker run -v /local/system:/local/system hmftools "$@"

The HLAscan tool and DB can be downloaded directly following the instructions [here](https://github.com/SyntekabioTools/HLAscan).

## Testing

Test files have been provided in tests/data and corresponding tool outputs have been provided in tests/output. Test files were sources from [GIAB](https://github.com/genome-in-a-bottle/giab_data_indexes/tree/master) for the test_DNA.bam and from [arcasHLA](https://github.com/RabadanLab/arcasHLA) for the test_RNA.bam. For the DNA, HG002 was downloaded and the BAM was then subset to the HLA A, B and C loci in order to generate a small file for test purposes. Here is the commands to generate:

        #!/bin/bash
        # Usage: ./subset_hla_regions.sh input_bam output_bam

        input_bam=$1
        output_bam=$2

        hla_regions="6:29910247-29944143 6:31321638-31349750 6:31236525-31283265"
        samtools view -b -o "${output_bam}" "${input_bam}" ${hla_regions}

## Credits

This package was created using [Cookiecutter] and the [papaemmelab/cookiecutter-toil] project template.
