FROM python:3.5.2

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY ./entry.sh /

RUN chmod +x ./entry.sh

EXPOSE 7000
ENTRYPOINT [ "/entry.sh" ]