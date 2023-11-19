from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

from .parsers import ResumeParser, JobDescriptionParser

class Screener:
    def __init__(self, path: str, job_description: str):
        print ("running constructor...")
        load_dotenv()

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        self.resume = ResumeParser(path)
        self.job_description = JobDescriptionParser(job_description)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def is_correct_fit(self):
        print ("running is_correct_fit...")
        prompt = ChatPromptTemplate.from_template("""
        Given the below job requirements, essential and nonessential, and the candidates resume, provide a YES or NO answer about whether the candidate is a truly good fit for the job.
        Job Description: {job_description}
        Resume: {resume}
        Answer:                                           
        """)

        rag_chain = (
            {"job_description": RunnablePassthrough(), "resume": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain.invoke({"job_description": self.job_description.requirements, "resume": self.resume.resume})

    def strengths(self):
        pass

    def weaknesses(self):
        pass