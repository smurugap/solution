import pyinotify
import gevent
import os
import uuid

roles = ["SaaS", "ServiceProvider", "Organization", "Department"]
events = ['create', 'update', 'delete', 'teardown']
artifact_dir = "/var/tmp"
script_dir = "/root/JFM-Testing"


def execute(script, env_str):
    subprocess.run("%s python %s"%(env_str, script), shell=True)

class Orchestrator(object):
    def __init__(self, role='Saas', event='create', execution_id=None):
        self.execution_id = execution_id or uuid.uuid4()
        self.create_artifacts_dir()

    def create_artifacts_dir(self):
        for role in roles:
            os.makedirs(self.get_artifacts_dir(role))

    def get_artifacts_dir(self, role):
        return os.path.join(artifact_dir, self.execution_id, role)

    def get_next_role(self, role):
        if roles[-1] == role:
            return roles[0]
        return roles[roles.index(role) + 1]

    def get_next_event(self, event):
        return events[events.index(event) + 1]

    def get_env_str(self, env):
        env_str = ""
        for k, v in env:
            env_str = env_str + "%s=%s "%(k, v)
        return env_str

    def onboard(self, role, event, **env):
        env['PYTEST_MARKER'] = event
        script = os.path.join(script_dir, role)

        if role == 'SaaS':
            env['ARTIFACT'] = self.get_artifacts_dir('SaaS')+'saas.yml'
            env_str = self.get_env_str(env)
            execute(script, env_str)
            self.onboard(self.get_next_role(role), event)
        else:
            greenlets = list()
            for filename in os.listdirs(self.get_artifacts_dir(role)):
                env['ARTIFACT'] = filename
                env_str = self.get_env_str(env)
                greenlets.append(gevent.spawn(script, env_str, shell=True))
            gevent.join(greenlets)
            if role != 'Department':
                self.onboard(self.get_next_role(role), event)

        next_role = self.get_next_role(role)
#        next_event = self.get_next_event(event)

obj = Orchestrator(execution_id=None)
obj.onboard(role='SaaS', event='create')
obj.update(role='SaaS', event='create')
obj.delete(role='SaaS', event='create')
obj.destroy(role='SaaS', event='create')
