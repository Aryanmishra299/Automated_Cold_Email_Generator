import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import chain
from portfolio import portfolio
from utility import clean_text

import warnings
warnings.filterwarnings("ignore")


def create_streamlit_app(llm, portfolio, clean_text):

    st.title("Cold Mail Generator")

    url_input = st.text_input(
        'Enter a URL:',
        value="https://www.accenture.com/in-en/careers/jobdetails?id=ATCI-5180677-S1905710_en"
    )

    submit_button = st.button('Submit')

    if submit_button:

        try:

            with st.spinner("Processing..."):

                loader = WebBaseLoader([url_input])

                data = loader.load().pop().page_content

                cleaned_data = clean_text(data)

                portfolio.load_portfolio()

                jobs = llm.extract_jobs(cleaned_data)

                for job in jobs:

                    skills = job.get('skills', [])

                    links = portfolio.query_links(skills)

                    email = llm.write_mail(job, links)

                    st.subheader("Generated Cold Email")

                    st.code(email, language='markdown')

        except Exception as e:

            st.error(f"An Error Occurred: {e}")


if __name__ == '__main__':

    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator"
    )

    llm = chain()

    portfolio_obj = portfolio()

    create_streamlit_app(
        llm,
        portfolio_obj,
        clean_text
    )