"""toil_hla pipeline."""

from toil.common import Toil

from toil_hla import jobs
from toil_hla import options
from toil_hla import constants


def run_toil(toil_options):
    """
    Toil implementation for toil_hla.

    Arguments:
        toil_options (NameSpace): an argparse name space with toil options.
    """
    print(toil_options.reference)

    start = jobs.StartJob(options=toil_options)

    if toil_options.lilac_img:
        if toil_options.normal_dna and toil_options.normal_dna_id:
            normal_dna = toil_options.normal_dna
            normal_dna_id = toil_options.normal_dna_id
            normal_dna_lilac_job = jobs.LilacJob(
                options=toil_options,
                bamfile=normal_dna,
                sample_id=normal_dna_id,
            )
            start.addChild(normal_dna_lilac_job)
        if toil_options.tumor_dna and toil_options.tumor_dna_id:
            tumor_dna = toil_options.tumor_dna
            tumor_dna_id = toil_options.tumor_dna_id
            tumor_dna_lilac_job = jobs.LilacJob(
                options=toil_options,
                bamfile=tumor_dna,
                sample_id=tumor_dna_id,
            )
            start.addChild(tumor_dna_lilac_job)

    if toil_options.hlascan_tool:
        if toil_options.normal_dna and toil_options.normal_dna_id:
            normal_dna = toil_options.normal_dna
            normal_dna_id = toil_options.normal_dna_id
            for gene in constants.HLA_GENES:
                normal_dna_hlascan_job = jobs.HLAscanJob(
                    options=toil_options,
                    bamfile=normal_dna,
                    sample_id=normal_dna_id,
                    gene=gene,
                )
                start.addChild(normal_dna_hlascan_job)
        if toil_options.tumor_dna and toil_options.tumor_dna_id:
            tumor_dna = toil_options.tumor_dna
            tumor_dna_id = toil_options.tumor_dna_id
            for gene in constants.HLA_GENES:
                tumor_dna_hlascan_job = jobs.HLAscanJob(
                    options=toil_options,
                    bamfile=tumor_dna,
                    sample_id=tumor_dna_id,
                    gene=gene,
                )
                start.addChild(tumor_dna_hlascan_job)

    if toil_options.arcashla_img:
        if toil_options.tumor_rna and toil_options.tumor_rna_id:
            tumor_rna = toil_options.tumor_rna
            tumor_rna_id = toil_options.tumor_rna_id
            tumor_rna_arcashla_extract = jobs.ArcasHLAExtract(
                options=toil_options,
                bamfile=tumor_rna,
                sample_id=tumor_rna_id,
            )
            tumor_rna_arcashla_genotype = jobs.ArcasHLAGenotype(
                options=toil_options,
                bamfile=tumor_rna,
                sample_id=tumor_rna_id,
            )
            tumor_rna_arcashla_extract.addChild(tumor_rna_arcashla_genotype)
            if toil_options.seq2hla_img:
                tumor_rna_seq2hla_job = jobs.Seq2HLAJob(
                    options=toil_options,
                    bamfile=tumor_rna,
                    sample_id=tumor_rna_id,
                )
                tumor_rna_arcashla_extract.addChild(tumor_rna_seq2hla_job)
            start.addChild(tumor_rna_arcashla_extract)

    # execute the pipeline
    with Toil(toil_options) as pipe:
        if not pipe.options.restart:
            pipe.start(start)
        else:
            pipe.restart()


def main():
    """Parse options and run toil."""
    args = options.get_parser().parse_args()
    args = options.process_parsed_options(options=args)
    run_toil(toil_options=args)
