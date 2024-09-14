rule all:
    input:
        "input/NIST.vcf",
        "output/NIST-ANNOT.vcf",
        "output/NIST-ANNOT.vcf.gz.tbi"
    shell:
        """
        echo "All rules executed successfully!"
        """

rule prepare_conda:
    shell:
        """
        conda create -n envvcf -c bioconda --file $HOME/vcf-pipe/requirements.txt
        """

rule install_reqs:
    shell:
        """
        apt-get install bcftools
        apt-get install samtools
        apt-get install tabix
        """

rule prepare_folders:
    shell:
        '''
        mkdir $HOME/vcf-pipe
        mkdir $HOME/vcf-pipe/input
        mkdir $HOME/vcf-pipe/output

        sudo chmod -R a+rwx $HOME/vcf-pipe
        cd $HOME/vcf-pipe
        '''

rule prepare_vcf:
    input:
        vcf_file = "input/{vcf}.vcf.gz"
    output:
        "input/{vcf}.vcf"
    shell:
        '''
        gzip -d $HOME/vcf-pipe/{input.vcf_file}
        '''

rule docker_vep:
    input:
        vcf_file = "input/{vcf}.vcf"
    output:
        "output/{vcf}-ANNOT.vcf"
    shell:
        '''
        sudo docker run -t -i -v $HOME/vep_data:/data ensemblorg/ensembl-vep
        cd vcf-pipe/
        vep -i {input.vcf_file} --cache --force_overwrite --hgvs --symbol --af --max_af --af_1kg -o {output} --vcf --stats_html --stats_text --fields "Allele,Consequence,IMPACT,SYMBOL,Gene,Feature_type,Feature,BIOTYPE,EXON,INTRON,HGVSc,HGVSp,cDNA_position,CDS_position,Protein_position,Amino_acids,Codons,Existing_variation,DISTANCE,STRAND,FLAGS,SYMBOL_SOURCE,HGNC_ID,HGVS_OFFSET,AF,AFR_AF,AMR_AF,EAS_AF,EUR_AF,SAS_AF,MAX_AF,MAX_AF_POPS,CLIN_SIG,SOMATIC,PHENO" --verbose
        '''

rule bgzipfy:
    input:
       "output/{vcf}-ANNOT.vcf"
    output:
        o1 = "output/{vcf}-ANNOT.vcf.gz",
        o2 = "output/{vcf}-ANNOT.vcf.gz.tbi"
    shell:
        '''
        bgzip -c {input} > {output}
        bcftools index -t {output}
        '''

rule execute_main:
    shell:
        '''
        cd $HOME/vcf-pipe
        python main.py
        '''
