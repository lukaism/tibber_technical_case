ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Download dependencies as a separate step to take advantage of Docker's caching.
COPY requirements.txt requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD python3 -m flask run --host=0.0.0.0
