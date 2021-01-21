import yaml
import gevent
import random
import os
import uuid
from gevent import subprocess

ARTIFACT_DIR = os.getenv('ARTIFACT', '/var/tmp/')
TESTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

''' Will be modified to take the below from User Input rather than hardcoded '''
ROLES = ['SaaS', 'ServiceProvider', 'Organization', 'Department']
EVENTS = ['onboard', 'execute', 'teardown']
PRODUCT = os.getenv('PRODUCT', 'CEM')
#EVENTS = ['onboard', 'update', 'delete', 'teardown']


class Node(object):
    def __init__(self, name, role, parent=None):
        self.parent = parent
        self.name = name
        self.role = role
        self.event = None
        self.running = False
        self.depth = self.parent.depth + 1 if self.parent else 0
        self.children = list()

    def add_child(self, node):
        self.children.append(node)

    def dump(self, index=0):
        print("-"*index, self.name, self.role, self.event)
        index = index + 1
        for child in self.children:
            child.dump(index)

    def sink_callback(self, callback, *args, **kwargs):
        callback(self, *args, **kwargs)
        for child in self.children:
            child.sink_callback(callback, *args, **kwargs)

    def swim_callback(self, callback, *args, **kwargs):
        callback(self, *args, **kwargs)
        self.parent.swim_callback(callback, *args, **kwargs)

class Orchestrator(object):
    def __init__(self, input_file, role='SaaS', event='onboard'):
        parsed = self.parse(input_file)
        self.input_file = input_file
        self.role = role
        self.event = event
        self.SaaS = Node('SaaS', 'SaaS')
        self.initialize(parsed)
        self.set_tree_event()
        self.exec_id = str(uuid.uuid4())

    def parse(self, input_file):
        with open(input_file, 'r') as fd:
            yargs = yaml.load(fd, Loader=yaml.FullLoader)
        return yargs

    def initialize(self, user_input):
        for role in ROLES[1:]:
            setattr(self, role, dict())
        self.initchildren(self.SaaS, user_input)

    def initchildren(self, parent, user_input):
        index = parent.depth + 1
        try:
            role = ROLES[index]
        except IndexError:
            return
        plural = role + 's'
        for name, details in user_input.get(plural, {}).items():
            node = Node(name, role, parent=parent)
            parent.add_child(node)
            getattr(self, role)[name] = node
            self.initchildren(node, details)

    def set_tree_event(self):
        if self.event == EVENTS[0] and self.role == 'SaaS':
            return
        self.SaaS.sink_callback(self.set_node_event)

    def set_node_event(self, node):
        if self.event == EVENTS[0]:
            if ROLES.index(node.role) < ROLES.index(self.role):
                node.event = self.event
        else:
            if ROLES.index(self.role) < ROLES.index(node.role):
                node.event = self.event
            else:
                node.event = EVENTS[EVENTS.index(self.event) - 1]

    def execute(self, node):
        if node.role == 'Department' and node.event == EVENTS[0]:
            return
        artifact = os.path.join(ARTIFACT_DIR, node.name+'_artifact.yaml')
        report = os.path.join(ARTIFACT_DIR, node.name+'-'+node.event+'.xml')
        print('Executing', node.name, node.role, node.event, 'report', report)
        cmd = "pytest -m %s --artifact=%s --user_input=%s --exec_id=%s"\
                " --junitxml=%s --product=%s %s"%(node.event, artifact,
                        self.input_file, self.exec_id, report,
                        PRODUCT, os.path.join(PRODUCT, node.role))
        cmd = "cd %s; %s"%(TESTDIR, cmd)
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            pass
        import time; gevent.sleep(random.randint(0, 3))

    def schedule(self):
        if self.role == 'SaaS':
            nodes = [self.SaaS]
        else:
            nodes = getattr(self, self.role).values()
        greenlets = list()
        for node in nodes:
            node.event = self.event
            greenlets.append(gevent.spawn(self._schedule, node))
        gevent.joinall(greenlets)

    def wait_till_nodes_complete(self, nodes, event):
        while True:
            for node in nodes:
                if node.event != event or node.running == True:
                    print('Waiting on node %s: state %s running %s - exp %s'%(
                        node.name, node.event, node.running, event))
                    gevent.sleep(5)
                    break
            else:
                break

    def get_next_role(self, role):
        return ROLES[ROLES.index(role) + 1]

    def get_prev_role(self, role):
        if role == 'SaaS':
            return ROLES[-1]
        return ROLES[ROLES.index(role) - 1]

    def get_next_event(self, event):
        try:
            index = EVENTS.index(event)
        except ValueError:
            index = -1
        except IndexError:
            return event
        return EVENTS[index + 1]

    def get_prev_event(self, event):
        index = EVENTS.index(event)
        return EVENTS[index - 1]

    def get_prev_nodes_event(self, node):
        if node.event == EVENTS[0]:
            if node.role == 'SaaS':
                return list(), None
            return [node.parent], EVENTS[0]
        elif node.role == ROLES[-1]:
            if node.event == ROLES[-2]:
                return list(), None
            return [self.SaaS], self.get_prev_event(node.event)
        else:
            return node.children, node.event

    def get_next_nodes_event(self, node):
        if node.event == EVENTS[0]:
            if node.role == ROLES[-1]:
                return [node], self.get_next_event(node.event)
            return node.children, EVENTS[0]
        elif node.role == 'SaaS':
            if node.event == EVENTS[-1]:
                return list(), None
            return self.Department.values(), self.get_next_event(node.event)
        else:
            return [node.parent], node.event

    def _schedule(self, node):
        prev_nodes, prev_event = self.get_prev_nodes_event(node)
        self.wait_till_nodes_complete(prev_nodes, prev_event)
        self.execute(node)
        node.running = False
        next_nodes, next_event = self.get_next_nodes_event(node)
        greenlets = list()
        for next_node in next_nodes:
            if next_node.event == next_event and next_node.running == True:
                continue
            next_node.running = True
            next_node.event = next_event
            greenlets.append(gevent.spawn(self._schedule, next_node))
        gevent.joinall(greenlets)

orchestrator = Orchestrator('/Solution/inputs/user_input.yaml', 'Department', 'teardown', 'SaaS', 'teardown')
orchestrator.schedule()
