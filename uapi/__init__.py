import logging
import sys
log_format = '[%(asctime)s %(levelname)s] %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    stream=sys.stdout
)
