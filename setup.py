from setuptools import setup

import versioneer

setup(
    name="snps2vcf",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Adam Faulconbridge, Andrew Riha",
    author_email="adam@sanogenetics.com, andrew@sanogenetics.com",
    packages=["snps2vcf"],
    description="Converter to turn D2C genetics files into a VCF file using the snps package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sanogenetics/snps2vcf",
    install_requires=open("requirements.txt").readlines(),
    extras_require={
        "dev": open("requirements-dev.txt").readlines(),
    },
)
