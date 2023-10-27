import os
import re
# Dinka Dereje
# https://siidaatech.com
# Input folder containing USFM files create a folder
input_folder = "USFM"

# Output folder for USX files create a folder
output_folder = "USX"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# List all files in the input folder
usfm_files = [f for f in os.listdir(input_folder) if f.endswith('.usfm')]

for usfm_file in usfm_files:
    # Construct the full path for input and output files
    input_file_path = os.path.join(input_folder, usfm_file)
    output_file_path = os.path.join(output_folder, re.sub(r'\.usfm$', '.usx', usfm_file))

    # Initialize variables
    usx_content = '<usx version="2.0">\n'
    book_title = None
    chapter = None

    # Open the input file for reading
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            if line.startswith('\\id '):
                # Extract the book title from \\id marker
                book_title = re.search(r'\\id\s+(.*)', line).group(1)
            elif line.startswith('\\c '):
                # Extract chapter number from \\c marker
                chapter = re.search(r'\\c\s+(\d+)', line).group(1)
                usx_content += f'  <book code="{book_title}" style="id">{book_title}</book>\n'
                usx_content += f'  <para style="mt">{book_title}</para>\n'
                usx_content += f'  <chapter number="{chapter}" style="c" />\n'
            elif line.startswith('\\v '):
                # Extract verse number and text from \\v marker
                verse_number = re.search(r'\\v\s+(\d+)', line).group(1)
                verse_text = re.search(r'\\v\s+\d+\s+(.*)', line)
                if verse_text:
                    verse_text = verse_text.group(1)
                    usx_content += f'    <para style="p">\n'
                    usx_content += f'      <verse number="{verse_number}" style="v" />{verse_text}</para>\n'
                else:
                    usx_content += f'    <para style="p">\n'
                    usx_content += f'      <verse number="{verse_number}" style="v" /></para>\n'
            elif line.startswith('\\li1 '):
                # Handle the new format with \\li1 markers
                list_item_text = re.search(r'\\li1\s+(.*)', line).group(1)
                usx_content += f'    <para style="p"><verse number="{verse_number}" style="li1" />{list_item_text}</para>\n'

    # Close the USX document
    usx_content += '</usx>'

    # Write the converted USX content to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(usx_content)

    print(f"Conversion complete for {usfm_file}. Output saved to {output_file_path}")
