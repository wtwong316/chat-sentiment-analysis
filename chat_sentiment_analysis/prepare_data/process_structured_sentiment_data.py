import json
import os

from chat_sentiment_analysis.common import common_path
from chat_sentiment_analysis.utils import file_utils


def read_file(filepath):
    """

    :param filepath:
    :return:
    """
    with open(filepath) as input_file:
        result = json.load(input_file)
    return result


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
        result = sentence.split()[start: end]
    return result


def parse_line(line: str):
    """

    :param line:
    :return:
    """
    result = {}
    sentence = line['text']
    result['sentence'] = sentence

    opinions = line['opinions']
    if len(opinions) == 0:
        response = 'there are no tuples'
    else:
        quadruples = []
        for quadruple in opinions:
            holder = 'None' if len(quadruple['Source'][0]) == 0 else '_'.join(quadruple['Source'][0])
            target = 'None' if len(quadruple['Target'][0]) == 0 else '_'.join(quadruple['Target'][0])
            if not target:
                print()
            expression = 'None' if len(quadruple['Polar_expression'][0]) == 0 else '_'.join(quadruple['Polar_expression'][0])
            polarity = quadruple['Polarity']
            quadruples.append('(%s, %s, %s, %s)' % (holder, target, expression, polarity))
        response = '; '.join(quadruples)
    result['response'] = response
    return result


if __name__ == '__main__':
    instructions = []
    sentences = []
    responses = []
    dataset_names = ['opener_en']
    filepath_template = os.path.join(common_path.project_dir,
                                     'data/original_data/semeval22_structured_sentiment'
                                     '/{dataset_name}/train.json')
    for dataset_name in dataset_names:
        filepath = filepath_template.format(dataset_name=dataset_name)
        lines = read_file(filepath)
        for line in lines:
            parsed_line = parse_line(line)
            # (h, t, e, p)
            #  h is a holder who expresses a polarity p towards a target t through a sentiment expression
            instructions.append('extract holder-target-Opinion-Sentiment Quadruple from the sentence')
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
    output_filepath = os.path.join(output_dir, 'htep.json')
    file_utils.write_lines(output_lines, output_filepath)
