from mlc import utils
import os
import shutil


def preprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    logger.info("Preparing to set up OpenOrca dataset")
    return {'return': 0}


def postprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    if env.get('MLC_DATASET_CALIBRATION', '') == "no":
        env['MLC_DATASET_PATH_ROOT'] = env['MLC_DATASET_OPENORCA_PATH']
        env['MLC_DATASET_PATH'] = env['MLC_DATASET_OPENORCA_PATH']
        env['MLC_DATASET_OPENORCA_PARQUET'] = os.path.join(
            env['MLC_DATASET_OPENORCA_PATH'], '1M-GPT4-Augmented.parquet')
        logger.info(f"Set OpenOrca dataset paths: root={env['MLC_DATASET_PATH_ROOT']}, path={env['MLC_DATASET_PATH']}")
        logger.info(f"Set OpenOrca parquet file path to {env['MLC_DATASET_OPENORCA_PARQUET']}")
    else:
        env['MLC_CALIBRATION_DATASET_PATH'] = os.path.join(
            os.getcwd(), 'install', 'calibration', 'data')
        logger.info(f"Set calibration dataset path to {env['MLC_CALIBRATION_DATASET_PATH']}")

    return {'return': 0}
