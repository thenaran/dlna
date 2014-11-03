#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012-2014 Narantech Inc. All rights reserved.
#  __    _ _______ ______   _______ __    _ _______ _______ _______ __   __
# |  |  | |   _   |    _ | |   _   |  |  | |       |       |       |  | |  |
# |   |_| |  |_|  |   | || |  |_|  |   |_| |_     _|    ___|       |  |_|  |
# |       |       |   |_||_|       |       | |   | |   |___|       |       |
# |  _    |       |    __  |       |  _    | |   | |    ___|      _|       |
# | | |   |   _   |   |  | |   _   | | |   | |   | |   |___|     |_|   _   |
# |_|  |__|__| |__|___|  |_|__| |__|_|  |__| |___| |_______|_______|__| |__|

# default
import os
import logging
import subprocess
from threading import Thread

# clique
import clique.runtime


__SET_FLAG__ = os.path.join(clique.runtime.home_dir(), "_flag")
__PREPARE__ = os.path.join(clique.runtime.res_dir(), "prepare.sh")
__CONF__ = os.path.join(clique.runtime.res_dir(), "minidlna.conf")


def _execute_dlna():
  cmd = "sudo /usr/local/sbin/minidlnad -f {path} -R".format(path=__CONF__)
  try:
    subprocess.check_call(cmd, shell=True)
    logging.info("Execute dlna.")
  except:
    logging.warn("Failed to execute dlna.", exc_info=True)


def _execute_dlna_renderer():
  cmd = "gmediarender -f %s" % clique.runtime.node_name()
  try:
    subprocess.check_call(cmd, shell=True)
    logging.info("Executed dlna renderer.")
  except:
    logging.warn("Failed to execute dlna renderer.", exc_info=True)


def initialize():
  if not os.path.exists(__SET_FLAG__):
    cmd = "sudo sh {prepare} {nodename} {appname};touch {flag}".format(prepare=__PREPARE__,
                                                                       nodename=clique.runtime.node_name(),
                                                                       appname=clique.runtime.app_name(),
                                                                       flag=__SET_FLAG__)
    try:
      subprocess.check_call(cmd, shell=True)
    except:
      logging.warn("Failed to initialize.", exc_info=True)
      if os.path.exists(__SET_FLAG__):
        subprocess.check_call("rm {flag}".format(flag=__SET_FLAG__),
                              shell=True)

def set_name():
  conf_path = os.path.join(clique.runtime.res_dir(), "minidlna.conf")
  cmd = "sed -i 's/^friendly_name=.*/friendly_name={}/g' {}".format(clique.runtime.node_name(), conf_path)
  try:
    subprocess.check_call(cmd, shell=True)
  except:
    logging.warn("Failed to set dlna name.", exc_info=True)


def start():
  try:
    logging.debug("Boot dlna app...")
    initialize()
    set_name()
    Thread(target=_execute_dlna).start()
    Thread(target=_execute_dlna_renderer).start()
    logging.debug("Start dlna app.")
  except:
    logging.exception("Failed to start the dlna...")
    raise


if __name__ == '__main__':
  start()
