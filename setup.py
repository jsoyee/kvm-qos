#!/bin/env python

import sys
import os
import shutil
import json
from distutils.sysconfig import get_python_lib

replacefile = json.loads(open("replace.info").read())

target = get_python_lib()
tmp = "/tmp/kvm-qos"
needbackup = True

def rmdirwithdeep(path):
    list = os.listdir(path)
    for name in list:
        if os.path.isdir(path + "/" +  name):
            rmdirwithdeep(path + "/" + name)
            if os.path.exists(path + "/" + name):
                os.removedirs(path + "/" + name)
        else:
            os.remove(path + "/" +name)

def mkdirPathDir(parent, path):
    list = path.split('/')
    path = parent
    for p in list:
        path = path + "/" + p
        if not os.path.exists(path):
            os.mkdir(path)

def insertText2File(target, onwhat, insertfile):
    with open(target+"_tmp",'w') as outfile:
        with open(target, 'r') as infile:
            for line in infile:
               outfile.write(line)
               if line.find(onwhat) > -1:
                   with open(insertfile, 'r') as insertf:
                       for l in insertf:
                           outfile.write(l)
    shutil.move(target+"_tmp", target)

action = "install"

if len(sys.argv) > 1:
    action = sys.argv[1]

if cmp(action, "install") == 0:
    if os.path.exists(tmp):
        print "Please run python setup.py uninstall firstly to uninstall"
    else:
        print "KVMQoS will install to %s" % target
        os.mkdir(tmp)
        for key in replacefile.keys():
            mkdirPathDir(tmp,  key[:key.rfind('/')])
            shutil.copy(target + "/" + key, tmp + "/" + key)
            insertText2File(target + "/" + key, replacefile[key], key)
        print "KVMQoS has installed, please restart the related serivces."
else:
    if os.path.exists(tmp):
        print "KVMQoS will be uninstall and rollback to before"
        for key in replacefile.keys():
            shutil.copy(tmp + "/" + key, target + "/" + key)
        rmdirwithdeep(tmp)
        print "KVMQoS has uninstalled, please restart the related serivces."
    else:
        print "The system have not installed KVMQoS, please install firstly!"
