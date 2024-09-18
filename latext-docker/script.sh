#!/bin/bash

# Fail on any error
set -e

# check if LATEX_FILE_URL is provided
if [ -z "$LATEX_FILE_URL" ]; then
    echo "ERROR: LATEX_FILE_URL is not set."
    exit 1
fi 

# Check if AWS credentials are present
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_REGION" ]; then
    echo "ERROR: AWS credentials are not set"
    exit 1
fi 

# Download the latex from S3
echo "Downloading latex file from $LATEX_FILE_URL ...."
curl -o ResumeLatex.tex "$LATEX_FILE_URL"

# Check if the file was downloaded
if [ ! -f "ResumeLatex.tex" ]; then
    echo "ERROR: Failed to downlaod the LaTex file."
    exit 1
fi

# Compile LaTex to PDF
echo "Compiling LaTex to PDF....."
pdflatex ResumeLatex.tex

# Check if the pdf was generated
if [ ! -f "ResumeLatex.pdf" ]; then
    echo "ERROR: PDF compilation failed"
    exit 1
fi

echo "PDF generated successfully....."

# Check for the output bucket env
if [ -z "$S3_OUTPUT_BUCKET" ]; then
    echo "ERROR: Env output bucket is not present"
    exit 1
fi

CURRENT_DATE=$(date +"%Y-%m-%d")
PDF_FILENAME="Resume_$CURRENT_DATE.pdf"
mv ResumeLatex.pdf $PDF_FILENAME


# Upload the pdf to S3 
aws s3 cp $PDF_FILENAME s3://$S3_OUTPUT_BUCKET/output/$PDF_FILENAME 

# Check if upload was successful
if [ $? -eq 0 ]; then
    echo "PDF successfully uploaded to S3://$S3_OUTPUT_BUCKET/output/$PDF_FILENAME"
else
    echo "ERROR: Failed to upload PDF to S3."
    exit 1
fi


# Generate the public URL for the uploaded PDF
PUBLIC_URL="https://$S3_OUTPUT_BUCKET.s3.$AWS_REGION.amazonaws.com/output/$PDF_FILENAME"

echo "Public URL for the PDF:"
echo $PUBLIC_URL
