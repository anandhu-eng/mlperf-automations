from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    meta = i['meta']
    os_info = i['os_info']
    logger = automation.action_object.logger

    if os_info['platform'] == 'windows':
        logger.info("Skipping ImageNet training dataset setup on Windows platform")
        return {'return': 0}

    env['MLC_DATASET_IMAGENET_TRAIN_REQUIRE_DAE'] = 'no'
    logger.info("Preparing to set up ImageNet training dataset")

    path = env.get('MLC_INPUT', env.get('IMAGENET_TRAIN_PATH', '')).strip()

    if path == '':
        if env.get('MLC_DATASET_IMAGENET_TRAIN_TORRENT_PATH'):
            path = env['MLC_DATASET_IMAGENET_TRAIN_TORRENT_PATH']
            env['MLC_DAE_EXTRA_TAGS'] = "_torrent"
            env['MLC_DAE_TORRENT_PATH'] = path
            env['MLC_DATASET_IMAGENET_VAL_REQUIRE_DAE'] = 'yes'
            logger.info(f"Using torrent file at {path}")
            return {'return': 0}
        else:
            error_msg = 'Please rerun the last CM command with --env.IMAGENET_TRAIN_PATH={path the folder containing full ImageNet training images} or envoke mlcr "get train dataset imagenet" --input={path to the folder containing ImageNet training images}'
            logger.error(error_msg)
            return {'return': 1, 'error': error_msg}
    elif not os.path.isdir(path):
        if path.endswith(".tar"):
            env['MLC_EXTRACT_FILEPATH'] = path
            env['MLC_DAE_ONLY_EXTRACT'] = 'yes'
            logger.info(f"Will extract ImageNet training dataset from {path}")
            return {'return': 0}
        else:
            error_msg = f"Path {path} doesn't exist"
            logger.error(error_msg)
            return {'return': 1, 'error': error_msg}
    else:
        env['MLC_EXTRACT_EXTRACTED_PATH'] = path
        logger.info(f"Using existing ImageNet training dataset at {path}")

    return {'return': 0}


def postprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    if os_info['platform'] == 'windows':
        logger.info("Skipping ImageNet training dataset post-processing on Windows platform")
        return {'return': 0}

    path = env['MLC_EXTRACT_EXTRACTED_PATH']
    path_tar = os.path.join(path, 'n01440764.tar')

    if not os.path.isfile(path_tar):
        error_msg = f"ImageNet file {path_tar} not found"
        logger.error(error_msg)
        return {'return': 1, 'error': error_msg}

    env['MLC_DATASET_PATH'] = path
    env['MLC_DATASET_IMAGENET_PATH'] = path
    env['MLC_DATASET_IMAGENET_TRAIN_PATH'] = path
    env['MLC_GET_DEPENDENT_CACHED_PATH'] = path

    logger.info(f"Successfully set up ImageNet training dataset at {path}")

    return {'return': 0}
