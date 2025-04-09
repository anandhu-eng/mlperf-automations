from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    logger.info("Preparing to set up BERT vocabulary")
    return {'return': 0}


def postprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    env['MLC_ML_MODEL_BERT_VOCAB_FILE_WITH_PATH'] = env['MLC_DATASET_SQUAD_VOCAB_PATH']
    logger.info(f"Set BERT vocabulary path to {env['MLC_ML_MODEL_BERT_VOCAB_FILE_WITH_PATH']}")

    return {'return': 0}
