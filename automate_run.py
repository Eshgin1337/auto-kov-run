import os
import shutil
import subprocess
import sys

def run_command(command):
    """Runs a shell command and prints the output."""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
    else:
        print(result.stdout)

def copy_linux_directory():
    """Copy the linux/ directory into copied_linux/ using rsync."""
    if os.path.exists("copied_linux"):
        print("Removing existing copied_linux/ directory.")
        shutil.rmtree("copied_linux")
    print("Copying linux/ to copied_linux/ using rsync...")
    run_command("rsync -auv linux/ copied_linux/")

def truncate_files(input_path):
    """Truncate a specific file or all .c files in the given directory."""
    if os.path.isfile(os.path.join("copied_linux", input_path)):
        # If it's a single file
        file_path = os.path.join("copied_linux", input_path)
        print(f"Truncating file: {file_path}")
        open(file_path, 'w').close()
    elif os.path.isdir(os.path.join("copied_linux", input_path)):
        # If it's a directory, truncate all .c files inside it
        print(f"Truncating all .c files in directory: {input_path}")
        command = f"find copied_linux/ -name '*.c' -exec truncate -s 0 {{}} \\;"
        run_command(command)
    else:
        print(f"Error: The path {input_path} does not exist in copied_linux/. Exiting...")
        sys.exit(1)

def generate_patch(patch_filename):
    """Generate a .diff patch file against the original source."""
    print(f"Generating patch file: {patch_filename} ...")
    command = f"diff -ruN linux/ copied_linux/ | sed 's|^diff -ruN linux/|diff -ruN |; s| copied_linux/| |; s|^--- linux/|--- |; s|^+++ copied_linux/|+++ |' > {patch_filename}"
    run_command(command)

def get_next_log_filename(base_name="faulty", extension=".logs"):
    """Find the next available log filename (faulty2.logs, faulty3.logs, etc.)."""
    counter = 2
    log_filename = f"{base_name}{extension}"
    while os.path.exists(log_filename):
        log_filename = f"{base_name}{counter}{extension}"
        counter += 1
    return log_filename

def run_koverage(patch_filename, input_path):
    """Run the koverage tool with the specified patch file."""
    # Determine the output filename based on the directory name
    if input_path == "copied_linux":
        output_file = "coverage_results_all_task.json"
    else:
        output_file = get_next_log_filename()

    print(f"Running koverage with patch file: {patch_filename}. Output will be saved in: {output_file}")
    command = f"koverage -f --linux-ksrc /home/eshgin/koverage_task/linux --config /home/eshgin/koverage_task/linux/.config --arch x86_64 --check-patch {patch_filename} -o {output_file} 2>&1 | tee {output_file}"
    run_command(command)

def main():
    if len(sys.argv) != 3:
        print("Usage: python automate_patch.py <file_or_directory_to_truncate> <patch_filename>")
        sys.exit(1)

    file_or_directory_to_truncate = sys.argv[1]
    patch_filename = sys.argv[2]

    # Step 1: Check if the copied_linux/ directory exists, and remove it if so
    if os.path.exists("copied_linux"):
        print("Existing copied_linux/ directory found. Removing...")
        shutil.rmtree("copied_linux")

    # Step 3: Copy linux/ directory to copied_linux/
    copy_linux_directory()

    # Step 4: Truncate the specified file(s) or directory
    truncate_files(file_or_directory_to_truncate)

    # Step 5: Generate the patch file
    generate_patch(patch_filename)

    # Step 6: Run koverage with the patch file
    run_koverage(patch_filename, file_or_directory_to_truncate)

    print("Process completed successfully!")

if __name__ == "__main__":
    main()
