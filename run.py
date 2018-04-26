#!/usr/bin/env python3
import socket, time, re
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *


class App:
    def __init__(self, master):
        self.create_frame(master)
        self.create_listen()


    def create_frame(self, master):
        lf = ttk.LabelFrame(master, text='内网文件传输')
        lf.pack(fill=X, padx=15, pady=8)

        topframe = Frame(lf)
        topframe.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        self.iptext = StringVar()
        self.ip = Entry(topframe, textvariable=self.iptext).pack(fill=X, expand=YES, side=LEFT)
        self.ib = Button(topframe, text='检测连接', padx=10, pady=5, command=self.testip).pack(padx=15, fill=X, expand=YES)

        bottom_frame = Frame(lf)
        bottom_frame.pack(fill=BOTH, expand=YES, side=TOP, padx=15, pady=8)

        self.filename = StringVar()
        self.file = Text(bottom_frame)
        self.file.pack()

        self.fb = Button(bottom_frame, text='Select File', padx=10, pady=5,
            command=self.open_file).pack(side=LEFT)
        self.go = Button(bottom_frame, text='Send File', padx=10, pady=5, command=self.send_file).pack(side=RIGHT)

        rec_frame = Frame(lf)
        rec_frame.pack(fill=BOTH, expand=YES, side=TOP, padx=15, pady=5)
        self.savefilenametext = StringVar()
        self.savefilename = Entry(rec_frame, textvariable=self.savefilenametext).pack(fill=X, expand=YES, side=LEFT)
        self.savefilenameb = Button(rec_frame, text='接受文件为', padx=10, pady=5, command=self.receive_file).pack(side=RIGHT)

        quit_frame = Frame(lf)
        quit_frame.pack(fill=BOTH, expand=YES, side=TOP, padx=15, pady=8)
        self.quit = Button(quit_frame, text='Quit', fg='red', command=lf.quit,
            padx=20, pady=10).pack()


    def testip(self):
        ip = self.iptext.get()
        print(ip)
        flag = True
        p = re.compile(r'^[0-9]{2,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$')
        m = p.match(ip)
        if m is None:
            self.text_show('ip: %s is illegal' % ip)
            return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            r = s.connect_ex((ip, port))
            if r == 0:
                self.text_show('ip : %s is up' % ip)
            else:
                self.text_show('ip : %s seems down' % ip)
        except socket.error as e:
            self.text_show('Can\'t create connection with %s\n' % ip + e + '')
            print(e)

    def create_listen(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((my_host, port))
        self.s.listen(5)
        ss = 'Server start at %s:%s' % (my_host, port) + '\n'
        ss += 'waiting for connection...\n'
        self.text_show(ss)

    def text_show(self, ss):
        self.file.config(state=NORMAL)        
        # self.file.delete(1.0, END)
        self.file.insert(END, ss + '\n')
        self.file.config(state=DISABLED)

    def open_file(self):
        fd = askopenfilename()
        self.filename.set(fd)
        self.text_show('Opened File : \n' + fd)
        print(fd)

    def send_file(self):
        filepath = self.filename.get()
        if filepath is None or not os.path.exists(filepath):
            self.text_show('Please Select File')
            return
        host = self.iptext.get()
        s = self.get_connect(host, port)
        start_time = time.time()
        with open(filepath, 'rb') as f:
            while True:
                try:
                    buf = f.read(buf_size)
                    if not buf:
                        break
                    s.sendall(buf)
                except socket.error as e:
                    print(e)
        end_time = time.time()
        s.close()
        self.text_show('File Transfer Completeed')
        self.text_show('It cost %.3d second(s)' % (end_time - start_time))
        print('File Transfer Completeed')

    def receive_file(self):
        filepath = self.savefilenametext.get()
        if filepath is None or filepath == '':
            self.text_show('Please input your save file name')
            return
        self.text_show('waiting for connection...')
        conn, addr = self.s.accept()
        self.text_show('Connected by : ' + str(addr))
        print('Connected by ', addr)
        start_time = time.time()
        with open(os.path.join(os.getcwd(), filepath), 'wb') as f:
            while True:
                buf = conn.recv(buf_size)
                if not buf:
                    break
                f.write(buf)
                f.flush()
        end_time = time.time()
        conn.close()
        self.text_show('Receive File Completed')
        self.text_show('It cost %.3f second(s)' % (end_time - start_time))
        print('Receive File Completed')

    def get_connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


my_host = get_host_ip()
port = 8000
buf_size = 1024


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    # root.iconbitmap('icobm.ico')
    root.mainloop()
    root.destroy()
