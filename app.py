import streamlit as st
import requests
import json


# Backend API URLs
UPLOAD_URL = "http://localhost:8000/upload"
QUERY_URL = "http://localhost:8000/query"

st.set_page_config(page_title="RAG App", layout="wide")

st.title("📄 RAG System Interface")

# -------------------------
# File Upload Section
# -------------------------
st.subheader("Upload File")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "md", "html"])

if uploaded_file is not None:
    if st.button("🚀 Upload"):
        with st.spinner("Processing file..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(UPLOAD_URL, files=files)
                result = response.json()

                if result.get("status") == "success":
                    st.success(f"✅ File uploaded: {result['filename']}")
                else:
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Upload failed: {e}")

st.markdown("---")

# -------------------------
# Query Section
# -------------------------


st.subheader("Ask a Question")

query_text = st.text_input("Enter your query")

if st.button("🔍 Run Query"):
    if not query_text.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Generating response..."):
            try:
                # Send query as query param (not JSON body)
                response = requests.post(QUERY_URL, params={"query": query_text})
                result = response.json()

                if "response" in result:
                    st.success("✅ Query processed successfully")
                    
                    
                    st.markdown("### 📄 Response (Pretty JSON)")
                    # Pretty print with indentation like Postman
                    
                    pretty_json = json.dumps(result, indent=4, ensure_ascii=False)
                    st.code(pretty_json, language="json")

                else:
                    st.error("❌ Unexpected response format")
                    pretty_json = json.dumps(result, indent=4, ensure_ascii=False)
                    st.code(pretty_json, language="json")

            except Exception as e:
                st.error(f"Query failed: {e}")
