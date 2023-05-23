"""toil_hla options."""

import subprocess

# from pysam import AlignmentFile
from toil_container import ContainerArgumentParser
import click

from toil_hla import __version__
from toil_hla import validators


def get_parser():
    """Get pipeline configuration using toil's argparse."""
    parser = ContainerArgumentParser(version=__version__)
    parser.description = "Run toil_hla pipeline."

    # we need to add a group of arguments specific to the pipeline
    settings = parser.add_argument_group("Pipeline configuration")

    settings.add_argument(
        "--outdir",
        help="Path to output directory.",
        required=True,
        type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    )

    settings.add_argument(
        "--reference",
        help="Path to reference genome. Juno users see: "
        "/juno/work/isabl/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta.",
        required=True,
        type=validators.validate_reference,
    )

    settings.add_argument(
        "--normal-dna",
        help="Path to normal DNA bam file.",
        required=False,
        type=validators.validate_bam,
    )

    settings.add_argument(
        "--normal-dna-id",
        help="Normal DNA ID.",
        required=False,
        type=str,
    )

    settings.add_argument(
        "--tumor-dna",
        help="Path to tumor DNA bam file.",
        required=False,
        type=validators.validate_bam,
    )

    settings.add_argument(
        "--tumor-dna-id",
        help="Tumor DNA ID.",
        required=False,
        type=str,
    )

    settings.add_argument(
        "--tumor-rna",
        help="Path to tumor RNA bam file.",
        required=False,
        type=validators.validate_bam,
    )

    settings.add_argument(
        "--tumor-rna-id",
        help="Tumor RNA ID.",
        required=False,
        type=str,
    )

    # Lilac args
    settings.add_argument(
        "--lilac-img",
        help="Lilac image.",
        required=False,
    )

    settings.add_argument(
        "--lilac-resource-dir",
        help="Path to Lilac resource directory.",
        required=False,
        type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    )

    # HLAscan args
    settings.add_argument(
        "--hlascan-tool",
        help="HLAscan binary.",
        required=False,
    )

    settings.add_argument(
        "--hlascan-resource-dir",
        help="Path to HLAscan resource directory.",
        required=False,
        type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    )

    # arcasHLA args
    settings.add_argument(
        "--arcashla-img",
        help="arcasHLA image.",
        required=False,
    )

    # seq2hla args
    settings.add_argument(
        "--seq2hla-img",
        help="seq2hla image.",
        required=False,
    )

    return parser


def process_parsed_options(options):
    """Perform validations and add post parsing attributes to `options`."""
    if options.writeLogs is not None:
        subprocess.check_call(["mkdir", "-p", options.writeLogs])
    return options
