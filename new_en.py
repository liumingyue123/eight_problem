#coding:utf-8
import numpy as np
import copy as cp

depth = 0 #深度，全局变量
ID = 0 #当前的id，全局变量
Target=np.array([[1,2,3],[8,0,4],[7,6,5]])
node_all = []#存所有的结点
open = [] #存编号
closed = []

def posnum(arr1,num):#定位某数字的位置，返回横纵坐标
    (x,y)=arr1.shape
    for i in range(x):
        for j in range(y):
            if arr1[i][j]==num:
                return i,j

def getabdis(arr1,arr2):#获取绝对距离，p(n)
    (x,y)=arr2.shape
    p_num=0
    for i in range(x):
        for j in range(y):
            a=(posnum(arr1,arr2[i][j]))[0]
            b=(posnum(arr1,arr2[i][j]))[1]
            p_num=abs(a-i)+abs(b-j)
    return p_num

def get_s(arr1,arr2):#s(n)
    (x,y)=arr1.shape
    s_num=0
    for i in range(x):
        for j in range(y):
            a1=posnum(arr1,(arr1[i][j]+1)%8)[0]
            a2=posnum(arr1,(arr1[i][j]+1)%8)[1]
            b1=posnum(arr2,(arr1[i][j]+1)%8)[0]
            b2=posnum(arr2,(arr1[i][j]+1)%8)[1]
            if (abs(a1-b1)+abs(a2-b2))!=1 and i!=1 and j!=1:
                s_num=s_num+2
            elif i==1 and j==1:
                s_num=s_num+1
    return s_num

def redirect(S):#返回值1代表已出现结点，0代表未出现结点，需要将之加入表中
    for i in range(len(open)):
        if np.all(node_all[open[i]].array==S.array):
            if node_all[open[i]].f>S.f:
                node_all[open[i]].parentid=S.parentid
        return 1
    for i in range(len(closed)):
        if np.all(node_all[closed[i]].array==S.array):
            if node_all[closed[i]].f>S.f:
                node_all[open[i]].parentid = S.parentid
                for j in range(len(S.child)):   #对closed表中结点则需要对其子结点也判断是否需要重定向
                    if node_all[S.child].d>S.d+1:   #此时重定向与否由深度决定
                        node_all[S.child].parentid = S.id
                return 1
    return 0


class node:
    def __init__(self , n , array , state , id , parentid , d,  p, s):
        self.array = array
        self.n = n  #矩阵格式,如3*3,则n=3
        self.state = state
        self.id = id
        self.parentid = parentid
        self.d = d
        self.p=p
        self.s=s
        self.f = self.d + self.p+3*self.s
        self.child=[]

    def loczero(self):
        #找到0的位置，返回其位置，第i行第j列
        b = np.where(self.array == 0)
        i = int(b[0])
        j = int(b[1])
        return i,j

    def right(self,i,j):
        #将空格右移，并产生子节点

        Right=cp.deepcopy(self)
        Right.array[i,j],Right.array[i,j+1]=Right.array[i,j+1],Right.array[i,j]#空格右移
        return Right


    def left(self,i,j):
        #将空格左移，并产生子节点

        Left = cp.deepcopy(self)
        Left.array[i, j-1], Left.array[i, j] = Left.array[i, j], Left.array[i, j-1]  # 空格左移
        return Left

    def up(self,i,j):
        #将空格上移移，并产生子节点

        Up = cp.deepcopy(self)
        Up.array[i-1, j], Up.array[i, j] = Up.array[i, j], Up.array[i-1, j]  # 空格上移移
        return Up



    def down(self,i,j):
        #将空格下移，并产生子节点

        Down = cp.deepcopy(self)
        Down.array[i+1, j], Down.array[i, j] = Down.array[i, j], Down.array[i+1, j]  # 空格右移
        return Down

    def Judge_Same(self,Node):#判断空格移动后产生的结点是否与已产生的结点相同,若相同则返回0

        if np.all(Node.array == node_all[self.parentid].array):  # 判断是否与已产生的节点相同
                return 0
        else:  #补全除ID外的信息
            Node.d = self.d+1
            Node.p = getabdis(Node.array, Target)
            Node.s = get_s(Node.array, Target)
            Node.f = Node.d + Node.p+3*Node.s
            Node.parentid=self.id
            Node.child=[]
        return Node

    def extend(self,Node):#扩展结点(补全ID，并将之添加进入结点表中)
        global ID
        Node = self.Judge_Same(Node)
        if Node != 0:  # 若能扩展且之前未出现过则扩展(移动)
            if redirect(Node) == 0:
                ID += 1
                Node.id = ID
                node_all.append(Node)
                open.append(Node.id)
                self.child.append(Node.id)

    def move(self):
        #根据locatezero判断出0的位置，然后根据0的位置，判断出可以移动的方向，然后分别调用对应的方向函数
        global ID
        i,j=self.loczero()
        if j!=0:
            #print("left")
            Left=self.left(i,j)
            self.extend(Left)
        if i!=0:
            #print("up")
            Up=self.up(i,j)
            self.extend(Up)
        if j!=self.n-1:
            #print("right")
            Right=self.right(i,j)
            self.extend(Right)
        if i!=self.n-1:
            #print("down")
            Down=self.down(i,j)
            self.extend(Down)


if __name__ == "__main__":
    #读入两个array
    arr1 = np.array([[1,2,3],[0,8,4],[7,6,5]])

    S = node(3 , array=arr1 , state=0 , id=ID , parentid=-1 , d = depth , p=getabdis(arr1,Target), s=get_s(arr1,Target))
    open.append(S.id)
    node_all.append(S)
    next_S=0
    List=[]#成功后的推导序列,存ID

    while 1:
        if len(open)==0:    #open表空，失败
            print("fail")
            break

        minf=65525  #选取open表中f值最小的结点
        next_S=0
        for i in range(len(open)):
            if node_all[open[i]].f<minf:
                minf=node_all[open[i]].f
                next_S=open[i]    #获取ID
        open.remove(node_all[next_S].id)
        closed.append(node_all[next_S].id)#将f值最小的结点放入closed表
        if (np.all(node_all[next_S].array==Target)):
            print("Success")
            break

        S=node_all[next_S]
        S.move()     #扩展结点
        print(S.array)
        #print(S.id)
    while node_all[next_S].id!=0:
        List.append(node_all[next_S].id)
        next_S=node_all[next_S].parentid
    List.reverse()
    print(arr1)

    for i in range(len(List)):
        print("下一步")
        print(node_all[List[i]].array)
