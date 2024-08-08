#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description:

Paramiko library. It creates an object connected to a remote machine (via password or rsa key). It provides
methods for the following operations: 
1. Copy files from remote to another remote machine
2. Upload/download a file or multiple files from remote


Requirements:
- Install paramiko:
pip3 install paramiko

@Author: mmir01
@Date: 08/08/2024
'''

import logging
import paramiko
import sys
import os


class paramikoSSH(object):
    '''
    We use Paramiko to connect to the remote machine
    '''
    def __init__(self, host, user, password=None, keyfile=None):
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        self.client = paramiko.client.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if(password):
            self.client.connect(host, port=22, username=user, password=password)
        elif(keyfile):
            self.client.connect(host, port=22, username=user, look_for_keys=False, pkey=keyfile, disabled_algorithms={'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']})
        else:
            print("Error. Password o public key needed")
            sys.exit(2)

    def __del__(self):
        self.client.close()

    '''
    Copy files in a directory from this remote (self) to a different one.
    remoteConnection: object returned when used this class (paramikoSSH)
    fileDict: dictionary where a key is the absolute path of the file
    to copy, and the value the absolute path in the destination
    ''' 
    def copyMultipleFilesToRemote(self, remoteConnection, fileDict):
        remote1Sftp = self.client.open_sftp()
        remote2Sftp = remoteConnection.client.open_sftp()

        for src, dst in fileDict.items():
            try:
                logging.info("Copying: %s in %s" % (src, dst))
                filedesc = remote1Sftp.file(src)
                remote2Sftp.putfo(filedesc, dst, confirm=True)
                logging.info("Copied")

            except FileNotFoundError as err:
                logging.error("Copy failed: %s " % err)      

        remote1Sftp.close()
        remote2Sftp.close()

    '''
    Copy files with the same extension from this remote (self) to a different 
    one.
    remoteConnection: object returned when used this class (paramikoSSH)
    origin: origin of the files to copy
    destination: destination of the files in the other remote machine
    extension: extension used to create a list with the files to copy
    ''' 
    def copyFilesWithExtensionToRemote(self, remoteConnection, origin, destination, extension):
        remote1Sftp = self.client.open_sftp()
        files = remote1Sftp.listdir(origin)
        files_to_copy = [ file for file in files if file.endswith(extension) ]
            
        if not files_to_copy:
            logging.error("No files found") 
            sys.exit(3)

        remote2Sftp = remoteConnection.client.open_sftp()
        for file_to_copy in files_to_copy:
            try:
                logging.info("Copying file: %s" % file_to_copy)
                #Linux based
                path_origin = origin + "/" + file_to_copy
                path_dest = destination + "/" + file_to_copy

                logging.debug("Copying: %s in %s" % (path_origin, path_dest))
                filedesc = remote1Sftp.file(path_origin)
                remote2Sftp.putfo(filedesc, path_dest, confirm=True)
                logging.info("Copied")

            except FileNotFoundError as err:
                logging.error("Copy failed: %s " % err)      

        remote1Sftp.close()
        remote2Sftp.close()

    '''
    Download a file from the remote machine
    ''' 
    def downloadFile(self, remote_file_path, local_path):
        sftp_connection = self.client.open_sftp()
        try:
            sftp_connection.get(remote_file_path, local_path, callback=self.__progress)
        except FileNotFoundError as err:
            logging.error("Download failed: %s" % err)
        sftp_connection.close()

    '''
    Download multiple files from the destination folder with the same extension
    ''' 
    def downloadFiles(self, origin, destination, extension):
        logging.debug('Getting files from remote...')
        sftp_connection = self.client.open_sftp()

        files = sftp_connection.listdir(origin)
        files_to_copy = [ file for file in files if file.endswith(extension) ]
        
        if not files_to_copy:
            logging.error("No files found") 
            sys.exit(3)

        for file_to_copy in files_to_copy:
            try:
                logging.info("Downloading: %s" % file_to_copy)
                #Linux based
                path_origin = origin + "/" + file_to_copy
                # Could be Linux or Windows
                path_dest = os.path.join(destination, file_to_copy)
                logging.debug("Downloading: %s in %s" % (path_origin, path_dest))
                sftp_connection.get(path_origin, path_dest, callback=self.__progress)
                logging.info("Downloaded")
            except FileNotFoundError as err:
                logging.error("Download failed: %s " % err)      

        sftp_connection.close()

    '''
    Execute the command provided in the remote machine and print an error if the exit code is not 0
    '''
    def executeCommand(self, command, errorMessage, verbose=False):
        command_return = self.__sendCommand(command, verbose)
        if(command_return != 0):
            logging.error('Command execution failed: %s' % errorMessage)
            sys.exit(127)
        logging.info('Command OK')

    '''
    Upload a file to the remote machine
    '''
    def uploadFile(self, file, remote_directory):
        sftp_connection = self.client.open_sftp()
        try:
            sftp_connection.put(file, remote_directory, callback=self.__progress, confirm=True)
        except FileNotFoundError as err:
            logging.error("Upload failed: %s" % err)
        sftp_connection.close()  
            
    '''
    Upload multiple files from the origin folder with the same extension
    ''' 
    def uploadFiles(self, origin, destination, extension):
        logging.debug('Uploading files from local...')
        sftp_connection = self.client.open_sftp()

        files = os.listdir(origin)
        files_to_copy = [ file for file in files if file.endswith(extension) ]
        
        if not files_to_copy:
            logging.error("No files found") 
            sys.exit(3)
        
        for file_to_copy in files_to_copy:
            try:
                logging.info("Uploading: %s" % file_to_copy)
                # Could be Linux or Windows
                path_origin = os.path.join(origin, file_to_copy)
                # Linux based
                path_dest = destination + "/" + file_to_copy
                logging.debug("Uploading: %s in %s" % (path_origin, path_dest))
                sftp_connection.put(path_origin, path_dest, callback=self.__progress, confirm=True)
                logging.info("Uploaded")
            except FileNotFoundError as err:
                logging.error("Upload failed: %s " % err)      

        sftp_connection.close()

    '''
    Print SCP progress (%)
    '''
    def __progress(self, sent, size):
        print("Progress: %.2f%%" % (float(sent)/float(size)*100), end="\r")

    '''
    Print SCP progress (bytes)
    '''
    def __progressBytes(self, sent, size):
        print("Progress: %d/%d" % (int(sent),int(size)), end="\r")

    '''
    Execute command in the remote machine
    Return the command exit code
    '''
    def __sendCommand(self, command, verbose=False):       
        logging.debug("Executing: %s " % command)
        stdin, stdout, stderr = self.client.exec_command(command)
        
        #Printing line by line if required
        if(verbose):
            line = stdout.readline()
            while (line != ""):
                sys.stdout.write(line)
                line = stdout.readline()  
            
        stdin.close()
        ret_code = stdout.channel.recv_exit_status()
        if(ret_code != 0):
            logging.error("Error code: %d" % ret_code)
            logging.error("Error message: %s" % stderr.read())
        
        return ret_code
