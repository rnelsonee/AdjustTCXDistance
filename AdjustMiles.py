# AdjustMiles
# Rick Nelson
#
# This program allows you to adjust the mileage of a TCX file (say, exported from a Garmin activity))
# It asks for a .tcx file as an input, then finds the first DistanceMeters tag_open, which should be
# the entire distance ran.
#
# The program then asks you for your new distance in miles, and then adjusts that tag_open, and all other
# DistanceMeters tag_opens, by that correction factor.
#
# The output is a new file (originalfile_corrected.txt, same folder) that has all new "tag_valueetched" distances
#
# Version history
# Ver   User    Description
#   1    RGN    Initial Release


# We will use a file open dialog
from tkinter import filedialog
from tkinter import *

def miles_or_not(question):
    reply = input(question)
    if reply[0].lower() == "y":
        return True
    elif reply[0].lower() == "n":
        return False
    else:
        print("Invalid answer, please answer with a \"y\" or an \"n\"")
        miles_or_not(question)


# Ask for TCX file, get path
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = [("TCX files","*.tcx")])

# Set filename to write to. It will take abc.tcx and write to abc_correctd.tcx
new_file_path = root.filename
new_file_path = new_file_path[:new_file_path.rfind(".")] + '_corrected.' + new_file_path[new_file_path.rfind(".")+1:]

# Load files
file_ori = open(root.filename,"r")
file_dst = open(new_file_path, "w")

text_marker = "DistanceMeters"
tag_open = "<" + text_marker + ">"
tag_close = "</" + text_marker + ">"
lines_replaced = 0
use_miles = True

print("")
for line in file_ori:
    # Three conditions: Finding DistanceMeters first time, finding subsequent times, and else
    # Set correction factor in first one, write new line. Write new (corrected) line in second case, write line as is in else
    tag_value = line[line.find("<"):line.find(">")+1]

    if (tag_value == tag_open) and (lines_replaced == 0):

        meters_found = True
        
        # Get number between "...>" and "</...."
        meters_orig = float(line[line.find(">")+1:line.find('</')])               # Grab the distance in meters

        use_miles = miles_or_not("Would you like to use miles? (y = miles, n = km): ")
        divisor = (1609.34 if use_miles else 1000)

        distance_orig = meters_orig/divisor
        print("Original file states you ran %0.2f " % distance_orig + ("miles" if use_miles else "km"))

        distance_new = float(input("What is the corrected distance (" + ("miles" if use_miles else "km") +")? "))
        correction_factor = distance_new/distance_orig
        print("The correction factor is %.3f/%.3f = %.3f" % (distance_new, distance_orig, correction_factor))
        
        new_text = line[:line.find('>')] + '>' + f'{meters_orig*correction_factor:.5f}' + tag_close
        file_dst.write(new_text+'\n')
        lines_replaced += 1
    
    elif (tag_value == tag_open) and (lines_replaced > 0):
        # This is for all the other times we find "<DistanceMeters>"
        # We just want to replace the number and write that new line out.

        meters_orig = float(line[line.find(">")+1:line.find('</')]) 
        new_text = line[:line.find('>')] + '>' + f'{meters_orig*correction_factor:.5f}' + tag_close
        file_dst.write(new_text+'\n')
        lines_replaced += 1
        if lines_replaced % 100 == 0:
            print(".", end='')
    
    else:
        # All lines that don't have "<DistanceMeters>" - write the line out as is
        file_dst.write(line)


file_ori.close()
file_dst.close()
print("\n%d lines replaced." % lines_replaced)
print("New file is " + new_file_path)

