#!/usr/bin/env python3

from subprocess import PIPE,Popen,\
check_output,DEVNULL,call,CalledProcessError,\
TimeoutExpired

import os


def backup_brew_list(file_name):
    print('backing up brew list to - '+file_name)
    command = 'brew list | cat > '+file_name
    try:
        print('Running cmd - '+command)
        p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        response,_ = p.communicate(input=None, timeout=900)
        response = response.decode('utf8')
        response  = response.split('\n')
        for response_line in response:
            if 'error' in response_line or 'fail' in response_line:
                    print(response_line)
        print(response)
        #p.kill()
    except (Exception) as e:
        p.kill()
        print(e)

def install_pkg():
    backup_brew_list('backup_brew_list.txt')
    f_pkg_list = open('pkg_list.txt','r')
    f_log = open('pkg_install_log.txt','w')
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
            f_log.write(response[len(response)-1])
            #p.kill()
            count = count + 1
        except (Exception) as e:
            p.kill()
            f_log.write('error in '+pkg)
            f_log.write(e)
    f_pkg_list.close()
    f_log.close()

def get_pkg_diff():
    pkg_diff_list = []
    f_pkg_list_bkp = open('backup_brew_list.txt','r')
    new_pkg_list = f_pkg_list_bkp.readlines()
    f_pkg_list_bkp.close()
    command = 'brew list'
    try:
        print('Running cmd - '+command)
        p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        response,_ = p.communicate(input=None, timeout=900)
        response = response.decode('utf8')
        response  = response.split('\n')
        for pkg in new_pkg_list:
            if pkg not in response:
                pkg_diff_list.add(pkg)
    except (Exception) as e:
        p.kill()
        print(e)
    return pkg_diff_list

def remove_pkgs(pkg_list):
     f_log = open('pkg_remove_log.txt','w')
    for pkg in pkg_list:
        command = 'brew remove '+pkg
        try:
            print('Running cmd - '+command)
            p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            response,_ = p.communicate(input=None, timeout=900)
            response = response.decode('utf8')
            f_log.write('removing '+pkg)
            response  = response.split('\n')
            for response_line in response:
                if 'error' in response_line or 'fail' in response_line:
                        f_log.write(response_line)
            f_log.write(response[len(response)-1])
            #p.kill()
            count = count + 1
        except (Exception) as e:
            p.kill()
            f_log.write('error in '+pkg)
            f_log.write(e)
    f_log.close()

def main():
    backup_brew_list()

if __name__ == '__main__':
    main()

