#!/usr/bin/env python3

from subprocess import PIPE,Popen,\
check_output,DEVNULL,call,CalledProcessError,\
TimeoutExpired

import os

def install_pkg(self):
    f_pkg_list = open('pkg_list.txt','r')
    f_log = open('pakg_list_install_log.txt','w')
    pkg_list = f_pkg_list.readlines()
    count = 1
    for pkg in pkg_list and count <= 100:
        print('installing '+pkg)
        command += 'brew install '+pkg
        try:
            print('Running cmd - '+command)
            p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            response,_ = p.communicate(input=None, timeout=900)
            response = response.decode('utf8')
            f_log.write('installing '+pkg)
            response  = response.split('\n')
            for response_line in response:
                if 'error' in response_line or 'fail' in response_line:
                        f_log.write(response_line)
            f_log.write(response[len(response)])
            print(response)
            #p.kill()
            count = count + 1
        except (Exception) as e:
            p.kill()
            f_log.write('error in '+pkg)
            f_log.write(e)
            
if __name__ == '__main__':
    install_pkg()