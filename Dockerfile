FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

#RUN mkdir -p /amp
#COPY ./requirements.txt /amp/
#RUN pip install --no-cache-dir --upgrade -r /amp/requirements.txt
#COPY /src /amp
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]