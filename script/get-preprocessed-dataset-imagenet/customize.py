from mlc import utils
import os
from os.path import exists
import shutil
import glob


def preprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    if 'MLC_IMAGENET_PREPROCESSED_PATH' in env:
        files = glob.glob(
            env['MLC_IMAGENET_PREPROCESSED_PATH'] +
            "/**/" +
            env['MLC_IMAGENET_PREPROCESSED_FILENAME'],
            recursive=True)
        if files:
            env['MLC_DATASET_PREPROCESSED_PATH'] = env['MLC_IMAGENET_PREPROCESSED_PATH']
            logger.info(f"Using existing preprocessed images from {env['MLC_DATASET_PREPROCESSED_PATH']}")
        else:
            error_msg = f"No preprocessed images found in {env['MLC_IMAGENET_PREPROCESSED_PATH']}"
            logger.error(error_msg)
            return {'return': 1, 'error': error_msg}
    else:
        if env.get('MLC_DATASET_REFERENCE_PREPROCESSOR', "0") == "1":
            logger.info(f"Using MLCommons Inference source from '{env['MLC_MLPERF_INFERENCE_SOURCE']}'")

        env['MLC_DATASET_PREPROCESSED_PATH'] = os.getcwd()
        logger.info(f"Setting preprocessed dataset path to {env['MLC_DATASET_PREPROCESSED_PATH']}")
        
        if env['MLC_DATASET_TYPE'] == "validation" and not exists(
                os.path.join(env['MLC_DATASET_PATH'], "val_map.txt")):
            val_map_src = os.path.join(env['MLC_DATASET_AUX_PATH'], "val.txt")
            val_map_dst = os.path.join(env['MLC_DATASET_PATH'], "val_map.txt")
            shutil.copy(val_map_src, val_map_dst)
            logger.info(f"Copied validation map from {val_map_src} to {val_map_dst}")

    preprocessed_path = env['MLC_DATASET_PREPROCESSED_PATH']

    if env.get('MLC_DATASET_TYPE', '') == "validation" and not exists(
            os.path.join(preprocessed_path, "val_map.txt")):
        val_map_src = os.path.join(env['MLC_DATASET_AUX_PATH'], "val.txt")
        val_map_dst = os.path.join(preprocessed_path, "val_map.txt")
        shutil.copy(val_map_src, val_map_dst)
        logger.info(f"Copied validation map from {val_map_src} to {val_map_dst}")

    if env.get('MLC_DATASET_TYPE', '') == "calibration":
        env['MLC_DATASET_IMAGES_LIST'] = env['MLC_MLPERF_IMAGENET_CALIBRATION_LIST_FILE_WITH_PATH']
        env['MLC_DATASET_SIZE'] = 500
        logger.info(f"Using calibration dataset with {env['MLC_DATASET_SIZE']} images from {env['MLC_DATASET_IMAGES_LIST']}")

    if env.get('MLC_DATASET_DATA_TYPE_INPUT', '') == '':
        env['MLC_DATASET_DATA_TYPE_INPUT'] = env['MLC_DATASET_DATA_TYPE']
        logger.info(f"Setting input data type to {env['MLC_DATASET_DATA_TYPE_INPUT']}")

    return {'return': 0}


def postprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    # finalize path
    preprocessed_path = env['MLC_DATASET_PREPROCESSED_PATH']
    preprocessed_images_list = []
    preprocessed_imagenames_list = []

    match_text = "/*." + env.get("MLC_DATASET_PREPROCESSED_EXTENSION", "*")
    logger.info(f"Searching for preprocessed files matching pattern: {match_text}")
    
    for filename in sorted(glob.glob(preprocessed_path + match_text)):
        preprocessed_images_list.append(filename)
        preprocessed_imagenames_list.append(os.path.basename(filename))
    
    logger.info(f"Found {len(preprocessed_images_list)} preprocessed files")
    
    with open("preprocessed_files.txt", "w") as f:
        f.write("\n".join(preprocessed_images_list))
    with open("preprocessed_filenames.txt", "w") as f:
        f.write("\n".join(preprocessed_imagenames_list))

    env['MLC_DATASET_PREPROCESSED_IMAGES_LIST'] = os.path.join(
        os.getcwd(), "preprocessed_files.txt")
    env['MLC_DATASET_PREPROCESSED_IMAGENAMES_LIST'] = os.path.join(
        os.getcwd(), "preprocessed_filenames.txt")
    
    logger.info(f"Saved preprocessed files list to {env['MLC_DATASET_PREPROCESSED_IMAGES_LIST']}")
    logger.info(f"Saved preprocessed filenames list to {env['MLC_DATASET_PREPROCESSED_IMAGENAMES_LIST']}")

    return {'return': 0}
