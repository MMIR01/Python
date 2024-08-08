#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description:

Example about how to use the paramikoSSHLibrary.


Requirements:
- Install paramiko:
pip3 install paramiko --proxy http://87.254.212.120:8080
- Update config.ini accordingly

Arguments:
--log: set logging level. Choose between: debug, info, error (default level INFO)

Error code:
1 - Local error
2 - Connection error (Wrong password or RSA key)
3 - Upload/download error


@Author: mmir01
@Date: 08/08/2024

Future work:
- Get md5sum in every transaction and compare to check files are no corrupted

'''

import argparse
import configparser
import getpass
import logging
import paramiko
import subprocess
import os
import sys
import time
from datetime import datetime
from paramikoSSHLibrary import paramikoSSH


'''
Execute command in a local shell
'''
def executeCommandLocal(command):
    try:
        subprocess.run([command], shell=True, check=True)
    except subprocess.TimeoutExpired as timeout:
        logging.error('Timeout while executing the command')
    except subprocess.CalledProcessError as e:
        logging.error('Error with command: %s' % command)
        sys.exit(1)


if __name__ == "__main__": 
    parser=argparse.ArgumentParser(description='''Script to copy files between two remote machines''')
    parser.add_argument('--log', '-l', dest="loglevel", default='DEBUG', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='set logging level (default level INFO)')
        
    #Start time
    startTime = time.time()
    
    #Get parameters from command line
    args=parser.parse_args()
    loglevel = args.loglevel

    numLevel = getattr(logging, loglevel.upper(), logging.INFO)
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y/%m/%d-%I:%M:%S', level=numLevel)

    # Reading from config file
    file = sys.argv[0]
    path = os.path.dirname(file)
    configFile = os.path.join(path, 'config.ini')

    if not os.path.isfile(configFile):
        logging.error("Config file not found")
        sys.exit(1)
    
    config = configparser.ConfigParser()
    config.read(configFile)

    machine1 = config.get('MACHINE1','address')
    machine1User = config.get('MACHINE1', 'user')
    machine1Folder = config.get('MACHINE1', 'machine1Folder')

    machine2 = config.get('MACHINE2','address')
    machine2User = config.get('MACHINE2', 'user')
    machine2Folder = config.get('MACHINE2', 'machine2Folder')


    # For this example, we will connect to the machine1 vi an rsaKey, and via password for the machine2
    if (not config.getboolean('MACHINE1','isRsaKey')):
        try:
            logging.info('Introduce password')
            machine1Pass = getpass.getpass()
        except Exception as error:
            logging.error('Error: ', error)
            sys.exit(2)
        
        logging.info('Connecting to machine 1: %s' % machine1)
        machine1Connection = paramikoSSH(host=machine1,user=machine1User,password=machine1Pass)
    else:
        keyfile = paramiko.RSAKey.from_private_key_file(config.get('MACHINE1','rsaPath'))
        logging.info('Connecting to: %s' % machine1)
        machine1Connection = paramikoSSH(host=machine1,user=machine1User,keyfile=keyfile)

    if (not config.getboolean('MACHINE2','isRsaKey')):
        try:
            logging.info('Introduce password')
            machine2Pass = getpass.getpass()
        except Exception as error:
            logging.error('Error: ', error)
            sys.exit(2)
        
        logging.info('Connecting to machine 2: %s' % machine2)
        machine2Connection = paramikoSSH(host=machine2,user=machine2User,password=machine2Pass)
    else:
        keyfile = paramiko.RSAKey.from_private_key_file(config.get('MACHINE2','rsaPath'))
        logging.info('Connecting to: %s' % machine2)
        machine2Connection = paramikoSSH(host=machine2,user=machine2User,keyfile=keyfile)


    # Dict with files to download from machine1
    fileDict = {}

    file1_src = "<file_origin_path>"
    file1_dst = "<file_dest_path>"
    fileDict.update(file1_src, file1_dst)
    
    file2_src = "<file_origin_path>"
    file2_dst = "<file_dest_path>"
    fileDict.update(file2_src, file2_dst)

    logging.info('Downloading...')
    for src,dst in fileDict:
        machine1Connection.downloadFile(src, dst)

    # Download files with the same extension
    dateNow = datetime.now()
    dateStr = dateNow.strftime("%Y%m%d_%I%M%S")
    newFolder = "/tmp/" + dateStr
    command = "mkdir " + newFolder
    executeCommandLocal(command)

    machine1Connection.downloadFiles(machine1Connection, newFolder, ".rpm")  

    # Copy files from machine1 to machine2
    fileDict = {}

    file1_src="<path_machine1>"
    file1_dst="<path_machine2>"
    fileDict.update({file1_src: file1_dst})

    file2_src="<path_machine1>"
    file2_dst="<path_machine2>"
    fileDict.update({file2_src: file2_dst})

    logging.info('Copying...')
    machine1Connection.copyMultipleFilesToRemote(machine2Connection, fileDict)


    #END OF THE PROGRAM
    endTime = time.time()
    
    #Execution time
    totalTime = endTime - startTime
    timeMin = totalTime/60
    timeSec = totalTime%60
    
    logging.info("Execution time: %d min %d s" %(timeMin, timeSec))
