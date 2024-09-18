FROM texlive/texlive:latest 

# Installing required packages
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install


# Set working directory
WORKDIR /workdir

# Environment variables for S3 and AWS credentials
ENV LATEX_FILE_URL=""
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_REGION=""
ENV S3_OUTPUT_BUCKET=""

# Copy the shell script
COPY script.sh /workdir/script.sh 

# Make the shell script executable
RUN chmod +x /workdir/script.sh 

# Set the entrypoint to shell script
ENTRYPOINT [ "/workdir/script.sh" ]
