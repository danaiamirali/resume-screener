from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from .parsers import ResumeParser, JobDescriptionParser

class Screener:
    def __init__(self, path: str, job_description: str):
        print ("running constructor...")
        load_dotenv()

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.path = path
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
        print("running strengths...")

        prompt = ChatPromptTemplate.from_template("""
        Given the below job description and the candidates relevant skills and experiences, point out strengths about the candidate's experiences relative to the job, if any.
        If there are any strengths, respond in the following format (delimited by triple backticks) for each strength, one after another in the style of a python list:
        \"\"\"
        [pair1, pair2, ... pairN] where pairI =                                          
        (
        "the relevant snippet, verbatim, from the candidate's resume",
        "your commentary on the strength and why it's good for the job"                                                                              
        )
        \"\"\"                                                                                    
        Job Description: {job_description}
        Relevant Skills and Experiences: {context}
        Answer:                                           
        """)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)   

        loader = UnstructuredPDFLoader(self.path)
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(data)

        embedding = OpenAIEmbeddings(model='text-embedding-ada-002')

        vectorstore = Chroma.from_documents(documents=splits, embedding=embedding)
        retriever = vectorstore.as_retriever()

        rag_chain = (
            {"job_description": RunnablePassthrough(), "context": retriever | format_docs}
            | prompt
            | self.llm
            | StrOutputParser()
        ) 

        return rag_chain.invoke(self.job_description.requirements)

    def weaknesses(self):
        pass