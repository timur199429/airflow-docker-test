import datetime as dt
import requests
from airflow.models import Variable
import header



date_today = dt.datetime.now().date()

def adprofex(campaign_id=None, date_format='%d.%m.%Y'):
  date_today = date_today.strftime(date_format)
  params = {
      'date_from': date_today,
  }
  if campaign_id:
    params['campaign_id'] = str(campaign_id)

  response = requests.get('https://adv-api.adprofex.com/api/ads', 
                          params=params, 
                          headers=header.adprofex)
  return response.json()['data']

if __name__ == '__main__':
  print(adprofex())