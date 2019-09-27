# kcrawler

[![Build Status](https://travis-ci.org/kenblikylee/kcrawler.svg?branch=master)](https://travis-ci.org/kenblikylee/kcrawler)
[![license](https://img.shields.io/github/license/kenblikylee/kcrawler)](https://github.com/kenblikylee/kcrawler/blob/master/LICENSE)

A python crawler authored by Ken.

## 1. 安装

``` sh
pip install kcrawler
# or
pip install --index-url https://pypi.org/simple kcrawler
```

更新:

``` sh
pip install --upgrade kcrawler
```

## 2. 使用

### 2.1 命令行

#### 2.1.1 指定城市爬取安居客小区房价

```python
kcrawler anjuke --city shenzhen --limit 50
```
数据保存在当前目录下，格式如下：

anjuke_shenzhen_community_price_20xx-xx-xx.csv

#### 2.1.2 爬取掘金专栏阅读量

```python
kcrawler juejin post --name ken --limit 100

kcrawler juejin post --name ken --limit 100 --url 'https://timeline-merger-ms.juejin.im/v1/get_entry_by_self?src=web&uid=5bd2b8b25188252a784d19d7&device_id=1567748420039&token=eyJhY2Nlc3NfdG9rZW4iOiJTTHVPcVRGQ1BseWdTZHF4IiwicmVmcmVzaF90b2tlbiI6ImJHZkJDVDlWQkZiQUNMdTYiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ%3D%3D&targetUid=5bd2b8b25188252a784d19d7&type=post&limit=20&order=createdAt'

```

数据保存在当前目录下，name 参数指定的子目录下，如: ./ken

#### 2.1.3 爬取掘金小册销售数据

``` python
kcrawler juejin book
```

数据保存在当前目录下，格式如下：

juejin_books_20xx-xx-xx.xls
