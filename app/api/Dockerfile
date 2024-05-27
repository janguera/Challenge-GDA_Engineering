FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /

# Install requirements
COPY app/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Copy app configuration
COPY .env_api /.env_api  

# Copy app code
COPY app/api /app/api

# Add PATH and PYTHONPATH to avoid issues w/ python modules
ENV PATH="$PATH:/"
ENV PYTHONPATH="$PYTHONPATH:/"

# Server config
ENV APP_MODULE="app.main:app"
ENV WORKERS_PER_CORE=4
ENV MAX_WORKERS=8
ENV PORT="8000"
EXPOSE 8000

