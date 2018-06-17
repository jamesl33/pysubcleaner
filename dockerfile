FROM python:3

WORKDIR /usr/src/pysubcleaner

COPY . /usr/src/pysubcleaner

RUN pip install --no-cache-dir pysrt

ENTRYPOINT ["python", "pysubcleaner.py"]
CMD ["--help"]
