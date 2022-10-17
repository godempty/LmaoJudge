from ..db import db
import subprocess, os, time, psutil, threading

def monitor_mem(arg):
    pid = arg[0]
    while 1:
        try:
            arg[1] = max(arg[1], psutil.Process(pid).memory_info().rss)
        except:
            break

def default_validator(test, ans, lang, tl, file, ml):
    execute = object()
    cmd = list()
    tstart = object()
    # assign run command for specific language
    if(lang == 'c++'):
        cmd = [file]
    
    try:
        execute = subprocess.Popen(cmd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # check memory
        # pass array to new thread because we want to return the memory usage
        memUse = [execute.pid, psutil.Process(execute.pid).memory_info().rss]
        monitor = threading.Thread(target = monitor_mem, args = [memUse])
        monitor.start()

        # start execution
        tstart = time.time()
        ret = execute.communicate(input=test, timeout=tl)
        tend = round((time.time() - tstart) * 1000.0)

        monitor.join()

        #verdict
        if(execute.returncode != 0):
            return [0, tend, memUse[1]]

        if(ret[0].strip() == ans):
            return [3, tend, memUse[1]]
        else:
            return [2, tend, memUse[1]]

    except subprocess.TimeoutExpired:
        execute.kill()
        return [1, round((time.time() - tstart) * 1000.0, 2), 0]

def judgement(pid, code, lang, subid):
    data = db['problem_test_data'].find_one({'_id': int(pid)})
    subdata = db['submission_data']
    
    file = os.path.abspath(os.path.dirname(__file__) + '/exes/'+str(subid))
    #compile
    if(lang == 'c++'):
        compil = subprocess.run(['g++', '-o', file, '-xc++', '-'], text=True, input=code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if(compil.returncode == 1):
            db['submission_data'].update_one({'_id': subid}, {'$set': {'done': 1, 'verdict': 'compile error'}})
            return

    save = [0, 0, 0, 0] #re tle wa ac
    name = ['RE', 'TLE', 'WA', 'AC']
    maxtime = -1
    maxmem = -1
    #start testing
    for k in range(data['total_subtasks']):
        tasks = data['subtasks'][k]
        for i in range(tasks['total']):
            get = default_validator(tasks['test'][i], tasks['ans'][i], lang, data['timelimit'], file, data['memlimit'])
            save[get[0]] = 1
            maxtime = max(maxtime, get[1])
            maxmem = max(maxmem, get[2])
            subdata.update_one({'_id': subid}, {'$set': {'subtask.'+str(k)+'.'+str(i): [name[get[0]], get[1], get[2]]}})

    verdict = "validation error" # show this if no verdict found
    # verdict that is at the front has higher priority for final verdict
    for a in range(4):
        if(save[a] == 1):
            verdict = name[a]
            break
    subdata.update_one({'_id': subid}, {'$set': {'done': 1, 'verdict': verdict, 'exetime': maxtime}})

    #delete executable
    if(lang == 'c++'):
        os.remove(file)
