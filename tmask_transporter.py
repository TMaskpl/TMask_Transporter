#!/usr/bin/python

import tmask_email
import tmask_path
import tmask_ssh

# pip3 install paramiko
import paramiko
import time
import os
import platform
from os.path import exists
import shutil
import hashlib
import json
import smtplib
from email.message import EmailMessage

# --- Zmienne ---

src = tmask_path.src
dst = tmask_path.dst
zip_pass = tmask_path.zip_password


# --- Funkcje  OLD ---
def dstFileMd5(dst):

    global dict_dst
    
    list_dst = os.listdir(dst)
    dict_dst = {}
    
    for file in list_dst:
        full_path = os.path.join(dst, file)
        if exists(full_path):
            hash_md5 = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
            dict_dst[file] = hash_md5
            
def copySrcDstMd5(src, dst):
    
    dstFileMd5(dst)

    global dict_src
    
    list_src = os.listdir(src)
    dict_src = {}

    for file in list_src:
        src_full_path = os.path.join(src, file)
        dst_full_path = os.path.join(dst, file)
        
        if exists(src_full_path):
            hash_md5 = hashlib.md5(
                open(src_full_path, 'rb').read()).hexdigest()
            dict_src[file] = hash_md5
            if file not in dict_dst:
                print(dict_src[file])
                print(f'Copy {src_full_path} --> {dst_full_path}')
                shutil.copyfile(src_full_path, dst_full_path)
            try:
                if dict_dst[file] != dict_src[file]:
                    print(f'Copy {src_full_path} --> {dst_full_path}')
                    shutil.copyfile(src_full_path, dst_full_path)
            except Exception as e:
                print(e)
                pass
            else:
                file_size = os.path.getsize(dst_full_path)
                print(
                    f'File --> {file} - {dict_src[file]} - {file_size}  bytes is OK')


# --- TST ---
# Kopiowanie z src plików których nie ma w dst i mają różne md5
def copySrcToDstRecuresiveMd5(src, dst):

    global d_src

    d_src = {}

    listDstRecuresiveMd5(src, dst)

    for r, d, f in os.walk(src, topdown=False):
        if len(f) != 0:
            for each_file in f:
                hash_md5 = hashlib.md5(
                    open(os.path.join(r, each_file), 'rb').read()).hexdigest()
                d_src[each_file] = hash_md5
                try:
                    if d_dst[each_file] != d_src[each_file]:
                        print(f'Copy file -->  {d_src[each_file]}')
                except Exception as e:
                    print(e)
                    pass
                else:
                    file_size = os.path.getsize(os.path.join(r, each_file))
                    print(
                        f'File --> {each_file} - {file_size}  bytes is OK')

    with open('d_src.json', 'w') as convert_file:
        convert_file.write(json.dumps(d_src))

        # print(d_src)



# --- Funkcje  PRO ---

# Wysyłanie maila z załącznikiem tekstowym
def sendEmail(dict_md5, file_stat):
    now = time.strftime("%Y-%m-%d_%H-%M")
    
    msg = EmailMessage()
    msg["From"] = tmask_email.sender
    msg["Subject"] = tmask_email.temat
    msg["To"] = tmask_email.received
    msg.set_content(tmask_email.body)
    msg.add_attachment(open(dict_md5, "r").read(), filename=dict_md5)
    msg.add_attachment(open(file_stat, "r").read(), filename=file_stat)

    s = smtplib.SMTP(tmask_email.smtp_server, tmask_email.port)
    s.login(tmask_email.login, tmask_email.password)
    s.send_message(msg)

# Wysyłanie maila z załącznikiem tekstowym MD5
def sendEmailMD5(dict_md5):
    now = time.strftime("%Y-%m-%d_%H-%M")

    msg = EmailMessage()
    msg["From"] = tmask_email.sender
    msg["Subject"] = tmask_email.temat
    msg["To"] = tmask_email.received
    msg.set_content(tmask_email.body)
    msg.add_attachment(open(dict_md5, "r").read(), filename=dict_md5)

    s = smtplib.SMTP(tmask_email.smtp_server, tmask_email.port)
    s.login(tmask_email.login, tmask_email.password)
    s.send_message(msg)
    
# Sprawdzenie wsystkich md5 plików w tylko w folderze dst
def listDstRecuresiveMd5(dst):
    
    global d_dst
    d_dst = {}
    stat_dst = {}
    
    # Przeszukaj cały folder dst i oblicz md5 do
    for r,d,f in os.walk(dst,topdown=False):
        if len(f) != 0:
            for each_file in f:
                full_path = os.path.join(r, each_file)
                hash_md5 = hashlib.md5(open(os.path.join(r,each_file), 'rb').read()).hexdigest()
                d_dst[full_path] = hash_md5
                file_size = os.path.getsize(full_path)
                stat_dst[full_path] = file_size

    with open('d_dst.json', 'w') as convert_file:
        convert_file.write(json.dumps(d_dst))
        
    with open('stat_dst.json', 'w') as convert_file:
        convert_file.write(json.dumps(stat_dst))
        
    sendEmail('d_dst.json', 'stat_dst.json')

# Copy all Src to DST
def copySrcToDst(src, dst):
    now = time.strftime("%Y-%m-%d_%H-%M")
    dst_path = os.path.join(dst, now)
    shutil.copytree(src, dst_path)
    
    listDstRecuresiveMd5(dst)

# Copy all Src to DST - ZIP
def copySrcToDstZip(src, dst):
    now = time.strftime("%Y-%m-%d_%H-%M")
    dst_path = os.path.join(dst, now)
    shutil.make_archive(dst_path, "zip", root_dir=src)
    
    listDstRecuresiveMd5(dst)

# Copy all Src to DST - ZIP with pass
# sudo apt install p7zip-full
# Rozpakowywyanie np. 7z x 2021-12-26_16-32.7z -pthc401
def copySrcToDstZipPass(src, dst, zip_pass):
    now = time.strftime("%Y-%m-%d_%H-%M")
    dst_path = os.path.join(dst, now)
    os.system(f"7z a {dst_path} {src} -p{zip_pass}")
    
    listDstRecuresiveMd5(dst)

# Wyświetl wszystkie pliki w folderze
def listFileOfEnd(path):
    list = []
    for r,d,f in os.walk(path,topdown=False):
        if len(f) != 0:
            for each_file in f:
                full_path = os.path.join(r, each_file)
                list.append(full_path)
    return list

# Wyświetl wszystkie pliki na serwerze zdalnym
def listFileRemoteServer(remote_path):
    import tmask_ssh

    r = tmask_ssh
    remote_list = []

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=r.hostname, username=r.username,
                password=r.password, port=r.port)
    stdin, stdout, stderr = ssh.exec_command(f'ls -1 {tmask_ssh.ssh_path}')
    for i in stdout.readlines():
        if len(i) != 0:
            remote_list.append(i)
    return remote_list

# Wyświetl Md5 plików na zdalnym serwerze
def showMd5FilesRemoteServer(remote_path):

    global r_d_dst
    r_d_dst = {}
    
    now = time.strftime("%Y-%m-%d_%H-%M")
    r = tmask_ssh

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=r.hostname, username=r.username,
                password=r.password, port=r.port)
    stdin, stdout, stderr = ssh.exec_command(f'for v in $(find {remote_path});do md5sum $v;done')
    for m in stdout.readlines():
        m = m.split('  ')
        md5 = m[0]
        file = m[1].replace('\n','')
        r_d_dst[file] = md5
        
    with open('RemoteFilesMD5.json', 'w') as convert_file:
        convert_file.write(json.dumps(r_d_dst))
        
    sendEmailMD5('RemoteFilesMD5.json')

# Wyślij po ssh wszystkie wskazane pliki
def sendBkpToRemoteServer(src_list_files):
    import tmask_ssh

    r = tmask_ssh

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=r.hostname, username=r.username,
                password=r.password, port=r.port)
    sftp_client = ssh.open_sftp()

    for each_file in src_list_files:
        if platform.system() == "Windows":
            filename_bkp = each_file.split('\\')[-1]
        else:
            filename_bkp = each_file.split('/')[-1]
        r_dst_path = os.path.join(r.ssh_path, filename_bkp)
        sftp_client.put(each_file, r_dst_path)

    sftp_client.close()
    ssh.close()

# Pobierz pliki z serwera
def getFilesWithServer(remote_files, local_files):
    import tmask_ssh
    
    now = time.strftime("%Y-%m-%d_%H-%M")
    r = tmask_ssh

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=r.hostname, username=r.username,
                password=r.password, port=r.port)
    sftp_client = ssh.open_sftp()
    
    list = []
    
    for r in listFileRemoteServer(tmask_ssh.ssh_path):
        if r != '\n':
            if len(r) != 0:
                r = r.replace('\n', '')
                # list.append(r)
                rr = (os.path.join(tmask_ssh.ssh_path, r))
                ll = (os.path.join(local_files, r))
                sftp_client.get(rr, ll)

    sftp_client.close()
    ssh.close()
    
    listDstRecuresiveMd5(local_files)



# Funkcja główna
def main():
    # copySrcToDstZipPass(src, dst, zip_pass)
    # sendBkpToRemoteServer()
    # listFileOfEnd(tmask_path.dst)
    # sendBkpToRemoteServer(listFileOfEnd(tmask_path.dst))
    # listFileRemoteServer(tmask_ssh.list_remote_files)
    # getFilesWithServer(tmask_ssh.ssh_path, tmask_path.src)
    showMd5FilesRemoteServer(tmask_ssh.ssh_path)
    
    
if __name__ == "__main__":
    main()
