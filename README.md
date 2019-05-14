# Slack to Growi
Slackの指定したチャンネルに昨日投稿されたリンクをGrowiに転記する

## 使用方法
1. `CHANGE_ME_config.py`に設定内容を書き込み`config.py`にrename
2. Cron等で毎日実行

## config.py の設定内容について
- GROWI_API_KEY:
Growiのユーザ設定から取得できるAPI KEY

- GROWI_URL:
 投稿を行うGrowiのURL
- GROWI_PATH = 投稿を行うGrowiのページのPATH

例: `https://demo.growi.org/Sandbox/TestXXX`であれば, `https://demo.growi.org` がURL `/Sandbox/TestXXX` がPATH

- SLACK_TOKEN:
SlackのAPI KEY 取得方法は割愛
- SLACK_CHANNEL_ID:
チャンネルのリンクに含まれるチャンネルのID
