FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /

# Install requirements
COPY app/api/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Copy app configuration
COPY .env_api /.env_api  

# Copy app code
COPY app/api /app/api

# Add PATH and PYTHONPATH to avoid issues w/ python modules
ENV PATH="$PATH:/"
ENV PYTHONPATH="$PYTHONPATH:/"

EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]