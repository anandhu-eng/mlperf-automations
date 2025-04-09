from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    meta = i['meta']
    os_info = i['os_info']
    logger = automation.action_object.logger

    env['MLC_DATASET_IMAGENET_VAL_REQUIRE_DAE'] = 'no'
    logger.info("Preparing to set up ImageNet validation dataset")

    full = env.get('MLC_IMAGENET_FULL', '').strip() == 'yes'

    path = env.get(
        'MLC_INPUT',
        env.get(
            'IMAGENET_PATH',
            env.get(
                'MLC_DATASET_IMAGENET_PATH',
                ''))).strip()

    if path == '':
        if full:
            if env.get('MLC_DATASET_IMAGENET_VAL_TORRENT_PATH'):
                path = env['MLC_DATASET_IMAGENET_VAL_TORRENT_PATH']
                env['MLC_DAE_EXTRA_TAGS'] = "_torrent"
                env['MLC_DAE_TORRENT_PATH'] = path
                env['MLC_DATASET_IMAGENET_VAL_REQUIRE_DAE'] = 'yes'
                logger.info(f"Using torrent file at {path}")
                return {'return': 0}
            else:
                env['MLC_DAE_URL'] = 'https://image-net.org/data/ILSVRC/2012/ILSVRC2012_img_val.tar'
                env['MLC_DAE_FILENAME'] = 'ILSVRC2012_img_val.tar'
                env['MLC_DATASET_IMAGENET_VAL_REQUIRE_DAE'] = 'yes'
                logger.info("Will download ImageNet validation dataset from official source")
                return {'return': 0}
        else:
            env['MLC_DATASET_IMAGENET_VAL_REQUIRE_DAE'] = 'yes'
            logger.info("Will download ImageNet validation dataset")
    elif not os.path.isdir(path):
        if path.endswith(".tar"):
            env['MLC_EXTRACT_FILEPATH'] = path
            env['MLC_DAE_ONLY_EXTRACT'] = 'yes'
            logger.info(f"Will extract ImageNet validation dataset from {path}")
            return {'return': 0}
        else:
            error_msg = f"Path {path} doesn't exist"
            logger.error(error_msg)
            return {'return': 1, 'error': error_msg}
    else:
        env['MLC_EXTRACT_EXTRACTED_PATH'] = path
        logger.info(f"Using existing ImageNet validation dataset at {path}")

    return {'return': 0}


def postprocess(i):

    os_info = i['os_info']
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    path = env['MLC_EXTRACT_EXTRACTED_PATH']
    path1 = os.path.join(path, 'imagenet-2012-val')
    if os.path.isdir(path1):
        path = path1
        logger.info(f"Found ImageNet validation dataset in subdirectory {path1}")

    path_image = os.path.join(path, 'ILSVRC2012_val_00000001.JPEG')

    if not os.path.isfile(path_image):
        error_msg = f"ImageNet file {path_image} not found"
        logger.error(error_msg)
        return {'return': 1, 'error': error_msg}

    files = os.listdir(path)
    if len(files) < int(env.get('MLC_DATASET_SIZE', 0)):
        error_msg = f"Only {len(files)} files found in {path}. {env.get('MLC_DATASET_SIZE')} expected"
        logger.error(error_msg)
        return {'return': 1, 'error': error_msg}

    env['MLC_DATASET_PATH'] = path
    env['MLC_DATASET_IMAGENET_PATH'] = path
    env['MLC_DATASET_IMAGENET_VAL_PATH'] = path
    env['MLC_GET_DEPENDENT_CACHED_PATH'] = path

    logger.info(f"Successfully set up ImageNet validation dataset at {path}")
    logger.info(f"Found {len(files)} validation images")

    return {'return': 0}
