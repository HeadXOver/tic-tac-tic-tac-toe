import ctypes

whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)
    


import tree



import shutil
import os

import pygame
from pygame.locals import*

bg_file = "basic\\final_bg.jpg"
flag_file = "basic\\flag_x.jpg"
bflag_x_file = "basic\\bigflag_x.jpg"
bflag_o_file = "basic\\bigflag_o.jpg"
white = (255,255,255)
black = (0,0,0)

fsmall=[[0 for i in range(9)] for i in range(9)]
fbig=[0,0,0,0,0,0,0,0,0]
flimit=0
fstep=0
flist=[]
yibaocun=False

jiao_step=jiao_ban=jiao4_yibu=jiao5=jiao=0


small=[[0 for i in range(9)] for i in range(9)]
dis_ps=[0 for i in range(81)]
big=[0,0,0,0,0,0,0,0,0]
record=[]
recordx=recordy=0
button_x = button_y = [0,0]
button_small=button_big=0
control = 0
limit=filenum=0
flag=mode=page=1
whowin=0
step=0


pygame.init()
#改变棋盘数据，返回谁控制
def setflag(x,y,sflag):
    global small,big,control,step,yibaocun
    step+=1
    print(step)
    small[x][y]=sflag
    check(x)
    if(yibaocun):
        yibaocun=False
    return big[y]
    
#刷新变量,重绘棋盘
def renew():
    global small,big,limit,flag,whowin,control,step,mode
    screen.blit(bg,(0,-5))
    pygame.draw.rect(screen,white,[19,17,468,468],5)
    screen.blit(pygame.image.load("basic\\x_put.jpg"),(500,450))
    small=[[0 for i in range(9)] for i in range(9)]
    big=[0,0,0,0,0,0,0,0,0]
    record=[]
    limit=0
    control=0
    flag=mode=1
    step=0
    whowin=0
    draw()
    screen.blit(pygame.image.load("basic\\电脑先手.jpg"),(510,150))
    screen.blit(pygame.image.load("basic\\teach.jpg"),(540,20))
    pygame.display.update()
    
#绘制棋盘
def draw():
    global small,big,limit,control,button_big,button_small,whowin,flag,step,mode
    screen.blit(bg,(0,-5))
    
    pygame.draw.rect(screen,white,[19,17,468,468],5)
    if(whowin!=0):
        for i in range(0,9):
            xy_i=turnXY(i)
            drlist=small[i]
            for j in range(0,9):
                xy_j=turnXY(j)
                x=37+164*(xy_i[0])+(xy_j[0])*37
                y=31+167*(xy_i[1])+(xy_j[1])*39
                if(drlist[j]==1):
                    screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
                if(drlist[j]==-1):
                    screen.blit(pygame.image.load("basic\\flag_o.jpg"),(x,y))
    
        for i in range(0,9):
            xy_i=turnXY(i)
            if(big[i]==1):
                screen.blit(pygame.image.load(bflag_x_file),((30+164*(xy_i[0])),(25+167*(xy_i[1]))))
            if(big[i]==-1):
                screen.blit(pygame.image.load(bflag_o_file),((30+164*(xy_i[0])),(25+167*(xy_i[1]))))
    if(whowin==1):
        screen.blit(pygame.image.load("basic\\x_win.jpg"),(500,350))
    elif(whowin==-1):
        screen.blit(pygame.image.load("basic\\o_win.png"),(500,350))
    else:
        if(step==0 and mode==1):
            screen.blit(pygame.image.load("basic\\电脑先手.jpg"),(510,150))
            screen.blit(pygame.image.load("basic\\teach.jpg"),(540,20))
        else:
            screen.blit(pygame.image.load("basic\\重开.jpg"),(510,200))
        for i in range(0,9):
            xy_i=turnXY(i)
            drlist=small[i]
            for j in range(0,9):
                xy_j=turnXY(j)
                x=37+164*(xy_i[0])+(xy_j[0])*37
                y=31+167*(xy_i[1])+(xy_j[1])*39
                if(drlist[j]==1):
                    screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
                if(drlist[j]==-1):
                    screen.blit(pygame.image.load("basic\\flag_o.jpg"),(x,y))
    
        for i in range(0,9):
            xy_i=turnXY(i)
            if(big[i]==1):
                screen.blit(pygame.image.load(bflag_x_file),((30+164*(xy_i[0])),(25+167*(xy_i[1]))))
            if(big[i]==-1):
                screen.blit(pygame.image.load(bflag_o_file),((30+164*(xy_i[0])),(25+167*(xy_i[1]))))

        if(control):
            if(control==1):
                screen.blit(pygame.image.load("basic\\x_control.jpg"),(500,450))
            if(control==-1):
                screen.blit(pygame.image.load("basic\\o_control.jpg"),(500,450))
            pygame.draw.rect(screen,(255,111,111),[19,17,468,468],5)
        else:
            if(flag==1):
                screen.blit(pygame.image.load("basic\\x_put.jpg"),(500,450))
            else:
                if(step>20 and step<=45):
                    screen.blit(pygame.image.load("basic\\o_put_think.jpg"),(500,450))
                else:
                    screen.blit(pygame.image.load("basic\\o_put.jpg"),(500,450))
            if(limit>=1 and limit<=9):
                xy_i=turnXY(limit-1)
                pygame.draw.rect(screen,(255,255,255),[(21+164*(xy_i[0])),(18+167*(xy_i[1])),133,133],3)

        pygame.display.update()
#存档绘制
def draw2(fsmall,fbig,flimit):
    screen.blit(pygame.image.load("basic\\存档.jpg"),(0,-5))
    
    for i in range(0,9):
        xy_i=turnXY(i)
        drlist=fsmall[i]
        for j in range(0,9):
            xy_j=turnXY(j)
            x=37+164*(xy_i[0])+(xy_j[0])*37
            y=31+167*(xy_i[1])+(xy_j[1])*39
            if(drlist[j]==1):
                screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
            if(drlist[j]==-1):
                screen.blit(pygame.image.load("basic\\flag_o.jpg"),(x,y))
    
    for i in range(0,9):
        xy_i=turnXY(i)
        if(fbig[i]==1):
            screen.blit(pygame.image.load(bflag_x_file),((30+164*(xy_i[0])),(25+167*(xy_i[1]))))
        if(fbig[i]==-1):
            screen.blit(pygame.image.load(bflag_o_file),((30+164*(xy_i[0])),(25+167*(xy_i[1]))))

    if(flimit>=1 and flimit<=9):
        xy_i=turnXY(flimit-1)
        pygame.draw.rect(screen,(255,255,255),[(21+164*(xy_i[0])),(18+167*(xy_i[1])),133,133],3)
    pygame.display.update()
#接收大格，返回谁控制或满格
def recheck(chlist):
    j=0
    for i in range(0,3):
        if(chlist[i*3]+chlist[i*3+1]+chlist[i*3+2]==3):
            j=1
            
        elif(chlist[i*3]+chlist[i*3+1]+chlist[i*3+2]==-3):
            j=-1

        elif(chlist[i]+chlist[i+3]+chlist[i+6]==3):
            j=1
        elif(chlist[i]+chlist[i+3]+chlist[i+6]==-3):
            j=-1

        elif((chlist[0]+chlist[4]+chlist[8]==3)or(chlist[2]+chlist[4]+chlist[6]==3)):
            j=1
        elif((chlist[0]+chlist[4]+chlist[8]==-3)or(chlist[2]+chlist[4]+chlist[6]==-3)):
            j=-1

    if(j==0):
        n=0
        for i in chlist:
            if(i!=0):
                n+=1
        if(n==9):
            j=10
    
    return j

#检查大格        
def check(n):
    global small,big
    big[n]=recheck(small[n])

#将点击位置转为坐标
def pos__button(xx,yy):
    global jiao_step,jiao_ban,jiao4_yibu,jiao5,jiao,yibaocun,flist,button_x,button_y,small,button_small,button_big,fsmall,fbig,flimit,fstep,filenum,page,dis_ps,step,limit,control,mode

    if(xx>509 and xx<631 and yy>149 and yy<198 and step==0 and mode==1):
        control=setflag(4,4,-1)
        limit=5
        draw()
    elif(xx>510 and xx<631 and yy>200 and yy<247 and step!=0 and mode==1):
        renew()
        
    elif(xx>509 and xx<631 and yy>198 and yy<242 and step==0 and mode==1):
        flist=[lists for lists in os.listdir("data\\dict_1") if(os.path.isfile(os.path.join("data\\dict_1",lists)))]
        filenum=len(flist)
        if(filenum==0):
            screen.blit(pygame.image.load("basic\\无存档.jpg"),(500,400))
        else:
            
            mode=2
            
            file = open("data\\dict_1\\dict_1.txt")
            r_line=0
            while 1:
                r_line+=1
                line = file.readline()       
                if not line:
                    break
                if(r_line<=81):
                    dis_ps[r_line-1]=int(line)
                elif(r_line==82):
                    flimit=int(line)
                elif(r_line==83):
                    fstep=int(line)
                
            for i in range(0,81):
                n=i//9
                fsmall[n][i-9*n]=dis_ps[i]
            for i in range(0,9):
                fbig[i]=recheck(fsmall[i])
            draw2(fsmall,fbig,flimit)
        
    elif(mode==None or (xx>512 and xx<626 and yy>242 and yy<284 and step!=0 and mode==1)):
        if(xx+yy>=1000):
            pygame.quit()
            exit()
        elif(yy<38):
            mode=1
            draw()
        elif(yy-xx>=263 or (xx>512 and xx<626 and yy>242 and yy<284 and step!=0 and mode==1)):
            n=0
            for i in range(0,9):
                for j in range(0,9):
                    dis_ps[n]=small[i][j]
                    n+=1
            save_num=os.listdir("data\\dict_1")
            save_name=1
            while("dict_"+str(save_name)+".txt" in save_num):
                save_name+=1
                    
            f= open("data\\dict_1\\dict_"+str(save_name)+".txt","w+")
            for w_key in dis_ps:
                f.write(str(w_key)+"\n")
            f.write(str(limit)+"\n"+str(step))
            f.close()
            if(yy-xx>=263):
                pygame.quit()
                exit()
            else:
                screen.blit(pygame.image.load("basic\\已保存.jpg"),(500,400))
                yibaocun=True

    elif(xx>540 and xx<671 and yy>21 and yy<69 and step==0 and mode==1):
        mode=3
        jiao_step=1
    
    
    if(xx>=33 and xx<68):
        button_x=[1,1]
    elif(xx>=68 and xx<108):
        button_x=[1,2]
    elif(xx>=108 and xx<143):
        button_x=[1,3]
    elif(xx>=197 and xx<234):
        button_x=[2,1]
    elif(xx>=234 and xx<273):
        button_x=[2,2]
    elif(xx>=273 and xx<307):
        button_x=[2,3]
    elif(xx>=360 and xx<397):
        button_x=[3,1]
    elif(xx>=397 and xx<436):
        button_x=[3,2]
    elif(xx>=436 and xx<=470):
        button_x=[3,3]
    else:
        button_x=[0,0]

    if(yy>=27and yy<68):
        button_y=[1,1]
    elif(yy>=68 and yy<108):
        button_y=[1,2]
    elif(yy>=108 and yy<143):
        button_y=[1,3]
    elif(yy>=197 and yy<234):
        button_y=[2,1]
    elif(yy>=234 and yy<273):
        button_y=[2,2]
    elif(yy>=273 and yy<307):
        button_y=[2,3]
    elif(yy>=360 and yy<397):
        button_y=[3,1]
    elif(yy>=397 and yy<436):
        button_y=[3,2]
    elif(yy>=436 and yy<=470):
        button_y=[3,3]
    else:
        button_y=[0,0]

    button_big=button_x[0]+button_y[0]*3-4
    button_small=button_x[1]+button_y[1]*3-4
#将整数0到8转为坐标0到2
def turnXY(n):
    y=0
    if(0<=n and n<=2):
        y=0
    if(3<=n and n<=5):
        y=1
    if(6<=n and n<=8):
        y=2

    x=(n+3)%3
    return [x,y]
#电脑回合
def computer():
    global small,record,limit,control,flag,step,whowin,big
    decision=tree.decide(small,limit,3+0.05*step)
    if(decision==None or decision==0):
        whowin=1
    else:
        record.append(decision)
        control=setflag(decision[1],decision[2],-1)
        whowin=tree.whowin(small)
        limit=decision[0]
        if(control==-1):
            control=0
        flag=1
    draw()


screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("战略树枝3.4")

bg = pygame.image.load(bg_file)
ico=pygame.image.load("basic\\pyico.png")
screen.blit(bg,(0,-5))
screen.blit(pygame.image.load("basic\\x_put.jpg"),(500,450))
pygame.draw.rect(screen,(255,255,255),[19,17,468,468],5)
pygame.display.set_icon(ico)
screen.blit(pygame.image.load("basic\\电脑先手.jpg"),(510,150))
screen.blit(pygame.image.load("basic\\teach.jpg"),(540,20))

def start_jiao():
    global jiao_step,jiao_ban,jiao4_yibu,button_x,button_y,jiao5,jiao,mode
    
    if(jiao_step==1):
        screen.blit(bg,(0,-5))
        for jiao_i in range(1,4):
            for jiao_j in range(1,4):
                numfile="basic\\jiao\\num\\"+str(3*jiao_j-3+jiao_i)+".jpg"
                screen.blit(pygame.image.load(numfile),(164*(jiao_i-1)+21,167*(jiao_j-1)+15))
                pygame.display.update()
        screen.blit(pygame.image.load("basic\\jiao\\txt1.jpg"),(500,200))
        jiao_step=2
    elif(jiao_step==2):
        screen.blit(bg,(0,-5))
        for jiao_i in range(1,4):
            for jiao_j in range(1,4):
                numfile="basic\\jiao\\num\\"+str(3*jiao_j-3+jiao_i)+".jpg"
                screen.blit(pygame.image.load(numfile),(40*(jiao_i-1)+21,40*(jiao_j-1)+15))
        screen.blit(pygame.image.load("basic\\jiao\\txt2.jpg"),(500,200))
        jiao_step=3
    elif(jiao_step==3):
        screen.blit(bg,(0,-5))
        screen.blit(pygame.image.load("basic\\jiao\\txt3.jpg"),(500,200))
        step3_end = False
        jiao3_step = [1,1]
        numfile="basic\\jiao\\num\\"+str(jiao3_step[1]*3-3+jiao3_step[0])+".jpg"
        pygame.draw.rect(screen,(111,255,255,),[21,15,133,133],3)
        screen.blit(pygame.image.load(numfile),(50*(jiao3_step[0]-1)+21,50*(jiao3_step[1]-1)+15))
        pygame.display.update()
        
        while True:
            
            for event in pygame.event.get():
                if (event.type==QUIT):
                    pygame.quit()
                    exit()
                if event.type==MOUSEBUTTONDOWN:
                    screen.blit(bg,(0,-5))
                    screen.blit(pygame.image.load("basic\\jiao\\txt3.jpg"),(500,200))
                    if(jiao3_step[1]>=3 and jiao3_step[0]>=3):
                        step3_end=True
                        screen.blit(pygame.image.load("basic\\jiao\\txt4.jpg"),(500,200))
                    elif(jiao3_step[1]==3):
                        jiao3_step[0]+=1
                        jiao3_step[1]=1
                    elif(jiao3_step[1]<3):
                        jiao3_step[1]+=1
                    numfile="basic\\jiao\\num\\"+str(jiao3_step[0]*3-3+jiao3_step[1])+".jpg"
                    pygame.draw.rect(screen,(111,255,255,),[164*(jiao3_step[1]-1)+21,167*(jiao3_step[0]-1)+15,133,133],3)
                    screen.blit(pygame.image.load(numfile),(50*(jiao3_step[1]-1)+21,50*(jiao3_step[0]-1)+15))
                    pygame.display.update()
            if(step3_end):
                break
        jiao_step=4
        
    elif(jiao_step==4):
        if(jiao4_yibu<5):
            jiao4_yibu+=1
        if(jiao4_yibu==1):
            screen.blit(bg,(0,-5))
            screen.blit(pygame.image.load("basic\\x_put.jpg"),(500,450))
            pygame.draw.rect(screen,(111,255,255),[535,455,45,45],5)
            screen.blit(pygame.image.load("basic\\xianshou.jpg"),(500,420))
        else:
            if(button_x[0]!=0 and button_y[0]!=0):
                xy_b=[button_x[0]-1,button_y[0]-1]
                xy_s=[button_x[1]-1,button_y[1]-1]
                x=37+164*(xy_b[0])+(xy_s[0])*37
                y=31+167*(xy_b[1])+(xy_s[1])*39
                screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
                pygame.draw.rect(screen,(255,255,255,),[164*(button_x[1]-1)+21,167*(button_y[1]-1)+15,133,133],3)
                screen.blit(pygame.image.load("basic\\jiao\\txt5.jpg"),(500,200))
                jiao_step=5
                jiao4_yibu=0
                jiao5=[button_x[1],button_y[1]]
    elif(jiao_step==5):
        if(button_x[0]==jiao5[0] and button_y[0]==jiao5[1]):
            xy_b=[button_x[0]-1,button_y[0]-1]
            xy_s=[button_x[1]-1,button_y[1]-1]
            x=37+164*(xy_b[0])+(xy_s[0])*37
            y=31+167*(xy_b[1])+(xy_s[1])*39
            screen.blit(pygame.image.load("basic\\flag_o.jpg"),(x,y))
            pygame.draw.rect(screen,(0,0,0,10),[164*(jiao5[0]-1)+21,167*(jiao5[1]-1)+15,133,133],3)
            pygame.draw.rect(screen,(255,255,255),[19,17,468,468],5)


            pygame.draw.rect(screen,(255,255,255,),[164*(button_x[1]-1)+21,167*(button_y[1]-1)+15,133,133],3)
            screen.blit(pygame.image.load("basic\\jiao\\txt6.jpg"),(500,200))
            jiao_step=6
    elif(jiao_step==6):
        screen.blit(bg,(0,-5))
        screen.blit(pygame.image.load("basic\\jiao\\txt7.jpg"),(500,200))
        jiao_step=7
    elif(jiao_step==7):
        pos__button(219,48)
        xy_b=[button_x[0]-1,button_y[0]-1]
        xy_s=[button_x[1]-1,button_y[1]-1]
        x=37+164*(xy_b[0])+(xy_s[0])*37
        y=31+167*(xy_b[1])+(xy_s[1])*39
        screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
        pos__button(255,87)
        xy_b=[button_x[0]-1,button_y[0]-1]
        xy_s=[button_x[1]-1,button_y[1]-1]
        x=37+164*(xy_b[0])+(xy_s[0])*37
        y=31+167*(xy_b[1])+(xy_s[1])*39
        screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
        
        screen.blit(pygame.image.load("basic\\jiao\\txt8.jpg"),(500,200))
        pygame.draw.rect(screen,(255,255,255,),[185,15,133,133],3)
        jiao_step=8
    elif(jiao_step==8):
        if(button_x==[2,3] and button_y==[1,3]):
            xy_b=[button_x[0]-1,button_y[0]-1]
            xy_s=[button_x[1]-1,button_y[1]-1]
            x=37+164*(xy_b[0])+(xy_s[0])*37
            y=31+167*(xy_b[1])+(xy_s[1])*39
            screen.blit(pygame.image.load("basic\\flag_x.jpg"),(x,y))
            screen.blit(pygame.image.load("basic\\jiao\\txt9.jpg"),(500,200))
            jiao_step=9
    elif(jiao_step==9):
        screen.blit(bg,(0,-5))
        screen.blit(pygame.image.load("basic\\jiao\\txt10.jpg"),(500,200))
        screen.blit(pygame.image.load("basic\\bigflag_x.jpg"),(195,25))
        jiao_step=10
    elif(jiao_step==10):
        screen.blit(pygame.image.load("basic\\jiao\\txt11.jpg"),(500,200))
        screen.blit(pygame.image.load("basic\\bigflag_x.jpg"),(195,25))
        screen.blit(pygame.image.load("basic\\bigflag_x.jpg"),(195,192))
        screen.blit(pygame.image.load("basic\\bigflag_x.jpg"),(195,359))
        jiao_step=11
    elif(jiao_step==11):
        screen.blit(bg,(0,-5))
        screen.blit(pygame.image.load("basic\\jiao\\txt12.jpg"),(500,200))
        screen.blit(pygame.image.load("basic\\bigflag_x.jpg"),(195,359))
        screen.blit(pygame.image.load("basic\\flag_o.jpg"),(71,275))
        jiao_step=12
    elif(jiao_step==12):
        screen.blit(pygame.image.load("basic\\jiao\\txt13.jpg"),(500,200))
        jiao_step=13
    elif(jiao_step==13):
        screen.blit(pygame.image.load("basic\\jiao\\txt14.jpg"),(500,200))
        pygame.draw.rect(screen,(255,111,111),[19,17,468,468],5)
        jiao_step=14
    elif(jiao_step==14):
        screen.blit(pygame.image.load("basic\\jiao\\txt15.jpg"),(500,200))
        screen.blit(pygame.image.load("basic\\x_control.jpg"),(500,450))
        jiao_step=15
    elif(jiao_step==15):
        screen.blit(pygame.image.load("basic\\jiao\\txt16.jpg"),(500,200))
        jiao_step=16
    elif(jiao_step==16):
        if(button_x!=[0,0] and button_y!=[0,0] and (button_x[0]!=2 or button_y[0]!=3)):
            pygame.draw.rect(screen,(255,255,255,),[164*(button_x[0]-1)+21,167*(button_y[0]-1)+15,133,133],3)
            screen.blit(pygame.image.load("basic\\jiao\\txt17.jpg"),(500,200))
            screen.blit(pygame.image.load("basic\\x_put.jpg"),(500,450))
            jiao_step=17
    elif(jiao_step==17):
        screen.blit(pygame.image.load("basic\\jiao\\txt18.jpg"),(500,200))
        jiao_step=18
    elif(jiao_step==18):
        renew()
        jiao=jiao_ban=False
        jiao_step=1
        
        



while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            if(whowin!=0 or step==0 or yibaocun):
                pygame.quit()
                exit()
            else:
                screen.blit(pygame.image.load("basic\\退出.jpg"),(0,-5))
                mode=None
            
                
            
        if event.type==MOUSEBUTTONDOWN:
            if(whowin!=0):
                renew()
            else:
                x,y=pygame.mouse.get_pos()
                print(x,y)
                pos__button(x,y)
                
                if(mode==1 and button_x[0]*button_x[1]*button_y[0]*button_y[1]!=0)and(whowin==0):
                    if(control==1):
                        if(big[button_big]==0):
                            limit=button_big+1
                            control=0
                            draw()
                            record.append([limit,recordx,recordy])
                            if(flag==-1):
                                computer()
                              
                    else:
                        if((small[button_big][button_small]==0)and((limit-1==button_big)or(limit==0))):
                            control=setflag(button_big,button_small,1)
                            flag=-1
                            whowin=tree.whowin(small)
                            draw()

                            if(whowin==0):
                                if(control==0):
                                    limit=button_small+1
                                    draw()
                                    record.append([limit,button_big,button_small])
                                    computer()
                                elif(control==-1 or control>4):
                                    limit=0
                                    draw()
                                    recordx=button_big
                                    recordy=button_small
                                    computer()
                elif(mode==3):
                    start_jiao()
                
                elif(mode==2):
                    if(x>=586 and x<=671):
                        if(y>=175 and y<=219):
                            step=0
                            mode=1
                            draw()
                        elif(y>=230 and y<=271):
                            mode=1
                            for i in range(0,9):
                                for j in range(0,9):
                                    small[i][j]=fsmall[i][j]
                            for i in range(0,9):
                                big[i]=fbig[i]
                                
                            control=0
                            limit=flimit
                            step=fstep
                            flag=1
                            draw()
                        elif(y>=283 and y<=316):
                            if(page!=1):
                                file.close()
                            os.remove("data\\dict_1\\dict_"+str(page)+".txt")
                            print(filenum)
                            if(filenum>1):
                                
                                n=page+1
                                while("dict_"+str(n)+".txt" in flist):
                                    
                                    os.rename("data\\dict_1\\dict_"+str(n)+".txt","data\\dict_1\\dict_"+str(n-1)+".txt" )
                                    n+=1
                                
                                    

                            mode=1
                            step=0
                            draw()
                    elif(y>256):
                        if(filenum>=page+1):
                            page+=1
                            file = open("data\\dict_1\\dict_"+str(page)+".txt")
                            r_line=0
                            while 1:
                                r_line+=1
                                line = file.readline()       
                                if not line:
                                    break
                                if(r_line<=81):
                                    dis_ps[r_line-1]=int(line)
                                elif(r_line==82):
                                    flimit=int(line)
                                elif(r_line==83):
                                    fstep=int(line)
                
                            for i in range(0,81):
                                n=i//9
                                fsmall[n][i-9*n]=dis_ps[i]
                            for i in range(0,9):
                                fbig[i]=recheck(fsmall[i])
                            draw2(fsmall,fbig,flimit)
                    elif(y<256):
                        if(page-1>=1):
                            page-=1
                            file = open("data\\dict_1\\dict_"+str(page)+".txt")
                            r_line=0
                            while 1:
                                r_line+=1
                                line = file.readline()       
                                if not line:
                                    break
                                if(r_line<=81):
                                    dis_ps[r_line-1]=int(line)
                                elif(r_line==82):
                                    flimit=int(line)
                                elif(r_line==83):
                                    fstep=int(line)
                
                            for i in range(0,81):
                                n=i//9
                                fsmall[n][i-9*n]=dis_ps[i]
                            for i in range(0,9):
                                fbig[i]=recheck(fsmall[i])
                            draw2(fsmall,fbig,flimit)
                
                        

    pygame.display.update()





                
