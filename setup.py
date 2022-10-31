from setuptools import setup

setup(
    name="snps2vcf",
    version="1.0.0",
    author="Adam Faulconbridge",
    author_email="adam@sanogenetics.com",
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
