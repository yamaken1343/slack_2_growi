import datetime

import requests
from config import GROWI_API_KEY, SLACK_TOKEN, GROWI_URL, SLACK_CHANNEL_ID, GROWI_PATH


# Growiから現在のバージョンのページを取得する
def get_previous_page(path):
    url = GROWI_URL + '/_api/pages.get'
    params = {'access_token': GROWI_API_KEY,
              'path': path}

    response = requests.get(url, params)
    r = response.json()
    page_id = r['page']['id']
    revision_id = r['page']['revision']['_id']
    pre_page_body = r['page']['revision']['body']
    return page_id, revision_id, pre_page_body


# append_bodyを追記してGrowiのページを更新する
def content_update(path, append_body):
    url = GROWI_URL + '/_api/pages.update'

    p_id, rev_id, pre_body = get_previous_page(path)
    post_data = {'access_token': GROWI_API_KEY,
                 'page_id': p_id,
                 'revision_id': rev_id,
                 'body': pre_body + '\n' + append_body,
                 'grant': '1'}

    r = requests.post(url, post_data)

    print(r.status_code)


# Slackから昨日投稿されたポストに含まれるリンクのタイトル,URL,冒頭の文をリストとして取得する
def get_yesterday_post():
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)

    unix_today = datetime.datetime.combine(today, datetime.time()).timestamp()
    unix_yesterday = datetime.datetime.combine(yesterday, datetime.time())

    url = 'https://slack.com/api/channels.history'

    # params = {'token': SLACK_TOKEN,
    #           'channel': SLACK_CHANNEL_ID,
    #           'latest': unix_today,
    #           'oldest': unix_yesterday}

    # for Debug
    params = {'token': SLACK_TOKEN,
              'channel': SLACK_CHANNEL_ID}

    response = requests.get(url, params)
    r_text = response.json()
    r_messages = r_text['messages']
    news_list = []
    for m in r_messages:
        if 'attachments' not in m.keys():
            continue
        for a in m['attachments']:
            news_title = a['title']
            news_title_link = a['title_link']
            news_text = a['text']
            # print(a['title'], a['title_link'], a['text'])
            news_list.append({'title': news_title, 'link': news_title_link, 'text': news_text})

    return news_list


# get_yesterday_postで取得したリストをWikiの投稿に適した形に修正
def list_2_md(news_list):
    if not news_list:
        return -1
    today = datetime.date.today()
    md = '## {}\n'.format(today)
    for n in news_list:
        md += '### {}\n{}\n{}\n'.format(n['title'], n['link'], n['text'])

    return md


def slack_2_wiki():
    news_list = get_yesterday_post()
    update_sentence = list_2_md(news_list)
    content_update(GROWI_PATH, update_sentence)


if __name__ == '__main__':
    slack_2_wiki()
