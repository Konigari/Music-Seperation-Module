FROM xserrat/facebook-demucs:latest

WORKDIR /srv

COPY ["*.py", "*.txt", "/srv"]

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "worker.py"]