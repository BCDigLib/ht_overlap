# conducts analysis of Alma records against HathiFiles, creating output that lists some bibliographic as well as
# physical item data like location, barcode, and volume information for books we hold that are not currently in
# HathiTrust to inform selection for digitization.
# usage: ht_overlap_analysis.py hathifile.txt bib_export.mrc phys_item_export.txt
# where hathifile.txt is a full, recent, unzipped text file from hathitrust.org/hathifiles and bib_export.mrc and
# phys_item_export.txt are the results of running an export bibliographic records job and an export physical items
# job on the same set in Alma, once the physical items export .csv has been resaved as a tab-delimited .txt

from pymarc import MARCReader
import sys

def main():
    # read in Hathifile and create a dictionary of OCLC numbers (lines 14-25 final but commented out for testing)
    oclc = dict()
    hathi = open(sys.argv[1], 'r')
    ht_in = hathi.read()
    lines = ht_in.splitlines()
    for line in lines:
        fields = line.split('\t')
        nums = fields[7].split(',')
        for num in nums:
            if num not in oclc:
                oclc[num] = []
    hathi.close()
    # read in physical items file and create dictionary of dictionaries - outer key is bib record MMS ID and inner
    # keys are barcodes, to link info from multiple vols. to the same bib record
    phys_items = dict()
    phys_export = open(sys.argv[3], 'r')
    phys_data = phys_export.read()
    vols = phys_data.splitlines()
    for vol in vols:
        vol_fields = vol.split('\t')
        sub_dict = dict()
        no_quotes = vol_fields[0].strip("'")
        sub_dict[vol_fields[3]] = [vol_fields[10], vol_fields[19], vol_fields[8]]
        if no_quotes in phys_items:
            phys_items[no_quotes][vol_fields[3]] = [vol_fields[10], vol_fields[19], vol_fields[8]]
        elif no_quotes not in phys_items:
            phys_items[no_quotes] = sub_dict
    phys_export.close()
    # read in the marc file using pymarc, check it record by record against each dictionary. For items that are
    # not in the Hathi OCLC dict, combine data from bib and item records and print to file.
    out = open('digitization_candidates.txt', 'w')
    with open(sys.argv[2], 'rb') as bibs:
        reader = MARCReader(bibs)
        for record in reader:
            alma_id = str(record['001'])
            title = record.title()
            author = record.author()
            year = record.pubyear()
            subjects = record.subjects()
            columns = [alma_id[6:len(alma_id)], title, author, year]
            # check for 901 field, since not all Alma sets exclude records with a 901
            if "Digitized" not in str(record['901']):
                for control_num in record.get_fields('035'):
                    value = str(control_num['a'])
                    if 'OCoLC' in value:
                        trimmed = ''.join(ch for ch in value if ch.isdigit())
                        if trimmed not in oclc:
                            try:
                                phys_entry = phys_items[columns[0]]
                            except KeyError:
                                continue
                            for key, values in phys_entry.items():
                                inner_dict = phys_entry[key]
                                out.write(str(key) + '\t')
                                for column in columns:
                                    out.write(str(column) + '\t')
                                for data in inner_dict:
                                    out.write(data + '\t')
                                for subject in subjects:
                                    out.write(str(subject['a']) + ',')
                                out.write('\t')
                                out.write('\n')
    bibs.close()
    out.close()


main()
