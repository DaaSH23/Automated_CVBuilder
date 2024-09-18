# Automated CV Builder

An automated resume/CV builder that generates LaTeX-based resumes dynamically based on job descriptions and other inputs. This project integrates AI to craft personalized content for your resume, making it ideal for customizing resumes for specific job applications.

## Table of contents

- [Features / Services](#features-services)
- [Installation](#installation)
- [API endpoints](#api-endpoints)
- [Usage](#usage)
- [Contact](#contact)


## Features / Services

- Latext-docker: this file is responsilble for creating docker image. Which compiles the latex to pdf and upload the pdf to S3 bucket.
- microservice: this is Python fastAPI integrated service, provides endpoint for interacting with S3 buckets, openai(Azure) and ECS docker container.


## Installation

To install the micorservice 

```bash
  git clone https://github.com/DaaSH23/Automated_CVBuilder.git
  cd Automated_CVBuilder
  cd microservice
```
```bash
  python3 -m venv env
  .\env\Scripts\activate
```
```bash
  pip install -r requirements.txt
```

To create the docker image
```bash
  cd latext-docker
```
build the docker image
```bash
  docker build -t latex-Compiler:latest .
```
test the docker image by creating a container (make sure you have docker installed).
```bash
  docker run --env LATEX_FILE_URL="https://your-s3-link-to-latex-file" \
           --env AWS_ACCESS_KEY_ID="your-aws-access-key" \
           --env AWS_SECRET_ACCESS_KEY="your-aws-secret-key" \
           --env AWS_REGION="your-aws-region" \
           --env S3_OUTPUT_BUCKET="your-s3-output-bucket-name" \
           latex-compiler:latest
```
After successful testing, push the image to AWS ECR and create a cluster in ECS.


Environment variables:
Create a .env file in the root directory with the following content

```bash
  AZURE_OPENAI_ENDPOINT=""
  AZURE_OPENAI_APIKEY=""
  AZURE_OPENAI_DEPLOYMENT_NAME="gpt-35-turbo-instruct"
  LATEX_FILE_URL="https://your-s3-link-to-latex-file" 
  AWS_ACCESS_KEY_ID="your-aws-access-key" 
  AWS_SECRET_ACCESS_KEY="your-aws-secret-key" 
  AWS_REGION="your-aws-region" 
  S3_OUTPUT_BUCKET="your-s3-output-bucket-name" 
  
```

Run the microservice 
```bash
  uvicorn main:app --reload
```

## API endpoints

- Updates the latex using openAI(Azure)
POST --> /generateContext/
body : {
          "job_description": ""
  }

- Saves the latex temporarily for processing
POST --> /updateLatext/
form-data: 
    file : main.tex

- Starts a container in AWS ECS for compiling the laTex file to pdf
POST -->  /start-task
body:
{
    "environment_variables": [
     {"name": "LATEX_FILE_URL", "value": ""},
      {"name": "AWS_ACCESS_KEY_ID", "value": ""},
      {"name": "AWS_SECRET_ACCESS_KEY", "value": ""},
      {"name": "AWS_REGION", "value": ""},
      {"name": "S3_OUTPUT_BUCKET", "value": ""}
    ]
}


## Usage
This project is ideal for individuals or developers who want to dynamically generate resumes tailored to specific job descriptions using AI. Simply set up the project, input a job description, and receive a customized LaTeX resume that can be further modified or printed directly.

## Contact
  email - reachtoabhisheko@gmail.com
  linkedIn - https://www.linkedin.com/in/abhishek-oraon-developer/
