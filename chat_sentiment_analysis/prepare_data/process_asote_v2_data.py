import os
import json
from collections import defaultdict

from chat_sentiment_analysis.common import common_path
from chat_sentiment_analysis.utils import file_utils


if __name__ == '__main__':
    base_input_dir = os.path.join(common_path.data_dir, 'original_data', 'ASOTE-v2')
    filepath_template = '{base_input_dir}/{dataset_name}/asote_gold_standard/train.txt'
    dataset_names = ['lapt14', 'rest14']
    instructions = []
    sentences = []
    responses = []
    max_instance_per_dataset = 100
    for dataset_name in dataset_names:
        filepath = filepath_template.format(base_input_dir=base_input_dir, dataset_name=dataset_name)
        lines = file_utils.read_all_lines(filepath)
        sentence_and_aspects = defaultdict(list)
        for line in lines:
            line_obj = json.loads(line)
            sentence_and_aspects[line_obj['sentence']].append(line_obj)

        sentence_num = 0
        for sentence, aspects in sentence_and_aspects.items():
            # aspect term extraction
            instruction = 'extract aspect terms from the sentence'
            instructions.append(instruction)
            sentences.append(sentence)
            aspect_terms = []
            for aspect in aspects:
                if 'aspect_term' not in aspect:
                    continue
                aspect_term = aspect['aspect_term']['term']
                aspect_terms.append(aspect_term)
            if len(aspect_terms) > 0:
                responses.append(','.join(aspect_terms))
            else:
                responses.append('there are no aspect terms in the sentence.')

            # aspect term-opinion term pair extraction
            instruction = 'extract aspect term-opinion term pairs from the sentence'
            instructions.append(instruction)
            sentences.append(sentence)
            pairs = []
            for aspect in aspects:
                if 'opinions' not in aspect:
                    continue
                opinions = aspect['opinions']
                for opinion in opinions:
                    if 'opinion_term' not in opinion:
                        continue
                    aspect_term = opinion['aspect_term']['term']
                    opinion_term = opinion['opinion_term']['term']
                    pair = '(%s, %s)' % (aspect_term, opinion_term)
                    pairs.append(pair)
            if len(pairs) > 0:
                responses.append(';'.join(pairs))
            else:
                responses.append('there are no aspect term-opinion term pairs in the sentence.')

            # aspect term, sentiment, opinion term triplet extraction
            instruction = 'extract aspect term, sentiment, opinion term triplets from the sentence'
            instructions.append(instruction)
            sentences.append(sentence)
            triplets = []
            for aspect in aspects:
                if 'opinions' not in aspect:
                    continue
                opinions = aspect['opinions']
                for opinion in opinions:
                    if 'opinion_term' not in opinion:
                        continue
                    aspect_term = opinion['aspect_term']['term']
                    opinion_term = opinion['opinion_term']['term']
                    triplet = '(%s, %s, %s)' % (aspect_term, opinion['polarity'], opinion_term)
                    triplets.append(triplet)
            if len(triplets) > 0:
                responses.append(';'.join(triplets))
            else:
                responses.append('there are no aspect term, sentiment, opinion term triplets in the sentence.')
    output_lines = []
    for i , instruction in enumerate(instructions):
        instance = {
            'instruction': instruction,
            'input': sentences[i],
            'output': responses[i]
        }
        output_lines.append(json.dumps(instance))

    output_dir = os.path.join(common_path.data_dir, 'task_data')
    output_filepath = os.path.join(output_dir, 'task_data.json')
    file_utils.write_lines(output_lines, output_filepath)
