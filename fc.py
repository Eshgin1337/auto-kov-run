import json

# myf = json.load("fw_all_diff_patch.diff.covreq")
# with open('fw_all_diff_patch.diff.covreq', 'r') as myc:

with open("fw_all_diff_patch.diff.covreq", "r") as file:
    data = json.load(file)

# Count files in each category
header_file_count = len(data.get("headerfile_loc", {}))
source_file_count = len(data.get("sourcefile_loc", {}))

# Total count of files
total_files = header_file_count + source_file_count

print(total_files)

