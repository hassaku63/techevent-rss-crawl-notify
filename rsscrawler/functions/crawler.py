import json
import feedparser

from rsscrawler.libs import queue
from rsscrawler.log import get_logger
log = get_logger(__name__)


# とりあえず Connpass のみ考える
feed_urls = {
    # 'TechPlay': 'https://rss.techplay.jp/event/w3c-rss-format/rss.xml',
    'Connpass/SRE.fm': 'https://sre-fm.connpass.com/ja.atom',
    'Connpass/Serverless': 'https://serverless.connpass.com/ja.atom',
    'Connpass/DDD-Community-Jp': 'https://ddd-community-jp.connpass.com/ja.atom',
    'Connpass/Kubernetes Meetup Tokyo': 'https://k8sjp.connpass.com/ja.atom',
    'Connpass/Microservices Meetup': 'https://microservices-meetup.connpass.com/ja.atom',
    'Connpass/PyCon JP': 'https://pyconjp.connpass.com/ja.atom',
    'Connpass/Machine Learning for Beginners!': 'https://mlforbiginners.connpass.com/ja.atom',
    'Connpass/LAPRAS': 'https://lapras.connpass.com/ja.atom',
    'Connpass/株式会社Serverless Operations': 'https://slsops.connpass.com/ja.atom',
    'Connpass/PyData.Tokyo': 'https://pydatatokyo.connpass.com/ja.atom',
    'Connpass/Forkwell': 'https://forkwell.connpass.com/ja.atom',
    'Connpass/TDDBC': 'https://tddbc.connpass.com/ja.atom',
    'Connpass/Kubernetes Meetup Novice': 'https://k8s-novice-jp.connpass.com/ja.atom',
    'Connpass/Amplify Meetup': 'https://aws-amplify-jp.connpass.com/ja.atom',
    'Connpass/Cloud Native Bright Future Meetup': 'https://cnbfmeetup.connpass.com/ja.atom',
    'Connpass/OpenID Foundation Japan': 'https://openid.connpass.com/ja.atom',
    'Connpass/Japan Datadog User Group': 'https://datadog-jp.connpass.com/ja.atom',
    'Connpass/aws-serverless': 'https://aws-serverless.connpass.com/ja.atom',
    'Connpass/M3 Engineer': 'https://m3-engineer.connpass.com/ja.atom',
    'Connpass/メルカリ／Mercari': 'https://mercari.connpass.com/ja.atom',
    'Connpass/Serverless LT初心者向け': 'https://serverlesslt.connpass.com/ja.atom',
    'Connpass/株式会社ZOZOテクノロジーズ': 'https://zozotech-inc.connpass.com/ja.atom',
    'Connpass/Containers on AWS': 'https://aws-container.connpass.com/ja.atom',
    'Connpass/Container Runtime Meetup': 'https://runtime.connpass.com/ja.atom',
    'Connpass/Oracle Code Night': 'https://oracle-code-tokyo-dev.connpass.com/ja.atom',
    'Connpass/PostgreSQLアンカンファレンス': 'https://pgunconf.connpass.com/ja.atom',
    'Connpass/VS Code Meetup': 'https://vscode.connpass.com/ja.atom',
    'Connpass/JAWS-UG コンテナ支部': 'https://jawsug-container.connpass.com/ja.atom',
    'Connpass/AWS Front-end Community': 'https://aws-amplify-jp.connpass.com/ja.atom',
    'Connpass/技術書典' : 'https://techbookfest.connpass.com/ja.atom',
    'Connpass/GYOMU Hackers Guild': 'https://gyomu-hackers-guild.connpass.com/ja.atom',
    'Connpass/Hatena Engineer Seminar': 'https://hatena.connpass.com/ja.atom',
    'Connpass/ssmjp': 'https://ssmjp.connpass.com/ja.atom',
    'Connpass/CloudNative Days': 'https://cloudnativedays.connpass.com/',
    'Connpass/Cloud Native Developers JP': 'https://cnd.connpass.com/ja.atom',
    'Connpass/サービス開発フリートーク': 'https://sdf.connpass.com/',
    'Connpass/ラクス': 'https://rakus.connpass.com/ja.atom',
    'Connpass/CircleCI': 'https://circleci.connpass.com/ja.atom',
    'Connpass/検索技術勉強会': 'https://search-tech.connpass.com/ja.atom'
}


def handler(event, context):
    for name, url in feed_urls.items():
        log.info(url)
        feed = feedparser.parse(url)
        # log.info(json.dumps(dict(feed.feed)))
        fdict = {}
        try:
            fdict = json.loads(json.dumps(feed))
        except Exception as e:
            log.error(f'json format error: {name}, {url}')
            log.error(e)
            continue
        data = {
            'name': name,
            'feed': fdict['feed'],
            'entries': []
        }
        for ent in fdict['entries']:
            data['entries'].append({
                'title': ent['title'],
                # 'title_detail': ent.get('title_detail', ''),
                'link': ent['link'],
                'id': ent['id'],
                # 'summary': ent['summary'],
                # 'summary_detail': ent.get('summary_detail', ''),
                'published': ent.get('published', None),
                'published_parsed': ent.get('published_parsed', None),
                'tags': ent.get('tags', []),
                'authors': ent.get('authors', None),
                'tp_eventdate': ent.get('tp_eventdate', None),
                'tp_eventstarttime': ent.get('tp_eventstarttime', None),
                'tp_eventendtime': ent.get('tp_eventendtime', None),
                'tp_eventplace': ent.get('tp_eventplace', None),
                'tp_eventaddress': ent.get('tp_eventaddress', None)
            })

        queue.send_rss(data)
        log.info({
            'event': 'Send rss info to queue',
            'message': f'{name}'
        })


if __name__ == '__main__':
    handler({}, {})