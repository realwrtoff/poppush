FROM python:3.7-alpine

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

ENV app /app
WORKDIR ${app}
ADD main.py $app

# 自己的部分
CMD ["python3", "main.py"]