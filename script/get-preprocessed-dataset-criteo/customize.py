from mlc import utils
import os
import shutil


def preprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    skip_preprocessing = False
    if env.get('MLC_DATASET_PREPROCESSED_PATH', '') != '':
        '''
        Path with preprocessed dataset given as input
        '''
        skip_preprocessing = True
        logger.info(f"Using preprocessed criteo dataset from '{env['MLC_DATASET_PREPROCESSED_PATH']}'")

    if not skip_preprocessing and env.get(
            'MLC_DATASET_PREPROCESSED_OUTPUT_PATH', '') != '':
        env['MLC_DATASET_PREPROCESSED_PATH'] = os.getcwd()
        logger.info(f"Setting preprocessed dataset path to {env['MLC_DATASET_PREPROCESSED_PATH']}")

    if not skip_preprocessing and env.get(
            'MLC_DATASET_CRITEO_MULTIHOT', '') == 'yes':
        i['run_script_input']['script_name'] = "run-multihot"
        # ${MLC_PYTHON_BIN_WITH_PATH} ${MLC_TMP_CURRENT_SCRIPT_PATH}/preprocess.py
        output_dir = env['MLC_DATASET_PREPROCESSED_PATH']
        dataset_path = env['MLC_DATASET_PATH']
        tmp_dir = os.path.join(output_dir, "tmp")
        run_dir = os.path.join(
            env['MLC_MLPERF_TRAINING_SOURCE'],
            "recommendation_v2",
            "torchrec_dlrm",
            "scripts")
        env['MLC_RUN_CMD'] = f'cd {run_dir} && bash ./process_Criteo_1TB_Click_Logs_dataset.sh {dataset_path} {tmp_dir} {output_dir} '

        logger.info(f"Using MLCommons Training source from '{env['MLC_MLPERF_TRAINING_SOURCE']}'")
        logger.info(f"Will process Criteo dataset from {dataset_path} to {output_dir} using temporary directory {tmp_dir}")

    return {'return': 0}


def postprocess(i):

    env = i['env']
    automation = i['automation']
    logger = automation.action_object.logger

    env['MLC_CRITEO_PREPROCESSED_PATH'] = env['MLC_DATASET_PREPROCESSED_PATH']
    logger.info(f"Set Criteo preprocessed path to {env['MLC_CRITEO_PREPROCESSED_PATH']}")

    env['MLC_GET_DEPENDENT_CACHED_PATH'] = env['MLC_CRITEO_PREPROCESSED_PATH']
    logger.info(f"Set dependent cached path to {env['MLC_GET_DEPENDENT_CACHED_PATH']}")

    return {'return': 0}
