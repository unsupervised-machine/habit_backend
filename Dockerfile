# Use the official AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Copy your requirements file and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy the rest of your application code to the container
COPY . ${LAMBDA_TASK_ROOT}

# Set the Lambda handler entry point.
# This example assumes your FastAPI app is in main.py and that
# you have a variable 'handler' defined as your Lambda handler.
CMD [ "main.handler" ]