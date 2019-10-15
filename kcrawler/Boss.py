from bs4 import BeautifulSoup as bs
import os
from .core.Crawler import Crawler, parse_tree, read_file

def _fo(x):
    p = list()
    if x[0]:
        p.append('i' + str(x[0]))
    if x[1]:
        p.append('c' + str(x[1]))
    if x[2]:
        p.append('p' + str(x[2]))
    return 'https://www.zhipin.com/{}/'.format('-'.join(p))

class Boss:
    _config = {
        'headers': 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'targets': {
            'city': {
                'url': 'https://www.zhipin.com/wapi/zpCommon/data/city.json',
                'method': 'get',
                'type': 'json'
            },
            'position': {
                'url': 'https://www.zhipin.com/wapi/zpCommon/data/position.json',
                'method': 'get',
                'type': 'json'
            },
            'industry': {
                'url': 'https://www.zhipin.com/wapi/zpCommon/data/oldindustry.json',
                'method': 'get',
                'type': 'json'
            },
            'conditions': {
                'url': 'https://www.zhipin.com/wapi/zpgeek/recommend/conditions.json',
                'method': 'get',
                'type': 'json'
            },
            'job': {
                'url': 'https://www.zhipin.com/wapi/zpgeek/recommend/job/list.json',
                'method': 'get',
                'type': 'json'
            },
            'queryjob': {
                'url': 'https://www.zhipin.com/job_detail/',
                'method': 'get',
                'type': 'html'
            },
            'queryjobpage': {
                'url': _fo,
                'method': 'get',
                'type': 'html'
            },
            'jobcard': {
                'url': 'https://www.zhipin.com/wapi/zpgeek/view/job/card.json',
                'method': 'get',
                'type': 'json'
            }
        }
    }
    _positions = None
    _cities = None
    _hotcities = None
    _industries = None
    _user_city = None
    _expects = None
    _conditions = None

    def __init__(self, headers=None):
        if headers:
            self._config['headers'] = headers
        elif os.path.isfile('headers'):
            self._config['headers'] = read_file('headers')
            print('read heades from file.')
        else:
            print('\u001b[32mno headers')
        self.crawler = Crawler(self._config)

    # 城市
    def city(self):
        if self._cities:
            return self._cities
        res = self.crawler.crawl('city')
        self._cities = parse_tree(res['zpData']['cityList'], 'code', 'subLevelModelList', ['name', 'pinyin', 'firstChar', 'rank'])
        self._hotcities = parse_tree(res['zpData']['hotCityList'], 'code', 'subLevelModelList')
        return self._cities
        
    # 热门城市
    def hotcity(self):
        if self._hotcities:
            return self._hotcities
        self.city()
        return self._hotcities
    
    # 职位类型
    def position(self):
        if self._positions:
            return self._positions
        res = self.crawler.crawl('position')
        self._positions = parse_tree(res['zpData'], 'code', 'subLevelModelList', 'name')
        return self._positions

    # 公司行业
    def industry(self):
        if self._industries:
            return self._industries
        res = self.crawler.crawl('industry')
        self._industries = parse_tree(res['zpData'], 'code', 'subLevelModelList')
        return self._industries
    
    # 筛选条件
    def conditions(self):
        if self._conditions:
            return self._conditions
        res = self.crawler.crawl('conditions')
        self._conditions = res['zpData']
        return self._conditions
    
    # 用户城市
    def userCity(self):
        if self._user_city:
            return self._user_city
        self._user_city = self.conditions()['cityConfig']
        return self._user_city

    # 期望列表
    def expect(self):
        if self._expects:
            return self._expects
        expectList = self.conditions()['expectList']
        self._expects = parse_tree(expectList, 'id', None, 'positionName')
        return self._expects
    
    # 推荐岗位
    def job(self, i, page):
        expects = self.expect()
        params = {'expectId': str(expects[i]['id']),
         'sortType': '1',
         'page': str(page),
         'salary': '',
         'degree': '',
         'experience': '',
         'stage': '',
         'scale': '',
         'districtCode': '',
         'businessCode': ''}
        res = self.crawler.crawl('job', params)
        zpData = res['zpData']
        if 'jobList' not in zpData:
            if 'message' in res:
                self.crawler._warn(res['message'])
                return
            else:
                self.crawler._warn('failed to crawl')
                return
        return parse_tree(zpData['jobList'], 'encryptJobId', None, ['jobName', 'salaryDesc', 'jobLabels', 'brandName', 'brandIndustry', 'lid'])

    # 岗位查询
    def _extractjob(self, soup):
        joblist = soup.find_all(class_='job-primary')
        res = []
        for jobitem in joblist:
            item = dict()
            item['jobName'] = jobitem.find('div', class_='job-title').text
            item['salaryDesc'] = jobitem.span.text
            item['jobLabels'] = [t for t in jobitem.p.contents if isinstance(t, str)]
            item['brandName'] = jobitem.find_all('h3')[1].text
            item['brandIndustry'] = jobitem.find_all('p')[1].contents[0]
            item['id'] = jobitem.a.attrs['data-jid']
            item['lid'] = jobitem.a.attrs['data-lid']
            res.append(item)
        return res

    def jobcard(self, jid, lid):
        res = self.crawler.crawl('jobcard', {'jid': jid, 'lid': lid})
        try:
            html = res['zpData']['html']
        except:
            self.crawler._warn(res['message'])
            return
        soup = bs(html, 'lxml')
        jobName = soup.find(class_='detail-top-title').text
        employer = soup.find(class_='detail-top-text').text
        jobDesc = soup.find(class_='detail-bottom-text').text.strip()

        return jobName, employer, jobDesc

    def queryjob(self, query=None, city=None, industry=None, position=None):
        soup = self.crawler.crawl('queryjob', dict(query=query, city=city, industry=industry, position=position))
        return self._extractjob(soup)
    def queryjobpage(self, query=None, city=None, industry=None, position=None, page=2):
        params = {'query': query, 'page': str(page), 'ka': 'page-{}'.format(page)}
        soup = self.crawler.crawl('queryjobpage', params, [industry, city, position])
        try:
            res = self._extractjob(soup)
        except:
            self.crawler._warn('failed')
            return
        return res
