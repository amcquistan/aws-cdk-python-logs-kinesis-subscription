import logging
import time
import random
import sys


logging.basicConfig(
  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
  handlers=[
      logging.StreamHandler(sys.stdout)
  ]
)


def make_log_stmt():
  i = random.randint(0, 4)
  if i < 3:
    logging.info("Houston, we are clear for take off")
  else:
    logging.error("Houston, we have a problem")


def main():
  while True:
    make_log_stmt()
    time.sleep(10)


if __name__ == '__main__':
  main()
