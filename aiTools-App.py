import streamlit as st
from mellea import start_session
from mellea.stdlib.sampling import RejectionSamplingStrategy

# To run streamlit:
#  streamlit run name_of_file.py
#  or
#  python -m streamlit run name_of_file.py

@st.cache_resource
def get_session():
    return start_session()


st.set_page_config(page_title="Dr. Reis's Office Hours")
st.title("Dr. Reis's Office Hours")
st.caption("Local LLM via Ollama · granite4.1:3b · no API key")

task = st.text_area(
    "What should the model do?",
    "Write an email inviting students to office hours.",
    height=100,
)

# --- EXERCISE 3: Multiple Requirements ---
st.write("### Requirements")
requirement1 = st.text_input("Requirement 1", "Exactly 3 sentences.")
requirement2 = st.text_input("Requirement 2", "Mention INV1 455.")
requirement3 = st.text_input("Requirement 3", "Mention Wednesday.")
requirement4 = st.text_input("Requirement 4", "Use a professional tone.")
requirement5 = st.text_input("Requirement 5", 'End with "Best, Dr. Reis."')

retries = st.slider("Max retries if the requirement fails", 1, 5, 3)

if st.button("Generate", type="primary"):
    m = get_session()

    # Bundle the inputs and filter out any blank ones
    all_reqs = [requirement1, requirement2, requirement3, requirement4, requirement5]
    reqs = [r for r in all_reqs if r.strip()]

    with st.spinner("Thinking..."): # Hci principle - let the user know something is happening
        result = m.instruct(
            task,
            requirements=reqs,
            strategy=RejectionSamplingStrategy(loop_budget=retries),
        )

    st.subheader("Output")
    st.write(str(result))