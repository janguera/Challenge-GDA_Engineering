FROM python:3.11

# Set the working directory
WORKDIR /src/streamlit

# Install requirements
COPY  src/streamlit/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /
# Copy configuration files
COPY .env_streamlit /.env_streamlit

# Copy app files
COPY src/streamlit /src/streamlit

COPY images /images
COPY .env_streamlit /.env_streamlit

ENV PYTHONPATH "${PYTHONPATH}:/src/streamlit:/src:/"

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "/src/streamlit/main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]