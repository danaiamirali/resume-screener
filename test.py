from modules.screener import Screener

job_desc = """
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

print ("test.py started...")
s = Screener("static/resume.pdf", job_desc)
