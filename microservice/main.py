# AI micro-service for handling the openai processing

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = FastAPI()

#----------------Azure openai credentials----------------
openai_key = os.getenv("AZURE_OPENAI_APIKEY")
openai_Endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_deploymentName = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

#----------------Initialize azure client----------------- 
client = AzureOpenAI(
    api_key=openai_key,
    api_version="2022-12-01",
    azure_endpoint=openai_Endpoint
)

class JobDescriptionInput(BaseModel):
    job_description: str
    

#----------------Generate context using openAI------------------
@app.post("/generateContext/")
async def generate_Context(data: JobDescriptionInput):
    try:
        
        #--------------------Check for job description------------------
        if not data.job_description:
            return {"erro": "Job description required!"}
        
        #---------------------Check for latex file---------------------
        if not os.path.exists("/ResumeLatex.tex"):
            return {"Latex Error": " Latex file not found, please upload the latex file."}
        
        #-------------Retrive the section skills section from latex---------------
        with open("ResumeLatex.tex", "r") as file : 
            LatexContent = file.read()
            
        pattern = r'(%EditedPartStart.*?%EditedPartEnd)'
        
        SkillsData = re.search(pattern, LatexContent, re.DOTALL)
        
        if SkillsData:
            SkillsData = SkillsData.group(1).strip()
            SkillsData = SkillsData.replace("%EditedPartStart", "")
            SkillsData = SkillsData.replace("%EditedPartEnd", "")        
            SkillsData = SkillsData.replace(r"\resumeSubItem", "\\resumeSubItem")
            print (SkillsData)
        else:
            return {"Latex Error":" Couldn't find the pointers for skills section"}
            

        #-------------------------Input prompt------------------------
        redefinedprompt = f"""
        Please update the following LaTeX code with the relevant details extracted from the job description provided below.

        LaTeX Code to Update:
        {SkillsData}

        Job Description:
        {data.job_description}

        Instructions:
        1. Review the job description carefully.
        2. For the 'Languages' section, add any programming languages mentioned in the job description that are not already listed.
        3. For the 'Frameworks' section, add any frameworks or libraries mentioned in the job description that are not already listed.
        4. For the 'Databases' section, add any database technologies mentioned in the job description that are not already listed.
        5. For the 'Tech/Cloud tools' section, add any relevant technologies or cloud tools mentioned in the job description that are not already listed.
        6. If any mentioned technologies do not fit into the above categories, add them to the category called 'Other Technologies', if it don't exist then create a new category called 'Other Technologies' at the last section in LaTeX code.
        7. Ensure that 'React' is categorized correctly as a framework, not a language.
        8. DO NOT repeat any tech stack in any sections, Remove the duplicates.
        9. DO NOT create any sections/categories if it's already created/mentioned, Remove the duplicates if exists.
        10. DO NOT add any other informations and sections/categories beside the once mentioned.

        Please provide the updated LaTeX code as the output.
        """
        
        
        #----------------------Call Azure client for AI response-----------------
        response = client.completions.create(
            model=openai_deploymentName,
            prompt=redefinedprompt,
            max_tokens=150,
            temperature=0.2
        )
        
        generated_text = response.choices[0].text.strip()
        
        #---------------------Calling the update latex function---------------------
        updatedLatexRes = await update_latex_function(repr(generated_text))
        
        if(updatedLatexRes == "updated"):
            #----------------returning the edited latex file----------------------
            return FileResponse("ResumeLatex.tex", media_type="application/x-tex", filename="ResumeLatex.tex") 
        else:
            raise HTTPException(status_code=500, detail="Failed to update latex file.")
        
    except Exception as ex : 
        raise HTTPException(status_code=500, details=str(ex)) 
    


#--------------------Saves the latex file temporarily--------------------- 
@app.post("/updateLatext/")
async def update_Latex(file: UploadFile):
    try:
        content = await file.read()
        
        latex_Content = content.decode('utf-8')
        
        with open("ResumeLatex.tex", "w") as temp_file:
            temp_file.write(latex_Content)
    
        return {"Message": "file saved temporarily!"}
    
    except Exception as ex:
        return HTTPException(status_code=500, detail=f"Falied to save the file: {str(ex)}")
    

#-----------------Function for updating the LaTeX file---------------------
async def update_latex_function(update_Content: str):
   try:
        with open("ResumeLatex.tex", "r") as file:
            content = file.read()

        pattern = r'(%EditedPartStart.*?%EditedPartEnd)'
                
        update_Content = update_Content.replace("'", "")
        update_Content = "%EditedPartStart\n" + update_Content + "\n%EditedPartEnd"
        
        new_content = re.sub( pattern, update_Content, content, flags=re.DOTALL)
        
        with open("ResumeLatex.tex", 'w') as file:
            file.write(new_content)
        
        return "updated"
    
   except Exception as ex:
       return ("Error: ", {str(ex)})


