import time

now = time.strftime("%Y-%m-%d_%H-%M")

login = ''
password = r''
sender = login
received = ''
smtp_server = '' 
port = 587

temat = f"Raport z backupu - {now}"
body = f''' To jest raport z backupu \n
Kopia z dnia - {now} \n
\n
    Contact : \n
mail: biuro@tmask.pl \n
    '''
