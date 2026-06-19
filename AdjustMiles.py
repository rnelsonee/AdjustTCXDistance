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
#   2    RGN    Abstracted writing corrected line to a function
#   3    RGN    Refactor


# We will use a file open dialog
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

TEXT_MARKER = "DistanceMeters"
TAG_OPEN = f"<{TEXT_MARKER}>"
TAG_CLOSE = f"</{TEXT_MARKER}>"
METERS_PER_MILE = 1609.34
METERS_PER_KM = 1000


def ask_yes_no(question):
    while True:
        reply = input(question).strip().lower()
        if reply.startswith("y"):
            return True
        if reply.startswith("n"):
            return False
        print('Invalid answer, please enter "y" or "n".')


def choose_input_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        initialdir=".",
        title="Select file",
        filetypes=[("TCX files", "*.tcx")],
    )


def build_output_path(source_path):
    path = Path(source_path)
    return path.with_name(f"{path.stem}_corrected{path.suffix}")


def extract_distance(line):
    start = line.find(">") + 1
    end = line.find("</")
    return float(line[start:end])


def replace_distance_line(line, new_value):
    start = line.find(">") + 1
    end = line.find("</")
    return f"{line[:start]}{new_value:.5f}{line[end:]}"


def get_correction_factor(original_meters):
    use_miles = ask_yes_no("\nWould you like to use miles? (y = miles, n = km): ")
    unit_name = "miles" if use_miles else "km"
    meters_per_unit = METERS_PER_MILE if use_miles else METERS_PER_KM

    original_distance = original_meters / meters_per_unit
    print(f"Original file states you ran {original_distance:.2f} {unit_name}")

    corrected_distance = float(input(f"What is the corrected distance ({unit_name})? "))
    correction_factor = corrected_distance / original_distance

    print(
        f"The correction factor is "
        f"{corrected_distance:.3f}/{original_distance:.3f} = {correction_factor:.3f}"
    )
    return correction_factor


def process_file(source_path, output_path):
    correction_factor = None
    lines_replaced = 0

    with open(source_path, "r") as source_file, open(output_path, "w") as output_file:
        for line in source_file:
            opening_tag = line[line.find("<") : line.find(">") + 1]

            if opening_tag != TAG_OPEN:
                output_file.write(line)
                continue

            meters = extract_distance(line)

            if correction_factor is None:
                correction_factor = get_correction_factor(meters)

            output_file.write(replace_distance_line(line, meters * correction_factor))
            lines_replaced += 1

    return lines_replaced


def main():
    source_path = choose_input_file()
    if not source_path:
        print("No file selected.")
        return

    output_path = build_output_path(source_path)
    lines_replaced = process_file(source_path, output_path)

    print(f"\n{lines_replaced} lines replaced.")
    print(f"New file is {output_path}")


if __name__ == "__main__":
    main()
