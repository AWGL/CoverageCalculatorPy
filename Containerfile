FROM docker.io/python:3.11

# Copy script into folder
COPY CoverageCalculatorPy.py /usr/bin/

RUN chmod +x /usr/bin/CoverageCalculatorPy.py

# Install pytabix
RUN  pip install pytabix==0.1

