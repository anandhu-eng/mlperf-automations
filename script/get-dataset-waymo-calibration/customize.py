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

    if env.get('MLC_DATASET_WAYMO_CALIBRATION_PATH', '') != '':
        if not os.path.exists(env['MLC_DATASET_WAYMO_CALIBRATION_PATH']):
            error_msg = f"Path {env['MLC_DATASET_WAYMO_CALIBRATION_PATH']} does not exist!"
            logger.error(error_msg)
            return {'return': 1, 'error': error_msg}
        logger.info(f"Using existing Waymo calibration dataset at {env['MLC_DATASET_WAYMO_CALIBRATION_PATH']}")
    else:
        logger.info("No existing Waymo calibration dataset found, will download")
        env['MLC_TMP_REQUIRE_DOWNLOAD'] = "yes"

    return {'return': 0}


def postprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    logger.info("Waymo calibration dataset setup completed")
    return {'return': 0}
