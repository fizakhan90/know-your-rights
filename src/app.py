import streamlit as st
from search import RightsSearch
from llm import RightsLLM

def main():
    st.title("Know Your Rights - Women's Legal Rights Information")
    
    search = RightsSearch()
    llm = RightsLLM()
    
    st.sidebar.header("Search Filters")
    region = st.sidebar.selectbox(
        "Select Region",
        ["All"] + ["California", "New York", "Texas"]  
    )
    
    category = st.sidebar.selectbox(
        "Select Category",
        ["All"] + ["Abortion Rights", "Maternity Rights", "Workplace Rights"]
    )
    
    
    st.write("Ask a question about women's rights in your region:")
    user_query = st.text_input("Your question")
    
    if st.button("Search"):
        if user_query:
            with st.spinner("Searching..."):
                
                results = search.search_rights(
                    region=None if region == "All" else region,
                    category=None if category == "All" else category
                )
                
                if results:
                
                    context = "\n".join([r['right_text'] for r in results])
                    
                    
                    response = llm.generate_response(context, user_query)
                    
            
                    st.write("### Answer")
                    st.write(response)
                    
                    
                    st.write("### Sources")
                    for r in results:
                        st.write(f"- {r['sources']}")
                else:
                    st.warning("No information found for your query.")
                    
    
    st.markdown("""
    ---
    **Disclaimer**: This tool provides general information about legal rights. 
    The information provided should not be considered legal advice. 
    Please consult with legal professionals for specific advice.
    """)

if __name__ == "__main__":
    main()

