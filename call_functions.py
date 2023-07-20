#Import the required Libraries
import streamlit as st
import pandas as pd
from typing import Any
from google.cloud import discoveryengine

# Defining variables for the project
project_id = "work-mylab-machinelearning"
location = "global"                    # Values: "global"
search_engine_id = "search-alphabet-financialr_1689840102872"
serving_config_id = "default_config"          # Values: "default_config"
search_query = "Google"

def f_list_docs_genai_es(project_id: str, location: str, search_engine_id: str) -> Any:
    # Create a client
    client = discoveryengine.DocumentServiceClient()
    # The full resource name of the search engine branch.
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

def f_show_auto_list_of_docs():
    vResult = f_list_docs_genai_es(project_id, location, search_engine_id)
    vResult = vResult  # Replace "YOUR_DATA_HERE" with the actual ListDocumentsPager object
    # Create a list of dictionaries for each document in the data
    documents_list = []
    for document in vResult.documents:
        document_data = {
            'File Name': f_remove_gs_prefix(document.content.uri),
        }
        documents_list.append(document_data)
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(documents_list)
    # Show the DataFrame as a table using Streamlit
    return df

def f_remove_gs_prefix(input_string):
    prefix = "gs://genai-appbuilder-es-alphabetfinancialreport/"
    if prefix in input_string:
        return input_string.replace(prefix, "gs://googlecloudstorage_to_store_files/")
    else:
        return input_string
    