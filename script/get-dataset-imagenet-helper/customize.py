from mlc import utils
import os


def postprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    script_path = env['MLC_TMP_CURRENT_SCRIPT_PATH']

    env['MLC_DATASET_IMAGENET_HELPER_PATH'] = script_path
    env['+PYTHONPATH'] = [script_path]

    logger.info(f"Set ImageNet helper path to {script_path}")
    logger.info("Added ImageNet helper path to PYTHONPATH")

    return {'return': 0}
