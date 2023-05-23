"""toil_hla jobs."""
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import isdir
import os
import subprocess

from toil_container import ContainerJob

# data directory with required executables
DATADIR = abspath(join(dirname(__file__), "data"))


class StartJob(ContainerJob):
    def __init__(self, options, memory="5G", runtime=90, **kwargs):
        """All steps are short low memory jobs unless otherwise specified."""
        super().__init__(
            memory=memory,
            options=options,
            cores=kwargs.pop("cores", 1),
            runtime=runtime,
            **kwargs,
        )


class LilacJob(ContainerJob):
    def __init__(self, options, bamfile, sample_id, **kwargs):
        """
        Run lilac on a BAM file.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            options (object): toil_hla options structure.
            bamfile (str): path to BAM file.
            sample_id (str): sample ID.
        """
        self.bamfile = bamfile
        self.sample_id = sample_id

        self.lilac_dir = join(options.outdir, "lilac")
        if not isdir(self.lilac_dir):
            os.makedirs(self.lilac_dir)

        self.lilac_img = options.lilac_img
        self.lilac_resource_dir = options.lilac_resource_dir

        super().__init__(
            memory="20G",
            options=options,
            cores=kwargs.pop("cores", 1),
            runtime=kwargs.pop("runtime", 90),
            **kwargs,
        )

    def run(self, fileStore):
        """Run the job."""
        outdir = join(self.lilac_dir, self.sample_id)
        if not isdir(outdir):
            os.makedirs(outdir)
        cmd = [
            self.lilac_img,
            "lilac",
            "-sample",
            self.sample_id,
            "-ref_genome",
            self.options.reference,
            "-resource_dir",
            self.options.lilac_resource_dir,
            "-reference_bam",
            self.bamfile,
            "-output_dir",
            outdir,
        ]

        self.call(cmd, cwd=outdir)


class HLAscanJob(ContainerJob):
    def __init__(self, options, bamfile, sample_id, gene, **kwargs):
        """
        Run hlascan on a BAM file.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            index (int): split job index.
            options (object): toil_hla options structure.
            bamfile (str): path to BAM file.
            sample_id (str): sample ID.
            gene (str): gene name.
        """
        self.bamfile = bamfile
        self.sample_id = sample_id
        self.gene = gene

        self.hlascan_dir = join(options.outdir, "hlascan")
        if not isdir(self.hlascan_dir):
            os.makedirs(self.hlascan_dir)

        self.hlascan_tool = options.hlascan_tool
        self.hlascan_resource_dir = options.hlascan_resource_dir

        super().__init__(
            memory="20G",
            options=options,
            cores=kwargs.pop("cores", 1),
            runtime=kwargs.pop("runtime", 90),
            **kwargs,
        )

    def run(self, fileStore):
        """Run the job."""
        outdir = join(self.hlascan_dir, self.sample_id)
        if not isdir(outdir):
            os.makedirs(outdir)
        cmd = [
            self.hlascan_tool,
            "-b",
            self.bamfile,
            "-v",
            "37",
            "-g",
            self.gene,
            "-d",
            self.hlascan_resource_dir,
            "||",
            "exit",
            "0",
        ]

        # Open a log file for writing
        with open(join(outdir, f"{self.gene}.txt"), "w", encoding="utf-8") as log_file:
            try:
                subprocess.check_call(cmd, cwd=outdir, stdout=log_file)
            except subprocess.CalledProcessError as _:
                pass


class RNAJob(ContainerJob):
    def __init__(self, options, bamfile, sample_id, **kwargs):
        """
        Run an RNA job.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            options (object): toil_hla options structure.
            bamfile (str): path to BAM file.
            sample_id (str): sample id.
        """
        self.bamfile = bamfile
        self.sample_id = sample_id

        self.arcashla_dir = join(options.outdir, "arcashla")
        if not isdir(self.arcashla_dir):
            os.makedirs(self.arcashla_dir)

        self.seq2hla_dir = join(options.outdir, "seq2hla")
        if not isdir(self.seq2hla_dir):
            os.makedirs(self.seq2hla_dir)

        self.arcashla_img = options.arcashla_img
        self.seq2hla_img = options.seq2hla_img

        super().__init__(
            options=options,
            cores=kwargs.pop("cores", 8),
            runtime=kwargs.pop("runtime", 90),
            memory=kwargs.pop("memory", "20G"),
            **kwargs,
        )


class ArcasHLAExtract(RNAJob):
    def __init__(self, options, bamfile, sample_id, **kwargs):
        """
        Run arcasHLA extract on a BAM file.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            options (object): toil_hla options structure.
            bamfile (str): path to BAM file.
            sample_id (str): sample id.
        """
        super().__init__(
            options=options,
            bamfile=bamfile,
            sample_id=sample_id,
            **kwargs,
        )

    def run(self, fileStore):
        """Run the job."""
        outdir = join(self.arcashla_dir, self.sample_id)
        if not isdir(outdir):
            os.makedirs(outdir)
        cmd = [
            self.arcashla_img,
            "extract",
            self.bamfile,
            "-o",
            outdir,
            "-t",
            "8",
            "-v",
        ]

        self.call(cmd, cwd=self.arcashla_dir)


class ArcasHLAGenotype(RNAJob):
    def __init__(self, options, bamfile, sample_id, **kwargs):
        """
        Run arcasHLA genotype on a BAM file.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            options (object): toil_hla options structure.
            bamfile (str): path to BAM file.
            sample_id (str): sample id.
        """
        super().__init__(
            options=options,
            bamfile=bamfile,
            sample_id=sample_id,
            **kwargs,
        )

    def run(self, fileStore):
        """Run the job."""
        outdir = join(self.arcashla_dir, self.sample_id)
        if not isdir(outdir):
            os.makedirs(outdir)
        fq1 = join(outdir, f"{self.sample_id}.extracted.1.fq.gz")
        fq2 = join(outdir, f"{self.sample_id}.extracted.2.fq.gz")
        cmd = [
            self.arcashla_img,
            "genotype",
            fq1,
            fq2,
            "-g",
            "A,B,C,DPB1,DQB1,DQA1,DRB1",
            "-o",
            outdir,
            "-t",
            "8",
            "-v",
        ]

        self.call(cmd, cwd=outdir)


class Seq2HLAJob(RNAJob):
    def __init__(self, options, bamfile, sample_id, **kwargs):
        """
        Run seq2HLA on a BAM file.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            options (object): toil_hla options structure.
            bamfile (str): path to BAM file.
            sample_id (str): sample id.
        """
        super().__init__(
            options=options,
            bamfile=bamfile,
            sample_id=sample_id,
            **kwargs,
        )

    def run(self, fileStore):
        """Run the job."""
        outdir = join(self.seq2hla_dir, self.sample_id)
        if not isdir(outdir):
            os.makedirs(outdir)
        fq1 = join(
            self.arcashla_dir, self.sample_id, f"{self.sample_id}.extracted.1.fq.gz"
        )
        fq2 = join(
            self.arcashla_dir, self.sample_id, f"{self.sample_id}.extracted.2.fq.gz"
        )
        cmd = [
            self.seq2hla_img,
            "-1",
            fq1,
            "-2",
            fq2,
            "-r",
            self.sample_id,
        ]

        self.call(cmd, cwd=outdir)
