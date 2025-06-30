import datetime as dt
import time
import requests
import os
import pandas as pd
from rich import print
from urllib.parse import urlparse
from airflow.decorators import dag, task
from airflow.utils import timezone
from datetime import timedelta


def extract_domain(url):
    # Добавляем схему, если её нет (для корректного парсинга)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Парсим URL
    parsed_url = urlparse(url)

    # Получаем домен и убираем www., если нужно
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]

    return 'https://' + domain

def adprofex_change_domain(teaser_id, new_url):

  json_data = {
      'ids': [
          teaser_id,
      ],
      'url': new_url
  }

  response = requests.post('https://adv-api.adprofex.com/api/ads/change-url', 
                           headers=Headers.adprofex(), 
                           json=json_data)
  print(response.text)


def get_new_domain(url, oneprofit_smart, oneprofit_news):
    if 'exp1=smart' in url:
        return oneprofit_smart
    elif 'utm_medium=2329' in url:
        return oneprofit_news
    # elif '/v1/short/' in url:
    #     return lucky_domain
    else:
        return extract_domain(url)

class Headers:
  def adprofex():
    return {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru',
        'Authorization': f'Bearer {os.getenv("ADPROFEX_TOKEN")}',
        'Connection': 'keep-alive',
        'Origin': 'https://advertiser.adprofex.com',
        'Referer': 'https://advertiser.adprofex.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
  def oneprofit():
     return {
    'Accept': 'application/json',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'Authorization': f'Bearer {os.getenv("ONEPROFIT_TOKEN")}',}

class GetTeasers:
  def __init__(self):
    self.date_today = dt.datetime.now().date()
  def adprofex(self, campaign_id=None, date_format='%d.%m.%Y'):
    date_today = self.date_today.strftime(date_format)
    params = {
        'date_from': date_today,
    }
    if campaign_id:
      params['campaign_id'] = str(campaign_id)

    response = requests.get('https://adv-api.adprofex.com/api/ads', 
                            params=params, 
                            headers=Headers.adprofex())
    return response.json()['data']


class GetDomain:
   
   def oneprofit_smart(self):
     params = {
    'page': '1',
    'is_archive': '0',
    'sort': 'false',
    'descending': '0',
    'is_smart': '1',
    'is_cpa': '0',
    'is_spo': '0',
    }
     response = requests.get('https://oneprofit.net/api/v1/setting/cabinet/sources',
                        params=params,
                        headers=Headers.oneprofit())
    #  return response
     url = response.json()['data'][0]['smart_offer_link']
     return extract_domain(url)
   
   def oneprofit_news(self):
    params = {
    'project_id': '1',
    'region_id': '1',
    }
    response = requests.get('https://oneprofit.net/api/v1/setting/purchase-domains', params=params, headers=Headers.oneprofit())
    return 'https://' + response.json()['data'][0]['name']



@dag(start_date=timezone.utcnow() - timedelta(days=1), 
     schedule="0 * * * *", 
     catchup=False)
def change_domain_dag():
  @task
  def get_teasers_from_adprofex():
    teasers = GetTeasers()
    adprofex_teasers = teasers.adprofex()
    return adprofex_teasers
  @task
  def transform_data(adprofex_teasers):
    df = pd.json_normalize(adprofex_teasers)
    # запущенные тизеры
    df = df[df['status_tooltip.primary.text'] == 'Запущен']
    # колонка где только домен
    df['domain'] = df['url'].apply(extract_domain)
    oneprofit_smart = GetDomain().oneprofit_smart()
    oneprofit_news = GetDomain().oneprofit_news()
    # колонка где новый домен
    df['new_domain'] = df['url'].apply(get_new_domain, args=(oneprofit_smart, oneprofit_news))
    df = df[df['domain'] != df['new_domain']]
    return df[['id','domain','url','new_domain']]
  @task
  def adprofex_change(df):
    count = 0
    max_count = None
    if not df.empty:
      for index, row in df.iterrows():
          teaser_url = row['url'].replace(row['domain'], row['new_domain'])
          teaser_id = row['id']
          adprofex_change_domain(teaser_id, teaser_url)
          time.sleep(3)
          count += 1
          if max_count and count == max_count:
            break
    else:
      print('df empty')

  teasers = get_teasers_from_adprofex()
  df = transform_data(teasers)
  adprofex_change(df)


change_domain_dag()