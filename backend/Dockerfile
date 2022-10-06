FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 444
CMD [ "gunicorn", "main:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:444" ]