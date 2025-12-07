import streamlit as st
import os

# --- Configuration: List of Problematic Characters (Gremlins) ---
# Define the dictionary of characters to find and replace.
# Key: The problematic Unicode character
# Value: What to replace it with (e.g., ' ' for a space, or '' for nothing)
GREMLINS = {
    '\u00a0': ' ',  # Non-Breaking Space (our main suspect) -> standard space
    '\u200b': '',   # Zero Width Space (often inserted by web editors) -> nothing
    '\u00ad': '',   # Soft Hyphen -> nothing
    '\uFEFF': '',   # Byte Order Mark (BOM) -> nothing (common issue with Windows files)
}
# ---------------------


st.set_page_config(page_title="Gremlin Cleaner", page_icon="🧼")
st.title("🧼 Python Gremlin Cleaner")
st.subheader("Replace Invisible Unicode Characters in Code Files")

# --- Cleaning Function ---
def clean_file(file_name):
    # --- IMPROVED FILE PATH RESOLUTION ---
    # This logic finds the file relative to the app's location, fixing FileNotFoundError.
    try:
        # Get the directory where the running script (cleaner_app.py) is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Join the script's directory with the file name provided by the user
        file_path = os.path.join(script_dir, file_name)
    except NameError:
        # Fallback for environments where __file__ isn't available (less common)
        file_path = file_name
        
    try:
        # 1. Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        gremlin_count = 0
        cleaned_content = original_content

        # 2. Iterate through the dictionary and perform replacements
        for bad_char, replace_with in GREMLINS.items():
            count = cleaned_content.count(bad_char)
            if count > 0:
                gremlin_count += count
                # Perform the replacement
                cleaned_content = cleaned_content.replace(bad_char, replace_with)
        
        if gremlin_count == 0:
            return 0, "No gremlins found! File is already clean."

        # 3. Overwrite the original file with the clean content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
            
        return gremlin_count, f"✅ Success! Replaced {gremlin_count} problematic characters."

    except FileNotFoundError:
        # This will still happen if the file is truly missing or path is wrong
        return 0, f"❌ Error: File not found at {file_path}. Ensure it's in the same folder."
    except Exception as e:
        return 0, f"❌ An unexpected error occurred: {e}"

# --- Streamlit UI ---

st.markdown("---")

st.warning("⚠️ **Safety Note:** This script overwrites the original file. Always **make a backup** before cleaning critical code!")

# Input field for the target file path
target_file = st.text_input(
    "Enter the file name (e.g., sharp-website.py):",
    value="sharp-website.py" # Pre-fill with the known problematic file
)

if st.button("🚀 Find & Clean Gremlins", type="primary"):
    if not target_file:
        st.error("Please enter a file name.")
    else:
        with st.spinner(f"Cleaning `{target_file}`..."):
            # We only pass the name, the function figures out the path
            count, message = clean_file(target_file)
            
            if "Success" in message:
                st.balloons()
                st.success(message)
                st.write(f"The file **{target_file}** is now ready to run!")
            else:
                st.error(message)

st.markdown("---")
st.write("Run this app, clean your code, and then switch back to running your website generator.")
