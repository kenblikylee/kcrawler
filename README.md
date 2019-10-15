# kcrawler

[![Build Status](https://travis-ci.org/kenblikylee/kcrawler.svg?branch=master)](https://travis-ci.org/kenblikylee/kcrawler)
[![license](https://img.shields.io/github/license/kenblikylee/kcrawler)](https://github.com/kenblikylee/kcrawler/blob/master/LICENSE)

A python crawler authored by Ken.


## 1. 安装

### 1.1 环境要求

- python>=3.0
- pip>=19.0

``` sh
python -V
pip install --upgrade pip
pip -V
```

### 1.2 查看最新版本

``` sh
pip search kcrawler
```

### 1.3 初次安装

``` sh
pip install kcrawler
# or
pip install --index-url https://pypi.org/simple kcrawler
```

### 1.4 更新已有安装

``` sh
pip install --upgrade kcrawler
# or
pip install --upgrade --index-url https://pypi.org/simple kcrawler
```

### 1.5 卸载

``` sh
pip uninstall -y kcrawler
```

## 2. 命令行调用

### 2.1 使用方式

使用 pip 安装成功后，会自动在系统搜索路径创建可执行程序：`kcrawler`, `kcanjuke`, `kcjuejin`。

> 通常是 `python` 或 `conda` 安装目录下的 `bin` 子目录下，例如：`/anaconda3/bin/kcrawler`。windows 平台会创建 `.exe` 文件。

`kcrawler` 是爬取所有网站应用的入口，命令执行格式如下：

``` sh
kcrawler <webapp> [webapp-data] [--options]
```

等效于：

``` sh
kc<webapp> [webapp-data] [--options]
```

例如：

```
kcrawler juejin books --url "https://..."
kcjuejin books --url "https://..."
```

### 2.2 使用示例

以 `kcrawler <webapp> [webapp-data] [--options]` 方式运行为例。

#### 2.2.1 爬取掘金小册数据

执行如下命令：

``` sh
kcrawler juejin book
```

命令执行成功，显示如下统计图表：

![](http://cdn.kenblog.top/juejin_books_927.png)

并将明细数据保存在当前目录下，同时保存 `.csv` 和 `.xls` 文件，文件名格式如下：

`juejin_books_YYYY-MM-DD.csv` `juejin_books_YYYY-MM-DD.xls`

#### 2.2.2 爬取掘金专栏阅读量

格式：

``` sh
kcrawler juejin post --name <username> --limit 100 --url '<user_post_url>'
```

- name: 目标爬取用户的名称，可以自定义，仅仅用于区分不同用户，同时作为爬取数据保存的文件夹名称
- limit: 限制爬取最新专栏数
- url: 目标爬取用户的接口地址，这个参数真正决定了要爬取谁的专栏

url 获取方式如下：

![](http://cdn.kenblog.top/juejin_post_url.png)

为了快速体验爬取效果，也提供了 url 缺省情况下的支持，爬取用户 [ken](https://juejin.im/user/5bd2b8b25188252a784d19d7/posts) 的专栏：

``` sh
kcrawler juejin post --name ken --limit 100
```

爬取明细数据，会在 `ken` 目录下，以爬取日期和时间命名，同时保存 `.csv` 文件和 `.xls` 文件。

#### 2.2.3 指定城市爬取安居客小区房价

首先需要获取[网站](https://shenzhen.anjuke.com/community/p50/)的 `cookie` 。获取方式参考[《python 自动抓取分析房价数据——安居客版 》2.4 小节](https://juejin.im/post/5d7f021bf265da03cf7abed2#heading-9)。


将 `<anjuke_cookie>` 替换成自己 `cookie`，运行如下命令：

``` sh
kcrawler anjuke --city shenzhen --limit 50 --cookie "<anjuke_cookie>"
```

也可以将 `cookie` 保存在当前目录下的 `anjuke_cookie` (无后缀)文件中，运行如下命令：

``` sh
kcrawler anjuke --city shenzhen --limit 50
```

![](http://cdn.kenblog.top/kcrawler_anjuke_shenzhen.gif)

![](http://cdn.kenblog.top/sz_com_927.png)

命令成功运行成功后，会显示房价平均值，最大值，最小值，并绘制房价分布直方图，关闭直方图后，明细数据将保存在当前目录下，形如：`anjuke_shenzhen_community_price_20xx-xx-xx.csv`。

> 获取其他城市的房价，只需将 `city` 参数改成安居客网站覆盖的城市拼音。可打开页面 [https://www.anjuke.com/sy-city.html](https://www.anjuke.com/sy-city.html) ，点击需要获取的城市，复制浏览器地址栏中城市对应的二级域名，如 beijing.anjuke.com 只取 beijing 作为 city 参数。

## 3. 导入 python 模块

### 3.1 Boss 接口

``` python
from kcrawler import Boss
boss  = Boss()

boss_positions = boss.position()
boss_cities = boss.city()
boss_hotcities = boss.hotcity()
boss_industries = boss.industry()
boss_user_city = boss.userCity()
boss_expects = boss.expect()

jobs = boss.job(0, 1)
tencent_jobs = boss.queryjob(query='腾讯', city=101280600, industry=None, position=101301)
tencent_jobs = boss.queryjobpage(query='腾讯', city=101280600, industry=None, position=101301, page=2)

jobcard = boss.jobcard('3c2016bbf8413f3b1XR63t-1FVI~', '505ee74b-504b-4aea-921c-a3dc2016be80.f1:common-155-GroupA--157-GroupA.15')
```

## Release history

[https://pypi.org/project/kcrawler/#history](https://pypi.org/project/kcrawler/#history)

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2019 kenblikylee
