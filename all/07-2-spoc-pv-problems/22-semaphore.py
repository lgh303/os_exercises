#coding=utf-8
#!/usr/bin/env python

import threading
import time

group_count = 3
thread_count = [3, 5, 2]
semaphore = threading.Semaphore(sum(thread_count))
next_group = 0
next_thread = [0, 0, 0]

class GroupThread(threading.Thread):
    def __init__(self, group_number, number):
        threading.Thread.__init__(self)
        self.group_number = group_number
        self.number = number

    def run(self):
        global condition, next_group, next_thread, group_count, thread_count
        while True:
            semaphore.acquire()
            if next_group == self.group_number and \
               next_thread[next_group] == self.number:
                print "Group %s, Thread %d Running... " \
                    %(chr(ord('A') + self.group_number), self.number)
                next_thread[self.group_number] = next_thread[self.group_number] + 1
                next_group = (self.group_number + 1) % group_count
                while (next_thread[next_group] >= thread_count[next_group]):
                    next_group = (next_group + 1) % group_count
                    if next_group == self.group_number:
                        break
                semaphore.release()
                break
            semaphore.release()


if __name__ == '__main__':
    threads = []
    for group in range(group_count):
        for number in range(thread_count[group]):
            threads.append(GroupThread(group, number))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
