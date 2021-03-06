import os
import pathlib
import json
import dotenv

project_root = pathlib.Path(__file__).parent / '../'

dotenv.load_dotenv()
RSSCRAWLER_STAGE = os.environ.get('RSSCRAWLER_STAGE', 'dev')

stage_env_path = project_root / f'.env.{RSSCRAWLER_STAGE}'
dotenv.load_dotenv(stage_env_path.resolve())

# Slack
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN', '')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '')
SLACK_INCOMING_WEBHOOK_URL = os.environ.get('SLACK_INCOMING_WEBHOOK_URL')

# AWS
AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')
AWS_REGION = os.environ.get('AWS_REGION')

# SQS
RSS_QUEUE_NAME = os.environ.get('RSS_QUEUE_NAME', '')


# Table
RSS_TABLE_NAME = os.environ.get('RSS_TABLE_NAME')
RSS_TABLE_GSI = os.environ.get('RSS_TABLE_GSI')

RSS_CONFIG = []
rss_config_path = project_root / 'rss.config.json'
with open(rss_config_path) as f:
    RSS_CONFIG = json.load(f)