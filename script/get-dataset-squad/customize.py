from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    logger.info("Preparing to set up SQuAD dataset")
    return {'return': 0}


def postprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    env['MLC_DATASET_SQUAD_PATH'] = os.path.dirname(
        env['MLC_DATASET_SQUAD_VAL_PATH'])
    env['MLC_DATASET_PATH'] = os.path.dirname(
        env['MLC_DATASET_SQUAD_VAL_PATH'])
    # env['MLC_DATASET_SQUAD_VAL_PATH'] = os.path.join(os.getcwd(), env['MLC_VAL_FILENAME'])

    logger.info(f"Set SQuAD dataset path to {env['MLC_DATASET_SQUAD_PATH']}")
    logger.info(f"Set dataset path to {env['MLC_DATASET_PATH']}")

    return {'return': 0}
