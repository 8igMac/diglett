FROM nvidia/cuda:12.4.1-base-ubuntu22.04

WORKDIR /code

# Install Pyaudio dependencies.
RUN apt-get update && apt-get upgrade -y && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
	portaudio19-dev \
	python3.10 \
	python3-pip

# Set environment variables
ENV POETRY_VERSION=1.8.2

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer.
COPY pyproject.toml poetry.lock /code/

# Install Python packages and disable creation of virtual env.
RUN poetry config virtualenvs.create false && \
	poetry install --no-interaction --only main --no-ansi

COPY . /code

CMD ["uvicorn", "diglett.main:app", "--host", "0.0.0.0", "--port", "80"]
