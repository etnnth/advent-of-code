FROM pypy:3-7.3.3-slim-buster as advent-of-code
WORKDIR advent-of-code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

