from cmind import utils
import os


def preprocess(i):

    os_info = i['os_info']
    env = i['env']

    path = env.get('CM_ML_MODEL_LLAMA3_DOWNLOAD_PATH', '').strip()

    if path != "":
        os.makedirs(path, exist_ok=True)
        env['CM_GIT_CHECKOUT_FOLDER'] = os.path.join(
            path, env['CM_ML_MODEL_NAME'])
        
    env['CM_TMP_REQUIRE_DOWNLOAD'] = 'yes'
    
    return {'return': 0}


def postprocess(i):

    env = i['env']

    env['CM_ML_MODEL_LLAMA3_CHECKPOINT_PATH'] = env['LLAMA3_CHECKPOINT_PATH']
    env['CM_GET_DEPENDENT_CACHED_PATH'] = env['CM_ML_MODEL_PATH']

    return {'return': 0}
