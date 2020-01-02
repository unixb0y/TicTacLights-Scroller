from PIL import Image
from letters import *
from random import *
import sys, argparse, copy, time, struct, serial

red =   ('07', '00', '00')
green = ('00', '07', '00')
blue =  ('00', '00', '07')
black = ('00', '00', '00')

def mapToRed(line):
    return list(map(lambda x: red if x == 1 else black, line))

def mapToGreen(line):
    return list(map(lambda x: green if x == 1 else black, line))

def mapToBlue(line):
    return list(map(lambda x: blue if x == 1 else black, line))

def mapToRand(line):
    return list(map(lambda x: ('0'+str(randint(1, 7)),
        '0'+str(randint(1, 7)), '0'+str(randint(1, 7)))
        if x == 1 else black, line))

def getMatrix(par):
    switcher={
        'a':a,'b':b,'c':c,
        'd':d,'e':e,'f':f,
        'g':g,'h':h,'i':i,
        'j':j,'k':k,'l':l,
        'm':m,'n':n,'o':o,
        'p':p,'q':q,'r':r,
        's':s,'t':t,'u':u,
        'v':v,'w':w,'x':x,
        'y':y,'z':z,'?':quest,
        '!':excl,'.':dot,
        '1':one,'2':two,
        '3':three,'4':four,
        '5':five,'6':six,
        '7':seven,'8':eight,
        '9':nine,'0':zero,
        ' ':space
    }
    return switcher.get(par,"Invalid character")

def createFullMatrix(string, colour):
    # combined 2D array of whole text
    lettermatrix = []

    # list of letters as 2D arrays
    letters = list(map(lambda x: getMatrix(x), string))
    for i in range(0,8):
        for j in range(0,len(string)):
            if j == 0:
                lettermatrix.append(letters[j][i])
            else:
                lettermatrix[i] = lettermatrix[i] + letters[j][i]
            lettermatrix[i] = lettermatrix[i] + [0]

    lettermatrix = list(map(colour, lettermatrix))
    return lettermatrix


def sendPacket(textMatrix, port):
    packet = bytes.fromhex('235426660008001200030007')

    for i in range(0, 8):
        for j in range(0, 18):
            if j < len(textMatrix[i]):
                packet += bytes.fromhex(textMatrix[i][j][0])
                packet += bytes.fromhex(textMatrix[i][j][1])
                packet += bytes.fromhex(textMatrix[i][j][2])
            else:
                packet += bytes.fromhex('000000')

    ser = serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    ser.write(packet)
    s = ser.read(1)
    ser.close()

def printText(text, colour, speed, port):
    if colour == 'red':
        colouringFunc = mapToRed
    elif colour == 'green':
        colouringFunc = mapToGreen
    elif colour == 'blue':
        colouringFunc = mapToBlue
    elif colour == 'random':
        colouringFunc = mapToRand

    screen = createFullMatrix(text, colouringFunc)
    while True:
        for i in range(0, len(screen[0])):
            if i%2==0:
                continue
            else:
                temp = copy.deepcopy(screen)
                for line in temp:
                    cache = line[:i]
                    del line[:i]
                    line += cache

                sendPacket(temp, port)
                time.sleep(speed)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', required=True,
        help='the text to display')
    parser.add_argument('-c', '--colour', default='blue',
        help='the preferred colour', choices=['red','green','blue','random'])
    parser.add_argument('-s', '--speed', default=0.05, type=float,
        help='the preferred speed')
    parser.add_argument('-p', '--port', default='/dev/tty.usbserial-DM031PBM',
        help='the port where your TicTacLights is attached')
    args = parser.parse_args()

    printText(args.text, args.colour, args.speed, args.port)

if __name__ == "__main__":
   main(sys.argv[1:])