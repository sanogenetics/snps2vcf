from io import StringIO

from snps2vcf import Converter


class TestSnps:
    def test_converter(self):
        input = StringIO()
        # TODO create input

        output = StringIO()

        Converter().convert(input, output)

        # TODO check output is valid VCF
        # TODO check output is expected VCF
