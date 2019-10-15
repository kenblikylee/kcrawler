from abc import ABCMeta, abstractmethod
import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from io import BytesIO

def read_file(file_path):
    with open(file_path) as f:
        content = f.read().strip()
    return content

def parse_headers(headers_raw):
    headers = {}
    for row in headers_raw.split('\n'):
        row = row.strip(':| ')
        if row:
            k, v = tuple(row.split(':', 1))
            headers[k.strip()] = str(v).strip()
    return headers

def parse_tree(tree, k='id', ck='children', attrs='name'):
    res = []
    for d in tree:
        node = dict()
        node['id'] = d[k]
        if isinstance(attrs, str):
            node[attrs] = d[attrs]
        elif isinstance(attrs, list):
            for attr in attrs:
                node[attr] = d[attr]
        if ck and ck in d and d[ck] and len(d[ck]):
            node['children'] = parse_tree(d[ck], k, ck, attrs)
        res.append(node)
    return res

class ABCrawler(metaclass = ABCMeta):
    def __init__(self, config):
        self._config = self._init(config)
    def _info(self, text):
        print('\u001b[30m{}\u001b[0m'.format(text))
    def _warn(self, text):
        print('\u001b[31m{}\u001b[0m'.format(text))
    def _tips(self, text):
        print('\u001b[32m{}\u001b[0m'.format(text))
    def _init(self, config):
        if 'headers' in config:
            headers = config['headers']
            if isinstance(headers, str):
                self._info('parse headers')
                config['headers'] = parse_headers(headers)
            else:
                self._tips('headers has parseed')
        if 'targets' in config:
            self._targets = config['targets']
        else:
            self._warn('no targets')
        return config
    @abstractmethod
    def crawl(self, target, payload=None, urlparts=None):
        if not target or \
            target not in self._targets:
            self._warn('invalid target')
            return
        target = self._targets[target]
        try:
            url = target['url']
            method = target['method'].lower()
            content_type = target['type']
            if callable(url):
                if not isinstance(urlparts, list):
                    self._warn('callable url require urlparts to be list')
                    return
                url = url(urlparts)
                # self._tips(url)
        except:
            self._warn('url, method and type is required')
            return
        if method not in ['get', 'post']:
            self._warn('unsupported method')
            return

        headers = self._config['headers']
        if method == 'get':
            if payload:
                res = requests.get(url, headers=headers, params=payload)
            else:
                res = requests.get(url, headers=headers)
        elif method == 'post':
            if payload:
                res = requests.get(url, headers=headers, data=payload)
            else:
                res = requests.get(url, headers=headers)

        if res.status_code != 200:
            self._warn('http status code: {}'.format(res.status_code))
            return

        if not content_type or \
            content_type not in ['html', 'json', 'bin', 'image']:
            return res
        if content_type == 'html':
            return bs(res.text, features='lxml') # 'html.parser'
        elif content_type == 'json':
            return res.json()
        elif content_type == 'bin':
            return res.content
        elif content_type == 'image':
            return Image.open(BytesIO(res.content))

class Crawler(ABCrawler):
    def crawl(self, target, payload=None, urlparts=None):
        return super().crawl(target, payload, urlparts)
