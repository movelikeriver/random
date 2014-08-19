#!/usr/bin/python
"""
Usage: 
  python vector_reallocation.py

Output result:
Before:
0 -1
1 -1
2 -1
3 -1
Start InsaneCompute()...
Start InsaneCompute()...
Start InsaneCompute()...
Start InsaneCompute()...
cost_ms: 7304
cost_ms: 7543
cost_ms: 8222
cost_ms: 8294
After:
0 7543
1 8222
2 8294
3 7304
"""

import threading
import time

RECUR_N = 23  # don't try crazy num.

class Report(object):
    def __init__(self):
        self.latency_ms = -1


class TaskManager(object):
    def __init__(self):
        self._tasks = []

    def AddTask(self, report):
        self._tasks.append(report)

    def Run(self):
        thread_list = []
        for task in self._tasks:
            t = threading.Thread(target=TaskManager.Update, args=(task,))
            thread_list.append(t)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    @staticmethod
    def Update(report):
        report.latency_ms = TaskManager.InsaneCompute()

    @staticmethod
    def InsaneCompute():
        print 'Start InsaneCompute()...'
        start = int(round(time.time() * 1000))
        for i in xrange(2, RECUR_N):
            TaskManager.Recur(i)
        cost_ms = int(round(time.time() * 1000)) - start
        print 'cost_ms:', cost_ms
        return cost_ms

    @staticmethod
    def Recur(n):
        if n <= 2:
            return n
        sum = 0
        for i in xrange(0, n):
            sum += TaskManager.Recur(i)
        return sum


def ScheduleTasks(n, global_vec, task_manager):
    for i in xrange(0, n):
        report = Report()
        global_vec.append(report)
        task_manager.AddTask(report)

def Print(global_vec):
    for i in xrange(0, len(global_vec)):
        print i, global_vec[i].latency_ms


def main():
    global_vec = []
    task_manager = TaskManager()
    ScheduleTasks(4, global_vec, task_manager)
    print 'Before:'
    Print(global_vec)
    task_manager.Run()
    print 'After:'
    Print(global_vec)


if __name__ == "__main__":
    main()
