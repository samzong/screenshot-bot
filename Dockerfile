FROM python:3.10-slim-buster

#ENV DEBIAN_FRONTEND=noninteractive
#
USER root

RUN sed -i "s@http://\(deb\|security\).debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list

# 安装 wget 和必要的库
RUN apt update && apt install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libglib2.0-0 \
    libxcb1 \
    libnss3 \
    --no-install-recommends

# 下载并安装 Google Chrome
RUN wget https://chrome-versions.com/google-chrome-stable-114.0.5735.90-1.deb
RUN dpkg -i google-chrome-stable-114.0.5735.90-1.deb; apt -fy install
RUN dpkg -i google-chrome-stable-114.0.5735.90-1.deb

RUN apt install -y fonts-wqy-zenhei --no-install-recommends

# 清理不必要的文件和缓存
RUN apt clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f google-chrome-stable-114.0.5735.90-1.deb


# 安装 Python 依赖 \
RUN pip install fastapi uvicorn selenium apitable selenium-screenshot chinesecalendar --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制代码
COPY . /app
WORKDIR /app

ENV DST_ID_OR_URL undefined
ENV API_TOKEN undefined
ENV CHROMEDRIVER_PATH undefined

RUN chmod +x /app/bin/chromedriver_linux_amd64

# 启动服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]