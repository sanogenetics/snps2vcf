import os
import tempfile
from typing import BinaryIO

from snps import SNPs

from . import _version

__version__ = _version.get_versions()["version"]


class Converter:
    def __init__(self) -> None:
        pass

    def convert(self, input: BinaryIO, output: BinaryIO) -> None:
        """Convert input to Build 38 VCF output."""
        s = SNPs(input.read())

        if not s.valid:
            return

        # ensure SNPs are mapped relative to Build 38
        if s.build == 36:
            s.remap(37)

        # attempt to get chip information for Build 36 and 37 files
        if s.build == 37:
            s.compute_cluster_overlap()
            s.identify_low_quality_snps()

        if s.build == 37:
            s.remap(38)

        # create temp file
        fd, tmp_path = tempfile.mkstemp()
        os.close(fd)

        # write VCF to temp file
        if s._cluster_overlap_computed and s._cluster:
            s.to_vcf(
                tmp_path, chrom_prefix="chr", qc_filter=True
            )  # chip cluster exists, so include chip info
        else:
            s.to_vcf(tmp_path, chrom_prefix="chr")

        # output temp file as binary
        with open(tmp_path, "rb") as f:
            output.write(f.read())

        os.remove(tmp_path)
