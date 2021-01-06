import pyinotify
import gevent
import os
import uuid

roles = ["SaaS", "ServiceProvider", "Organization", "Department"]
events = ['create', 'update', 'delete', 'teardown']
artifact_dir = "/var/tmp"
script_dir = "/root/JFM-Testing"


def execute(script, env_str):
    #subprocess.run("%s python %s"%(env_str, script), shell=True)
    print(script, env_str)

class Orchestrator(object):
    def __init__(self, role='Saas', event='create', execution_id=None):
        self.execution_id = execution_id or uuid.uuid4()
        self.create_artifacts_dir()

    def create_artifacts_dir(self):
        for role in roles:
            os.makedirs(self.get_artifacts_dir(role), exist_ok=True)

    def get_artifacts_dir(self, role):
        return os.path.join(artifact_dir, self.execution_id, role)

    def get_next_role(self, role):
        return roles[roles.index(role) + 1]

    def get_prev_role(self, role):
        if role == roles[0]:
            return roles[-1]
        return roles[roles.index(role) - 1]

    def get_next_event(self, event):
        return events[events.index(event) + 1]

    def get_next_role_event(self, role, event):
        if role == 'Department' and event == 'create':
            event = 'update'
            return role, event
        elif event != 'create':
            if role == 'SaaS':
                event = self.get_next_event(event)
            role = self.get_prev_role(role)
            return role, event
        elif event == 'create':
            role = self.get_next_role(role)
            return role, event

    def get_env_str(self, env):
        env_str = ""
        for k, v in env.items():
            env_str = env_str + "%s=%s "%(k, v)
        return env_str

    def execute(self, role, event, **env):
        env['PYTEST_MARKER'] = event
        script = os.path.join(script_dir, role)

        if role == 'SaaS':
            env['ARTIFACT'] = os.path.join(self.get_artifacts_dir('SaaS'), 'saas.yml')
            env_str = self.get_env_str(env)
            execute(script, env_str)
            if event == 'teardown':
                return
            next_role, next_event = self.get_next_role_event(role, event)
            self.execute(next_role, next_event)
        else:
            next_role, next_event = self.get_next_role_event(role, event)
            greenlets = list()
            for filename in os.listdir(self.get_artifacts_dir(role)):
                env['ARTIFACT'] = os.path.join(self.get_artifacts_dir(role), filename)
                env_str = self.get_env_str(env)
                greenlets.append(gevent.spawn(execute, script, env_str))
            gevent.joinall(greenlets)
            self.execute(next_role, next_event)

obj = Orchestrator(execution_id="aabb")
obj.execute(role='SaaS', event='create')
