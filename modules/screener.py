from dotenv import load_dotenv
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate

import os

class Screener:
    def __init__(self):
        load_dotenv()
        API_KEY = os.getenv("OPENAI_API_KEY")

        loader = UnstructuredPDFLoader("../uploads/resume_med.pdf")
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(data)
        embedding = OpenAIEmbeddings(model='text-embedding-ada-002', api_key=API_KEY)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embedding)

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.retriever = vectorstore.as_retriever()

        self.job_description = """
        Below are the skills needed for this project. Students with the following relevant skills and interest, regardless of major, are encouraged to apply! This is a team based multidisciplinary project. Students on the team are not expected to have experience in all areas, but should be willing to learn and will be asked to perform a breadth of tasks throughout the two semester project.
        Advanced Data Science and Modeling Techniques
        Specific Skills: Applied project experience with Large Language Models and other applied AI techniques OR advanced coursework

        Likely Majors: DATA, STATS, MATH, CS


        Data Science
        Specific Skills: General skills in Data Science, good software development skills, and a willingness to quickly develop new technical skills as required for the project

        EECS 281(or equivalent) is required

        Likely Majors: DATA, CS


        General Coding
        Specific Skills: General Programming skills, good software engineering practice and design, and a willingness to quickly develop new technical skills as required for the project 

        EECS 281 (or equivalent) is required

        Likely Majors: CS, DATA, BBA/CS



        Additional Desired Skills/Knowledge/Experience
        Successful team-based project experience.  Excellent interpersonal skills
        Project Management utilizing Agile/Scrum
        Experience in business process analysis
        Interest in and general knowledge of Commercial Banking
        Practical experience implementing predictive analytics in a complex data environment
        Ability and desire to independently learn new technology skills as necessary for the project
        Experience implementing large language models, neural networks and self-supervised / semi-supervised learning models
        """

        pass
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def is_correct_fit(self):
        prompt = ChatPromptTemplate.from_template("""
        Given the below job description and the candidates relevant skills and experiences, provide a YES or NO answer about whether the candidate is a truly good fit for the job.
        Job Description: {job_description}
        Relevant Skills and Experiences: {context}
        Answer:                                           
        """)

        rag_chain = (
            {"job_description": self.job_description, "context": self.retriever | self.format_docs}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain.run()

    def strengths(self):
        pass

    def weaknesses(self):
        pass