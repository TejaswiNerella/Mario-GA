import numpy as np

import pytesseract

import cv2

from PIL import ImageGrab

from pynput.keyboard import Key, Controller,Listener
import time
import random
#variables and functions
keyboard=Controller() 
frun=open("1-1r.txt","r+")
fjump=open("1-1j.txt","r+")
fmove=open("1-1m.txt","r+")
level="1-1"
jCounter=0
scoreList=[]
runList2=[[""],[""],[""],[""],[""]]
jumpList2=[[""],[""],[""],[""],[""]]
moveList2=[[""],[""],[""],[""],[""]]
runList=frun.read().split(" ")
jumpList=fjump.read().split(" ")
moveList=fmove.read().split(" ")
lives=0
loop2=True
loop=True
loop3=True
run=False
jump=False
right=False
left=False
scrollCheck=0
scrollInc=0
index=0
timer=0
frun.close()
fjump.close()
fmove.close()
score=0
capo=0

def on_press(key):
    if(key==Key.esc):
        global loop2
        loop2=False
listner=Listener(on_press=on_press)
def levelString():
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
    cap = ImageGrab.grab(bbox=(600, 145, 655, 170))
    cap_gray=cv2.cvtColor(np.array(cap),cv2.COLOR_BGR2GRAY)
    cap_thresh=cap_gray
    cv2.threshold(cap_gray,210,255,cv2.THRESH_BINARY,cap_thresh)
    teststr=pytesseract.image_to_string(
        cap_thresh,
            config='digits')
    teststr=teststr.strip()
    if(len(teststr)==2):
        teststr=teststr[0]+"-"+teststr[1]
    return teststr[len(teststr)-3:len(teststr)]

def scrollScreen():
    pytesseract.pytesseract.tesseract_cmd=r'/opt/homebrew/bin/tesseract'
    cap= ImageGrab.grab(bbox=(1090,590,1190,750))
    return np.array(cap)
def scoreString():
    pytesseract.pytesseract.tesseract_cmd=r'/opt/homebrew/bin/tesseract'
    cap= ImageGrab.grab(bbox=(95,145,170,170))
    teststr=pytesseract.image_to_string(
        cv2.cvtColor(np.array(cap),cv2.COLOR_BGR2GRAY),
            config='digits')
    if(teststr.strip()==""):
        teststr="0"
    teststr.replace(".","")
    return teststr.strip()
def liveString():
    pytesseract.pytesseract.tesseract_cmd=r'/opt/homebrew/bin/tesseract'
    cap= ImageGrab.grab(bbox=(1120,145,1280,170))
    teststr=pytesseract.image_to_string(
        cv2.cvtColor(np.array(cap),cv2.COLOR_BGR2GRAY),
            config='digits')
    return teststr.strip()
def randomMove():
    integer=random.randint(1,12)
    if(integer==1):
        return "left"
    else:
        return "right"

def randomJump():
    global jCounter
    integer=random.randint(1,10)
    if(jCounter>=3):
        jCounter=0
        return "noj"
    if(integer<=8):
        jCounter=jCounter+1
        return "jump"
    else:
        jCounter=0
        return "noj"
def randomRun():
    integer=random.randint(1,10)
    if(integer==1):
        return "nor"
    else:
        return "run"
def readAct(act):
    if(act=="left"):
        return Key.left
    if(act=="right"):
        return Key.right
    if(act=="jump"):
        return Key.space
    if(act=="noj"):
        return "noj"
    if(act=="run"):
        return Key.shift
    if(act=="nor"):
        return "nor"

def act(action):
    global left
    global right
    global jump
    global run
    if(action==Key.right):
        if(left):
            keyboard.release(Key.left)
        left=False
        if not(right):
            right=True
            keyboard.press(action)
    if(action==Key.left):
        if(right):
            keyboard.release(Key.right)
        right=False
        if not(left):
            left=True
            keyboard.press(action)
    if(action==Key.space):
        if not(jump):
            jump=True
            keyboard.press(action)
    if(action=="noj"):
        if(jump):
            keyboard.release(Key.space)
        jump=False
    if(action==Key.shift):
        if not(run):
            run=True
            keyboard.press(action)
    if(action=="nor"):
        if(run):
            keyboard.release(Key.shift)
        run=False
def mutate(action_list,list_type):
    thing=True
    for i in range(len(action_list)):
        integer=random.randint(1,10)
        limit=6*i/len(action_list)
        if(integer<limit):
            if(list_type=="move"):
                action_list[i]=randomMove()
            elif(list_type=="jump"):
                action_list[i]=randomJump()
                if(i>=3):
                    for j in range(3):
                        if not(action_list[i-(j+1)]=="jump"):
                            thing=False
                            break
                    if(thing):
                        action_list[i]="noj"            
            elif(list_type=="run"):
                action_list[i]=randomRun()
def addValue(scoreList,value):
    holder=0
    if(len(scoreList)==5):
        for i in range(4):
            scoreList[i]=scoreList[i+1]
        scoreList[4]=value
    else:
        scoreList.append(value)
def maxList(scoreList):
    maximum=0
    maxIndex=0
    for i in range(len(scoreList)):
        if(scoreList[i]>=maximum):
            maximum=scoreList[i]
            maxIndex=i
    return maxIndex

#code
listner.start()
time.sleep(2)
while(loop2):
    while(loop):
        if(loop3):
            keyboard.release(Key.right)
            keyboard.release(Key.up)
            keyboard.release(Key.shift)
            keyboard.release(Key.left)
            for i in range(len(runList)):
                if(liveString()==""):
                    time.sleep(.5)
                    print("failure")
                    loop=False
                    break
                if(int(liveString())==(lives-1)):
                    loop=False
                    lives=lives-1
                    jumpList=jumpList[:(i-40)]
                    runList=runList[:(i-40)]
                    moveList=moveList[:(i-40)]
                    break
                screeno=scrollScreen()
                if not(type(scrollCheck) is int):
                    if not(np.array_equal(scrollCheck,screeno)):
                        scrollInc=scrollInc+1
                scrollCheck=screeno
                liveso=liveString()
                if not(liveso==""):
                    if not(int(liveso)==(lives-1)):
                        lives=int(liveso)
                    else:
                        loop=False
                        lives=int(liveso)
                        jumpList=jumpList[:(i-40)]
                        runList=runList[:(i-40)]
                        moveList=moveList[:(i-40)]
                        break
                act(readAct(runList[i]))
                act(readAct(jumpList[i]))
                act(readAct(moveList[i]))
                time.sleep(0.1)
                timer=timer+0.1
                if not(levelString()==level):
                    loop=False
                    break
        if not(loop):
                break
        loop3=False
        runs=randomRun()
        runList.append(runs)
        jumps=randomJump()
        jumpList.append(jumps)
        moves=randomMove()
        moveList.append(moves)
        act(readAct(runs))
        act(readAct(jumps))
        act(readAct(moves))
        time.sleep(0.1)
        timer=timer+0.1
        if(liveString()==""):
                loop=False
                break
        if(int(liveString())==(lives-1)):
            loop=False
            jumpList=jumpList[:(len(jumpList)-40)]
            runList=runList[:(len(runList)-40)]
            moveList=moveList[:(len(moveList)-40)]
            break
        screeno=scrollScreen()
        if not(type(scrollCheck) is int):
            if not (np.array_equal(scrollCheck,screeno)):
                scrollInc=scrollInc+1
        scrollCheck=screeno
        scoreso=scoreString()
        if(scoreso==""):
            scoreso="0"
        if not(int(scoreso)<score):
            score=int(scoreso)
        if not(levelString()==level or int(scoreso)<score):
            loop=False
            break
    scores=(scrollInc*10)
    print("index:"+str(index))
    print("score:"+str(scores))
    print("lives:"+liveString())
    score=0
    timer=0
    scrollInc=0
    scrollCheck=0
    addValue(scoreList,scores)
    addValue(jumpList2,jumpList)
    addValue(runList2,runList)
    addValue(moveList2,moveList)
    index=index+1
    if not(levelString()==level):
        print("beaten")
        print(levelString())
        time.sleep(1.25)
        frun=open(level+"r.txt","w")
        fjump=open(level+"j.txt","w")
        fmove=open(level+"m.txt","w")
        frun.write(" ".join(runList))
        fjump.write(" ".join(jumpList))
        fmove.write(" ".join(moveList))
        frun.close()
        fjump.close()
        fmove.close()
        index=0
    elif(index==5):
        print("new gen")
        index=maxList(scoreList)
        level=levelString()
        print("winning index:"+str(index))
        frun=open(level.strip()+"r.txt","w")
        fjump=open(level.strip()+"j.txt","w")
        fmove=open(level.strip()+"m.txt","w")
        frun.write(" ".join(runList2[index]))
        fjump.write(" ".join(jumpList2[index]))
        fmove.write(" ".join(moveList2[index]))
        frun.close()
        fjump.close()
        fmove.close()
        index=0
    level=levelString()
    frun=open("".join([level,"r.txt"]),"r+")
    fjump=open(level+"j.txt","r+")
    fmove=open(level+"m.txt","r+")
    runList=frun.read().split(" ")
    moveList=fmove.read().split(" ")
    jumpList=fjump.read().split(" ")
    frun.close()
    fjump.close()
    fmove.close()
    keyboard.release(Key.right)
    keyboard.release(Key.up)
    keyboard.release(Key.shift)
    keyboard.release(Key.up)
    loop=True
    loop3=True
    right=False
    left=False
    jump=False
    run=False
    if(loop2 and index>0):
        mutate(runList,"run")
        mutate(jumpList,"jump")
        mutate(moveList,"move")
