import streamlit as st
from typing import List
import pandas as pd
from google.cloud import discoveryengine

# curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# "https://discoveryengine.googleapis.com/v1alpha/projects/388889235558/locations/global/collections/default_collection/dataStores/search-website-financialne_1689171425441/servingConfigs/default_search:search" \
# -d '{"query":"<QUERY>","pageSize":10,"queryExpansionSpec":{"condition":"AUTO"},"spellCorrectionSpec":{"mode":"AUTO"},"safeSearch":false}'

project_id = "work-mylab-machinelearning"
location = "global"                    # Values: "global"
search_engine_id = "search-website-financialne_1689171425441"
serving_config_id = "default_config"          # Values: "default_config"
search_query = "Google"

def json_to_table(json_data):
    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame.from_dict(json_data)

    # Display the DataFrame as a table using Streamlit
    st.table(df)

def search_genai_es(
    project_id: str,
    location: str,
    search_engine_id: str,
    serving_config_id: str,
    search_query: str,
) -> List[discoveryengine.SearchResponse.SearchResult]:
    # Create a client
    client = discoveryengine.SearchServiceClient()

    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = client.serving_config_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        serving_config=serving_config_id,
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
    )
    response = client.search(request)
    for result in response.results:
        print(result)

    return response.results

if __name__ == "__main__":
    # Example JSON data
    example_json = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 28],
        "Country": ["USA", "Canada", "UK"]
    }

    st.header("JSON to Table Example")
    st.subheader("Original JSON Data:")
    st.json(example_json)

    st.subheader("JSON Data in Table:")
    json_to_table(example_json)

    json_to_table(st.write(search_genai_es(
    project_id,
    location,
    search_engine_id,
    serving_config_id,
    search_query)))
