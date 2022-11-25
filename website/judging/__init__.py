from ..db import db
import subprocess, os, time, psutil, threading

def monitor_mem(arg):
    pid = arg[0]
    while 1:
        try:
            arg[1] = max(arg[1], psutil.Process(pid).memory_info().rss)
        except:
            break

def default_runner(pid, test_number, lang, tl, exe_file, ml):
    execute = object()
    cmd = list()
    tstart = object()
    inputs = open('../../test_data/'+str(pid)+"/"+str(test_number)+".in", 'r') #test case

    # assign run command for specific language
    if(lang == 'c++'):
        cmd = [exe_file]
    
    try:
        execute = subprocess.Popen(cmd, text=True, stdin=inputs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tstart = time.time()

        # check memory (broken)
        # pass array to new thread because we want to return the memory usage
        memUse = [execute.pid, psutil.Process(execute.pid).memory_info().rss]
        # monitor = threading.Thread(target = monitor_mem, args = [memUse])
        # monitor.start()

        # wait execution
        ret = execute.wait(timeout=tl)
        tend = round((time.time() - tstart) * 1000.0)

        # monitor.join()

        #verdict
        if(execute.returncode != 0):
            return [0, tend, memUse[1]]

        # set up for answer comparing
        res_list = [k for k in ret[0].split('\n')]
        if(res_list[-1] == ''):
            res_list.pop()
        
        rd = open('../../test_data/'+str(pid)+"/"+str(test_number)+".out", 'r')
        ans_list = [k.strip() for k in rd.readlines()]
        if(ans_list[-1] == ''):
            ans_list.pop()
        rd.close()
        inputs.cloes()
        
        if(res_list == ans_list):
            return [3, tend, memUse[1]]
        else:
            return [2, tend, memUse[1]]

    except subprocess.TimeoutExpired:
        inputs.close()
        execute.kill()
        return [1, round((time.time() - tstart) * 1000.0, 2), 0]

def judgement(pid, code, lang, subid):
    # name of executable
    exe_file = os.path.abspath(os.path.dirname(__file__) + '/exes/'+str(subid))

    prob_data = db['problems'].find_one({'pid': int(pid)})
    subdata = db['submission_data']

    # compile
    if(lang == 'c++'):
        compil = subprocess.run(['g++', '-o', exe_file, '-xc++', '-'], text=True, input=code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if(compil.returncode == 1):
            subdata.update_one({'_id': subid}, {'$set': {'done': 1, 'verdict': 'compile error'}})
            return

    save = [0, 0, 0, 0] #re tle wa ac
    name = ['RE', 'TLE', 'WA', 'AC']

    # compare with the execution time later on and get the maximum
    maxtime = -1
    maxmem = -1

    #start testing
    cur_test_num = 1
    for k in prob_data['subtask_range']:
        k = int(k)
        for i in range(cur_test_num, k+1):
            get = default_runner(pid, cur_test_num, lang, prob_data['time_limit'], exe_file, prob_data['memory_limit'])
            save[get[0]] = 1
            maxtime = max(maxtime, get[1])
            maxmem = max(maxmem, get[2])
            subdata.update_one({'_id': subid}, {'$set': {'subtask.'+str(k)+'.'+str(i): [name[get[0]], get[1], get[2]]}})
        
        cur_test_num = k+1
            
    # for k in range(data['total_subtasks']):
    #     tasks = data['subtasks'][k]
    #     for i in range(tasks['total']):
    #         get = default_validator(tasks['test'][i], tasks['ans'][i], lang, data['timelimit'], file, data['memlimit'])
    #         save[get[0]] = 1
    #         maxtime = max(maxtime, get[1])
    #         maxmem = max(maxmem, get[2])
    #         subdata.update_one({'_id': subid}, {'$set': {'subtask.'+str(k)+'.'+str(i): [name[get[0]], get[1], get[2]]}})

    # verdict = "validation error" # show this if no verdict found
    # verdict that is at the front has higher priority for final verdict
    for a in range(4):
        if(save[a] == 1):
            verdict = name[a]
            break
    subdata.update_one({'_id': subid}, {'$set': {'done': 1, 'verdict': verdict, 'exetime': maxtime}})

    #delete executable
    os.remove(exe_file)
