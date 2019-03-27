

import socket
import os
class Client:
    def __init__(self):
        socketbind = 9000
        ip = "127.0.0.1"
        self.server = (ip, socketbind)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server)
    
    def close(self):
        self.sock.send("#close")
    
    
    def messageSender(self):
        while (True):
            
            self.sock.send("#askFiles")
            datas = (self.sock.recv(1024))
            datas = datas.strip()
            datas = datas.replace(' ','')
            datas = datas.replace('[','')
            datas = datas.replace(']','')
            datas = datas.replace('\'','')
            datas = datas.split(',')
            
            ranged = []
            for a in range(len(datas)):
                datas[a]=datas[a].replace('\\\\','/')
                print ("%s. %s"%(a, datas[a]))

                ranged.append(a)   
            print("Pilih berdasarkan nomor")
            fileask = raw_input()
            fileask = int(fileask)
            if not fileask in ranged:
                continue
            
            first = True
            fileask = str(fileask)
            self.sock.sendall("#ask")
            self.sock.send(fileask)
            data = self.sock.recv(1024)

            
            if ("#sendingFile" in data):
                data = self.sock.recv(1024)
                if ("#start" in data):
                    data= self.sock.recv(1024)
                    filename = data.rstrip()
                   
                    filename = filename.replace("\\", "/")
                    print ("[+] receiving " + str(filename))
                    filename = filename[2:]
                    fp = open(filename, "wb+")
                    while True:
                        data = self.sock.recv(1024)        
                        
                        if "##EOF" in data:
                            print(data)
                            print ("[-] received " + filename )
                            fp.close()
                            break
                        fp.write(data)
            else:
                
                while True:
                    
                    data = self.sock.recv(1024)
                    
                    if ("#directoryEnd" in data):
                        print "[-] all files done"
                        break
                    
                    elif ("#directoryName" in data):
                        
                        data = self.sock.recv(1024)
                        data = data.strip()
                        if(first):
                            data = data.split('/')
                            data = data[len(data)-1]
                        print "[+] receiving directory" +data
                        if (not os.path.exists(data)):
                            os.mkdir(data)
                        os.chdir(data)
                        
                    elif ("#directoryDone" in data):
                        print "[-] Current directory done"
                        os.chdir('..')
                        
                    elif("#start" in data):
                        data= self.sock.recv(1024)
                        filename = data.strip()
                        print ("[+] receiving " + str(filename))
                        print filename
                        fp = open(filename, "wb+")
                        while True:
                            data = self.sock.recv(1024)        
                            
                            if "##EOF" in data:
                                fp.close()
                                break
                            fp.write(data)

if __name__ == "__main__":
    try:
        main = Client()
        main.messageSender()
    except KeyboardInterrupt:
        main.close()
        print("done")