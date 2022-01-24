FROM python:3.7
# Create app directory
WORKDIR /
COPY ./ ./sspinfra
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY src /app
EXPOSE 5000
CMD [ "python", "app.py" ]
