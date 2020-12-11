FROM pypy:3.7-slim as advent-of-code
WORKDIR advent-of-code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

