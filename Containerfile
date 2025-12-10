FROM docker.io/python:3.11

# Copy script into folder
COPY CoverageCalculatorPy.py ./

RUN chmod +x CoverageCalculatorPy.py

# Install pytabix
RUN  pip install pytabix==0.1

