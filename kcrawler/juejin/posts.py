#!/usr/local/bin/python

import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import argparse
import os
from .urlparser import rebuild_juejin_url

headers = {
    'Origin': 'https://juejin.im',
    'Referer': 'https://juejin.im/user/5bd2b8b25188252a784d19d7/posts',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
}

def anlysis_by_url(url, name='', visual=False, **argkw):
    print("\n=============================================================\n")
    print("postcrawler v0.1\n")
    print("author: kenbliky\n")
    print("\n=============================================================\n")
    url = rebuild_juejin_url(url, **argkw)
    res = requests.get(url, headers=headers)
    print("\ncrawl posts data on juejin.\n-----------\nget posts from {} ...\n".format(url))
    if res.status_code != 200:
        print('数据获取失败，请检查token是否失效')
        return

    json_data = res.json()

    article_list = json_data['d']['entrylist']
    total = json_data['d']['total']
    if not total or (total == 0):
        print('{} has no posts!\n'.format(name))
        return
    print('got {} posts.\n'.format(total))
    interest_list = [(article['title'], article['viewsCount'], article['rankIndex'], article['createdAt'])
                     for article in article_list]
    df = pd.DataFrame(interest_list, columns=['title', 'viewsCount', 'rankIndex', 'createdAt'])
    df_sort_desc = df.sort_values('viewsCount', ascending=False).reset_index(drop=True)
    
    if visual:
        print('data visualization ...\n')
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))

        plt.subplots_adjust(wspace=0.5, hspace=0.5)

        df = df.sort_values('viewsCount')

        df.plot(subplots=True, ax=axes[0], x='title', y='viewsCount', kind='barh', legend=False)

        df.plot(subplots=True, ax=axes[1], labels=df['title'], y='viewsCount', kind='pie', legend=False, labeldistance=1.2)

        plt.subplots_adjust(left=0.3)
        plt.show()

    # 如果 name 不为空字符串，创建子目录
    save_dir = os.path.join('.', name)
    if name and (not os.path.isdir(save_dir)):
        os.mkdir(save_dir)

    filename = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    #  保存 csv 文件
    csv_file = filename + '.csv'
    csv_path = os.path.join(save_dir, csv_file)
    df_sort_desc.to_csv(csv_path, index=False)
    print("saved to {}.\n".format(csv_path))
    # 保存 excel 文件
    excel_file = filename + '.xls'
    excel_path = os.path.join(save_dir, excel_file)
    sheet_name = time.strftime("%Y-%m-%d", time.localtime())
    df_sort_desc.to_excel(excel_path, sheet_name=sheet_name, index=False)
    print("saved to {}.\n".format(excel_path))
    print("\n-----------\npersonal website: https://kenblog.top\njuejin: https://juejin.im/user/5bd2b8b25188252a784d19d7")

juejin_zhuanlan_api_full_url = 'https://timeline-merger-ms.juejin.im/v1/get_entry_by_self?src=web&uid=5bd2b8b25188252a784d19d7&device_id=1567748420039&token=eyJhY2Nlc3NfdG9rZW4iOiJTTHVPcVRGQ1BseWdTZHF4IiwicmVmcmVzaF90b2tlbiI6ImJHZkJDVDlWQkZiQUNMdTYiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ%3D%3D&targetUid=5bd2b8b25188252a784d19d7&type=post&limit=20&order=createdAt'

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, default=juejin_zhuanlan_api_full_url, help='URL.')
    parser.add_argument('-n', '--name', type=str, default='', help='name, to create a sub directory.')
    parser.add_argument('-l', '--limit', type=int, default=20, help='limit of posts.')
    parser.add_argument('-f', '--file', type=str, default='', help='crawl posts from file.')
    parser.add_argument('-v', '--visual', nargs='?', type=bool, default=False, help='data visualization on.')
    args = parser.parse_args()
    return args

def read_file(path):
    with open(path, 'r') as f:
        res = []
        for line in f.readlines():
            cols = line.split(',')
            row = tuple([col.strip() for col in cols])
            res.append(row)
    return res

def main(args):
    url, name, limit, _file, vis = juejin_zhuanlan_api_full_url, '', 20, '', False
    if 'url' in args:
        url = args['url']
    if 'name' in args:
        name = args['name']
    if 'limit' in args:
        limit = int(args['limit'])
    if 'file' in args:
        _file = args['file']
    if 'visual' in args:
        vis = True

    if _file and os.path.isfile(_file):
        plist = read_file(_file)
        for (name, url) in plist:
            anlysis_by_url(url, name, vis, limit=limit)
    anlysis_by_url(url, name, vis, limit=limit)

if __name__ == '__main__':
    args = get_cli_args()
    file = args.file
    vis = args.visual
    if vis is None:
        vis = True
    if file and os.path.isfile(file):
        plist = read_file(file)
        for (name, url) in plist:
            anlysis_by_url(url, name, vis, limit=args.limit)
    else:
        anlysis_by_url(args.url, args.name, vis, limit=args.limit)
