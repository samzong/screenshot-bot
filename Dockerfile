FROM python:3.10-slim-buster

#ENV DEBIAN_FRONTEND=noninteractive
#
USER root

RUN sed -i "s@http://\(deb\|security\).debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list

RUN apt update && \
    apt install -y libglib2.0-0 libxcb1 libnss3 --no-install-recommends && \
    apt clean



# 安装 Python 依赖 \
RUN pip install fastapi uvicorn selenium apitable selenium-screenshot chinesecalendar --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制代码
COPY . /app
WORKDIR /app

ENV DST_ID_OR_URL undefined
ENV API_TOKEN undefined
ENV CHROMEDRIVER_PATH /app/bin/chromedriver_linux_amd64

RUN chmod +x /app/bin/chromedriver_linux_amd64

# 启动服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]