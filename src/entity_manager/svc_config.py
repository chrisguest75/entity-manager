import os


class SvcConfig(object):

    __instance = None

    def __init__(self):
        self._server_port = os.environ.get('ENTITY_MANAGER_SERVER_PORT',
                                           '9099')

    @staticmethod
    def get_instance():
        if SvcConfig.__instance is None:
            SvcConfig.__instance = SvcConfig()
        return SvcConfig.__instance

    @property
    def server_port(self):
        return int(self._server_port)
