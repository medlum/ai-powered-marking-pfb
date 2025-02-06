import streamlit as st
from huggingface_hub import InferenceClient
from utils import *
from streamlit_extras.grid import grid
import zipfile
from pathlib import Path
from sys_message import *
from charset_normalizer import from_path
import ast
import pandas as pd

# ---------set up page config -------------#
st.set_page_config(page_title="PFB Assistive Marking AI Tool",
                   layout="centered",
                   page_icon="🐶",
                   initial_sidebar_state="expanded")

# ---------set css-------------#
st.markdown(btn_css, unsafe_allow_html=True)
st.markdown(image_css, unsafe_allow_html=True)

# --- Initialize the Inference Client with the API key ----#
try:
    client = InferenceClient(token=st.secrets.api_keys.huggingfacehub_api_token)
except Exception as e:
    st.error(f"Error initializing Inference Client: {e}")
    st.stop()


# ------- initialize first system message --------#
if 'msg_history' not in st.session_state:

    st.session_state.msg_history = []
    
    system_message = """
    Your name is Cosmo, a friendly AI assistant to a teacher who teach Python. 
    You are tasked to mark the students' coding assignments.
    Follow the instructions to mark:
    - Use the marking rubrics available for assigning marks. 
    - Assign a mark for each of the criterion in the marking rubrics.
    - Do not assign more than the maximum mark in each criterion.
    - Write a short comment for each marking criteria after assigning the marks.
    - Return the marks and the comment in a dictionary : {
            'Name': [ ],
            'Program Correctness': [ ],
            'Code Readability': [ ],
            'Code Efficiency': [ ],
            'Documentation': [ ],
            'Assignment Specifications': [ ]
            'Comments' : [ ]
        }  
    - Use single quotation '' for strings in the dictionary.
    - Locate the student's name in the assignment under #####  Store your, name, email, student_id and class_number as STRINGS #####
    - Use the code solutions given by the teacher as a point of reference for a model answer. 
    - Use the data "SpaceUsage.csv" to evaluate the code for the program correctness criteria. 
    - Check if the code is able to produce the correct output and write as a txt file.
    - Your answer should only have the return dictionary and nothing else. 
    """
    
    st.session_state.msg_history.append(
        {"role": "system", "content": f"{system_message}"}
    )
    st.session_state.msg_history.append(
        {"role": "system", "content": f"Code solutions given by the teacher as reference: {code_solutions}"})

    st.session_state.msg_history.append(
    {"role": "system", "content": f"Marking rubrics for reference: {mark_rubrics}"})
    
    st.session_state.msg_history.append(
    {"role": "system", "content": f"This is the correct output that the assignment should produce: {correct_output}"})

    st.session_state.msg_history.append(
    {"role": "system", "content": f"SpaceUsage.csv data: {data}"})


# ------- write chat conversations of session state --------#
for msg in st.session_state.msg_history:
    if msg['role'] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ------- create side bar --------#
with st.sidebar:
    st.title(":rainbow[Cosmo]. :gray[PFB Assistive marking AI]", help=intro_var)
    st.image('cosmo.jpeg', width=80)
    model_id = st.selectbox(":blue[Select an AI model]", 
                            ["Qwen/Qwen2.5-72B-Instruct",
                             "Qwen/Qwen2.5-Coder-32B-Instruct",
                             "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                             "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
                             "meta-llama/Llama-3.3-70B-Instruct",
                             "meta-llama/Llama-3.1-8B-Instruct"],
                            index=4,
                            help=model_help)
    upload_student_report = st.file_uploader(":blue[Upload a ZIP file]", type=["zip"])
    evaluate_btn = st.button(":material_search_insights: Evaluate Report", type="primary")
    clear_btn = st.button(":material_refresh: Clear History", type="primary")
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)

#--- extract pdf and add to session state---#
data = []
if upload_student_report is not None:
    if evaluate_btn:
        if not model_id:
            st.error("Please select an AI model.")
            st.stop()

        # Define extraction path
        extract_folder = "extracted_pyfiles"

        # Extract ZIP file
        try:
            with zipfile.ZipFile(upload_student_report, "r") as zip_ref:
                zip_ref.extractall(extract_folder)
        except zipfile.BadZipFile:
            st.error("The uploaded file is not a valid ZIP file.")
            st.stop()
        except Exception as e:
            st.error(f"An error occurred while extracting the ZIP file: {e}")
            st.stop()

        py_files = list(Path(extract_folder).rglob("*.py"))
        if not py_files:
            st.error("No Python files found in the uploaded ZIP file.")
            st.stop()

        for file in py_files:
            try:
                # Using from_path to detect encoding
                result = from_path(file)
                best_match = result.best()
                encoding = best_match.encoding if best_match else "utf-8"

                # Read the file with the detected encoding
                with open(file, "r", encoding=encoding) as f:
                    student_report = f.read()

                # Display file content with syntax highlighting
                st.sidebar.code(student_report, language="python")

            except UnicodeDecodeError:
                st.error(f"Failed to decode the file {file.name}.")
                continue
            except Exception as e:
                st.error(f"An error occurred while processing the file {file.name}: {e}")
                continue

            st.session_state.msg_history.append({
                "role": "system",
                "content": f"Mark this assignment: {student_report}"
            })

            try:
                with st.spinner("EVALUATING CODE..."):
                    with st.empty():
                        stream = client.chat_completion(
                            model=model_id,
                            messages=st.session_state.msg_history,
                            temperature=0.5,
                            max_tokens=5524,
                            top_p=0.7,
                            stream=True,
                        )
                        collected_response = ""

                        for chunk in stream:
                            if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                                collected_response += chunk.choices[0].delta.content
                                st.chat_message("assistant").write(collected_response)

                        # Convert string to dict
                        try:
                            actual_dict = ast.literal_eval(collected_response)
                            data.append(actual_dict)
                        except (ValueError, SyntaxError):
                            st.error("The model's response is not in the expected format.")
                            continue

                        del st.session_state.msg_history[5:]

            except Exception as e:
                st.error(f"Error generating response: {e}")

if data:
    combined_data = {}
    for entry in data:
        for key, value in entry.items():
            if key in combined_data:
                combined_data[key] += value  # Extend existing list
            else:
                combined_data[key] = value  # Initialize key with list

    df = pd.DataFrame(combined_data)
    df['Total'] = df[['Program Correctness', 
                      'Code Readability', 
                      'Code Efficiency', 
                      'Documentation', 
                      'Assignment Specifications']].sum(axis=1)
    # Rearrange columns to place 'total' at the 6th position 
    columns = list(df.columns)
    columns.insert(6, columns.pop(columns.index('Total')))
    df = df[columns]
    st.dataframe(df)
    st.balloons()

