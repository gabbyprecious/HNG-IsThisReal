# Convert json file to spaCy format.
import plac
import logging
import argparse
import sys
import os
import json
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VOB = os.path.join(DATA_DIR, 'ner_corpus_260.json')
DB = os.path.join(DATA_DIR, 'training_data')

@plac.annotations(input_file=(VOB, "option", "i", str), output_file=(DB, "option", "o", str))

def main(input_file, output_file):
    try:
        training_data = []
        lines=[]
        with open(VOB, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                point = annotation['points'][0]
                labels = annotation['label']
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    entities.append((point['start'], point['end'] + 1 ,label))


            training_data.append((text, {"entities" : entities}))

        print(training_data)

        with open(DB, 'wb') as fp:
            pickle.dump(training_data, fp)

    except Exception as e:
        logging.exception("Unable to process " + input_file + "\n" + "error = " + str(e))
        return None
if __name__ == '__main__':
    plac.call(main)