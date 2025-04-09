from mlc import utils
import os
import shutil


def preprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    logger.info("Preparing to set up CNN/DailyMail dataset")
    if env.get('MLC_CNNDM_INTEL_VARIATION', '') == 'yes':
        i['run_script_input']['script_name'] = "run-intel"
        logger.info("Using Intel variation of CNN/DailyMail dataset")
    else:
        logger.info(f"Using MLCommons Inference source from '{env['MLC_MLPERF_INFERENCE_SOURCE']}'")

    return {'return': 0}


def postprocess(i):
    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    if env.get('MLC_DATASET_CALIBRATION', '') == "no":
        env['MLC_DATASET_PATH'] = os.path.join(os.getcwd(), 'install')
        env['MLC_DATASET_EVAL_PATH'] = os.path.join(
            os.getcwd(), 'install', 'cnn_eval.json')
        env['MLC_DATASET_CNNDM_EVAL_PATH'] = os.path.join(
            os.getcwd(), 'install', 'cnn_eval.json')
        env['MLC_GET_DEPENDENT_CACHED_PATH'] = env['MLC_DATASET_PATH']
        logger.info(f"Set CNN/DailyMail dataset paths: path={env['MLC_DATASET_PATH']}, eval={env['MLC_DATASET_EVAL_PATH']}")
    else:
        env['MLC_CALIBRATION_DATASET_PATH'] = os.path.join(
            os.getcwd(), 'install', 'cnn_dailymail_calibration.json')
        env['MLC_CALIBRATION_DATASET_CNNDM_PATH'] = os.path.join(
            os.getcwd(), 'install', 'cnn_dailymail_calibration.json')
        env['MLC_GET_DEPENDENT_CACHED_PATH'] = env['MLC_CALIBRATION_DATASET_PATH']
        logger.info(f"Set CNN/DailyMail calibration dataset paths: path={env['MLC_CALIBRATION_DATASET_PATH']}")

    return {'return': 0}
