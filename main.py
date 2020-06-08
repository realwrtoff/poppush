#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import redis
import json


import logging
import logging.handlers
import traceback

LOG_FILE = "./poppush.log"


def init_log():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    sh = logging.StreamHandler()  # 往屏幕上输出
    sh.setFormatter(formatter)  # 设置屏幕上显示的格式
    th = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when='H', interval=1, backupCount=40)
    th.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(th)
    logger.setLevel(logging.INFO)


def main():
    opts, args = getopt.getopt(sys.argv, "h", ["help"])
    if len(args) < 2:
        queue = os.getenv('EXCEPT_QUEUE', 'except_queue')
    else:
        queue = args[1]

    redis_host = os.getenv('REDIS_HOST', '10.0.1.31')
    redis_port = int(os.getenv('REDIS_PORT', '21600'))
    redis_password = os.getenv('REDIS_PASSWORD', 'Rds123')

    rds = redis.Redis(host=redis_host, port=redis_port, db=0, password=redis_password, decode_responses=True)

    while True:
        try:
            content = rds.lpop(queue)
            if content is None:
                time.sleep(1)
                continue
            task = json.loads(content)
            length = rds.rpush(task['type'], content)
            logging.info('rpush {0}, queue length {1}'.format(task['type'], length))
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    # unittest.main()
    init_log()
    main()
