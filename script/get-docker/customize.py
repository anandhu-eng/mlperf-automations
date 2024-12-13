from cmind import utils
import os


def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    automation = i['automation']

    recursion_spaces = i['recursion_spaces']

    file_name = 'docker.exe' if os_info['platform'] == 'windows' else 'docker'
    env['FILE_NAME'] = file_name

    if 'CM_DOCKER_BIN_WITH_PATH' not in env:
        r = i['automation'].find_artifact({'file_name': file_name,
                                           'env': env,
                                           'os_info': os_info,
                                           'default_path_env_key': 'PATH',
                                           'detect_version': True,
                                           'env_path_key': 'CM_DOCKER_BIN_WITH_PATH',
                                           'run_script_input': i['run_script_input'],
                                           'recursion_spaces': recursion_spaces})
        if r['return'] > 0:
            if r['return'] == 16:
                run_file_name = "install"
                r = automation.run_native_script(
                    {'run_script_input': i['run_script_input'], 'env': env, 'script_name': run_file_name})
                if r['return'] > 0:
                    return r
            else:
                return r

    return {'return': 0}


def detect_version(i):
    r = i['automation'].parse_version({'match_text': r'[Docker|podman] version\s*([\d.]+)',
                                       'group_number': 1,
                                       'env_key': 'CM_DOCKER_VERSION',
                                       'which_env': i['env']})
    if r['return'] > 0:
        return r

    version = r['version']

    tool = "docker"

    if "podman" in r['string'].lower():
        tool = "podman"


    print(i['recursion_spaces'] + '    Detected version: {}'.format(version))
    return {'return': 0, 'version': version, "tool":tool}


def postprocess(i):
    env = i['env']

    r = detect_version(i)

    if r['return'] > 0:
        return r

    version = r['version']
    tool = r['tool']
    found_file_path = env['CM_DOCKER_BIN_WITH_PATH']

    found_path = os.path.dirname(found_file_path)
    env['CM_DOCKER_INSTALLED_PATH'] = found_path
    env['+PATH'] = [found_path]

    env['CM_DOCKER_CACHE_TAGS'] = 'version-' + version

    env['CM_DOCKER_VERSION'] = version
    
    env['CM_CONTAINER_TOOL'] = tool

    return {'return': 0, 'version': version}
