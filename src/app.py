import streamlit as st
import pandas as pd
from typing import Optional
from search import RightsSearch

def initialize_session_state():
    if 'search' not in st.session_state:
        st.session_state.search = RightsSearch()
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'last_results' not in st.session_state:
        st.session_state.last_results = None

def display_search_results(results: dict, query: Optional[str] = None):
    if results['rag_response']:
        st.write("### Answer")
        st.write(results['rag_response'])

    if results['results']:
        st.markdown("### Detailed Results")
        result_data = [{
            "Region": r['region'],
            "Category": r['category'],
            "Source": r['sources'],
            "Similarity": r.get('similarity', None)
        } for r in results['results']]
        df = pd.DataFrame(result_data)
        st.table(df)
    else:
        st.warning("No results found matching your criteria.")

def display_conversation_history():
    if st.session_state.conversation_history:
        with st.expander("View Conversation History", expanded=False):
            for i, (q, r) in enumerate(st.session_state.conversation_history, 1):
                st.markdown(f"**Q{i}:** {q}")
                st.markdown(f"**A{i}:** {r}")
                st.divider()

def main():
    st.set_page_config(
        page_title="Know Your Rights - Women's Legal Rights Information",
        page_icon="⚖️",
        layout="wide",
    )

    initialize_session_state()

    st.title("Know Your Rights - Women's Legal Rights Information")
    
    with st.sidebar:
        st.header("Search Filters")
        region = st.selectbox(
            "Select Region",
            ["All", "California", "New York", "Texas"]
        )
        category = st.selectbox(
            "Select Category",
            ["All", "Abortion Rights", "Maternity Rights", "Workplace Rights"]
        )

    col1, col2 = st.columns([3, 1])
    with col1:
        user_query = st.text_input(
            "Ask a question about women's rights:",
            placeholder="E.g., What are my maternity leave rights in California?"
        )
    with col2:
        search_button = st.button("Search", type="primary", use_container_width=True)

    if search_button and user_query:
        with st.spinner("Searching..."):
            try:
                results = st.session_state.search.enhanced_search(
                    region=None if region == "All" else region,
                    category=None if category == "All" else category,
                    search_text=user_query
                )
                if results['rag_response']:
                    st.session_state.conversation_history.append(
                        (user_query, results['rag_response'])
                    )
                st.session_state.last_results = results
                display_search_results(results, user_query)
            except Exception as e:
                st.error(f"Search error: {str(e)}")

    display_conversation_history()

    if st.session_state.last_results:
        st.divider()
        st.subheader("Follow-up Questions")
        follow_up = st.text_input(
            "Ask a follow-up question:",
            placeholder="Need more details about something specific?"
        )
        if st.button("Ask Follow-up"):
            if follow_up:
                with st.spinner("Processing follow-up..."):
                    try:
                        results = st.session_state.search.enhanced_search(
                            search_text=follow_up,
                            is_follow_up=True
                        )
                        if results['rag_response']:
                            st.session_state.conversation_history.append(
                                (follow_up, results['rag_response'])
                            )
                        display_search_results(results, follow_up)
                    except Exception as e:
                        st.error(f"Error processing follow-up: {str(e)}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Disclaimer**: This tool provides general information about legal rights. 
    For specific legal advice, please consult with qualified legal professionals.
    """)

if __name__ == "__main__":
    main()
