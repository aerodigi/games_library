FROM python:3
COPY . .
RUN pip3 install flask
RUN pip3 install pymongo
CMD ["python3" , "main.py"]