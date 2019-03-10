

import imaplib
import email
import base64
import tkinter as tk
from tkinter import PanedWindow
from tkinter import scrolledtext
import AskBox as ab
import os


server = 'imap.yandex.ru'
user = 'YourBox@yandex.ru'
pssw = 'YourPassword'

Mail = 0
CurFolder = 'inbox'
MailCnt = 0
CurrentCnt = 0
CurMessage = {}
MsgHead = dict()
MsgBody = ''
AttCnt =0
AttFn = []
BodyTxt = ''

MailServer = None

mainW = 1000
mainH = 600
smX = 100
smY = 30
main_geo = ('{}x{}+{}+{}'.format(mainW, mainH, smX, smY))

root = tk.Tk()
mail_win = None

def CreateUI(master):
    global main_geo, mail_win
    win = PanedWindow(master, relief='groove')
    master.geometry(main_geo)
    master.title('MailBox Scrolling')
    win.pack(fill=tk.BOTH, expand=1)
    mail_win = scrolledtext.ScrolledText(bg='blue', fg='white', width=100, height=10, wrap=tk.WORD)
    mail_win.configure(font=("Times New Roman", 16))
    win.add(mail_win)
    win2 = PanedWindow(orient=tk.VERTICAL, relief='groove')
    bot = tk.Label(text="bottom pane", bg='green')
    win2.add(bot)
    win.add(win2)
    win3 = PanedWindow(orient=tk.HORIZONTAL, relief='groove')
    top = tk.Label(text="top pane", bg='gray')
    win3.add(top)
    win2.add(win3)

def CreateMenu(master):
    menubar = tk.Menu(master)
    master.config(menu=menubar)
    fileMenu = tk.Menu(menubar, tearoff=0)
    fileMenu.add_command(label="Exit", command=quit)
    cmdMenu = tk.Menu(menubar, tearoff=0)
    cmdMenu.add_command(label="GetNext", command=GetNext)
    cmdMenu.add_command(label="GetPrev", command=GetPrev)
    cmdMenu.add_command(label="SaveAttachments", command=SaveAttach)
    menubar.add_cascade(label="File", menu=fileMenu)
    menubar.add_cascade(label="Message", menu=cmdMenu)
    menubar.add_command(label="Next", command=GetNext)
    menubar.add_command(label="Prev", command=GetPrev)


def MailConnect(folder=''):
    global MailServer
    global server, user, pssw, CurFolder
    if folder!='':
        CurFolder = folder
    MailServer = imaplib.IMAP4_SSL(server,993)
    MailServer.login(user, pssw)
    MailServer.select(CurFolder)
    r, data = MailServer.search(None, 'ALL')

def MailStop():
    global MailServer
    MailServer.close()

def getUids():
    global MailCnt,CurFolder, mail_win
    Mail = imaplib.IMAP4_SSL(server)
    try:
        Mail = imaplib.IMAP4_SSL(server,993)
    except Exception as ex:
        ab.show_info(mail_win,'No access to server !')
        return 'Er'
    r = Mail.login(user, pssw)
    r,uid = Mail.select(CurFolder)
    if r != 'OK':
        ab.show_info(mail_win,'No such folder: '+CurFolder)
        return 'Er'
    MailCnt = int(uid[0])  # Берем последний ID
    Mail.close()
    return 'OK'

def getSpecifiedMsg(msgN):
    global MailServer
    r, data = MailServer.fetch(str(msgN), '(RFC822)')
    try:
        msg = email.message_from_string(data[0][1])
    except TypeError:
        msg = email.message_from_bytes(data[0][1])
    return msg

def getMsg(N):
    global MsgHead
    if N>MailCnt or N<0:
        ab.show_info(root,str(N)+': -incorrent MsgNumber\nMust be 0..'+str(MailCnt))
        return
    MsgHead = dict()
    MsgHead['MsgN'] = N
    MailConnect()
    message = getSpecifiedMsg(N)
    MailStop()
    return message



def MsgParser(msg):
    global MsgHead,MsgBody, AttCnt,AttFn, BodyTxt
    Subj = msg["Subject"]
    h = email.header.decode_header(Subj)
    encoded_title, coding = h[0]
    Subject = encoded_title.decode(coding)
    MsgHead['Date'] = msg["Date"]
    MsgHead['Code'] = coding
    MsgHead['Subject'] = Subject
    Ot = msg['From']
    m = Ot.split('?')
    if len(m)>1:
        From = base64.b64decode(m[3]).decode(m[1])
    else:
        From = Ot
    MsgHead['From'] = From
    # ----------------------------------Attachments
    AttCnt = 0
    AttFn = []
    for part in msg.walk():
        ctype = part.get_content_maintype
        if ctype == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        app_fn = part.get_filename()
        #app_data = part.get_payload(decode=True)
        AttCnt += 1
        AttFn.append(app_fn)
    # ----------------------------------BODY
    if msg.is_multipart():
        for part in msg.get_payload():
            body = part.get_payload()
            # more processing?
    else:
        body = msg.get_payload()

    try:
        s = base64.b64decode(body).decode(coding)
    except Exception as ex:
        s = 'Error: \nError of Body decoding'
        return
    MsgBody = s


def SaveAttach():
    global AttFn, AttCnt
    if AttCnt==0:
        ab.show_info(mail_win,'No attachment')
        return
    msg = getMsg(CurrentCnt)
    att_dir = os.getcwd() + '/Att/'
    if not os.path.isdir(att_dir):
        os.mkdir(att_dir)
    # вытащить из msg вложения
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        app_fn = part.get_filename()
        app_data = part.get_payload(decode=True)
        fullfn = att_dir + app_fn
        fi = open(fullfn, 'wb')
        fi.write(app_data)
        fi.close
    ab.show_info(mail_win,'  Ready !\nResult in "'+att_dir+'"')


def VisMessage():
    global mail_win
    mail = mail_win
    global MsgHead,MailCnt, AttCnt,AttFn, MsgBody,BodyTxt
    mail.delete(1.0,tk.END)
    mail.insert(1.0, 'Message: '+str(MsgHead['MsgN'])+' / '+str(MailCnt)\
                     +'     Code: '+MsgHead['Code']+'\n')
    mail.insert(2.0, 'Date: '+MsgHead['Date']+'\n')
    mail.insert(3.0, 'From: '+MsgHead['From']+'\n')
    mail.insert(4.0, 'Subject: '+MsgHead['Subject']+'\n')
    t=''
    for f in AttFn:
        t=t+f+' ; '
    mail.insert(5.0, 'Attachments: '+str(AttCnt)+'  '+t+'\n')
    mail.insert(6.0, '       \n')
    mail.insert(7.0, '       MessageBody: \n')
    mail.insert(8.0, MsgBody+'\n')


def GetNext():
    global CurrentCnt,MailCnt, BodyTxt
    pass
    CurrentCnt -= 1
    if CurrentCnt <=0:
        CurrentCnt = MailCnt
    Msg = getMsg(CurrentCnt)
    MsgParser(Msg)
    VisMessage()

def GetPrev():
    global CurrentCnt,MailCnt
    pass
    CurrentCnt += 1
    if CurrentCnt > MailCnt:
        CurrentCnt = 1
    Msg = getMsg(CurrentCnt)
    MsgParser(Msg)
    VisMessage()


if __name__ == '__main__':

    CreateUI(root)
    CreateMenu(root)
    CurFolder = 'inbox'
    root.title('MailBox Scrolling  Server: ' + server + '  Folder: '+CurFolder)
    r = getUids()
    if r=='OK':
        print('CurFolder:',CurFolder,'  MailCnt:',MailCnt)
        CurrentCnt = MailCnt+1
        GetNext()


    root.mainloop()


