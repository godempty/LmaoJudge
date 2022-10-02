from ..db import db
import subprocess, os, time

def default_validator(test, ans, lang, time, file, memory):
    execute = object()
    cmd = list()
    # assign run command for specific language
    if(lang == 'c++'):
        cmd = [file]
    
    try:
        execute = subprocess.Popen(cmd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = execute.communicate(input=test, timeout=time)

        if(execute.returncode != 0):
            return 0

        if(ret[0].strip() == ans):
            return 3
        else:
            return 2

    except subprocess.TimeoutExpired:
        execute.kill()
        return 1

def judgement(pid, code, lang, subid):
    data = db['problem_test_data'].find_one({'_id': int(pid)})
    
    file = os.path.abspath(os.path.dirname(__file__) + '/exes/'+str(subid))
    #compile
    if(lang == 'c++'):
        compil = subprocess.run(['g++', '-o', file, '-xc++', '-'], text=True, input=code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if(compil.returncode == 1):
            db['submission_data'].update_one({'_id': subid}, {'$set': {'done': 1, 'verdict': 'compile error'}})
            return

    update = {'done': 1, 'subtask': list()}

    save = [0, 0, 0, 0] #re tle wa ac
    name = ['RE', 'TLE', 'WA', 'AC']
    #start testing
    for tasks in data['subtasks']:
        update['subtask'].append(list())
        for i in range(tasks['total']):
            get = default_validator(tasks['test'][i], tasks['ans'][i], lang, data['timelimit'], file, data['memlimit'])
            save[get] = 1
            update['subtask'][-1].append([name[get], 0, 0])

    verdict = "validation error" # show this if no verdict found
    # verdict that is at the front has higher priority for final verdict
    for a in range(4):
        if(save[a] == 1):
            verdict = name[a]
            break
    update['verdict'] = verdict
    db['submission_data'].update_one({'_id': subid}, {'$set': update})

    #delete executable
    if(lang == 'c++'):
        os.remove(file)
