# Dockerfile

# 1. Use official Python base image
FROM python:3.10

# 2. Set working directory inside the container
WORKDIR /app

# 3. Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential
# 5. Copy project files into the container
COPY . /app/

# 6. Expose port for Django
EXPOSE 8000

# 7. Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]