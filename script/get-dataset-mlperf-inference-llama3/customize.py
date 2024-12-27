from cmind import utils
import os


def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    if os_info['platform'] == "windows":
        return {'return': 1, 'error': 'Script not supported in windows yet!'}

    if env.get('CM_DATASET_LLAMA3_PATH', '') == '':
        env['CM_TMP_REQUIRE_DOWNLOAD'] = "yes"

    return {'return': 0}


def postprocess(i):

    env = i['env']

    if env.get('CM_TMP_REQUIRE_DOWNLOAD', '') == "yes":
        env['CM_DATASET_LLAMA3_PATH'] = os.path.join(env['CM_DATASET_LLAMA3_PATH'], env['CM_DATASET_FILE_NAME'])

    return {'return': 0}