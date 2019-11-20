# AdjustMiles
# Rick Nelson
#
# This program allows you to adjust the mileage of a TCX file (say, exported from a Garmin activity))
# It asks for a .tcx file as an input, then finds the first DistanceMeters tag, which should be
# the entire distance ran.
#
# The program then asks you for your new distance in miles, and then adjusts that tag, and all other
# DistanceMeters tags, by that correction factor.
#
# The output is a new file (originalfile_corrected.txt, same folder) that has all new "stretched" distances
#
# Version history
# Ver   User    Description
#   1    RGN    Initial Release



from tkinter import filedialog
from tkinter import *

# Ask for TCX file, get path
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = [("TCX files","*.tcx")])

# Set filename to write to. It will take abc.tcx and write to abc_correctd.tcx
new_file_path = root.filename.replace(".tcx","_corrected.tcx")

# Load files
file_ori = open(root.filename,"r")
file_dst = open(new_file_path, "w")

meters_found = False
tag = "<DistanceMeters>"
lines_replaced = 0

print("")
for line in file_ori:
    # Three conditions: Finding DistanceMeters first time, finding subsequent times, and else
    # Set correction factor in first one, write new line. Write new (corrected) line in second case, write line as is in else
    str = line.strip()[:len(tag)]
    if (str == tag) and (meters_found == False):
        meters_found = True
        str = line.strip()[len(tag):]
        # str is now the rest of the line: "123.45</DistanceMaters"
        
        meters_orig = float(str[0:str.find('<')])               # Grab the distance in meters
        miles_orig = meters_orig/1609.34                        # Convert to miles
        print("Original file states you ran %0.2f miles" % miles_orig)
        
        miles_new = float(input("What is the corrected mileage? "))
        correction_factor = miles_new/miles_orig
        print("The correction factor is %.3f/%.3f = %.3f" % (miles_new, miles_orig, correction_factor))
        new_text = "        " + tag + f'{meters_orig*correction_factor:.5f}' + "</DistanceMeters>"
        file_dst.write(new_text+'\n')
        lines_replaced += 1
    elif (str == tag) and (meters_found == True):
        str = line[line.find('>')+1:]
        meters_orig = float(str[0:str.find('<')])
        new_text = line[:line.find('>')] + '>' + f'{meters_orig*correction_factor:.5f}' + "</DistanceMeters>"
        file_dst.write(new_text+'\n')
        lines_replaced += 1
        if lines_replaced % 100 == 0:
            print(".", end='')
    else:
        file_dst.write(line)


file_ori.close()
file_dst.close()
print("\nDone! %d lines replaced." % lines_replaced)
print("New file is " + new_file_path)