
# -*- coding: utf-8 -*-

import tkinter as tk
import os

class AskBoxM(tk.Toplevel):

    fVar = []
    fBtn = []

    def __init__(self,master,bg,qt,var, btns=['Yes','No'], fVis=(True,True),fVal=(0,1)):
        self.flags = ['-ask no more','-delete to trash']
        self.master = master
        self.var = var
        tk.Toplevel.__init__(self, self.master, bg=bg, padx=1, pady=1)  # Initalise the Toplevel
        self.resizable(False, False)
        self.qtxt = tk.Text(self, fg='black',height=4, padx=2)
        self.qtxt.insert(tk.INSERT,qt)
        self.qtxt.configure(state=tk.DISABLED)
        self.qtxt.pack_propagate(False)
        self.qtxt.pack(side=tk.TOP,fill=tk.X)
        self.buframe = tk.LabelFrame(self,text='')
        for btn in btns :
            bu = tk.Button(self.buframe,text=btn)
            bu.bind('<Button-1>', self.btn_func)
            bu.pack(side=tk.LEFT)
        self.buframe.pack(side=tk.TOP)
        self.flagframe = tk.LabelFrame(self,text='')
        j = -1
        for flag in self.flags :
            self.fVar.append(tk.IntVar())
            j += 1
            self.fVar[j].set(fVal[j])
            fl = tk.Checkbutton(self.flagframe,text=flag, variable=self.fVar[j])
            self.fBtn.append(fl)
            if fVis[j] : fl.pack(side=tk.LEFT)
        self.flagframe.pack(side=tk.TOP)
        self.transient(self.master)
        self.wait_visibility()
        self.grab_set()
        self.focus_set()

    def btn_func(self,event):
        btn = event.widget
        r = btn['text'] + ';' + str(self.fVar[0].get()) + ';' + str(self.fVar[1].get())
        self.var.set(r)
        self.destroy()


def ask_dir_content(dir):
    if dir[-1] != '/': dir = dir + '/'
    dir_cnt =0
    file_cnt =0
    files = os.listdir(dir)
    for f in files:
        #print(dir+f)
        if os.path.isdir(dir + f):
            dir_cnt += 1
        else:
            file_cnt += 1
    if dir_cnt + file_cnt == 0:
        return 'empty'
    else:
        return 'Dir/File: '+str(dir_cnt)+'/'+str(file_cnt)

def get_askbox_result(win,var,qtext,butt):
    AskBox = AskBoxM(master=win, bg='blue', qt=qtext, var=var, btns=butt)
    AskBox.geometry('400x120+150+100')
    AskBox.wait_window()
    r = var.get()
    return r

def get_askbox_answer(win,var,qtext,butt,bg='blue'):
    AskBox = AskBoxM(master=win, bg=bg, qt=qtext, var=var, btns=butt)
    wx = win.winfo_rootx()+20
    wy = win.winfo_rooty()+70
    AskBox.geometry('400x120+{}+{}'.format(wx,wy))
    AskBox.wait_window()
    r = var.get()
    return r

def ask_confirm(win,var,qtext):
    AskBox = AskBoxM(master=win, bg='blue', qt=qtext,
                     var=var, btns=['Yes','No'], fVis=(False,False))
    wx = win.winfo_rootx()+20
    wy = win.winfo_rooty()+70
    AskBox.geometry('400x100+{}+{}'.format(wx,wy))
    AskBox.title('Confirm')
    AskBox.wait_window()
    r = var.get()
    ans,mult,trash = r.split(';')
    return ans

def show_info(win,qtext):
    var = tk.StringVar()
    AskBox = AskBoxM(master=win, bg='blue', qt=qtext, var=var,
                     btns=['OK'], fVis=(False,False))
    wx = win.winfo_rootx()+20
    wy = win.winfo_rooty()+70
    AskBox.geometry('400x100+{}+{}'.format(wx,wy))
    AskBox.title('Info')
    AskBox.wait_window()
    return 'OK'


if __name__ == '__main__':

    mainW = 800
    mainH = 300
    smX = 100
    smY = 30
    main_geo = ('{}x{}+{}+{}'.format(mainW, mainH,smX,smY))

    root = tk.Tk()
    root.geometry(main_geo)
    root.title('AskBoxM Testing')
    SomeVar = tk.StringVar()

    fgroup = ['file01','file02','file03','file04','file05','file06','file07',
              'file08','file09','file10']

    def ask():
        global SomeVar
        qt = qText.get('1.0',tk.END)
        r = get_askbox_result(root,SomeVar,qt,['Yes','Cancel'])
        print('r=',r)

    def imitate_filegroup_deleting():
        global SomeVar, fgroup
        fg = fgroup
        max = len(fg)
        j = 0
        ask_flag = True
        for fn in fg:
            j += 1
            cnt = 'Cnt : '+str(j)+' / '+str(max)
            qt = cnt + '\nУдалить файл "'+fn+'" ?'
            if ask_flag :
                Ab = AskBoxM(master=root, bg='blue', qt=qt, var=SomeVar,
                             btns=['Yes', 'No', 'Skip', 'Cancel'],
                             fVis=(True, True), fVal=(0, 1))
                Ab.geometry('350x100+150+100')
                Ab.wait_window()
                r = SomeVar.get()
                print('r=', r)
                cmd, noask, trash = r.split(';')
                print(cmd, noask, trash)
                noask = int(noask)
                trash = int(trash)
                if noask : ask_flag =False
            else :
                print(cnt, fn)


    qText = tk.Text(root,  fg='black', height=6)
    qText.insert(tk.INSERT, 'Удалить указанный файл ?')
    qText.pack_propagate(False)
    qText.pack(side=tk.TOP, fill=tk.X)
    bu = tk.Button(root,text='Ask',command=ask).pack()
    buDel = tk.Button(root,text='GroupDelete', command=imitate_filegroup_deleting).pack()

    root.mainloop()



