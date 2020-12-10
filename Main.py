"""
Danny Gastelum
CSC 153 - 01
Fall 2020

"""

import math as Math
import numpy as np
from PIL import Image
import sys

global img, secret

def setimg(imgpath):
    global img
    img = Image.open(imgpath).convert('RGBA')
    print(img.format, img.size, img.mode)

def setsecret(secretstring):
    global secret
    secret = secretstring
def binaryString(message, delim):
    if (delim):
        return ' '.join(format(ord(x), 'b').zfill(8) for x in message)
    return ''.join(["{0:b}".format(x).zfill(8) for x in bytes(message, "utf-8")])


def replacebit(number, bit):
    if bit == 0:
        return (number & ~1) | 0
    else:
        return (number & ~1) | 1


def savenewimage(newimg, path):
    newimg.save(path + ".png")


def verifycompatiblesize():
    imgsize = Math.floor((img.size[0] * img.size[1]) / 8)
    secretsize = Math.ceil(len(binaryString(secret, False)) / 8) + 16
    print(img.format, img.size, img.mode, img)
    print('image bytes: ' + str(imgsize) + ' message size: ' + str(secretsize))
    if imgsize > secretsize:
        return True;
    else:
        return False;


def arrtostring(array):
    result = ''
    for x in array:
        result += str(x)
    return result


def imgarr():
    return np.array(img)


def nullstring():
    return 1


def stegoimg(newimage):
    count = 0
    binsecret = binaryString(secret, False)
    secretsize = binsecret.__len__()
    print(secretsize)
    curPos = 0
    data = imgarr()
    for idx, x in enumerate(data):
        if curPos >= (secretsize+16):
            break
        for idy, y in enumerate(x):

            # print("secret: " + binsecret[curPos])
            if curPos < secretsize:
                r = np.uint8(replacebit(y[0], int(binsecret[curPos])))
                curPos += 1
                g = np.uint8(replacebit(y[1], int(binsecret[curPos])))
                curPos += 1
                b = np.uint8(replacebit(y[2], int(binsecret[curPos])))
                curPos += 1
                a = np.uint8(replacebit(y[3], int(binsecret[curPos])))
                curPos += 1
            elif curPos < (secretsize + 16):
                r = np.uint8(12)
                g = np.uint8(34)
                b = np.uint8(56)
                a = np.uint8(78)
                curPos += 4
            else:
                # print(count)
                break
            # print("Before -- r:" + str(y[0]) + " g:" + str(y[1]) + " b:" + str(y[2]) + " a:" + str(y[3]),
            #       end=' After -- ')
            data[idx][idy] = np.array([r, g, b, a], dtype='uint8')

            # print(" r:" + str(y[0]) + " g:" + str(y[1]) + " b:" + str(y[2]) + " a:" + str(y[3]) + " count: ", end=' ')
            # print(count)
            count += 1
    savenewimage(Image.fromarray(data, 'RGBA'), newimage.split(".")[0])


def getsecret(imgPath):
    data = np.array(Image.open(imgPath).convert('RGBA'))
    count = 0
    buildsecret = ""
    terminate = 0
    prevwasterm = False
    curPos = 0
    nullvalue1 = arrtostring(np.unpackbits(np.uint8(12)))
    nullvalue2 = arrtostring(np.unpackbits(np.uint8(34)))
    nullvalue3 = arrtostring(np.unpackbits(np.uint8(56)))
    nullvalue4 = arrtostring(np.unpackbits(np.uint8(78)))
    for idx, x in enumerate(data):
        if terminate > 3:
            break
        for idy, y in enumerate(x):
            if terminate < 4:
                r = str(np.unpackbits(y[0])[7])
                curPos += 1
                g = str(np.unpackbits(y[1])[7])
                curPos += 1
                b = str(np.unpackbits(y[2])[7])
                curPos += 1
                a = str(np.unpackbits(y[3])[7])
                curPos += 1
                if ((arrtostring(np.unpackbits(y[0])) != nullvalue1)) & (
                        arrtostring(np.unpackbits(y[1])) != nullvalue2) & (
                        arrtostring(np.unpackbits(y[2])) != nullvalue3) & (
                        arrtostring(np.unpackbits(y[3])) != nullvalue4):
                    # print(((arrtostring(np.unpackbits(y[0])) != nullvalue)) & (
                    #         arrtostring(np.unpackbits(y[1])) != nullvalue) & (
                    #               arrtostring(np.unpackbits(y[2])) != nullvalue) & (
                    #               arrtostring(np.unpackbits(y[3])) != nullvalue))
                    buildsecret += r + g + b + a
                    prevwasterm = False
                    terminate = 0
                else:
                    if prevwasterm == True & terminate == 3:
                        terminate += 1
                        break
                    else:
                        prevwasterm = True
                        terminate += 1

            else:
                break
            # print("Before -- r:" + str(y[0]) + " g:" + str(y[1]) + " b:" + str(y[2]) + " a:" + str(y[3]), end=' After -- ')

            # print(" r:" + str(y[0]) + " g:" + str(y[1]) + " b:" + str(y[2]) + " a:" + str(y[3]) + " count: ", end=' ')
            # print(count)
            #count += 1
    # print(buildsecret)
    # if terminate >= 4:
    #     print(terminate)

        return convertsercret(buildsecret)
    else:
        return "NO MESSAGE WAS FOUND" + str(terminate)



def convertsercret(binsecret):
    array = [binsecret[x:x + 8] for x in range(0, len(binsecret), 8)]
    result = ""
    for x in array:
        result += str((chr(int(x, 2))))
    return result

def compareimgs(imgpath1, imgpath2, secret):
    data1 = np.array(Image.open(imgpath1).convert('RGBA'))
    data2 = np.array(Image.open(imgpath2).convert('RGBA'))
    secretsize = Math.ceil(len(binaryString(secret, False)) / 8) + 16
    count=0

    for i, d1 in enumerate(data1):

        for j, d1 in enumerate(d1):
            print("Original image        Modified Image")
            print(data1[i][j])
            print("        ")
            print(data2[i][j])
            print("\n")
            count += 1

            if(count>=secretsize):
                break
        if (count >= secretsize):
            break


def main():
    # arguments: "task", "secret", "image path", "new image name"
    if sys.argv[1] == 'set':
        setsecret(sys.argv[2])
        setimg(sys.argv[3])
        if verifycompatiblesize():
            stegoimg(sys.argv[4])
            print("success")
        else:
            raise Exception("Secret to large for image. See size of image above")
    # arguments: task, image path
    elif sys.argv[1] == 'get':
        print(getsecret(sys.argv[2]))
    elif sys.argv[1] == 'compare':
        #"original image" "Modified image" "secret"
        compareimgs(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise Exception("Task not recognized: " + sys.argv[1] )


if __name__ == "__main__":
    main()



# This is a hidden message to demonstrate Steganography for CSC153 group 5 project. Group Members: Danny Gastelum, CJ Angelina Torres, Graciela Meza