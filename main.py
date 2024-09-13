import pysam
import sys
import argparse
import os
import gzip
import cyvcf2
import pprint

# Parse command-line arguments to get the folder path

class Pathing(object):
    def __init__(self, folder):
        self.folder = folder
        self.in_folder = os.path.join(folder, 'input')
        self.out_folder = os.path.join(folder, 'output')
        self.store = {}
        self.cvcf = None
        self.pvcf = None
        self.tvcf = None
        
    def vcf_store(self, vcf_list):
        for vcf_name in vcf_list:
            self.store[vcf_name[0]] = os.path.join(self.in_folder, vcf_name[1])

    
    def pysam_vcf(self, vcf_name):
        self.pvcf = vcf_name
        
        
    def cyvcf_vcf(self, vcf_name):
        self.cvcf = vcf_name
        
    def set_tbi(self, vcf_name):
        self.tvcf = vcf_name


def create_io(folder):
    try:
        os.mkdir(os.path.join(folder, 'input'))
        os.mkdir(os.path.join(folder, 'output'))
    except FileExistsError as e:
            print("IO folders already exist\n")
    except Exception as e:
            print(f"Error creating IO folders, is the folder a valid one?\nException {e}")
            sys.exit(1)
        
    
def folder_inspect(folder):
    vcf_files = []
    
    if os.path.isdir(folder):
        print("\nCreating IO folders...\n")
        create_io(folder)
        
    print("Checking for vcf files...\n")
  
    # Iterate through all files in the folder
    print(f"Current files in {cpath.in_folder}:\n")
    for filename in os.listdir(cpath.in_folder):
        print(filename)
        
    index = 0
    for filename in os.listdir(cpath.in_folder):
        index += 1
        if filename.endswith('.vcf'):
            vcf_files.append((index, filename))
        elif filename.endswith('.vcf.gz'):
            if os.path.exists(os.path.join(cpath.in_folder, os.path.splitext(filename)[0])): print(f"\nUncompressed {filename} already exists\n"); continue
            print("\nIt's recommended to use a uncompressed vcf file.")
            gz_ask = input("Want to decompress the vcf file? ")
            if gz_ask.lower() in ['yes', 'y']:
                with gzip.open(os.path.join(cpath.in_folder, filename), 'rb') as f_in:
                    with open(os.path.join(cpath.in_folder, filename[:-3]), 'wb') as f_out:
                        f_out.write(f_in.read())
                vcf_files.append((index, filename[:-3]))
                print(f"\n{filename[:-3]} created successfully.")
            else:
                vcf_files.append((index, filename))
    
    print('Valid vcf files found:\n')
    cpath.vcf_store(vcf_files)
    for vcf in vcf_files:
        print(f"{vcf[0]} - {vcf[1]}")
    print("\n--------------------------------\n--------------------------------\n")

def inspect_vcf():
    print("Available vcf files for query:\n")
    vcf_files = cpath.store
    for key, value in vcf_files.items():
        print(f"{key} - {value}")
        
    choice = input('\nChoose the vcf of choice: ')

    if choice.isdigit() and int(choice) in list(vcf_files.keys()):
        print(f"\nSelected vcf: {vcf_files[int(choice)]}\n")
        pvcf = pysam.VariantFile(vcf_files[int(choice)], mode='rb')
        cvcf = cyvcf2.VCF(vcf_files[int(choice)])
        if os.path.exists(vcf_files[int(choice)].replace('.vcf', '.vcf.tbi')):
            tvcf = pysam.TabixFile(vcf_files[int(choice)])
            cpath.set_tbi(tvcf)
            print("\n...Tabix File Loaded...\n")
            
        cpath.pysam_vcf(pvcf)
        cpath.cyvcf_vcf(cvcf)
    else:
        print("Invalid choice, please try again (Try using the index numbers!).\n")
        inspect_vcf()

def vcf_looker():
    vcf_opts = {1: "See Header",
                2: "See VCF head (first 10 lines)",
                3: "Query VCF options",
                4: "Choose other VCF",
                5: "Exit"}
    
    print("Available options:\n")
    for key, value in vcf_opts.items():
        print(f"{key} - {value}")
    
    choice = input('\nChoose the desired option: ')
    
    if choice.isdigit() and int(choice) in list(vcf_opts.keys()):
        print(f"\nSelected option: {vcf_opts[int(choice)]}\n")
        match int(choice):
            case 1:
                print(cpath.pvcf.header)
            case 2:
                vcf_head()
            case 3:
                query_vcf_options()
            case 4:
                inspect_vcf()
            case 5:
                sys.exit(0)
    else:
        print("Invalid choice, please try again (Try using the index numbers!).\n")
        vcf_looker()
    vcf_looker()

def query_vcf_options():
    vcf_query_opt = {1: "Query By Position (i.e: 'chr:posStart-posEnd)",
                     2: "Filter By Allele Frequency",
                     3: "Query By ID (dbSnp)",
                     4: "Choose other VCF",
                     5: "Return",
                     6: "Exit"}
    
    for key, value in vcf_query_opt.items():
        print(f"{key} - {value}")
        
    choice = input('\nChoose the desired option: ')
    if choice.isdigit() and int(choice) in list(vcf_query_opt.keys()):
        print(f"\nSelected option: {vcf_query_opt[int(choice)]}\n")
        match int(choice):
            case 1:
                query_vcf(1)
            case 2:
                query_vcf(2)
            case 3:
                query_vcf(3)
            case 4:
                inspect_vcf()
            case 5:
                vcf_looker()
            case 6:
                sys.exit(0)
    else:
        print("Invalid choice, please try again (Try using the index numbers!).\n")
        vcf_looker()
        
def query_vcf(opt):
    cvcf = cpath.cvcf
    pvcf = cpath.pvcf
    #tvcf = cpath.tvcf
    #cvcf.set_index(tvcf)

    cvcf.add_format_to_header({'ID': 'MLPSAC', 'Description': 'unk', 'Type':'Character', 'Number': '1'})
    cvcf.add_format_to_header({'ID': 'MLPSAF', 'Description': 'unk', 'Type':'Character', 'Number': '1'})
    
    try:
        if opt == 1:
            position = input("Enter the position (chr:posStart-posEnd | '1:324822-911595'): ")
            pos_string = position.replace('-', ':').split(':')
            for record in cvcf:
                if record.CHROM == pos_string[0] and int(record.start) >= int(pos_string[1]) and int(record.start) <= int(pos_string[2]):
                    format_record(record)
        elif opt == 2:
            value = input("Enter the af value: ")
            limit = 0
            for record in cvcf:
                if type(record.INFO['AF'] == tuple):
                    limit += 1
                    format_record(record)
                elif float(record.INFO['AF']) >= float(value):
                    limit += 1
                    format_record(record)
                if limit == 100:
                    print('\nLimited at 100 variants for query.')
                    break
        elif opt == 3:
            id = input("Enter the dbSnp ID: ")
            for record in cvcf:
                if record.ID == id:
                    format_record(record)
        else:
            print("Invalid option, please try again.\n")
            query_vcf_options()
    except:
        raise
    vcf_looker()

def format_record(record):
    print("")
    pos_dict = {'01 - CHROM': record.CHROM, '02 - POS':record.POS,'03 - ID':record.ID, '04 - REF':record.REF, '05 - ALT':record.ALT}
    rec_dict = {'06 - QUAL':record.QUAL, '07 - FILTER':record.FILTER, '08 - AC':record.INFO.get('AC'), '09 - AF':record.INFO.get('AF'),
                '10 - AN':record.INFO.get('AN'), '11 - DB':record.INFO.get('DB'), '12 - DP':record.INFO.get('DP'), '13 - Dels':record.INFO.get('Dels'),
                '14 - FS':record.INFO.get('FS'), '15 - GC':record.INFO.get('GC'), '16 - Run':record.INFO.get('HRun'), '17 - HaplotypeScore': record.INFO.get('HaplotypeScore'),
                '18 - MLEAC':record.INFO.get('MLEAC'), '19 - MLEAF':record.INFO.get('MLEAF'), '20 - MQ':record.INFO.get('MQ'), '21 - MQ0':record.INFO.get('MQ0'),
                '22 - QD':record.INFO.get('QD')}
    
    csq = record.INFO.get('CSQ').split('|')
    csq_keys = ['23 - Allele', '24 - Consequence', '25 - IMPACT', '26 - SYMBOL',
                '27 - Gene', '28 - Feature_type', '29 - Feature', '30 - BIOTYPE',
                '31 - EXON', '32 - INTRON', '33 - HGVSc', '34 - HGVSp', '35 - cDNA_position',
                '36 - CDS_position', '37 - Protein_position', '38 - Amino_acids',
                '39 - Codons', '40 - Existing_variation', '41 - DISTANCE', '42 - STRAND',
                '43 - FLAGS', '44 - SYMBOL_SOURCE', '45 - HGNC_ID', '46 - HGVS_OFFSET',
                '47 - AF', '48 - AFR_AF', '49 - AMR_AF', '50 - EAS_AF', '51 - EUR_AF',
                '51 - SAS_AF', '52 - MAX_AF', '53 - MAX_AF_POPS', '54 - CLIN_SIG',
                '55 - SOMATIC', '56 - PHENO']
    
    if len(csq) == len(csq_keys):
        csq_dict = {csq_keys[enum]: value for enum, value in enumerate(csq)}
    else:
        csq_dict = {csq_keys[enum]: value for enum, value in enumerate(csq[0:len(csq_keys)])}
    
    pprint.pprint(pos_dict)
    pprint.pprint(rec_dict)
    pprint.pprint(csq_dict)
    print("\n----")
    #print(csq_dict)

def fix_list(list):
    return [x for x in list if x!= '']

def vcf_head():
    print(f"\nFirst 10 variants of {cpath.pvcf.filename}:\n")
    vcount = 0
    for record in cpath.cvcf:
        vcount +=1
        print(record)
        if vcount == 10:
            break
    print("\n--------------------------------\n--------------------------------\n")
    vcf_looker()
    
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--folder', '-f', type=str, default=os.getcwd(), required=False)

    args = ap.parse_args()

    cpath = Pathing(folder=args.folder)
    print(f"Current working folder setted as {cpath.folder}")
    
    folder_inspect(cpath.folder)
    inspect_vcf()
    vcf_looker()