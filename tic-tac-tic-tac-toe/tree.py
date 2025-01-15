first=1
sticknum=7

#大格中数量
def blanknum(list9,t):
    n=0
    for i in list9:
        if(i==t):
            n+=1
    return n

#大格被占情况
def check(list9):
    m=0
    for i in range(0,3):
        n=list9[3*i]+list9[3*i+1]+list9[3*i+2]
        if(n==3):
            m=1
            break
        elif(n==-3):
            m=-1
            break

        n=list9[i]+list9[i+3]+list9[i+6]
        if(n==3):
            m=1
            break
        elif(n==-3):
            m=-1
            break

        n=list9[0]+list9[4]+list9[8]
        if(n==3):
            m=1
            break
        elif(n==-3):
            m=-1
            break
        n=list9[2]+list9[4]+list9[6]
        if(n==3):
            m=1
            break
        elif(n==-3):
            m=-1
            break
    if(m==0):
        n=blanknum(list9,0)
        if(n==0):
            return 10
    return m
    
#谁赢
def whowin(small):
    global first
    big=[0,0,0,0,0,0,0,0,0]
    for i in range(0,9):
        big[i]=check(small[i])
    n=check(big)
    if(n==1 or n==-1):
        return n
    if(n==10):
        m=blanknum(big,1)
        l=blanknum(big,-1)
        if(first==1):
            if(l>=m):
                return -1
            return 1
        else:
            if(m>=l):
                return 1
            return -1
    return 0

#一个大格的价值
def partvalue(small,list9,flag,turn):
    n=check(list9)
    if(n!=0 and n<=4):
        return -72*n
    threenum=value=0
    for i in range(0,3):
        if(list9[3*i]!=-flag and list9[3*i+1]!=-flag and list9[3*i+2]!=-flag):
            n=list9[3*i]+list9[3*i+1]+list9[3*i+2]
            if(n==0):
                value+=1
            elif(n==1*flag):
                value+=3
            elif(n==2*flag):
                value+=9
                threenum+=1
        
        if(list9[i]!=-flag and list9[i+3]!=-flag and list9[i+6]!=-flag):
            n=list9[i]+list9[i+3]+list9[i+6]
            if(n==0):
                value+=1
            elif(n==1*flag):
                value+=3
            elif(n==2*flag):
                value+=9
                threenum+=1
        

    if(list9[0]!=-flag and list9[4]!=-flag and list9[8]!=-flag):
        n=list9[0]+list9[4]+list9[8]
        if(n==0):
            value+=1
        elif(n==1*flag):
            value+=3
        elif(n==2*flag):
            value+=9
            threenum+=1

    if(list9[2]!=-flag and list9[4]!=-flag and list9[6]!=-flag):
        n=list9[2]+list9[4]+list9[6]
        if(n==0):
            value+=1
        elif(n==1*flag):
            value+=3
        elif(n==2*flag):
            value+=9
            threenum+=1

    twice=[0,0,0,0,0,0,0,0,0]

    for i in range(0,9):
        if(list9[i]==0):
            list9[i]=flag
            n=check(list9)
            if(n==flag):
                twice[i]=1
                threenum-=1
            list9[i]=0

    if(turn>=5):
        return value-threenum*6
    n=blanknum(twice,1)
    if(n!=0):
        for i in range(0,9):
            if(twice[i]==1):
                n=partvalue(small,small[i],-flag,turn+1)
                if(n>0):
                    value-=n/12

    return value-threenum*6

#整体价值
def envalue(small,limit,flag):
    big=[0,0,0,0,0,0,0,0,0]
    for i in range(0,9):
        big[i]=check(small[i])
    list9=[0,0,0,0,0,0,0,0,0]
    for i in range(0,9):
        if(big[i]!=0):
            list9[i]=big[i]*(-72)
        else:
            boyi=5
            list9[i]=partvalue(small,small[i],-1,1)-partvalue(small,small[i],1,1)
    value=0
    for i in range(0,3):
        if(abs(list9[3*i])<700 and abs(list9[3*i+1])<700 and abs(list9[3*i+2])<700):
            value+=(list9[3*i]+list9[3*i+1]+list9[3*i+2])/3
        if(abs(list9[i])<700 and abs(list9[i+3])<700 and abs(list9[i+6])<700):
            value+=(list9[i]+list9[i+3]+list9[i+6])/3
    if(abs(list9[0])<700 and abs(list9[4])<700 and abs(list9[8])<700):
        value+=(list9[0]+list9[4]+list9[8])/3
    if(abs(list9[2])<700 and abs(list9[4])<700 and abs(list9[6])<700):
        value+=(list9[2]+list9[4]+list9[6])/3

    
    if(abs(big[limit])>288):
        value=0.6*value+28.8*flag
    elif(flag==big[limit]):
        value+=(-big[limit])/4
    

    

    return value*3/20

#树枝
def trystick(small,limit,flag,turn,max1):
    global sticknum
    value=72*flag
    if(turn>=sticknum):
        if(limit!=0):
            for i in range(0,9):
                if(small[limit-1][i]==0):
                    small[limit-1][i]=flag
                    n=whowin(small)
                    if(n==-flag):
                        small[limit-1][i]=0
                        continue
                    if(n==flag):
                        small[limit-1][i]=0
                        return -72*flag
                    n=envalue(small,i,flag)

                    big=[0,0,0,0,0,0,0,0,0]
                    for j in range(0,9):
                        big[j]=check(small[j])

                    if(big[i]==1):
                        n=0.95*n-3.6
                    elif(big[i]==-1):
                        n=0.95*n+3.6
                    elif(big[i]>4):
                        n=0.95*n+3.6*(-flag)
                    if(flag==-1):
                        if(n>max1):
                            small[limit-1][i]=0
                            return max1
                        if(n>value):
                            value=n
                    else:
                        if(n<max1):
                            small[limit-1][i]=0
                            return max1
                        if(n<value):
                            value=n
                    small[limit-1][i]=0

        else:
            big=[0,0,0,0,0,0,0,0,0]
            for i in range(0,9):
                big[i]=check(small[i])
            for k in range(1,10):
                if(big[k-1]==0):
                    limit=k
                    for i in range(0,9):
                        if(small[limit-1][i]==0):
                            small[limit-1][i]=flag
                            n=whowin(small)
                            if(n==-flag):
                                small[limit-1][i]=0
                                continue
                            if(n==flag):
                                small[limit-1][i]=0
                                return -72*flag
                            n=envalue(small,i,flag)

                            big=[0,0,0,0,0,0,0,0,0]
                            for j in range(0,9):
                                big[j]=check(small[j])

                            if(big[i]==-flag):
                                n=0.95*n-3.6
                            elif(big[i]==flag):
                                n=0.95*n+3.6
                            elif(big[i]>4):
                                n=0.95*n+3.6*(-flag)
                            if(flag==-1):
                                if(n>=max1):
                                    small[limit-1][i]=0
                                    return max1
                                if(n>value):
                                    value=n
                            else:
                                if(n<=max1):
                                    small[limit-1][i]=0
                                    return max1
                                if(n<value):
                                    value=n
                            small[limit-1][i]=0

        return value

    
    elif(turn<sticknum):
        if(limit!=0):
            for i in range(0,9):
                if(small[limit-1][i]==0):
                    small[limit-1][i]=flag
                    n=whowin(small)
                    if(n==-flag):
                        small[limit-1][i]=0
                        continue
                    if(n==flag):
                        small[limit-1][i]=0
                        return -72*flag

                    big=[0,0,0,0,0,0,0,0,0]
                    for j in range(0,9):
                        big[j]=check(small[j])

                    

                    if(big[i]==-flag or big[i]>4):
                        if(big[limit-1]==flag):
                            n=trystick(small,i+1,-flag,turn+1,value)
                            if(flag==-1):
                                if(n>=max1):
                                    small[limit-1][i]=0
                                    return max1
                                if(n>value):
                                    value=n
                            else:
                                if(n<=max1):
                                    small[limit-1][i]=0
                                    return max1
                                if(n<value):
                                    value=n
                    elif(big[i]==0):
                        n=trystick(small,i+1,-flag,turn+1,value)
                        if(flag==-1):
                            if(n>=max1):
                                small[limit-1][i]=0
                                return max1
                            if(n>value):
                                value=n
                        else:
                            if(n<=max1):
                                small[limit-1][i]=0
                                return max1
                            if(n<value):
                                value=n
                    elif(big[i]==flag):
                        for j in range(0,9):
                            if(big[j]==0):
                                n=trystick(small,j+1,-flag,turn+1,value)
                                if(flag==-1):
                                    if(n>=max1):
                                        small[limit-1][i]=0
                                        return max1
                                    if(n>value):
                                        value=n
                                else:
                                    if(n<=max1):
                                        small[limit-1][i]=0
                                        return max1
                                    if(n<value):
                                        value=n
                              
                    small[limit-1][i]=0

        else:
            big=[0,0,0,0,0,0,0,0,0]
            for i in range(0,9):
                big[i]=check(small[i])
            for k in range(1,10):
                if(big[k-1]==0):
                    limit=k
                    for i in range(0,9):
                        if(small[limit-1][i]==0):
                            small[limit-1][i]=flag
                            n=whowin(small)
                            if(n==-flag):
                                small[limit-1][i]=0
                                continue
                            if(n==flag):
                                small[limit-1][i]=0
                                return -72*flag

                            big=[0,0,0,0,0,0,0,0,0]
                            for j in range(0,9):
                                big[j]=check(small[j])

                            if(big[i]==-flag or big[i]>4):
                                if(big[limit-1]==flag):
                                    n=trystick(small,i+1,-flag,turn+1,value)
                                    if(flag==-1):
                                        if(n>=max1):
                                            small[limit-1][i]=0
                                            return max1
                                        if(n>value):
                                            value=n
                                    else:
                                        if(n<=max1):
                                            small[limit-1][i]=0
                                            return max1
                                        if(n<value):
                                            value=n
                            elif(big[i]==0):
                                n=trystick(small,i+1,-flag,turn+1,value)
                                if(flag==-1):
                                    if(n>=max1):
                                        small[limit-1][i]=0
                                        return max1
                                    if(n>value):
                                        value=n
                                else:
                                    if(n<=max1):
                                        small[limit-1][i]=0
                                        return max1
                                    if(n<value):
                                        value=n
                            elif(big[i]==flag):
                                for j in range(0,9):
                                    if(big[j]==0):
                                        n=trystick(small,j+1,-flag,turn+1,value)
                                        if(flag==-1):
                                            if(n>=max1):
                                                small[limit-1][i]=0
                                                return max1
                                            if(n>value):
                                                value=n
                                        else:
                                            if(n<=max1):
                                                small[limit-1][i]=0
                                                return max1
                                            if(n<value):
                                                value=n
                              
                            small[limit-1][i]=0

        return value
                    
                

def decide(small,limit,trynum):
    global sticknum,end
    relimit=limit
    if(trynum<=0):
        return None
    sticknum=trynum
    value=-72
    move=[0,0,0]
    if(limit!=0):
        for i in range(0,9):
            if(small[limit-1][i]==0):
                small[limit-1][i]=-1
                n=whowin(small)
                if(n==1):
                    small[limit-1][i]=0
                    continue
                if(n==-1):
                    small[limit-1][i]=0
                    return [0,limit-1,i]
                
                big=[0,0,0,0,0,0,0,0,0]
                for j in range(0,9):
                    big[j]=check(small[j])
                    
                if(big[i]==1 or big[i]>4):
                    n=trystick(small,0,1,1,value)
                    print(n)
                    if(n>value):
                        value=n
                        move=[0,limit-1,i]
                elif(big[i]==0):
                    n=trystick(small,i+1,1,1,value)
                    print(n)
                    if(n>value):
                        value=n
                        move=[i+1,limit-1,i]
                elif(big[i]==-1):
                    for j in range(0,9):
                        if(big[j]==0):
                            n=trystick(small,j+1,1,1,value)
                            print(n)
                            if(n>value):
                                value=n
                                move=[j+1,limit-1,i]
                small[limit-1][i]=0

    else:
        big=[0,0,0,0,0,0,0,0,0]
        for i in range(0,9):
            big[i]=check(small[i])
        for k in range(1,10):
            if(big[k-1]==0):
                
                limit=k
                for i in range(0,9):
                    if(small[limit-1][i]==0):
                        small[limit-1][i]=-1
                        n=whowin(small)
                        if(n==1):
                            small[limit-1][i]=0
                            continue
                        if(n==-1):
                            small[limit-1][i]=0
                            return [0,limit-1,i]
                
                        big=[0,0,0,0,0,0,0,0,0]
                        for j in range(0,9):
                            big[j]=check(small[j])
                    
                        if(big[i]==1 or big[i]>4):
                            n=trystick(small,0,1,1,value)
                            if(n>value):
                                value=n
                                move=[0,limit-1,i]
                        elif(big[i]==0):
                            n=trystick(small,i+1,1,1,value)
                            if(n>value):
                                value=n
                                move=[i+1,limit-1,i]
                        elif(big[i]==-1):
                            for j in range(0,9):
                                if(big[j]==0):
                                    n=trystick(small,j+1,1,1,value)
                                    if(n>value):
                                        value=n
                                        move=[j+1,limit-1,i]
                        small[limit-1][i]=0

    if(value>-72):
        return move
    else:
        return decide(small,relimit,trynum-1)
        
    
    
    
    

    
