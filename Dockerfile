FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

# This command will be run from the current working directory.
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
