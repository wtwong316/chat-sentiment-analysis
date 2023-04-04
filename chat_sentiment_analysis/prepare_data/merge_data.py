import json
import os

from chat_sentiment_analysis.common import common_path
from chat_sentiment_analysis.utils import file_utils


if __name__ == '__main__':
    task_data_dir = os.path.join(common_path.data_dir, 'task_data')
    filenames = os.listdir(task_data_dir)
    output_lines = []
    for filename in filenames:
        if filename == 'task_data.json':
            continue
        filepath = os.path.join(task_data_dir, filename)
        data_part = file_utils.read_all_lines(filepath)
        output_lines.extend(data_part)

    output_dir = os.path.join(common_path.data_dir, 'task_data')
    output_filepath = os.path.join(output_dir, 'task_data.json')
    file_utils.write_lines(output_lines, output_filepath)