import os
import tempfile
from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from snps.resources import ReferenceSequence
from snps.utils import gzip_file

from snps2vcf import Converter


class TestSnps(TestCase):
    def run_converter_test(self, build):
        with open("tests/input/generic.csv", "r") as f:
            input = StringIO(f.read())

        output = StringIO()

        with tempfile.TemporaryDirectory() as tmpdir:
            dest = os.path.join(tmpdir, "generic.fa.gz")
            gzip_file("tests/input/generic.fa", dest)
            seq = ReferenceSequence(ID="1", assembly="GRCh38", path=dest)

            mock1 = Mock(return_value={"1": seq})
            mock2 = PropertyMock(return_value=build)
            mock3 = Mock(return_value=(["1"], []))
            with patch("snps.resources.Resources.get_reference_sequences", mock1):
                with patch("snps.SNPs.build", mock2):
                    with patch("snps.SNPs.remap", mock3):
                        Converter().convert(input, output)

                    # read expected result
                    with open("tests/output/vcf_generic.vcf", "r") as f:
                        expected = f.read()

                    output.seek(0)
                    self.assertIn(expected, output.read())

    def test_converter_build_36(self):
        self.run_converter_test(36)

    def test_converter_build_37(self):
        self.run_converter_test(37)

    def test_converter_build_38(self):
        self.run_converter_test(38)

    def test_converter_empty(self):
        input = StringIO()
        output = StringIO()

        Converter().convert(input, output)

        self.assertEqual("", output.read())
