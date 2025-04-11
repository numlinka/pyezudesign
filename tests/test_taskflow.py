# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

# std
import unittest

# tests
from ezudesign.taskflow import *


class TestUtils (unittest.TestCase):
    def test_taskflow(self):
        lst = []
        def task1(lst): lst += [1]
        def task2(lst): lst += [2]
        def task3(lst): lst += [3]
        def task4(lst): lst += [4]
        def task5(lst): lst += [5]

        flow = TaskFlow()
        flow.add_task(task1, 1000)
        flow.add_task(task3, 1002)
        flow.add_task(task5, 1004)
        flow.add_task(task4, 1003)
        flow.add_task(task2, 1001)

        flow.run(lst)
        self.assertEqual(lst, list(range(1, 6)))

    def test_taskflow_remove(self):
        lst = []
        def task1(lst): lst += [1]
        def task2(lst): lst += [2]
        def task3(lst): lst += [3]
        def task4(lst): lst += [4]
        def task5(lst): lst += [5]

        flow = TaskFlow()
        iid = flow.add_task(task1, 1000)
        flow.add_task(task3, 1002)
        flow.add_task(task5, 1004)
        flow.add_task(task4, 1003)
        flow.add_task(task2, 1001, "task2")

        flow.remove_task(iid)
        flow.remove_task("task2")
        flow.remove_task(task3)

        flow.run(lst)
        self.assertEqual(lst, [4, 5])

    def test_taskflow_stop(self):
        lst = []
        def task1(lst): lst += [1]
        def task2(lst): lst += [2]
        def task3(lst): raise StopTaskFlow
        def task4(lst): lst += [4]
        def task5(lst): lst += [5]

        flow = TaskFlow()
        flow.add_task(task1, 1000)
        flow.add_task(task3, 1002)
        flow.add_task(task5, 1004)
        flow.add_task(task4, 1003)
        flow.add_task(task2, 1001)

        flow.run(lst)
        self.assertEqual(lst, [1, 2])

    def test_taskflow_exception(self):
        def task(): raise ZeroDivisionError

        flow = TaskFlow()
        flow.add_task(task)

        self.assertRaises(ZeroDivisionError, flow.run)
