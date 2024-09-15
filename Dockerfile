FROM python:3.12-alpine3.20
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
# CMD ["python", "-m", "flask", "--app", "src/app", "run","--port","80"]
# CMD ["python", "-m", "flask", "--app", "src/app", "run"]
CMD ["python3","run.py"]


