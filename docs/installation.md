# 安装

## 准备

### git
首先，你需要安装git，可参考[github文档](https://docs.github.com/cn/github/getting-started-with-github/quickstart/set-up-git)进行安装和配置。

### 包管理器

本项目推荐使用poetry进行python和包管理。可参考[官网文档](https://python-poetry.org/docs/)进行安装。

## 安装Hearthbot

1. 克隆Hearthbot源码到本地：
```
git clone https://github.com/ZelKnow/Hearthbot.git --recursive
```

2. 安装依赖
```
poetry install --no-dev
```

## 配置

打开项目根目录下的.env.prod进行项目的配置。

| 配置项        | 说明                                       |
| ------------- | ------------------------------------------ |
| HOST          | 主机名，需与go-cqhttp端配置一致            |
| PORT          | 端口，需与go-cqhttp端配置一致              |
| AUTO_AGREE    | 是否自动同意加群和加好友邀请               |
| COMMAND_START | 命令的起始标记，用于判断一条消息是不是命令 |
| MAX_RESPONSE  | 输出搜索结果时一页最多展示多少条           |

## 安装go-cqhttp

请参考[官方文档](https://docs.go-cqhttp.org/guide/quick_start.html)安装并配置好go-cqhttp

## 运行

1. 启动机器人
```
poetry run nb run
```
2. 启动go-cqhttp
3. 在QQ聊天框对机器人输入```!help```，如机器人回复帮助信息，则启动成功。