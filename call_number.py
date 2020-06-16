# script that takes a file produced by ht_overlap_analysis.py and a set of call numbers and outputs a new version of
# the overlap file limited to call numbers in that range


def main():
    while True:
        infile = input("Please list the name of file to sort including extension: ")
        try:
            overlap = open(infile, 'r')
        except FileNotFoundError:
            print("That file does not exist in your current directory. Please move the file to your current directory"
                  "or check your spelling")
            continue
        else:
            break
    outfile = open('sorted_queue.txt', 'w')
    letters = input("Please list the letters of the LC Call number you wish to sort by (e.g. BX)")
    while True:
        try:
            lower_num = int(input("Please enter the lower bound of the numerical call number range as a whole number: "))
        except ValueError:
            print("Cannot parse your input. Please make sure it is a whole number with no letters or periods (e.g. "
                  "1100)")
            continue
        else:
            break
    while True:
        try:
            upper_num = int(input("Please enter the upper bound of the numerical call number range as a whole number: "))
        except ValueError:
            print("Cannot parse your input. Please make sure it is a whole number with no letters or periods (e.g. "
                  "1100)")
            continue
        else:
            break
    data = overlap.read()
    lines = data.splitlines()
    for line in lines:
        fields = line.split('\t')
        call_num = fields[7]
        if letters in call_num[0:3]:
            period_loc = fields[7].index('.')
            number_part = fields[7][2:period_loc]
            try:
                if lower_num < int(number_part) < upper_num:
                    outfile.write(line + '\n')
            except ValueError:
                pass
    overlap.close()
    outfile.close()


main()
