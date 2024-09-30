
# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
          echo "Usage: $0 <file_name> <line_number>"
            exit 1
fi

FILE="$1"
LINE_NUMBER="$2"

# Check if the file exists
if [ ! -f "$FILE" ]; then
          echo "File $FILE not found!"
            exit 1
fi

# Check if the line number is a valid positive integer
if ! [[ "$LINE_NUMBER" =~ ^[0-9]+$ ]]; then
          echo "Error: Line number must be a positive integer."
            exit 1
fi

# Check if the line number is within the file's range
TOTAL_LINES=$(wc -l < "$FILE")
if [ "$LINE_NUMBER" -gt "$TOTAL_LINES" ]; then
          echo "Error: Specified line number $LINE_NUMBER is greater than the total lines in the file ($TOTAL_LINES)."
            exit 1
fi

# Extract lines starting from the next line after the specified line number and overwrite the file
tail -n +"$((LINE_NUMBER + 1))" "$FILE" > temp_file && mv temp_file "$FILE"

echo "File '$FILE' has been updated successfully."
