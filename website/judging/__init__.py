from ..db import db
import subprocess, os, time, psutil, platform

def default_runner(pid, test_number, lang, tl, exe_file, ml):
    execute = object()
    cmd = list()
    tstart = object()
    test_file_string = os.path.dirname(__file__)+'/../../test_data/'+str(pid)+"/"+str(test_number)
    inputs = open(test_file_string+'.in', 'r') #test case

    # assign run command for specific language
    if(lang == 'c++'):
        cmd = [exe_file]
    elif(lang == 'python3'):
        cmd = ['python3', exe_file]
    
    try:
        execute = subprocess.Popen(cmd, text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # check memory (broken)
        # pass array to new thread because we want to return the memory usage
        memUse = [execute.pid, psutil.Process(execute.pid).memory_info().rss]
        # monitor = threading.Thread(target = monitor_mem, args = [memUse])
        # monitor.start()

        # start giving inputs
        tstart = time.time()
        ret = execute.communicate(input = inputs.read(), timeout=tl)
        tend = round((time.time() - tstart) * 1000.0)

        # monitor.join()

        #verdict
        if(execute.returncode != 0):
            return [0, tend, memUse[1], ret[1]]

        # set up for answer comparing
        res_list = [k for k in ret[0].split('\n')]
        if(res_list[-1] == ''):
            res_list.pop()
        
        rd = open(test_file_string+".out", 'r')
        ans_list = [k.strip() for k in rd.readlines()]
        if(ans_list[-1] == ''):
            ans_list.pop()
        rd.close()
        inputs.close()
        
        if(res_list == ans_list):
            return [3, tend, memUse[1], '']
        else:
            return [2, tend, memUse[1], '']

    except subprocess.TimeoutExpired:
        inputs.close()
        execute.kill()
        return [1, round((time.time() - tstart) * 1000.0, 2), 0, '']

def judgement(pid, code, lang, subid):
    # name of executable
    exe_file = os.path.abspath(os.path.dirname(__file__) + '/exes/'+str(subid))

    prob_data = db['problems'].find_one({'pid': int(pid)})
    doc = db['submission_data']
    subdata = db['submission_data'].find_one({'_id': subid})

    # compile / put code into file
    if(lang == 'c++'):
        compil = subprocess.run(['g++', '-o', exe_file, '-xc++', '-'], text=True, input=code, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if(compil.returncode == 1):
            subdata.update({'done': 1, 'verdict': 'CE', 'error_msg': compil.stderr})
            doc.replace_one({'_id': subid}, subdata)
            return
    elif(lang == 'python3'):
        exe_file += '.py'
        wt = open(exe_file, 'w')
        wt.write(code)
        wt.close()

    save = [0, 0, 0, 0] #re tle wa ac
    name = ['RE', 'TLE', 'WA', 'AC']

    # compare with the execution time later on and get the maximum
    maxtime = -1
    maxmem = -1

    #start testing
    prev_test = 1
    cur_subtask = 0
    abort = 0
    for k in prob_data['subtask_range']:
        k = int(k)
        for i in range(prev_test, k+1):
            if(abort):
                subdata['subtask'][cur_subtask][i-prev_test] = ['abort', 0, 0]
                continue

            get = default_runner(pid, i, lang, int(prob_data['time_limit']), exe_file, int(prob_data['memory_limit']))
            save[get[0]] = 1
            maxtime = max(maxtime, get[1])
            maxmem = max(maxmem, get[2])
            subdata['subtask'][cur_subtask][i-prev_test] = [name[get[0]], get[1], get[2]]
            subdata['error_msg'] = get[3]
            if(get[0] == 0):
                abort = 1
        
        prev_test = k+1
        cur_subtask += 1
            
    # verdict = "validation error" # show this if no verdict found
    # verdict that is at the front has higher priority for final verdict
    for a in range(4):
        if(save[a] == 1):
            verdict = name[a]
            break
    subdata.update_one({'_id': subid}, {'$set': {'done': 1, 'verdict': verdict, 'exetime': maxtime}})
    if verdict == 'AC':
        thissub = subdata.find_one({'_id':subid})
        thisuserid = thissub['userid']
        solved = db['account'].find_one({'name': thisuserid})['solved']
        ACcount = db['account'].find_one({'name': thisuserid})['AC']
        if pid not in solved:
            solved.append(pid)
            db['account'].update_one({'name': thisuserid}, {'$set': {'solved': solved, 'AC':ACcount+1}})
    subdata.update({'done': 1, 'verdict': verdict, 'exetime': maxtime})
    doc.replace_one({'_id': subid}, subdata)

    #delete executable
    if(platform.system() == 'Windows'):
        os.remove(exe_file+'.exe')
    else:
        os.remove(exe_file)
