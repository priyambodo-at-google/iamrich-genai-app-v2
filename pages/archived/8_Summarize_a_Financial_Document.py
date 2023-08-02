import streamlit as st
import pandas as pd

st.header('Multiple File Upload')
uploaded_files = st.file_uploader('Upload your files',
accept_multiple_files=True,  accept_multiple_files=True, type=['png', 'pdf'])

for f in uploaded_files:
    st.write(f)

data_list = []
for f in uploaded_files:
    data = pd.read_csv(f)
    data_list.append(data)

df = pd.concat(data_list)

