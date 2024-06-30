import io
import os
import tempfile

from snps import SNPs


class Converter:
    def __init__(self) -> None:
        pass

    def convert(self, input: io.TextIOWrapper, output: io.TextIOWrapper) -> None:
        """Convert input to Build 38 VCF output."""
        s = SNPs(bytes(input.read(), encoding="utf-8"))

        if not s.valid:
            return

        # ensure SNPs are mapped relative to Build 38
        if s.build == 36:
            s.remap(37)

        if s.build == 37:
            s.remap(38)

        # create temp file
        fd, tmp_path = tempfile.mkstemp()
        os.close(fd)

        # write VCF to temp file
        s.to_vcf(tmp_path, chrom_prefix="chr")

        # output temp file
        with open(tmp_path, "r") as f:
            output.write(f.read())

        os.remove(tmp_path)
