Aplicação simples para treino e demonstração.

Capaz de identificar arquivos vcfs (seja em .gz ou não) e processar algumas coisas como filtro por Frequência Alélica, pesquisa por regiões ou dbSnpespecífico. As linhas de output são customizadas para facilitar a leitura.

O aplicativo espera que um vcf anotado pelo Variant Effect Predictor (Ensembl) seja utilizado, mas é capaz de lidar com arquivos vcf sem anotação.

O VCF anotado foi criado pela seguinte linha de comando:

[vep -i input/NIST.vcf --cache --force_overwrite --hgvs --symbol --af --max_af --af_1kg -o output/ANNOT-NIST.vcf --vcf --stats_html --stats_text --fields "Allele,Consequence,IMPACT,SYMBOL,Gene,Feature_type,Feature,BIOTYPE,EXON,INTRON,HGVSc,HGVSp,cDNA_position,CDS_position,Protein_position,Amino_acids,Codons,Existing_variation,DISTANCE,STRAND,FLAGS,SYMBOL_SOURCE,HGNC_ID,HGVS_OFFSET,AF,AFR_AF,AMR_AF,EAS_AF,EUR_AF,SAS_AF,MAX_AF,MAX_AF_POPS,CLIN_SIG,SOMATIC,PHENO" --verbose]

---

O código foi escrito em Python 3.12.5, adquirido via distribuição Anaconda, utilizando VSCode 1.93.0.

---

Comandos executados e desenhados para Ubuntu conforme versão abaixo.

Distributor ID: Ubuntu
Description:    Ubuntu 22.04.3 LTS
Release:        22.04
Codename:       jammy

---

O Variant Effect Predictor utilizado foi o disponibilizado pelo Ensembl via DockerHub (https://hub.docker.com/r/ensemblorg/ensembl-vep/). Usando o GRCh38.

---

Sem mais, espero que gostem, independente de qualquer coisa, foi divertido fazer!

Jullian G. Damasceno.