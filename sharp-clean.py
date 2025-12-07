import streamlit as st

# --- Configuration: List of Problematic Characters (Gremlins) ---
GREMLINS = {
    '\u00a0': ' ',  # Non-Breaking Space -> standard space
    '\u200b': '',   # Zero Width Space -> nothing
    '\u00ad': '',   # Soft Hyphen -> nothing
    '\uFEFF': '',   # Byte Order Mark (BOM) -> nothing
}
# ---------------------

st.set_page_config(page_title="Gremlin Cleaner - Paste Mode", page_icon="🧼")
st.title("🧼 Gremlin Cleaner - Copy/Paste Mode")
st.subheader("Clean Invisible Characters Directly in the Browser")

# --- Cleaning Function for Text Input ---
def clean_text_content(original_content):
    gremlin_count = 0
    cleaned_content = original_content

    # Iterate through the dictionary and perform replacements
    for bad_char, replace_with in GREMLINS.items():
        count = cleaned_content.count(bad_char)
        if count > 0:
            gremlin_count += count
            # Perform the replacement
            cleaned_content = cleaned_content.replace(bad_char, replace_with)
            
    return cleaned_content, gremlin_count

# --- Streamlit UI ---

st.markdown("---")

# Input Text Area
original_code = st.text_area(
    "1. Paste your problematic code here:",
    height=300,
    placeholder="Paste the code block that gave you the SyntaxError..."
)

# Output Variable
cleaned_code = ""
total_gremlins = 0

if st.button("🚀 Find & Clean Gremlins", type="primary"):
    if not original_code:
        st.warning("Please paste some code to analyze.")
    else:
        with st.spinner("Cleaning code..."):
            cleaned_code, total_gremlins = clean_text_content(original_code)
        
        st.success(f"✅ Cleaned! Found and replaced **{total_gremlins}** problematic characters.")

        # Show Output Text Area
        st.markdown("---")
        st.markdown("### 2. Copy the Cleaned Code")
        
        st.code(cleaned_code, language='python') # Use st.code for better display/copy

        if total_gremlins > 0:
             st.info("💡 Copy the code above and replace the old content in your Python file.")

# Ensure the app remains responsive even without a button click
