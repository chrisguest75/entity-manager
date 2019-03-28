# -*- coding: utf-8 -*-

import os
import json
import yaml
import logging
import logging.config
import time


def _get_logger():
    logger = logging.getLogger('entitymanager.server')
    return logger


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)


class EntityManagerServer:
    def __init__(self):
        self.logger = _get_logger()

    async def handle_request_health(self, request):
        return web.Response()


LOGGING_CONFIG_TEXT = """
version: 1
root:
  level: DEBUG
  handlers: ['console']
formatters:
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: "(asctime) (levelname) (name) (message)"
filters:
    entitymanagerlogfilter:
        (): entitymanager.server.entitymanagerLogFilter
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    stream: ext://sys.stdout
    formatter: json
    filters: [entitymanagerlogfilter]
"""


@web.middleware
async def log_error_middleware(request, handler):
    try:
        response = await handler(request)
    except aiohttp.web_exceptions.HTTPException:
        # assume if we're throwing this that it's already logged
        raise
    except Exception:
        _get_logger().exception("Unexpected exception in call")

        error_string = "Internal Server Error\n" + traceback.format_exc()
        raise aiohttp.web_exceptions.HTTPInternalServerError(text=error_string)
    return response


def initialize_web_app(app, w2v_server):
    app.middlewares.append(log_error_middleware)
    app.router.add_get('/health', server.handle_request_health)


class EntityManagerLogFilter(logging.Filter):
    def __init__(self):
        self.language = os.environ.get("ENTITY_MANAGER_LANGUAGE", "en")
        self.version = os.environ.get("ENTITY_MANAGER_VERSION", None)

    def filter(self, record):
        """Add language, and if available, the version"""
        record.entity_manager_language = self.language
        if self.version:
            record.entity_manager_version = self.version
        return True


def main():
    """Main function"""
    logging_config_file = os.environ.get("LOGGING_CONFIG_FILE", None)
    if logging_config_file:
        logging_config_path = pathlib.Path(logging_config_file)
        with logging_config_path.open() as file_handle:
            logging_config = yaml.safe_load(file_handle)
    else:
        logging_config = yaml.safe_load(LOGGING_CONFIG_TEXT)
    print("*** LOGGING CONFIG ***")
    print(logging_config)
    print("*** LOGGING CONFIG ***")
    logging.config.dictConfig(logging_config)

    config = SvcConfig.get_instance()
    server = EntityManagerServer()
    server.load(config.vectors_file)

    app = web.Application()
    initialize_web_app(app, server)
    web.run_app(app, port=config.server_port)


if __name__ == '__main__':
    main()
