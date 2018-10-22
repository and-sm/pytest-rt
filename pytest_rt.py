import json
import pytest
import uuid
import time
import requests
# from conftest import endpoint, show_errors
from _pytest.runner import runtestprotocol


class Rt(object):

    def __init__(self, config=None):

        self.config = config
        self.uuid = str(uuid.uuid4())
        self.endpoint = config.option.url
        # self.show_errors = show_errors

    def post(self, payload):
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        try:
            requests.post(self.endpoint, data=json.dumps(payload), headers=headers)
        except requests.exceptions.ConnectionError as error:
                print(error)

    def pytest_collection_modifyitems(self, session):
        tests = []
        for item in session.items:
            node = dict()
            node["location"] = item.location[2]
            node["nodeid"] = item.nodeid
            tests.append(node)
        self.post({"fw": "2",
                   "type": "startTestRun",
                   "tests": tests,
                   "env": session.config.option.env,
                   "startTime": time.time(),
                   "job_id": self.uuid})

    def pytest_runtest_logstart(self, nodeid, location):
        # print("pytest_runtest_logstart")
        self.post({
            "fw": "2",
            "type": "startTestItem",
            "job_id": self.uuid,
            "test": nodeid,
            "startTime": str(time.time())})

    def pytest_runtest_logreport(self, report):
        if report.when == "call" and report.outcome == "failed":
            if report.failed and not hasattr(report, "wasxfail"):
                # "name": item.name,
                # "suite": str(item.parent),
                # "desc": item.name,
                # "reason": report
                self.post({
                    "fw": "2",
                    "type": "stopTestItem",
                    "job_id": self.uuid,
                    "test": report.nodeid,
                    "status": "failed",
                    "msg": str(report.longreprtext),
                    "stopTime": str(time.time())
                })
        elif report.when == "call" and report.outcome == "passed":
            self.post({
                "fw": "2",
                "type": "stopTestItem",
                "job_id": self.uuid,
                "test": report.nodeid,
                "status": "passed",
                "msg": str(report.longreprtext),
                "stopTime": str(time.time())
            })
        elif (report.when == "call" and report.outcome == "skipped") or (report.when == "setup" and
                                                                         report.outcome == "skipped"):
            self.post({
                "fw": "2",
                "type": "stopTestItem",
                "job_id": self.uuid,
                "test": report.nodeid,
                "status": "skipped",
                "msg": str(report.longreprtext),
                "stopTime": str(time.time())
            })

    def pytest_sessionfinish(self, session):
        self.post({
            "fw": "2",
            "type": "stopTestRun",
            "job_id": self.uuid,
            "stopTime": str(time.time())})


def pytest_addoption(parser):
    group = parser.getgroup("pytest-rt")
    group.addoption("--rt", default=False, dest="rt", action="store_true", help="Enable realtime status send")
    group.addoption("--rte", default=None, dest="env", action="store", help="Environment")
    group.addoption("--rtu", default=None, dest="url", action="store", help="Testgr URL")


def pytest_configure(config):
    rt = config.getoption("rt")
    env = config.getoption("env")
    url = config.getoption("url")
    if rt:
        plugin = Rt(config)
        config._rt = plugin
        config.pluginmanager.register(plugin)


def pytest_unconfigure(config):
    plugin = getattr(config, "_rt", None)
    if plugin is not None:
        del config._rt
        config.pluginmanager.unregister(plugin)