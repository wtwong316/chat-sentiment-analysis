import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# project_dir = '/my-alpaca/MyDrive/my-alpaca'

templates_dir = os.path.join(project_dir, 'chat_sentiment_analysis', 'templates')

if __name__ == '__main__':
    print(project_dir)
