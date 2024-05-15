# Screenshot Bot

## 构建镜像和运行

dockerfile 一直想迁移到内网服务器，不过因为性能问题未解决，所以这部分暂时是搁置的，你如果想试试，可以参考下面的方法。

```bash
docker buildx build --load  --platform linux/amd64 -t screenshot-bot:v3  .

docker run -d --platform linux/amd64 --name screenshot-bot \
  -e CHROMEDRIVER_PATH=/app/bin/chromedriver_linux_amd64 \
  -e API_TOKEN=usk4faMS1dP8Tsr6ytchczb \
  -p 8001:8000 \
  release.daocloud.io/ndx-product/screenshot-bot:latest
```

目前需要关注的是项目需要chrome的依赖，这里使用了 `selenium/standalone-chrome` 镜像，在构建的时候指定平台为 `linux/amd64`。

如果需要了解更多，可以查看 Dockerfile 的配置。

## 项目运行办法 -> 看这里

虽然已经支持了在服务端跑，不过由于 Apitable 的性能问题，所以还是建议在本地跑， 且高性能电脑。

比如，我的电脑是 M1 Max， 64G 内存。 仍然需要 1个小时才能跑完。

> **包含了大量延迟和等待时间，如果不等待，apitable 错误率会极大增加。**

### 执行条件

启动程序的脚本: 

1. 电脑安装了 chromedriver 和 Chrome ，并且版本搭配
2. 使用 Poetry 安装依赖，或者 pip 安装 requirements.txt 里的依赖
3. 执行 source test-env.sh 来设置环境变量
4. 执行 `uvicorn main:app --port 8001` 在本地启动 fastapi 接口

在浏览器打开地址: http://127.0.0.1:8001/docs/

### 接口介绍

1. `/test-screenshot` 测试截图接口，可以用来测试是否能正常截图

```bash
curl -X 'GET' \
  'http://127.0.0.1:8001/test-screenshot' \
  -H 'accept: application/json'
```

以上测试正常了之后，说明截图环境和参数配置正常了； 否则不能进行下一步。

2.`/start_task` 启动任务

datasheet_id 目前仅支持 项目事项跟踪通知表或者镜像文件的id，`dstrqpMc5uCrC8lWge`，目前会自动发送频次为 “每天” 的群里。

```bash
curl -X 'POST' \
  'http://127.0.0.1:8001/start_task' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "datasheet_id": "dstrqpMc5uCrC8lWge",
  "is_test": true
}'
```

### 运行条件要求

需要在公司内网的服务器，或者连到 vpn， 依赖 apitbale。

### chromedriver 和 Chrome 的关系

项目依赖 chromedriver 和 Chrome，并且需要两者的版本搭配；

1. 先去 [chromedriver 官网](https://chromedriver.chromium.org/downloads) 下载 chromedriver，注意下载的版本号
2. 然后，去 [Chrome](https://chrome-versions.com/)，下载对应版本的 Chrome，注意版本号匹配
3. 下载时注意选择对应的操作系统，比如 Mac、Linux、Windows 和 arm64、amd64 的区别
4. 在 [bin](./bin) 目录下，预置了 Mac M1 和 Linux 的 chromedriver，你可以直接使用，如果不是这两个系统，你需要自己下载并替换
5. Dockerfile 内预置下载了 Chrome 下载，与 bin 目录下的 chromedriver 版本是匹配的

