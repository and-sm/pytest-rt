import json
import pytest
import uuid
import time
import requests
import hashlib
from _pytest.runner import runtestprotocol


class Rt:

    def __init__(self, config=None):

        self.config = config
        self.uuid = str(uuid.uuid4())
        self.endpoint = config.option.url
        self.rt_custom_id = config.option.rt_custom_id
        self.rt_return_job = config.option.rt_return_job
        self.tests = list()
        self.test_uuid = None

    def post(self, payload):

        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        try:
            requests.post(self.endpoint, data=json.dumps(payload), headers=headers)
        except requests.exceptions.ConnectionError as error:
            print(error)

    def generate_id(self, data):

        string = (self.rt_custom_id + data).encode('utf-8')
        return str(int(hashlib.md5(string).hexdigest(), 16))[0:31]

    def append_test(self, item):

        node = dict()
        node["location"] = item.location[2]
        node["nodeid"] = item.nodeid
        if self.rt_custom_id:
            node["uuid"] = self.generate_id(item.nodeid)
        else:
            node["uuid"] = str(uuid.uuid4())
        node["description"] = item._obj.__doc__
        self.tests.append(node)

    def pytest_collection_modifyitems(self, session, items, config):

        from _pytest.mark import deselect_by_keyword, deselect_by_mark

        deselect_by_keyword(items, config)
        deselect_by_mark(items, config)

        for item in session.items:
            self.append_test(item)

        self.post({"fw": "2",
                   "type": "startTestRun",
                   "tests": self.tests,
                   "env": session.config.option.env,
                   "custom_data": session.config.option.rt_custom_data,
                   "startTime": time.time(),
                   "job_id": self.uuid,
                   "custom_id": self.rt_custom_id})

    def pytest_runtest_logstart(self, nodeid):

        for item in self.tests:
            if item["nodeid"] == nodeid:
                self.test_uuid = item["uuid"]

        if self.test_uuid is not None:
            self.post({
                "fw": "2",
                "type": "startTestItem",
                "job_id": self.uuid,
                "uuid": self.test_uuid,
                "custom_id": self.rt_custom_id,
                "startTime": str(time.time())})

    def pytest_runtest_logreport(self, report):

        if self.test_uuid is not None:
            if report.when == "call" and report.outcome == "failed":
                if report.failed and not hasattr(report, "wasxfail"):
                    screens_for_upload = ""
                    if hasattr(pytest, 't_screen'):
                        screens_for_upload = pytest.t_screen
                    self.post({
                        "fw": "2",
                        "type": "stopTestItem",
                        "job_id": self.uuid,
                        "uuid": self.test_uuid,
                        "custom_id": self.rt_custom_id,
                        "status": "failed",
                        "msg": str(report.longreprtext) + "\n\nCaptured stdout call:\n" + str(report.capstdout),
                        "stopTime": str(time.time()),
                        "screens": screens_for_upload
                    })
            elif report.when == "setup" and report.outcome == "failed":
                if report.failed and not hasattr(report, "wasxfail"):
                    screens_for_upload = ""
                    if hasattr(pytest, 't_screen'):
                        screens_for_upload = pytest.t_screen
                    self.post({
                        "fw": "2",
                        "type": "stopTestItem",
                        "job_id": self.uuid,
                        "uuid": self.test_uuid,
                        "custom_id": self.rt_custom_id,
                        "status": "failed",
                        "msg": str(report.longreprtext) + "\n\nCaptured stdout call:\n" + str(report.capstdout),
                        "stopTime": str(time.time()),
                        "screens": screens_for_upload
                    })
            elif report.when == "call" and report.outcome == "passed":
                screens_for_upload = ""
                if hasattr(pytest, 't_screen'):
                    screens_for_upload = pytest.t_screen
                self.post({
                    "fw": "2",
                    "type": "stopTestItem",
                    "job_id": self.uuid,
                    "uuid": self.test_uuid,
                    "custom_id": self.rt_custom_id,
                    "status": "passed",
                    "msg": str(report.longreprtext),
                    "stopTime": str(time.time()),
                    "screens": screens_for_upload
                })
            elif (report.when == "call" and report.outcome == "skipped") or (report.when == "setup" and
                                                                             report.outcome == "skipped"):
                self.post({
                    "fw": "2",
                    "type": "stopTestItem",
                    "job_id": self.uuid,
                    "uuid": self.test_uuid,
                    "custom_id": self.rt_custom_id,
                    "status": "skipped",
                    "msg": str(report.longreprtext),
                    "stopTime": str(time.time())
                })

    def send_report(self, session):

        if session.config.option.rt_job_report is True:
            return "1"
        return "0"

    def pytest_sessionfinish(self, session):

        self.post({
            "fw": "2",
            "type": "stopTestRun",
            "job_id": self.uuid,
            "custom_id": self.rt_custom_id,
            "stopTime": str(time.time()),
            "send_report": self.send_report(session)})
        if self.rt_return_job:
            with open("testgr_last_job.txt", "w") as file:
                file.write(self.uuid)


def pytest_addoption(parser):
    group = parser.getgroup("pytest-rt")
    group.addoption("--rt", default=False, dest="rt", action="store_true", help="Enable realtime status send")
    group.addoption("--rte", default=None, dest="env", action="store", help="Environment")
    group.addoption("--rtu", default=None, dest="url", action="store", help="Testgr URL")
    group.addoption("--rt-custom-id", default=None, dest="rt_custom_id", action="store",
                    help="Custom ID, required for pytest-xdist")
    group.addoption("--rt-job-report", default=None, dest="rt_job_report", action="store_true",
                    help="Send Testgr job result via email")
    group.addoption('--rt-custom-data', dest='rt_custom_data',
                    help='With --rt-custom-data {\"key\": \"value\"} option you can send additional data to '
                         'Testgr server')
    group.addoption('--rt-return-job', dest='rt_return_job', action="store_true",
                    help='With --rt-return-job option you can return job UUID')


def pytest_configure(config):
    rt = config.getoption("rt")
    if rt:
        plugin = Rt(config)
        config._rt = plugin
        config.pluginmanager.register(plugin)


def pytest_unconfigure(config):
    plugin = getattr(config, "_rt", None)
    if plugin is not None:
        del config._rt
        config.pluginmanager.unregister(plugin)


