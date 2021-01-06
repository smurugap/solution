import gevent
import os
import uuid

from multiprocessing import Process

ROLES = ["SaaS", "ServiceProvider", "Organization", "Department"]
EVENTS = ['onboard', 'update', 'delete', 'teardown']
ARTIFACT_DIR = "/artifacts"
SCRIPT_DIR = "/jfm-test/Tests/Solution/"

def get_env_str(env):
    env_str = ""
    for k, v in env.items():
        env_str = env_str + "%s=%s "%(k, v)
    return env_str

def justprint(*args, **kwargs):
    print(*args, **kwargs)

def execute(role, artifact, event, user_input, execution_id):
    #env_str = get_env_str(env)
    #subprocess.run("pytest --artifact %s -m %s --user_input %s --exec_id %s Tests/Solution/%s"%(
    #    artifact, event, user_input, execution_id, role), shell=True)
    print(script, artifact, event)

class Orchestrator(object):
    def __init__(self, execution_id=None):
        self.execution_id = execution_id or uuid.uuid4()
        self.create_artifacts_dir()

    def create_artifacts_dir(self):
        for role in ROLES:
            os.makedirs(self.get_artifacts_dir(role), exist_ok=True)

    def get_artifacts_dir(self, role):
        return os.path.join(ARTIFACT_DIR, self.execution_id, role)

    @staticmethod
    def get_next_role(role):
        return ROLES[ROLES.index(role) + 1]

    @staticmethod
    def get_prev_role(role):
        if role == ROLES[0]:
            return ROLES[-1]
        return ROLES[ROLES.index(role) - 1]

    @staticmethod
    def get_next_event(event):
        return EVENTS[EVENTS.index(event) + 1]

    @staticmethod
    def get_next_role_event(role, event):
        if role == 'Organization' and event == 'onboard':
            return 'Department', 'update'
        elif event != 'onboard':
            if role == 'SaaS':
                event = Orchestrator.get_next_event(event)
            role = Orchestrator.get_prev_role(role)
            return role, event
        elif event == 'onboard':
            role = Orchestrator.get_next_role(role)
            return role, event

    def execute(self, role, event):
        script = os.path.join(SCRIPT_DIR, role)
        if role == 'SaaS':
            artifact = os.path.join(self.get_artifacts_dir('SaaS'), 'saas.yml')
            execute(script, artifact, event)
            if event == 'teardown':
                return
            next_role, next_event = Orchestrator.get_next_role_event(role, event)
            self.execute(next_role, next_event)
        else:
            greenlets = list()
            next_role, next_event = Orchestrator.get_next_role_event(role, event)
            for filename in os.listdir(self.get_artifacts_dir(role)):
                artifact = os.path.join(self.get_artifacts_dir(role), filename)
                greenlets.append(gevent.spawn(execute, script, artifact, event))
            gevent.joinall(greenlets)
            self.execute(next_role, next_event)

obj = Orchestrator(execution_id="aabb")
obj.execute(role='SaaS', event='onboard')
