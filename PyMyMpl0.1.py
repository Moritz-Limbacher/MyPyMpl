#Import Modules
import pygame, mmpl_lib, os, time, sys, random
import tkinter as tkr
from threading import Thread

pygame.init()
pygame.mixer.init()
mix = pygame.mixer.music
clock = pygame.time.Clock()

#simpleaudio

#Music location

direct = os.listdir("c:\\Users\\")
workdir = os.getcwd()
print("c:\\Users\\{0}\\Music".format(direct[-2]))
musicdir = "c:\\Users\\{0}\\Music".format(direct[-2])
endl = [".mp3", ".mp4", ".mp5", ".mp6"]
songverw = mmpl_lib.msaf(musicdir, endl) # musiclist
songlist = mmpl_lib.mksl(songverw) # all songs in a list

#Create Window
screensze = pygame.display.list_modes()
windowsze = [int(screensze[-1][0]/1.55), int(screensze[-1][1]/1.8)]
player = tkr.Tk()

#Edit Window
player.title("Audio Player")
player.geometry(str(windowsze[0])+"x"+str(windowsze[1]))
player.minsize(windowsze[0], windowsze[1])

#Action event
os.chdir(musicdir)

#Musiclist classes
#Songlist
class musiclistlabel():
    def __init__(self, musicnl, root, windowsze):
        self.threads = []
        self.sels = 0
        self.wins = windowsze
        self.root = root
        self.musicnl = musicnl
        self.autoplay = tkr.BooleanVar()
        self.randomplay = tkr.BooleanVar()
        #command keys with default values
        self.beforek = '7'
        self.nextk = '8'
        self.pausk = '9'
        self.playk = ['0', '\r'] # \r = Enter
        self.keysl = 4
        # intern variablses
        self.plays = False

    def keys_init(self, kfn):
        dirnow = os.getcwd()
        os.chdir(workdir)
        if kfn in os.listdir(os.getcwd()):
            if os.path.getsize(kfn) > 0:
                with open(kfn) as file:
                    self.beforek, self.nextk, self.pausk, self.playk = mmpl_lib.read_key_option(kfn, self.keysl) # not finished
                
            else:
                print('options.txt does not encode any options')
        else:
            print('options.txt not found in workdir')
        os.chdir(dirnow)

    def build(self):
        # load keys for not default value
        self.keys_init('options.txt')
        # build gui
        self.Frame1 = tkr.Frame(self.root)
        self.Frame1.pack(fill=tkr.BOTH, expand=True)
        self.Frame2 = tkr.Frame(self.root)
        self.Frame2.pack()
        self.buildmenu(self.Frame2)
        self.buildbuttons(self.Frame2)
        self.scrollbar = tkr.Scrollbar(self.Frame1, orient = "vertical")
        self.scrollbar.pack(side='right', fill='y')
        
        self.listbox = tkr.Listbox(self.Frame1, yscrollcommand = self.scrollbar.set)
        for i in range(len(self.musicnl)):
            self.listbox.insert(tkr.END, self.musicnl[i])
        self.listbox.pack(expand=True, fill='both')
        self.listbox.select_set(0)

        self.scrollbar.config(command = self.listbox.yview)
        self.buildkeys(self.Frame1)

        
    def buildbuttons(self, frame):
        #Register Buttons
        self.Button1 = tkr.Button(frame, width = 8, height = 3, text = "PLAY >", command = self.pressplay)#, image = self.tbimg)
        self.Button1.grid(row = 0, column = 3)
        self.Button2 = tkr.Button(frame, width = 8, height = 3, text = "STOP X", command = self.stopplayer)
        self.Button2.grid(row = 0, column = 4)

        self.Button3 = tkr.Button(frame, width = 12, height = 3, text = ">> VORWARD ", command = self.forward)
        self.Button3.grid(row = 0, column = 5)
        self.Button4 = tkr.Button(frame, width = 12, height = 3, text = "BACKWARD <<", command = self.backward)
        self.Button4.grid(row = 0, column = 1)

        self.Button5 = tkr.Button(frame, width = 8, height = 3, text = "Pause", command = self.pausbutton)
        self.Button5.grid(row = 0, column = 2)

        self.Button6 = tkr.Checkbutton(frame, text = "Autoplay", variable = self.autoplay, onvalue=True, offvalue=False)
        self.Button6.grid(row = 2, column = 5)

        self.Button7 = tkr.Checkbutton(frame, text = "Mix", variable = self.randomplay, onvalue=True, offvalue=False)
        self.Button7.grid(row = 2, column = 4)

        #Song name
        self.label1 = tkr.LabelFrame(frame, width = int(self.wins[0]/7), text = "  available songs  ") #LabelFrame
        self.label1.grid(row = 1, column = 0, columnspan = 3)

    def buildkeys(self, frame):
        self.root.bind('<KeyPress>', self.keypressed)

    def buildsens(self, frame):
        self.playing_sens = tkr.BooleanVar(self.root)
        
    def keypressed(self, event):
        #print(event)
        if event.char in self.nextk:
            self.forward()
        if event.char in self.beforek:
            self.backward()
        elif event.char in self.pausk:
            self.pausbutton()
        elif event.char in self.playk:
            self.pressplay()

    def buildmenu(self, frame):
        self.menubar = tkr.Menu(frame)
        self.menubar.add_command(label="File", command = self.opener)
        self.root.config(menu = self.menubar)
        
    def opener(self):
        pass

    def pressplay(self):
        self.sels = Sllabel.listbox.curselection()
        if len(self.sels) == 0:
            self.sels = 0
        else:
            self.sels = self.sels[0]
        self.listbox.see(self.sels)
        self.play(self.sels)
        
    def play(self, n):
        self.plays = True
        if n == -1:
            self.sels = Sllabel.listbox.curselection()[0]
        else:
            self.sels = n
        search, songname = mmpl_lib.tkf(self.sels, songlist, songverw)
        if search == True:
            mix.load(songname)
            self.playthread = Thread(target=mix.play)
            self.playthread.start()
        #if self.autoplay == True: 
        #    ap = Thread(self.autoplay())#self.autoplayf()) why is there the f?! 
        self.listbox.see(self.sels)

    def tkf(self, n, sl):
        songname = sl[n]
        found = False
        search = False
        i, j, k = 0, 0, 0
        while search == False and i < len(songverw):
            j = 0
            while search == False and j < int((len(songverw[i])-1)):
                k = 0
                while search == False and k < len(songverw[i][1+j][1]):
                    if songname == songverw[i][1+j][1][k]:
                        search = True
                        mmpl_lib.chdir(songverw[i][0])
                    k += 1
                j += 1
            i += 1
        return search, songname

    def stopplayer(self):
        mix.stop()

    def exitplayer(self):
        mix.stop()
        sys.exit()

    def pausbutton(self):
        if mix.get_busy():
            mix.pause()
            self.listbox.see(self.sels)
            self.plays = False
            
        else:
            mix.unpause()
            self.plays = True
    
    def forward(self):
        self.sels = Sllabel.listbox.curselection()[0]
        if self.randomplay.get() == True:
            self.listbox.selection_clear(self.sels)
            self.sels = random.randint(0, len(self.musicnl))
            try:
                self.listbox.selection_set(self.sels)
            except:
                print('selection of randomsong failed, start at first song')
                self.sels = 0
            self.play(self.sels)
            self.listbox.see(self.sels)
            
        elif self.sels+1 < len(self.musicnl):
            self.listbox.selection_clear(self.sels)
            self.sels += 1
            self.listbox.selection_set(self.sels)
            self.play(self.sels)
            self.listbox.see(self.sels)
            
    def backward(self):
        self.sels = Sllabel.listbox.curselection()[0]
        if self.sels > 0:
            self.listbox.selection_clear(self.sels)
            self.sels -= 1
            self.listbox.selection_set(self.sels)
            self.play(self.sels)
            self.listbox.see(self.sels)

def play_next():
    while True:
        clock.tick(1)
        if mix.get_busy() == False and Sllabel.plays == True and Sllabel.autoplay.get() == True:
            Sllabel.forward()
            Sllabel.pressplay()
        else:
            pass
            
#Songliste
Sllabel = musiclistlabel(songlist, player, windowsze)
Sllabel.build()

# play_next to start the next song after one is finished
Thread(target=play_next).start()

#Activate
player.mainloop()
