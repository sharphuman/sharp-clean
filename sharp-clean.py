import os

# 1. Read the file
file_path = 'sharp-website.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 2. Perform the cleaning (replacing the unicode character)
# Note: The raw character might need to be copied into the string like this: '\u00a0'
cleaned_content = content.replace('\u00a0', ' ')

# 3. Overwrite the original file with the clean content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print("File cleaned successfully! Run your Streamlit app now.")
