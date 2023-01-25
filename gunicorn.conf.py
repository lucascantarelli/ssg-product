import structlog
import structlog_extensions

"""
# Classe de configuração do Gunicorn
# https://docs.gunicorn.org/en/stable/settings.html
"""

# SERVER SOCKET
bind = "127.0.0.1:443"
backlog = 2048

# DEBUGGING
reload = True
reload_engine = "auto"

# CONFIGURATION
print_config = False

# WORKER PROCESSES
workers = 3
worker_class = "gthread"
worker_connections = 1000
timeout = 30
keepalive = 2

# PROCESS MANAGEMENT
proc_name = "ssg-product"

# SSL
certfile = "certs/localhost.crt"
ssl_version = "TLSv1_2"
keyfile = "certs/localhost.key"


# LOGGING
errorlog = "logs/gunicorn.log"
loglevel = "info"
capture_output = True

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
        structlog_extensions.processors.CombinedLogParser("gunicorn.access"),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


pre_chain = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
]

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "error_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": pre_chain,
        },
        "access_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "error_formatter",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "error_formatter",
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access_formatter",
        }
    },
    'loggers': {
        'gunicorn.error': {
            'handlers': ['error_console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'flask.app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['access_console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}
