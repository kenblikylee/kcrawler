#!/usr/local/bin/python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import time
import argparse

def get_headers(city, page, cookie):
    headers = {
        'authority': '{}.anjuke.com'.format(city),
        'method': 'GET',
        'path': '/community/p{}/'.format(page),
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': cookie,
        'pragma': 'no-cache',
        'referer': 'https://{}.anjuke.com/community/p{}/'.format(city, page),
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    return headers

def get_html_by_page(city, page, cookie):
    headers = get_headers(city, page, cookie)
    url = 'https://{}.anjuke.com/community/p{}/'.format(city, page)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print('页面不存在！')
        return None
    return res.text

def extract_data_from_html(html):
    soup = BeautifulSoup(html, features='lxml')
    list_content = soup.find(id="list-content")
    if not list_content:
        print('list-content elemet not found!')
        return None
    items = list_content.find_all('div', class_='li-itemmod')
    if len(items) == 0:
        print('items is empty!')
        return None
    return [extract_data(item) for item in items]

def extract_data(item):
    name = item.find_all('a')[1].text.strip()
    address = item.address.text.strip()
    if item.strong is not None:
        price = item.strong.text.strip()
    else:
        price = None
    finish_date = item.p.text.strip().split('：')[1]
    latitude, longitude = [d.split('=')[1] for d in item.find_all('a')[3].attrs['href'].split('#')[1].split('&')[:2]]
    return name, address, price, finish_date, latitude, longitude

def is_in_notebook():
    import sys
    return 'ipykernel' in sys.modules

def clear_output():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    if is_in_notebook():
        from IPython.display import clear_output as clear
        clear()

def crawl_all_page(city, cookie, limit=0):
    page = 1
    data_raw = []
    while True:
        try:
            if limit != 0 and (page-1 == limit):
                break
            html = get_html_by_page(city, page, cookie)
            data_page = extract_data_from_html(html)
            if not data_page:
                break
            data_raw += data_page
            clear_output()
            print('crawling {}th page ...'.format(page))
            page += 1
        except:
            print('maybe cookie expired!')
            break
    print('crawl {} pages in total.'.format(page-1))
    return data_raw

def create_df(data):
    columns = ['name', 'address', 'price', 'finish_date', 'latitude', 'longitude']
    return pd.DataFrame(data, columns=columns)

def clean_data(df):
    df.dropna(subset=['price'], inplace=True)
    df = df.astype({'price': 'float64', 'latitude': 'float64', 'longitude': 'float64'})
    return df

def visual(df):
    fig, ax = plt.subplots()
    df.plot(y='price', ax=ax, bins=20, kind='hist', label='房价频率直方图', legend=False)
    ax.set_title('房价分布直方图')
    ax.set_xlabel('房价')
    ax.set_ylabel('频率')
    plt.grid()
    plt.show()

def run(city, cookie, limit):
    data = crawl_all_page(city, cookie, limit)
    if len(data) == 0:
        print('empty: crawled noting!')
        return
    df = create_df(data)
    df = clean_data(df)
    visual(df)

    _price = df['price']
    _max, _min, _average, _median, _std = _price.max(), _price.min(), _price.mean(), _price.median(), _price.std()
    print('\n{} house price statistics\n-------'.format(city))
    print('count:\t{}'.format(df.shape[0]))
    print('max:\t¥{}\nmin:\t¥{}\naverage:\t¥{}\nmedian:\t¥{}\nstd:\t¥{}\n'.format(_max, _min, round(_average, 1), _median, round(_std, 1)))
    
    df.sort_values('price', inplace=True)
    df.reset_index(drop=True, inplace=True)
    #  保存 csv 文件
    dt = time.strftime("%Y-%m-%d", time.localtime())
    csv_file = 'anjuke_{}_community_price_{}.csv'.format(city, dt)
    df.to_csv(csv_file, index=False)

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city', type=str, help='city.')
    parser.add_argument('-k', '--cookie', type=str, help='cookie.')
    parser.add_argument('-l', '--limit', type=int, default=0, help='page limit (30 records per page).')
    args = parser.parse_args()
    return args

def read_cookie(cookie_file='anjuke_cookie'):
    print("\nread cookie from file {} ...\n".format(cookie_file))
    with open(cookie_file) as f:
        cookie = f.read().strip()
    return cookie

def main(args):
    city, cookie, limit = '', '', 0
    if 'cookie' in args:
        cookie = args['cookie']
    else:
        cookie = read_cookie()
    if 'city' in args:
        city = args['city']
    else:
        print('--city required.')
        return
    if 'limit' in args:
        limit = int(args['limit'])
    run(city, cookie, limit)

if __name__ == '__main__':
    args = get_cli_args()
    if args.cookie is None:
        cookie = read_cookie()
    else:
        cookie = args.cookie
    run(args.city, cookie, args.limit)
