FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 5000
#ENV NAME World

# Set the entrypoint to the wait-for-mysql.sh script

# Define the command to run your application
# Run app.py when the container launches
#CMD ["python", "mybot.py"]

CMD ["sh","script.sh"]
 

