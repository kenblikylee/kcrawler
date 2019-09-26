#!/usr/local/bin/python

import requests
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import time

headers = {
    'Origin': 'https://juejin.im',
    'Referer': 'https://juejin.im/books',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'
}

def decode_url(url):
    adr, query = url.split("?")
    params = { kv.split("=")[0]:kv.split("=")[1] for kv in query.split("&")}
    return adr, params

def encode_url(url, params):
    query = "&".join(["{}={}".format(k, v) for k, v in params.items()])
    return "{}?{}".format(url, query)

def get_url(alias, page, url=None):
    if url is None:
        url = 'https://xiaoce-timeline-api-ms.juejin.im/v1/getListByLastTime?uid=5bd2b8b25188252a784d19d7&client_id=1567748420039&token=eyJhY2Nlc3NfdG9rZW4iOiJTTHVPcVRGQ1BseWdTZHF4IiwicmVmcmVzaF90b2tlbiI6ImJHZkJDVDlWQkZiQUNMdTYiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ%3D%3D&src=web&alias=&pageNum=1'
    base_url, query = decode_url(url)
    query['alias'] = alias
    query['pageNum'] = str(page)
    return encode_url(base_url, query)

def get_allbooks(alias='', url=None):
    page = 1
    allbooks = []
    while True:
        books = get_books(alias, page, url)
        if books is None or (len(books) == 0):
            print('\ncrawled {} records for {} in total.'.format(len(allbooks), alias if alias != '' else 'all'))
            break
        page += 1
        allbooks += books
    return allbooks

def get_books(alias='', page=1, url=None):
    url = get_url(alias, page, url)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print('数据获取失败，请尝试提供 url 参数！')
        return None
    json_data = res.json()
    if not 'd' in json_data:
        return None
    book_list = json_data['d']
    return extract_data_from_book_list(book_list)

def extract_data_from_book_list(book_list):
    return [(book['userData']['username'], # 作者
             book['userData']['company'], # 作者所在公司
             book['userData']['jobTitle'], # 作者职业
             book['profile'], # 作者头衔
             book['title'], # 小册标题
             book['price'], # 小册价格
             book['buyCount'], # 购买数量
             book['pv'], # pv
             book['lastSectionCount'], # 最新章节数
             book['contentSize'], # 内容长度
             book['desc'], # 描述
             book['createdAt'], # 小册创建时间
             book['finishedAt'], # 小册完成时间
             book['updatedAt'], # 小册更新时间
            ) for book in book_list]

def get_allcates(url=None):
    allbooks = []
    insert_cate = lambda c, l: [(c, *t) for t in l]
    for c, t in [('frontend', '前端'),
            ('backend', '后端'),
            ('mobile', '移动开发'),
            ('blockchain', '区块链'),
            ('general', '通用')]:
        allbooks += insert_cate(t, get_allbooks(c, url=url))
    return allbooks

def analysis(allbooks):
    df = pd.DataFrame(allbooks, columns=['分类',
                                         '作者',
                                         '公司',
                                         '职业',
                                         '头衔',
                                         '小册',
                                         '价格',
                                         '购买数量',
                                         '访问量',
                                         '章节数',
                                         '字数',
                                         '介绍',
                                         '创建时间',
                                         '完成时间',
                                         '更新时间'])
    totalAmount = df['价格'] * df['购买数量']
    df.insert(8, '销售收入', totalAmount)

    dt = time.strftime("%Y-%m-%d", time.localtime())

    csv_file = 'juejin_books_{}.csv'.format(dt)
    df.to_csv(csv_file, index=False)
    print('\nsaved to csvfile {}.\n'.format(csv_file))

    excel_file = 'juejin_books_{}.xls'.format(dt)
    df.to_excel(excel_file, sheet_name=dt, index=False)
    print('\nsaved to excel {}.\n'.format(excel_file))

    try:
        df_cate_ave_price = df.groupby('分类').mean()[['价格']]
        df_cate_sum_buy = df.groupby('分类').sum()[['购买数量']]
        df_cate_sum_sales = df.groupby('分类').sum()[['销售收入']]
        
        price_average = df['价格'].mean()
        buy_total = df['购买数量'].sum()
        sales_total = df['销售收入'].sum()

        fig, axs = plt.subplots(1, 3, figsize=(12, 4))

        ax = df_cate_ave_price.plot(ax=axs[0], table=df_cate_ave_price.T.applymap(lambda x: format(round(x), ',')), kind='bar', grid=True)
        ax.set_title('小册平均价格 {}元'.format(round(price_average)))
        ax.get_xaxis().set_visible(False)
        
        ax = df_cate_sum_buy.plot(ax=axs[1], table=df_cate_sum_buy.T.applymap(lambda x: format(round(x), ',')), kind='bar', grid=True)
        ax.set_title('总购买数 {}'.format(format(buy_total, ',')))
        ax.get_xaxis().set_visible(False)
        
        ax = df_cate_sum_sales.plot(ax=axs[2], table=df_cate_sum_sales.T.applymap(lambda x: format(round(x), ',')), kind='bar', grid=True)
        ax.set_title('总销售收入 {}元'.format(format(int(round(sales_total)), ',')))
        ax.get_xaxis().set_visible(False)
        
        fig.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        plt.show()
    except:
        pass
    return df

def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='url.')
    args = parser.parse_args()
    return args

def main(args):
    url = None
    if 'url' in args:
        url = args['url']
    analysis(get_allcates(url))

if __name__ == "__main__":
    args = get_cli_args()
    analysis(get_allcates(args.url))
