from cmind import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']

    path = env.get('LLAMA3_CHECKPOINT_PATH', '').strip()
    if path == '' or not os.path.exists(path):
        env['CM_TMP_REQUIRE_DOWNLOAD'] = 'yes'
        if env.get('CM_LLAMA3_MODEL_DOWNLOAD_PATH','') == '':
            env['CM_LLAMA3_MODEL_DOWNLOAD_PATH'] = os.getcwd()

    return {'return': 0}


def postprocess(i):

    env = i['env']
    if env.get('LLAMA3_CHECKPOINT_PATH', '') == '':
        env['LLAMA3_CHECKPOINT_PATH'] = env['CM_ML_MODEL_PATH']
    else:
        env['CM_ML_MODEL_PATH'] = env['LLAMA3_CHECKPOINT_PATH']
    env['CM_ML_MODEL_LLAMA3_CHECKPOINT_PATH'] = env['LLAMA3_CHECKPOINT_PATH']
    env['CM_GET_DEPENDENT_CACHED_PATH'] = env['CM_ML_MODEL_PATH']

    return {'return': 0}
