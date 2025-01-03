from cmind import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']

    path = env.get('CM_ML_MODEL_LLAMA3_DOWNLOAD_PATH', '').strip()

    if path != "":
        os.makedirs(path, exist_ok=True)
        env['CM_ML_MODEL_LLAMA3_DOWNLOAD_PATH'] = path
    else:
        env['CM_ML_MODEL_LLAMA3_DOWNLOAD_PATH'] = os.getcwd()

    return {'return': 0}


def postprocess(i):

    env = i['env']
    if env.get('CM_TMP_REQUIRE_DOWNLOAD', '') == 'yes':
        env['LLAMA3_CHECKPOINT_PATH'] = env['CM_ML_MODEL_PATH']
    else:
        env['CM_ML_MODEL_PATH'] = env['LLAMA3_CHECKPOINT_PATH']
    env['CM_ML_MODEL_LLAMA3_CHECKPOINT_PATH'] = env['LLAMA3_CHECKPOINT_PATH']
    env['CM_GET_DEPENDENT_CACHED_PATH'] = env['CM_ML_MODEL_PATH']

    return {'return': 0}
