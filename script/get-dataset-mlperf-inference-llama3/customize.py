from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    if os_info['platform'] == "windows":
        logger.error('Script not supported in windows yet!')
        return {'return': 1, 'error': 'Script not supported in windows yet!'}

    if env.get('MLC_DATASET_LLAMA3_PATH', '') == '':
        logger.info("No existing Llama3 dataset path found, will download")
        env['MLC_TMP_REQUIRE_DOWNLOAD'] = "yes"
    else:
        logger.info(f"Using existing Llama3 dataset at {env['MLC_DATASET_LLAMA3_PATH']}")

    if env.get('MLC_OUTDIRNAME', '') != '':
        env['MLC_DOWNLOAD_PATH'] = env['MLC_OUTDIRNAME']
        logger.info(f"Setting download path to {env['MLC_DOWNLOAD_PATH']}")

    return {'return': 0}


def postprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    if env.get('MLC_TMP_REQUIRE_DOWNLOAD', '') == "yes":
        env['MLC_DATASET_LLAMA3_PATH'] = os.path.join(
            env['MLC_DATASET_LLAMA3_PATH'], env['MLC_DATASET_FILE_NAME'])
        logger.info(f"Updated Llama3 dataset path to {env['MLC_DATASET_LLAMA3_PATH']}")

    return {'return': 0}
