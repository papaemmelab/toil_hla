"""toil_hla validators."""

from glob import glob
import os

import click
import pandas as pd

from toil_hla import exceptions
from toil_hla import constants


def validate_patterns_are_files(patterns, check_size=True):
    """
    Check that a list of `patterns` are valid files.

    Arguments:
        patterns (list): a list of patterns to be check.
        check_size (bool): check size is not zero for all files matched.

    Returns:
        bool: True if all patterns match existing files.
    """
    for pattern in patterns:
        files = list(glob(pattern))

        if not files:
            msg = f"{pattern} pattern matched no files."
            raise exceptions.ValidationError(msg)

        for i in files:
            if not os.path.isfile(i):
                msg = f"{i} is not a file."
                raise exceptions.ValidationError(msg)

            if check_size and not os.path.getsize(i) > 0:
                msg = f"{i} is an empty file."
                raise exceptions.ValidationError(msg)

    return True


def validate_patterns_are_dirs(patterns):
    """
    Check that a list of `patterns` are valid dirs.

    Arguments:
        patterns (list): a list of directory patterns.

    Returns:
        bool: True if all patterns match existing directories.
    """
    for pattern in patterns:
        dirs = list(glob(pattern))

        if not dirs:
            msg = f"{pattern} pattern matched no dirs."
            raise exceptions.ValidationError(msg)

        for i in dirs:
            if not os.path.isdir(i):
                msg = f"{i} is not a directory."
                raise exceptions.ValidationError(msg)

    return True


def validate_bam(value):
    """Make sure the passed bam has an index file."""
    value = os.path.abspath(value)
    index = str(value) + ".bai"

    if not os.path.isfile(value):
        raise click.UsageError(value + " should exist.")

    if not os.path.isfile(index):
        raise click.UsageError(index + " should exist.")

    return value


def validate_reference(value):
    """Make sure the passed fasta has an index file."""
    value = os.path.abspath(value)
    index = str(value) + ".fai"

    if not os.path.isfile(index):
        raise click.UsageError(index + " should exist.")

    return value


def validate_picard_path(picard_path):
    """Make sure picard path has necessary file inputs."""
    picard_preadapter_file = glob(f"{picard_path}/*pre_adapter_detail_metrics")
    picard_baitbias_file = glob(f"{picard_path}/*bait_bias_detail_metrics")

    if not picard_preadapter_file or not picard_baitbias_file:
        msg = "Missing pre adapter or bait bias picard metrics."
        raise exceptions.ValidationError(msg)

    if len(picard_preadapter_file) == 1:
        picard_preadaptor = pd.read_csv(picard_preadapter_file[0], sep="\t", skiprows=6)
        for header in constants.PICARD_CONTEXT_COLS + constants.PICARD_PRE_ADAPTER_COLS:
            if header not in picard_preadaptor.keys():
                msg = f"No {header} column in pre adapter file."
                raise exceptions.ValidationError(msg)
    else:
        msg = "More than one pre adapter file, please merge."
        raise exceptions.ValidationError(msg)

    if len(picard_baitbias_file) == 1:
        picard_baitbias = pd.read_csv(picard_baitbias_file[0], sep="\t", skiprows=6)
        for header in constants.PICARD_CONTEXT_COLS + constants.PICARD_BAIT_BIAS_COLS:
            if header not in picard_baitbias.keys():
                msg = f"No {header} column in bait bias file."
                raise exceptions.ValidationError(msg)
    else:
        msg = "More than one bait bias file, please merge."
        raise exceptions.ValidationError(msg)

    return True


def validate_classification_mode(value):
    """Make sure the passed fasta has an index file."""
    if not value in ["rf", "cnn", "mix"]:
        raise click.UsageError(
            "Classification mode doesn't exist. Please use rf, cnn or mix."
        )

    return value
