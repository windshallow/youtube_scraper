#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# https://stackoverflow.com/questions/6974695/python-process-pool-non-daemonic

import multiprocessing
# We must import this explicitly, it is not imported by the top-level
# multiprocessing module.
import multiprocessing.pool
import time

from random import randint
from crawl import domain_crawl


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def sleepawhile(t):
    print("Sleeping %i seconds..." % t)
    time.sleep(t)
    return t


def work(num_procs):
    print("Creating %i (daemon) workers and jobs in child." % num_procs)
    pool = multiprocessing.Pool(num_procs)

    result = pool.map(sleepawhile, [randint(1, 5) for x in range(num_procs)])  # 在1到5之间的整数中随机取num_procs个，组成列表

    # The following is not really needed, since the (daemon) workers of the
    # child's pool are killed when the child is terminated, but it's good
    # practice to cleanup after ourselves anyway.
    pool.close()
    pool.join()
    return result


def test():
    print("Creating 5 (non-daemon) workers and jobs in main process.")
    pool = MyPool(5)

    result = pool.map(work, [randint(1, 5) for x in range(5)])

    pool.close()
    pool.join()
    print(result)


# -------------
def work_2(urls):
    # urls list
    pool = multiprocessing.Pool(len(urls))
    result = pool.map(domain_crawl, urls)
    pool.close()
    pool.join()
    return result


def test_2():
    pool = MyPool()


if __name__ == '__main__':
    test()
