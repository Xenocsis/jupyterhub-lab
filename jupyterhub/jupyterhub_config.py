import json
from dockerspawner import DockerSpawner
from jupyterhub.auth import Authenticator
import os

c = get_config()
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = "notebook-image"
c.DockerSpawner.cmd = ["start-singleuser.sh"]
c.DockerSpawner.network_name = "jupyterhub-lab_jupyterhub-network"
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = True

c.DockerSpawner.notebook_dir = "/home/jovyan/work"


c.DockerSpawner.volumes = {
    "jupyterhub-user-{username}": "/home/jovyan/work"
}

c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.hub_ip = "0.0.0.0"
c.DockerSpawner.post_start_cmd = """
bash -c '
if [ ! -f /home/jovyan/work/default.ipynb ]; then
    cp /srv/default.ipynb /home/jovyan/work/default.ipynb
fi
'
"""
class FileAuth(Authenticator):

    def load_users(self):
        with open("/srv/jupyterhub/users.json") as f:
            return json.load(f)

    async def authenticate(self, handler, data):
        users = self.load_users()

        username = data.get("username")
        password = data.get("password")

        if users.get(username) == password:
            return username

        return None

c.JupyterHub.authenticator_class = FileAuth
c.Authenticator.allow_all = True
