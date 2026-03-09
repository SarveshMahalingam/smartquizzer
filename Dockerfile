# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. FORCE INSTALL DEPENDENCIES (Added werkzeug)
RUN pip install --no-cache-dir streamlit google-generativeai bs4 pdfminer requests pandas phonenumbers werkzeug pymongo

# 4. Copy the rest of your app's code into the container
COPY . .

# 5. Expose the port Streamlit uses
EXPOSE 8501

# 6. The bulletproof command to run your app
CMD ["python", "-m", "streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]