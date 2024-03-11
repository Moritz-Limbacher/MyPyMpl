import os, re

def tkf(n, sl, songverw):
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
                    os.chdir(songverw[i][0])
                k += 1
            j += 1
        i += 1
    return search, songname

def istfold(sl):
    fl = []
    for i in range(len(sl)):
        if not "." in sl[i]:
            fl.append(sl[i])
    return fl

def msl(musicfol, el): #musicfolder, endline(e. g. .mp3)
    os.chdir(musicfol)
    dirl = os.listdir()
    sl = [musicfol]

    folders = istfold(dirl)
    for i in range(len(folders)):
        dirl.remove(folders[i])
    
    for i in range(len(el)):
        epl = []
        for j in range(len(dirl)):
            if el[i] in dirl[j]:
                epl.append(dirl[j])
                dirl[j] = '0'
        sl.append([el[i], epl])
    while '0' in dirl:
        dirl.remove('0')
    folders.insert(0, musicfol)

    return sl, [folders]

def mknf(urdir, fn, el): #urdirectory, folder name
    ndrn = tr(musicfol + "\\" + fn)
    msl(ndrn, el)

def msaf(mdir, endl): # will look through all folders in the mdir ("c:\\Users\\User\\Music") and list all files with endings in endl (['.mp3', 'mp4', ...])
    sl = [[], []]
    folders = []
    afr = msl(mdir, endl) #actual folder returnlist
    sl[0].append(afr[0])
    sl[1] = afr[1]
    while len(sl[1]) != 0:
        for i in range(len(sl[1])):
            for j in range(1, len(sl[1][i])):
                afr = msl(sl[1][i][0] + "\\" + sl[1][i][j], endl)
                sl[1][i][j] = '0'
                sl[0].append(afr[0])
                sl[1].append(afr[1][0])
            while '0' in sl[1][i]:
                sl[1][i].remove('0')
            if len(sl[1][i]) == 1:
                sl[1][i] = '0'
        while '0' in sl[1]:
            sl[1].remove('0')
    return sl[0]

def mksl(msafl): #makesonglist from msaf-return list
    songlist = []
    for i in range(len(msafl)):
        for j in range(len(msafl[i][1][1])):
            if len(msafl[i][1][1][j]) > 0:
                songlist.append(msafl[i][1][1][j])
    return songlist

def read_key_option(file, nkeys): #  wants file for: with open('options.txt') as file:
    with open(file) as f:
        fdata = f.readlines()
        kl = ['7', '8', '9', '0']#beforek, nextk, pausk, palykl
        for i in range(len(fdata)):
            if fdata[i] == '[keyoptions]:\n':
                for j in range(1, nkeys+1):
                    kl.append(fdata[i+j].replace(' ','').split('=')[-1].split(',')[:-1])
        return(kl[0], kl[1], kl[2], kl[3])

musicdir = "c:\\Users\\User\\Music"

'''windows 11:
direct = os.listdir("c:\\Users\\")
musicdir = "c:\\Users\\{0}\\Music".format(direct[-2])
'''

endl = [".mp3"]
 

