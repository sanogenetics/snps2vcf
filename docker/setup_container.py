from snps.resources import Resources

r = Resources()

r.get_assembly_mapping_data("NCBI36", "GRCh37")
r.get_assembly_mapping_data("GRCh37", "GRCh38")
r.get_reference_sequences(assembly="GRCh38")
