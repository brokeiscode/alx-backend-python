# Use a base Python image.
FROM python:3.10

# Set the working directory inside the container. All subsequent commands will run from here.
WORKDIR /app

# Copy the requirements file into the working directory.
COPY requirements.txt .

# Install the dependencies from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project code into the container's working directory.
COPY . .

# Expose port 8000. This is the default port for Django's development server.
EXPOSE 8000

# Run the Django development server when the container starts.
# The '0.0.0.0' address makes the server accessible from outside the container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
