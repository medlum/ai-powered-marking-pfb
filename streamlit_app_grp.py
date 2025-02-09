import streamlit as st
from huggingface_hub import InferenceClient
from sys_message_grp_brief import *
from sys_message_grp import *
from utils_grp import *
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
client = InferenceClient(token=st.secrets.api_keys.huggingfacehub_api_token)

# ------- initialize first system message --------#
if 'msg_history' not in st.session_state:

    st.session_state.msg_history = []
    st.session_state.msg_history.append({"role": "system", "content": f"{system_message}"})
    st.session_state.msg_history.append(
        {"role": "system", "content": f"""Here are the modular code solutions given by the teacher for reference: 
                                        1. Cash on hand : {code_coh}
                                        2. Profit and Loss : {code_pnl}
                                        3. Overheads : {code_overheads}
                                        4. Utility helper : {code_tool}"""})

    st.session_state.msg_history.append(
    {"role": "system", "content": f"Marking rubrics for reference: {mark_rubrics}"})
    st.session_state.msg_history.append(
    {"role": "system", "content": f"This is the project brief: {project_brief}"})
    st.session_state.msg_history.append(
    {"role": "system", "content": f"""These are the various csv data provided by the teacher:
                                    1. Cash on hand increasing each day: {coh_increasing}  
                                    2. Cash on hand decreasing each day: {coh_decreasing}  
                                    3. Cash on hand fluctuating each day: {coh_volatile}  
                                    4. Profit and Loss increasing each day: {pnl_increasing}
                                    5. Profit and Loss decreasing each day: {pnl_decreasing}
                                    6. Profit and Loss fluctuating each day: {pnl_volatile}
                                    7. Overheads data: {overheads}"""})
    st.session_state.msg_history.append(
    {"role": "system", "content": f"""These are the 'summary_report.txt' files provided by the teacher as the correct output:
                                    1. When cash on hand and profit and loss are increasing each day: {output_increasing}  
                                    2. When cash on hand and profit and loss are decreasing each day: {output_decreasing}  
                                    3. When cash on hand and profit and loss are fluctuating each day:: {output_volatile}"""})

# ------- create side bar --------#
with st.sidebar:
    st.title(":rainbow[Cosmo]. :gray[PFB Group Project Assistive Marking AI]", help=intro_var)
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
if upload_student_report:

    extracted_content = extract_and_read_files(upload_student_report)

    for folder, contents in extracted_content.items():

        if contents["team_members"]:
            st.session_state.msg_history.append({
                "role": "user", "content": f"""Mark this assignment:
                                            - Student names: {contents["team_members"]}
                                            - Submitted assignment: {contents["python_files"]}
                                            """})
            
            team_members = "\n".join([line.strip() for line in contents["team_members"]])

            st.sidebar.text(team_members)
            for filename, file_content in contents["python_files"]:
                st.sidebar.markdown(f"**{filename}**")
                st.sidebar.code(file_content, language="python")
            
            if evaluate_btn:
                with st.status("Evaluating...", expanded=True) as status:
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
                                st.text(collected_response.replace('{','').replace('}',''))

                        # Convert string to dict
                        actual_dict = ast.literal_eval(collected_response)
                        data.append(actual_dict)
                        del st.session_state.msg_history[7:]
                        status.update(label="Evaluation complete...", state="complete", expanded=True)

if clear_btn:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.cache_data.clear()

if data:
   
    for entry in data:
        for key, value in entry.items():
            if key == "Team members" and isinstance(value, list):
                entry["Team members"] = ",".join(value)
            elif key == "Feedback" and isinstance(value, list):
                entry["Feedback"] = " ".join(value)  # Convert list to string
           

    df = pd.DataFrame(data)
    st.dataframe(df)

 