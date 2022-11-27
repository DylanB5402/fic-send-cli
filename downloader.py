import os
import smtplib
from email import encoders
from email.mime import multipart, base
import subprocess
import AO3

def send_fic(url : str, email_address : str, password : str, kindle_email):
    port = 587
    fic_filename = ''
    if ('archiveofourown' in url):
        fic_filename = download_epub_from_ao3(url)
    else:
        fic_filename = download_epub_and_get_file_name(url)
    print('fic downloaded!')
    email = smtplib.SMTP('smtp.gmail.com', port)
    email.ehlo()
    email.starttls()
    email.login(email_address, password)
    msg = multipart.MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = kindle_email
    msg['Subject'] = ''
    attachment = open(fic_filename, 'rb')
    p = base.MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % fic_filename)
    msg.attach(p)
    text = msg.as_string()
    email.sendmail(email_address, kindle_email, text)
    print('fic sent!')
    email.quit()
    attachment.close()
    os.remove(fic_filename)

def download_epub_and_get_file_name(url : str):
    url = https_to_http(url)
    subprocess.run(['fichub_cli', '-u', url])
    files = os.listdir(os.curdir)
    for file in files:
        if file[-5:] == '.epub':
            return file

def download_epub_from_ao3(url: str):
    id = AO3.utils.workid_from_url(url)
    work = AO3.Work(id)
    file_name = f"{work.title}.epub"
    with open(file_name, "wb") as file:
        file.write(work.download("EPUB"))
    return file_name


def https_to_http(url : str):
    url = url[0:4] + url [5:]
    return url