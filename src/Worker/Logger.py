import datetime
import os

class Logger:
    def log(self, ip, ap, message):
        f = self.create_or_open(ip.getUID())
        self.write(f, "User: "+message)
        if ap.preface != "__empty__":
            self.write(f, ap.preface)
        if ap.mainAnswer != "__empty__":
            self.write(f, ap.mainAnswer)
        if ap.last != "__empty__":
            self.write(f, ap.last)
        self.write(f, "-----")
        f.close()
    
    def create_or_open(self, file):
        filename = 'logging/'+file+'.txt'

        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        return open(filename,append_write)
    
    def write(self, file, string):
        file.write(datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S") + ": " + string.replace("\n", " ") + "\n")