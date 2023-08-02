#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from typing import Any
from google.cloud import discoveryengine
import json

project_id = "work-mylab-machinelearning"
location = "global"                    # Values: "global"
search_engine_id = "search-alphabet-financialr_1689840102872"
serving_config_id = "default_config"          # Values: "default_config"
search_query = "Google"

def remove_gs_prefix(input_string):
    prefix = "gs://genai-appbuilder-es-alphabetfinancialreport/"
    if prefix in input_string:
        return input_string.replace(prefix, "gs://googlecloudstorage_to_store_files/")
    else:
        return input_string
    
def uploadFilesToStorage(uploaded_files):
    if uploaded_files is not None:
        for f in uploaded_files:
            st.write(f)
        data_list = []
        for f in uploaded_files:
            data = pd.read_csv(f)
            data_list.append(data)
        df = pd.concat(data_list)

def list_documents_genai_es(project_id: str, location: str, search_engine_id: str) -> Any:
    # Create a client
    client = discoveryengine.DocumentServiceClient()
    # The full resource name of the search engine branch.
    # e.g. projects/{project}/locations/{location}/dataStores/{data_store}/branches/{branch}
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        branch="default_branch",
    )
    response = client.list_documents(parent=parent)
    print(f"Documents in {search_engine_id}:")
    for result in response:
        print(result)
    return response

def show_list_of_alphabet_docs():
    vResult = list_documents_genai_es(project_id, location, search_engine_id)
    vResult = vResult  # Replace "YOUR_DATA_HERE" with the actual ListDocumentsPager object
    # Create a list of dictionaries for each document in the data
    documents_list = []
    for document in vResult.documents:
        document_data = {
            'File Name': remove_gs_prefix(document.content.uri),
        }
        documents_list.append(document_data)
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(documents_list)
    # Show the DataFrame as a table using Streamlit
    st.dataframe(df)

# Add a title and intro text
st.title('Ask Questions to your Documents')
st.text('Upload/choose your financial documents and ask questions to it')

# Create file uploader object
uploaded_files = st.file_uploader('Upload your files', accept_multiple_files=True, type=['pdf', 'html'])

# Use Alphabet Docs
st.write('Or explore these public Alphabet financial documents as an example:')
show_list_of_alphabet_docs()

# Create a button to upload files
st.button('Upload files')

