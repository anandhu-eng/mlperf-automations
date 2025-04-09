from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    logger.info("Preparing to set up OpenImages annotations")
    return {'return': 0}


def postprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    env['MLC_DATASET_ANNOTATIONS_FILE_PATH'] = os.path.join(
        env['MLC_DATASET_ANNOTATIONS_FILE_PATH'], 'openimages-mlperf.json')
    env['MLC_DATASET_ANNOTATIONS_DIR_PATH'] = os.path.dirname(
        env['MLC_DATASET_ANNOTATIONS_FILE_PATH'])
    env['MLC_DATASET_OPENIMAGES_ANNOTATIONS_FILE_PATH'] = env['MLC_DATASET_ANNOTATIONS_FILE_PATH']
    env['MLC_DATASET_OPENIMAGES_ANNOTATIONS_DIR_PATH'] = env['MLC_DATASET_ANNOTATIONS_DIR_PATH']

    logger.info(f"Set OpenImages annotations file path to {env['MLC_DATASET_ANNOTATIONS_FILE_PATH']}")
    logger.info(f"Set OpenImages annotations directory path to {env['MLC_DATASET_ANNOTATIONS_DIR_PATH']}")

    return {'return': 0}
