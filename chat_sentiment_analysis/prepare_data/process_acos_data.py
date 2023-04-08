import json
import os

from chat_sentiment_analysis.common import common_path
from chat_sentiment_analysis.utils import file_utils


def extract_segment_from_sentence(start, end, sentence):
    """

    :param start:
    :param end:
    :param sentence:
    :return:
    """
    result = 'None'
    start = int(start)
    end = int(end)
    if start == -1:
        return result
    else:
        result = ' '.join(sentence.split()[start: end])
    return result


def parse_line(line: str):
    """

    :param line:
    :return:
    """
    result = {}
    fields = line.split('\t')
    if len(fields) < 2:
        print()
    sentence = fields[0]
    result['sentence'] = sentence
    quadruples = []
    sentiment_mapping = {
        '0': 'negative',
        '1': 'neutral',
        '2': 'positive'
    }
    for quadruple in fields[1:]:
        quadruple = quadruple.split(' ')
        aspect_start, aspect_end = quadruple[0].split(',')
        aspect = extract_segment_from_sentence(aspect_start, aspect_end, sentence)
        category = quadruple[1]
        sentiment = sentiment_mapping[quadruple[2]]
        opinion_start, opinion_end = quadruple[3].split(',')
        opinion = extract_segment_from_sentence(opinion_start, opinion_end, sentence)
        quadruples.append('(%s, %s, %s, %s)' % (aspect, category, sentiment, opinion))
    result['response'] = '; '.join(quadruples)
    return result


if __name__ == '__main__':
    instructions = []
    sentences = []
    responses = []
    dataset_names = ['Restaurant-ACOS']
    filepath_template = os.path.join(common_path.project_dir,
                                     'data/original_data/acos/{dataset_name}/rest16_quad_train.tsv')
    for dataset_name in dataset_names:
        filepath = filepath_template.format(dataset_name=dataset_name)
        lines = file_utils.read_all_lines(filepath)
        for line in lines:
            parsed_line = parse_line(line)
            instructions.append('extract Aspect-Category-Opinion-Sentiment Quadruple from the sentence')
            sentences.append(parsed_line['sentence'])
            responses.append(parsed_line['response'])

    output_lines = []
    for i, instruction in enumerate(instructions):
        instance = {
            'instruction': instruction,
            'input': sentences[i],
            'output': responses[i]
        }
        output_lines.append(json.dumps(instance))

    output_dir = os.path.join(common_path.data_dir, 'task_data')
    output_filepath = os.path.join(output_dir, 'acos.json')
    file_utils.write_lines(output_lines, output_filepath)
