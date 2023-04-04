import json
import os

from chat_sentiment_analysis.prepare_data.data_object import get_dataset_class_by_name
from chat_sentiment_analysis.common import common_path
from chat_sentiment_analysis.utils import file_utils


if __name__ == '__main__':
    instructions = []
    sentences = []
    responses = []
    dataset_names = ['SemEval-2014-Task-4-REST']
    for dataset_name in dataset_names:
        dataset = get_dataset_class_by_name(dataset_name)()
        training_set = dataset.train_data
        for doc in training_set:
            absa_sentences = doc.absa_sentences
            for absa_sentence in absa_sentences:
                sentence = absa_sentence.text.strip()
                aspect_categories = []
                aspect_sentiment_pairs = []
                for category in absa_sentence.aspect_categories:
                    aspect_categories.append(category.category)
                    aspect_sentiment_pairs.append('(%s, %s)' % (category.category, category.polarity))

                instruction = 'detect aspect categories from the sentence'
                if len(aspect_categories) > 0:
                    response = ','.join(aspect_categories)
                else:
                    response = 'There are no aspect categories in the sentence'
                sentences.append(sentence)
                instructions.append(instruction)
                responses.append(response)

                instruction = 'detect aspect category-sentiment pairs from the sentence'
                if len(aspect_sentiment_pairs) > 0:
                    response = '; '.join(aspect_sentiment_pairs)
                else:
                    response = 'There are no aspect category-sentiment pairs in the sentence'
                sentences.append(sentence)
                instructions.append(instruction)
                responses.append(response)

    output_lines = []
    for i, instruction in enumerate(instructions):
        instance = {
            'instruction': instruction,
            'input': sentences[i],
            'output': responses[i]
        }
        output_lines.append(json.dumps(instance))

    output_dir = os.path.join(common_path.data_dir, 'task_data')
    output_filepath = os.path.join(output_dir, 'acsa.json')
    file_utils.write_lines(output_lines, output_filepath)
