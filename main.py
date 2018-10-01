import requests
import json
from urllib.parse import quote
requests.packages.urllib3.disable_warnings()
import datetime
import time
import threading
import queue

with open('config.json', 'r') as fd:
    cfg = json.load(fd)

cb_api = cfg.get('cb_api')
url = cfg.get('cb_url')
year = cfg.get('year')
month = cfg.get('month')
day = cfg.get('day')

payload = {'X-Auth-Token': cb_api}
intelKeyz = list(cfg.get('queries').keys())
intelz = cfg.get('queries')
orig = datetime.datetime(year, month, day)
delta = datetime.datetime.today() - orig
date_list = [orig + datetime.timedelta(days=i) for i in range(delta.days + 1)]

class INTEL_TESTER():
    def begin(self):
        while queue.Queue.qsize(q) != 0:
            taskObj = q.get()
            query = taskObj.get("query")
            timestamp = taskObj.get("mehTime")
            title = taskObj.get("title")
            desc = taskObj.get("desc")
            ref = taskObj.get("ref")    

            print("[+] {} for {}\n   Query: {}".format(title, timestamp, query))
            try:
                queryResultsTotal = process_query(0, 0, quote(query, safe='&='), timestamp)
                with open("metrics.csv", "a+") as wf:
                    wf.write('|'.join(map(str, [timestamp, queryResultsTotal.get("total_results"), title, query, desc, ref]))+"\n")

            except Exception as e:
                print("----> Exception with {} on {}: Error: {}".format(title, meh_time, e))
            q.task_done()

def process_query(rows, start, query, date):
    get_deets = requests.get("{}/api/v1/process?cb.urlver=&rows={}&start={}&sort=&q={}&cb.min_last_update={}T00:00:00Z&cb.max_last_update={}T23:59:59Z".format(url, rows, start, query, date, date), headers=payload, verify=False)
    return get_deets.json()

if __name__ == '__main__':
    q = queue.Queue()

    ## Write the header column
    with open("metrics.csv", "w+") as wf:
        wf.write("date|results|title|query|desc|ref\n")

    for i in intelKeyz:
        ke = intelz[i]
        for d in date_list:
            meh_time = d.strftime('%Y-%m-%d')

            ## Don't run the test for today because its not over
            if meh_time == time.strftime("%Y-%m-%d"):
                continue

            taskItem = {}
            taskItem["mehTime"] = meh_time
            taskItem["query"] = ke.get("query")
            taskItem["title"] = i
            taskItem["desc"] = ke.get("desc")
            taskItem["ref"] = ke.get("ref")
            q.put(taskItem)

    for i in range(1):
        ## TODO: Include a thread lock for the csv outout file
        stk = INTEL_TESTER()
        worker = threading.Thread(target=stk.begin, daemon=False)
        worker.start()