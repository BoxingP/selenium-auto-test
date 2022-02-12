import datetime
import json
import os
import re
import time


class JSONReport(object):
    def __init__(self, json_path):
        self.json_path = os.path.abspath(os.path.expanduser(os.path.expandvars(json_path)))
        self.nodes = {}
        self.summary = {}
        self.run_index = 0
        self.session_start_time = None
        self.created_at = None

    def generate_report(self, tests):
        report = {
            'report': {
                'tests': tests,
                'summary': self.summary,
                'created_at': self.created_at
            }
        }
        return report

    def get_outcome(self, report):
        if report.failed:
            if report.when != 'call':
                return 'error'
            else:
                if hasattr(report, 'wasxfail'):
                    return 'xpassed'
                else:
                    return 'failed'
        elif report.skipped:
            if hasattr(report, 'wasxfail'):
                return 'xfailed'
            else:
                return 'skipped'
        return report.outcome

    def get_overall_outcome(self, report):
        if report['setup']['outcome'] != 'passed':
            return report['setup']['outcome']
        if report['call']['outcome'] == 'passed':
            return report['teardown']['outcome']
        return report['call']['outcome']

    def generate_stage_report(self, report):
        outcome = self.get_outcome(report)

        stage_report = {
            'name': report.when,
            'duration': getattr(report, 'duration', 0.0),
            'outcome': outcome
        }

        if hasattr(report, 'wasxfail'):
            stage_report['xfail_reason'] = report.wasxfail

        if report.longrepr:
            stage_report['longrepr'] = str(report.longrepr)

        stage_matcher = re.compile(r'^Captured (.+) {}$'.format(report.when))
        for header, content in report.sections:
            match = stage_matcher.match(header)
            if match:
                stage_report[match.group(1)] = content

        return stage_report

    def update_summary(self, outcome, report):
        if report.passed and report.when != 'call':
            return
        if outcome not in self.summary:
            self.summary[outcome] = 1
        else:
            self.summary[outcome] += 1

    def pytest_runtest_logreport(self, report):
        stage_report = self.generate_stage_report(report)

        self.update_summary(stage_report['outcome'], report)

        if report.nodeid not in self.nodes:
            self.nodes[report.nodeid] = {
                'name': report.nodeid,
                'duration': stage_report['duration'],
                'run_index': self.run_index
            }
            self.run_index += 1

        self.nodes[report.nodeid][report.when] = stage_report
        self.nodes[report.nodeid]['duration'] += stage_report['duration']

    def pytest_sessionstart(self, session):
        self.session_start_time = time.time()

    def pytest_sessionfinish(self, session):
        session_stop_time = time.time()
        session_duration = session_stop_time - self.session_start_time

        self.created_at = str(datetime.datetime.now())

        self.summary['num_tests'] = len(self.nodes)
        self.summary['duration'] = session_duration

        tests = []
        for test, detail in self.nodes.items():
            detail['outcome'] = self.get_overall_outcome(detail)
            tests.append(detail)

        report = self.generate_report(tests)

        if not os.path.exists(os.path.dirname(self.json_path)):
            os.makedirs(os.path.dirname(self.json_path))

        with open(self.json_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(report))
