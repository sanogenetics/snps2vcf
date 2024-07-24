import gzip
import os
import tempfile
from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from snps.resources import ReferenceSequence
from snps.utils import gzip_file

from snps2vcf import Converter


class TestSnps(TestCase):
    def run_converter_test(self, build, compress_input=False):
        with open("tests/input/generic.csv", "rb") as f:
            in_data = f.read()

        if compress_input:
            compressed_data = BytesIO()
            with gzip.GzipFile(fileobj=compressed_data, mode="wb") as gz:
                gz.write(in_data)
            in_data = BytesIO(compressed_data.getvalue())
        else:
            in_data = BytesIO(in_data)

        output = BytesIO()

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
                        Converter().convert(in_data, output)

                    # read expected result
                    with open("tests/output/vcf_generic.vcf", "rb") as f:
                        expected = f.read()

                    output.seek(0)
                    self.assertIn(expected, output.read())

    def test_converter_build_36(self):
        self.run_converter_test(36)

    def test_converter_build_37(self):
        self.run_converter_test(37)

    def test_converter_build_38(self):
        self.run_converter_test(38)

    def test_converter_build_36_compressed(self):
        self.run_converter_test(36, compress_input=True)

    def test_converter_build_37_compressed(self):
        self.run_converter_test(37, compress_input=True)

    def test_converter_build_38_compressed(self):
        self.run_converter_test(38, compress_input=True)

    def test_converter_empty(self):
        input_empty = BytesIO()
        output_empty = BytesIO()

        Converter().convert(input_empty, output_empty)

        self.assertEqual(b"", output_empty.read())
