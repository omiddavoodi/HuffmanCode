import math
import copy

def tobin(n):
    if n == 0: return "0"
    m = n
    h = 0
    s = ""
    while (True):
        s = str(m % 2) + s
        if (m != 1):
            m = math.floor(m / 2)
        else:
            return s
        h += 1

def ton(bina):
    ret = 0
    co = len(bina)-1
    for i in bina:
        if (i == "1"):
            ret += 2**(co)
        co -= 1
    return ret

def tob(bina):
    s = []
    ct = 0
    co = 7
    loic = len(bina)-1
    for i in range(loic+1):
        if (bina[i] == "1"):
            ct += (2**co)
        co -= 1
        if (co < 0 or i == loic):
            co = 7
            s.append(ct)
            ct = 0
    return s

def mb(n, k):
    h = n
    while (len(h) < k):
        h = "0" + h
    return h

class node:
    val = 0
    char = ''
    rcsl = []
    code = ""
    def __init__(self, a, c = ''):
        self.val = a
        self.char = c

def findcharcounts(s):
    ret = {}
    ret2 = []
    for i in range(256):
        ret[chr(i)] = 0
    for i in s:
        ret[chr(i)] = ret[chr(i)] + 1
    for i in range(256):
        if (ret[chr(i)] > 0):
            temp = node(ret[chr(i)], chr(i))
            ret2.append(temp)
    return ret2

def sortcc(l):
    for i in range(len(l)):
        for j in range(i):
            if (l[j].val < l[i].val):
                t = l[i]
                l[i] = l[j]
                l[j] = t
        
def generatetree(l):
    xt = len(l)
    lx = copy.deepcopy(l)
    while (xt > 1):
        bnode = node(lx[xt-1].val + lx[xt-2].val)
        bnode.rcsl = []
        bnode.rcsl.append(lx[xt-1])
        bnode.rcsl.append(lx[xt-2])
        bhi = []
        for z in range(len(lx)-2):
            bhi.append(lx[z])
        lx = copy.deepcopy(bhi)
        lx.append(bnode)
        sortcc(lx)
        xt = xt - 1
    return lx
        
def findcodes(l, h):
    if (len(l.rcsl) > 1):
        l.rcsl[0].code = l.code + "0"
        l.rcsl[1].code = l.code + "1"
        findcodes(l.rcsl[0], h)
        findcodes(l.rcsl[1], h)
    else:
        h.append(l)

def main(fname):
    fi = open(fname,"b+r")
    contents = fi.read()
    fi.close()

    if (chr(contents[0]) == "O" and chr(contents[1]) == "C" and contents[2] == "F"):
        nli = []
        li = findcharcounts(contents)
        print ("Char counts found")
        sortcc(li)
        li = generatetree(li)
        print ("Huffman tree generated")
        findcodes(li[0], nli)
        print ("Codes found")
        resu = ""

        s = 0
        t = ""
        for i in nli:
            t += mb(tobin(ord(i.char)),8)
            t += mb(tobin(len(i.code)),8)
            t += i.code
        print ("Header built")

        coinft = [0,0,0,0,0,0]
        nfet = len(contents)
        coinft[0] = (nfet % 256)
        nfet = math.floor(nfet / 256)
        coinft[1] = (nfet % 256)
        nfet = math.floor(nfet / 256)
        coinft[2] = (nfet % 256)
        nfet = math.floor(nfet / 256)
        coinft[3] = (nfet % 256)
        nfet = math.floor(nfet / 256)
        coinft[4] = (nfet % 256)
        nfet = math.floor(nfet / 256)
        coinft[5] = (nfet % 256)
        nfet = math.floor(nfet / 256)

        print ("Filesize calculated")
        contidf = ""
        for nvj in coinft:
            contidf += (mb(tobin(nvj),8))
        t += contidf
        newfile = [ord("O") ,ord("C") ,ord("F"), (len(nli)-1)]
        print ("Main file compression started")
        for nki in contents:
            for jni in nli:
                if chr(nki) == jni.char:
                    t += jni.code
                    break
        print ("Main file compression finished")
        q = tob(t)
        print ("Binary changed to bytes")
        newfile.extend(q)

        fi = open(fname+".ocf","b+w")
        fi.write(bytes(newfile))
        fi.close()
        print ("Operation finished")
    else:
        nli = []
        offset=32

        s = ""
        for i in contents:
            s += mb(tobin(i),8)
        for q in range(contents[3]+1):
            temp = node(ton(s[offset+8:offset+16]),chr(ton(s[offset:offset+8])))
            temp.code = s[offset+16:offset+16+temp.val]
            nli.append(copy.deepcopy(temp))
            offset += 16 + temp.val
        sortcc(nli)
        nchars = ton(s[offset:offset+8]) + 256 * ton(s[offset+8:offset+16])
        nchars += 256 * 256 * ton(s[offset+16:offset+24]) + 256 * 256 * 256 * ton(s[offset+24:offset+32])
        nchars += 256 ** 4 * ton(s[offset+32:offset+40]) + 256 ** 5 * ton(s[offset+40:offset+48])
        offset += 48
        s = s[offset:len(s)]
        
        knio = 0
        hjno = 0
        flisd = []
        while (hjno < nchars):
            hjno += 1
            for kio in nli:
                if ((kio.code) == s[knio:knio+len(kio.code)]):
                    flisd.append(ord(kio.char))
                    knio += len(kio.code)
                    break
        fi = open(fname[0:len(fname) - 4],"b+w")
        fi.write(bytes(flisd))
        fi.close()
