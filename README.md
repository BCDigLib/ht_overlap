# ht_overlap
Scripts to inform digitization selection to help us contribute unique materials to HathiTrust

BC Libraries prefers to contribute unique material to HathiTrust. The scripts in this repo use HathiFiles (https://www.hathitrust.org/hathifiles) along with Alma exports to produce a spreadsheet that can be used for digitization selection.

Usage:
Create a logical set in Alma based on your desired query paramaters (ours often include physical location, condition notes, and cataloging history for special collections materials.)
Run two exports based on that set - a bibliographic record export (binary, single file, then converted to .mrk) and a physical items export. The physical items export will need to be converted from a csv to a tsv, and potentially to have extra quotation marks removed.
Download the most recent full hathifile from the URL linked above.
Run ht_overlap_analysis.py with those three files as inputs, and import the resulting text file into an excel or gsheets spreadsheet.

The produced output file can then be used to run call_number.py and produce a list of digitization candidates focused on a specific collection area. The output file of call_number.py is a tab-delimited text file, but once imported into Excel (being careful to mark the ItemNumber and ReferenceNumber fields as text, not general), the resulting excel file can be imported into Aeon to produce a queue of candidate items for digitization.