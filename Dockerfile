FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 5000
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "mybot.py"]
