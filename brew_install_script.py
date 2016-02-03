#!/usr/bin/env python3

from subprocess import PIPE,Popen,\
check_output,DEVNULL,call,CalledProcessError,\
TimeoutExpired

import os


def backup_brew_list(file_name):
    print('backing up brew list to - '+file_name+'.txt')
    command = 'brew list | cat > '+file_name+'.txt'
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
        print(str(e)+'\n')

def install_pkg(file_name):
    f_pkg_list = open(file_name+'.txt','r')
    f_log = open(file_name+'.log','w')
    pkg_list = f_pkg_list.readlines()
    count = 1
    for pkg in pkg_list:
        if count <= 100:
            print('installing '+pkg)
            command = 'brew install '+pkg
            try:
                print('Running cmd - '+command)
                p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                response,_ = p.communicate(input=None, timeout=300)
                response = response.decode('utf8')
                f_log.write('installing '+pkg)
                response  = response.split('\n')
                for response_line in response:
                    if 'error' in response_line or 'fail' in response_line:
                        f_log.write(response_line+'\n')
                f_log.write(response[len(response)-2]+'\n')
                #p.kill()
                count = count + 1
            except (Exception) as e:
                p.kill()
                f_log.write('error in '+pkg+'\n')
                f_log.write(str(e)+'\n')
        f_log.write('\n\n\n\n')
    f_pkg_list.close()
    f_log.close()

def get_pkg_diff(backup_file_name):
    pkg_diff_list = []
    f_pkg_list_bkp = open(backup_file_name+'.txt','r')
    bckup_pkg_list = f_pkg_list_bkp.readlines()
    f_pkg_list_bkp.close()
    command = 'brew list'
    try:
        print('Running cmd - '+command)
        p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        response,_ = p.communicate(input=None, timeout=300)
        response = response.decode('utf8')
        response  = response.split('\n')
        print('response of brew list - '+str(response))
        print('response of backup list - '+str(bckup_pkg_list))
        for pkg in response:
            if pkg+'\n' not in bckup_pkg_list and pkg != '':
                pkg_diff_list.append(pkg)
    except (Exception) as e:
        p.kill()
        print(str(e)+'\n')
    f_pkg_list_bkp.close()
    return pkg_diff_list

def clear_brew_cache():
    command = 'brew remove '+pkg
    try:
        print('Running cmd - '+command)
        p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        response,_ = p.communicate(input=None, timeout=300)
        response = response.decode('utf8')
        response  = response.split('\n')

    except (Exception) as e:
        p.kill()
        print(str(e)+'\n')

def remove_pkgs(pkg_list):
    f_log = open('pkg_list_remove.log','w')
    for pkg in pkg_list:
        command = 'brew remove '+pkg
        try:
            print('Running cmd - '+command)
            p = Popen(command,shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            response,_ = p.communicate(input=None, timeout=300)
            response = response.decode('utf8')
            f_log.write('removing '+pkg+'\n')
            response  = response.split('\n')
            for response_line in response:
                if 'error' in response_line or 'fail' in response_line:
                        f_log.write(response_line)
            f_log.write(response[len(response)-1])
        except (Exception) as e:
            p.kill()
            f_log.write('error in '+pkg+'\n')
            f_log.write(str(e)+'\n')
    f_log.close()

def main():
    backup_brew_list('backup_brew_list')
    install_pkg('pkg_list')
    remove_pkgs(get_pkg_diff('backup_brew_list'))

if __name__ == '__main__':
    main()

