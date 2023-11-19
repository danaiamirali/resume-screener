import PyPDF2
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

class ResumeParser:
    def __init__(self, path: str):
        print ("parsing resume...")
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

            skills_prompt = ChatPromptTemplate.from_template("""
            Given the below resume, extract the candidate's skills, if any, verbatim. Return them in the following format (delimited by triple backticks):
            \"\"\"
            Skills:
            - skill 1 (verbatim from resume)
            - skill 2 (verbatim from resume)
            ...
            \"\"\"                                                                                    
            Resume: {resume}
            Answer:                                           
            """)

            experiences_prompt = ChatPromptTemplate.from_template("""
            Given the below resume, extract the candidate's experiences, if any, verbatim. Return them in the following format (delimited by triple backticks):
            \"\"\"
            Experiences:
            - experience 1 (date range)
                - bullet points (verbatim from resume)                                                      
            - experience 2 (date range)
                - bullet points (verbatim from resume)
            ...
            \"\"\"                                                                                    
            Resume: {resume}
            Answer:                                           
            """)

            education_prompt = ChatPromptTemplate.from_template("""
            Given the below resume, extract the candidate's education history and any listed classes, if any, verbatim. Return them in the following format (delimited by triple backticks):
            \"\"\"
            Education:
            - education 1 (verbatim from resume)
            - education 2 (verbatim from resume)
            ...
            \"\"\"                                                                                    
            Resume: {resume}
            Answer:                                           
            """)

            interests_prompt = ChatPromptTemplate.from_template("""
            Given the below resume, extract the candidate's interests, if any, verbatim. Return them in the following format (delimited by triple backticks):
            \"\"\"
            Interests:
            - interest 1 (verbatim from resume)
            - interest 2 (verbatim from resume)
            ...
            \"\"\"                                                                                    
            Resume: {resume}
            Answer:                                           
            """)

            prompts = [skills_prompt, experiences_prompt, education_prompt, interests_prompt]
            threads = []
            self.resume = "" 
            for prompt in prompts:
                threads.append(Thread(target = lambda x : ))

                rag_chain = (
                    {"resume": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                )
                try: 
                    self.resume += rag_chain.invoke(text)
                except:
                    pass



class JobDescriptionParser:
    def __init__(self, description: str):
        print ("parsing job description...")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        
        essentials_prompt = ChatPromptTemplate.from_template("""
        Given the below job description and the candidates relevant skills and experiences, please list anything listed as, essential, required, or otherwise needed essentially for a candidate to apply. If any, please be verbatim when listing these requirements, otherwise return nothing.
        Return them in the following format (delimited by triple backticks):
        \"\"\"
        Essential Skills:
        - skill 1 (verbatim from resume)
        - skill 2 (verbatim from resume)
        ...
        \"\"\"                                                                                    
        Job Description: {job_description}. 
        Answer:                                           
        """)

        rag_chain = (
            {"job_description": RunnablePassthrough()}
            | essentials_prompt
            | llm
            | StrOutputParser()
        )

        essentials = rag_chain.invoke(description)

        desirables_prompt = ChatPromptTemplate.from_template("""
        Given the below job description and the candidates relevant skills and experiences, please list anything listed as beneficial or preffered, or otherwise non-essential but beneficial to have. The if the requirement is already satisfied, don't include it at all.
        Return them in the following format (delimited by triple backticks):
        \"\"\"
        Desirable Skills:
        - skill 1 (verbatim from resume)
        - skill 2 (verbatim from resume)
        ...
        \"\"\"                                              
        Job Description: {job_description}
        Satisfied: {context}
        Preferred Requirements:                                           
        """)

        rag_chain = (
            {"job_description": RunnablePassthrough(), "context": RunnablePassthrough()}
            | desirables_prompt
            | llm
            | StrOutputParser()
        )

        desirables = rag_chain.invoke({"job_description": description, "context": essentials})

        self.requirements = essentials + "\n" + desirables
        self.essentials = essentials

        