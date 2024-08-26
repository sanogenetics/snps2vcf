import gzip
import os
import tempfile
from io import BytesIO
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from snps.resources import ReferenceSequence
from snps.utils import gzip_file

from snps2vcf import Converter


class TestSnps(TestCase):
    def run_converter_test(self, build, compress_input=False, use_filesystem=False):
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
                        with patch("snps.SNPs.compute_cluster_overlap") as mock_compute:
                            with patch(
                                "snps.SNPs.identify_low_quality_snps"
                            ) as mock_identify:
                                if use_filesystem:
                                    # Write input to a temporary file
                                    input_file = (
                                        Path(tmpdir) / "input.csv.gz"
                                        if compress_input
                                        else Path(tmpdir) / "input.csv"
                                    )
                                    with input_file.open("wb") as infile:
                                        infile.write(in_data.getvalue())

                                    # Define output file
                                    output_file = Path(tmpdir) / "output.vcf"

                                    # Run converter with file paths
                                    Converter().convert(
                                        input_file.open("rb"), output_file.open("wb")
                                    )

                                    # Read and compare output from file
                                    with output_file.open("rb") as outfile:
                                        output = outfile.read()

                                else:
                                    # Run converter with stdin and stdout
                                    Converter().convert(in_data, output)
                                    output = output.getvalue()

                                # Check that the mocked methods were called
                                if build == 37:
                                    mock_compute.assert_called_once()
                                    mock_identify.assert_called_once()
                                else:
                                    mock_compute.assert_not_called()
                                    mock_identify.assert_not_called()

                    # Read expected result
                    with open("tests/output/vcf_generic.vcf", "rb") as f:
                        expected = f.read()

                    self.assertIn(expected, output)

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

    def test_converter_filesystem_build_36(self):
        self.run_converter_test(36, use_filesystem=True)

    def test_converter_filesystem_build_37(self):
        self.run_converter_test(37, use_filesystem=True)

    def test_converter_filesystem_build_38(self):
        self.run_converter_test(38, use_filesystem=True)

    def test_converter_filesystem_build_36_compressed(self):
        self.run_converter_test(36, compress_input=True, use_filesystem=True)

    def test_converter_filesystem_build_37_compressed(self):
        self.run_converter_test(37, compress_input=True, use_filesystem=True)

    def test_converter_filesystem_build_38_compressed(self):
        self.run_converter_test(38, compress_input=True, use_filesystem=True)
