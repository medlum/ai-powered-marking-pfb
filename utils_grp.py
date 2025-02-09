import zipfile
from pathlib import Path
from charset_normalizer import from_path
import streamlit as st
import shutil

def is_valid_zip(zip_path):
    """Checks if a file is a valid ZIP archive."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            return zip_file.testzip() is None
    except zipfile.BadZipFile:
        return False

def extract_and_read_files(main_zip_path):
    """
    Extracts all Python (.py) files and specifically reads team_members.txt from a zip file that contains subfolders,
    preserving folder structure.
    """
    extract_folder = "extracted_files"
    
    # Clear previous extractions
    if Path(extract_folder).exists():
        shutil.rmtree(extract_folder)
    
    # Extract main ZIP file
    with zipfile.ZipFile(main_zip_path, "r") as main_zip:
        main_zip.extractall(extract_folder)
    
    # Locate nested ZIP files and extract them if valid
    for nested_zip_path in Path(extract_folder).rglob("*.zip"):
        if is_valid_zip(nested_zip_path):
            with zipfile.ZipFile(nested_zip_path, "r") as nested_zip:
                nested_extract_folder = nested_zip_path.parent / "nested_extracted"
                nested_zip.extractall(nested_extract_folder)
    
    # Organize extracted files by folder
    extracted_data = {}
    
    for folder in Path(extract_folder).glob("**"):  # Ensure folders are properly iterated
        if folder.is_dir():  # Process only directories
            folder_name = str(folder.relative_to(extract_folder))
            extracted_data[folder_name] = {"team_members": None, "python_files": []}
            
            team_members_file = folder / "team_members.txt"
            if team_members_file.exists():
                with open(team_members_file, "r", encoding="utf-8") as f:
                    extracted_data[folder_name]["team_members"] = f.readlines()
            
            for py_file in folder.glob("*.py"):  # Avoid recursive rglob to limit scope per folder
                result = from_path(py_file)
                encoding = result.best().encoding if result.best() else "utf-8"
                with open(py_file, "r", encoding=encoding) as f:
                    extracted_data[folder_name]["python_files"].append((py_file.name, f.read()))
    
    return extracted_data

# Example usage in Streamlit
#uploaded_file = st.file_uploader("Upload a ZIP file", type=["zip"])
#text = ""
#if uploaded_file:
#    extracted_content = extract_and_read_files(uploaded_file)
#    
#    for folder, contents in extracted_content.items():
#
#        st.write(contents)
#        
#        if contents["team_members"]:
#            st.sidebar.markdown("**Contents of team_members.txt:**")
#            team_members = "\n".join([line.strip() for line in contents["team_members"]])
#            st.sidebar.text(team_members)
#
#            for filename, file_content in contents["python_files"]:
#                st.sidebar.markdown(f"**{filename}**")
#                st.sidebar.code(file_content, language="python")
            




# custom CSS for buttons
btn_css = """
<style>
    .stButton > button {
        color: #383736; 
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 30px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #383736; 
        background-color: #c4c2c0; /* Darker green on hover */
    }
</style>
"""

image_css = """
<style>
.stImage img {
    border-radius: 50%;
    #border: 5px solid #f8fae6;
}
</style>

"""



model_help = ":blue[Models with less parameters have faster inference speed but often at the expense of a more quality answer.]"

rubrics_help = ":blue[Upload a set of marking rubrics with a **criterion** column in PDF.]"

report_help =":blue[Report with more than 3,000 words may experience '*max limit token error*'. Click on **Clear History** and try again.]"

eval_btn_help = ":blue[Click to evaluate the internship report]"

intro_var = """
:blue[While AI marking can help with consistency and efficiency, it's crucial to review and verify the marks and feedback generated.]
"""

disclaimer_var = "Disclaimer: This AI-powered tool is designed to assist in marking reports by providing helpful suggestions and evaluations. However, it may occasionally make errors or misinterpret content. Final judgment and accuracy should be verified by a qualified evaluator."

creator_var = "Andy Oh is the creator behind this AI-powered tool, designed to transform how educators manage their workload by introducing an innovative solution to streamline their tasks." 