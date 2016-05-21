from PIL import Image
import random
import math
def save_im(matrix):
    imageH = len(matrix)
    imageW = len(matrix[0])
    myimage = Image.new("RGB",(imageW,imageH),"white")
    result = myimage.load()
    for y in range (imageH) :
        for x in range (imageW):
            if matrix[y][x] == 0:
                result[x,y] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                #result[x,y] = (255,255,255)
            else:
                result[x,y] = (0,0,0)
    myimage.save("/home/soheil/mysite/Website/static/Captcha.jpg")
    #myimage.show()

def get_letter_matrix(a):
    img_filename = "/home/soheil/mysite/Website/Words/%s.jpg" %a
    im = Image.open(img_filename)
    pixel = im.load()
    imageW = im.size[0]
    imageH = im.size[1]
    matrix = []
    for y in range (imageH) :
        matrix.append([])
        for x in range (imageW):
            if (pixel[x,y][0]+pixel[x,y][1]+pixel[x,y][2] > 300):
                matrix[y].append(0)
            else:
                matrix[y].append(1)
    emmatrix = []
    for i in range(200):
        emmatrix.append([])
        for j in range(200):
            emmatrix[i].append(0)

    rot_angle = random.random() * (3.14159*2)
    for y in range (imageH) :
        for x in range (imageW):
            if matrix[y][x] == 1:
                r = (y**2 + x**2) ** 0.5
                preang = math.acos(x/r)
                newang = preang - rot_angle
                x1 = int(r*(math.cos(newang)))
                y1 = int(r*(math.sin(newang)))
                emmatrix[y1+50][x1+50] = 1
    enmatrix= []
    for i in range(45):
        enmatrix.append([])
        for j in range(45):
            enmatrix[i].append(0)
    flag = False
    for y in range (200) :
        for x in range(200):
            if emmatrix[y][x] == 1 :
                y1 = y
                flag = True
                break
        if flag :
            break
    flag = False
    for x in range (200) :
        for y in range(200):
            if emmatrix[y][x] == 1 :
                x1 = x
                flag = True
                break
        if flag :
            break
    for y in range(y1,200):
        for x in range(x1,200):
            if emmatrix[y][x] == 1 :
                enmatrix[y-y1][x-x1] = 1
    return enmatrix
def make_captcha(a,b,c):
    #return 0
    mat1=get_letter_matrix(a)
    mat2=get_letter_matrix(b)
    mat3=get_letter_matrix(c)
    capmatrix= []
    for i in range(50):
        capmatrix.append([])
        for j in range(140):
            capmatrix[i].append(0)
    for y in range(50):
        if y<5 :
            continue
        for x in range(140):
            if x<5 :
                continue
            if x<50 :
                if mat1[y-5][x-5]==1:
                    capmatrix[y][x] = 1
            elif x<95 :
                if mat2[y-5][x-50]==1:
                    capmatrix[y][x] = 1
            elif x<140 :
                if mat3[y-5][x-95]==1:
                    capmatrix[y][x] = 1
    #print a , b , c
    save_im(capmatrix)
'''
x=[0,0,0]
for i in range(3):
    rand = random.randint(1,36)
    if rand<11 :
        x[i] = chr(rand+47)
    else:
        x[i] = chr(rand+86)
#save_im(make_captcha(x[0],x[1],x[2]))
make_captcha(x[0],x[1],x[2])



'''
#make_captcha("s","f","f")

#show_im(matrix)
