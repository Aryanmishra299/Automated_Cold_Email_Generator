import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')


class chain:

    def __init__(self):

        self.llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0
        )

    def extract_jobs(self, cleaned_text):

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the careers page of a website.

            Your job is to extract job postings and return JSON format containing:
            - role
            - experience
            - skills
            - description

            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(
            input={'page_data': cleaned_text}
        )

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)

        except OutputParserException:
            raise OutputParserException(
                "Content too big unable to parse jobs..!!"
            )

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:

            {job_description}

            ### INSTRUCTION:

            You are Aryan Mishra, an AI Engineer with 2+ years experience in:

            1. OCR extraction services
            2. AI automation
            3. Problem solving
            4. Delivering projects before deadlines

            You received an achievement award from a client for completing
            a complex project before the deadline.

            Write a professional cold email for the above job.

            Also include the most relevant portfolio projects from:
            {links_list}

            Show why Aryan Mishra is the best fit.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke({
            'job_description': str(job),
            'links_list': links
        })

        return res.content


if __name__ == "__main__":
    print(api_key)