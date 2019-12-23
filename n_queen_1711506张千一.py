import tkinter as tk
import tkinter.messagebox
import numpy as np
import threading
import time


#判断当前pos是否和已有的state冲突
def conflict(pos, states):
    now_r = len(states)
    now_c = pos
    for i in range(now_r):
        # 判断是否在同一列/斜率为+-1
        if states[i] == now_c or states[i] + i == now_c + now_r or states[i] - i == now_c - now_r:
            return True
    return False


#递归，产生所有情况
def comeup_all(n, states_all):
    # 计数变量
    global count_all
    for j in range(n):
        if not conflict(j, states_all):
            # 不冲突则添加
            states_all.append(j)
            if len(states_all) == n :
                count_all = count_all + 1
                temp = states_all.copy()
                results_all.append(temp)
                states_all.pop()
            else:
                comeup_all(n, states_all)
    if len(states_all) > 0:
        # pop掉，进行下一个求解
        states_all.pop()


#检查点击按钮前是否输入了n以及n是否合法
def check_n():
    try:
        n = int(n_in.get())
        #未输入n便执行
        if len(n_in.get()) == 0:
            tk.messagebox.showinfo(title='tips', message='请先输入n！')
            return
    except:
        tk.messagebox.showinfo(title='tips', message='先输入正确的n！')
        return


#画图（标黄）
def draw(old_list,new_list):


    for i in range(n):
        #覆盖原结果
        canvas_new.create_rectangle(xs[old_list[i]],ys[i],xs[old_list[i]+1],ys[i+1],fill='white')
    #绘制新结果
    for i in range(n):
        canvas_new.create_rectangle(xs[new_list[i]],ys[i],xs[new_list[i]+1],ys[i+1],fill='yellow')


# 确认按钮的响应
def hit1():
    global n
    global canvas_new
    global rec_h,rec_w
    global ys,xs

    check_n()

    # 更改n
    n = int(n_in.get())

    #保存棋盘坐标
    xs=[]
    ys=[]

    # 画矩阵
    rec_h = height - 200
    rec_w = width - 200
    # 画布覆盖
    canvas_new = tk.Canvas(window, bg='white', height=rec_h, width=rec_w)
    canvas_new.place(x=100, y=30, anchor='nw')
    # x
    for i in range(0, rec_h, int(np.ceil(rec_h / n))):
        canvas_new.create_line(2, i+2, rec_w+2 , i+2)
        xs.append(i+2)
    else:
        canvas_new.create_line(2, rec_h, rec_w+2, rec_h)
        xs.append(rec_h)
    # y
    for i in range(0, rec_w, int(np.ceil(rec_w / n))):
        canvas_new.create_line(i+2, 2, i+2, rec_h + 2)
        ys.append(i+2)
    else:
        canvas_new.create_line(rec_w, 2, rec_w, rec_h+2)
        ys.append(rec_w)

    #重置文本框
    t.delete(0.0, 'end')

    #重置求解
    global states_all
    global count_all
    global results_all

    states_all = []
    count_all = 0
    results_all = []

    #重置单线程计数器
    global count_hit2

    count_hit2=-1
    #添加一个线程，进行单步求解
    one_step=threading.Thread(target=comeup_all,args=(n,states_all))
    one_step.start()


# 逐步求解按钮
def hit2():
    global count_hit2

    #未输入n便执行

    check_n()

    # 已逐步求解完所有解
    if count_hit2 == len(results_all)-1:
        tk.messagebox.showinfo(title='tips', message='已逐步求解完所有解，共有%d个！' % (count_all))
        return

    count_hit2=count_hit2+1
    #用flag跳出
    flag=False
    while flag == False:
        try:
            draw(results_all[-1], results_all[count_hit2])
            draw(results_all[count_hit2 - 1], results_all[count_hit2])
            temp = '本次求解为：'
            temp += str(results_all[count_hit2])
            temp += '\n'
            t.insert('end', temp)
            print(results_all[count_hit2])
        except:
            print('waiting')
            time.sleep(0.1)
        else:
            flag = True


# 最终解按钮
def hit3():
    #未输入n便执行

    check_n()

    #print(count_all)
    #print(results_all)
    temp='-'*20
    temp+='\n'
    t.insert('end',temp)
    ill='总输出为：'
    ill+='\n'
    t.insert('end',ill)
    for i in range(len(results_all)):
        #遍历results，输出解
        if i == 0:
            draw(results_all[count_hit2], results_all[i])
        else:
            draw(results_all[i-1], results_all[i])
        canvas.update()
        time.sleep(0.05)
        temp = results_all[i]
        t.insert('end', temp)
        t.insert('end','\n')
    temp='-'*20
    temp+='\n'
    t.insert('end',temp)
    if threading.activeCount() == 1 :
        tk.messagebox.showinfo(title='tips', message='共有%d个解' % (count_all))
    else:
        tk.messagebox.showinfo(title='tips', message='正在求解中，当前已求出%d个解' % (count_all))


def window():
    global n_in
    global canvas
    global window
    global t

    # init窗口
    window = tk.Tk()
    window.title('n_queen')
    window.geometry('%dx%d' % (height, width))

    # 添加画布
    canvas = tk.Canvas(window, bg='white', height=height, width=width)
    canvas.place(x=0, y=0, anchor='nw')

    # 添加输入n的文本框
    n_in = tk.Entry(window, show=None, width=4)
    # 提醒输入n的标签
    l1 = tk.Label(window, text='该问题的n为：', bg='white', font=('Arial', 12), width=20, height=2)
    # 添加绘制原始图片按钮
    b1 = tk.Button(window, text='确认', width=3, height=1, bg='white', font=('Arial', 12), command=hit1)
    # 添加绘制逐渐求解按钮
    b2 = tk.Button(window, text='逐一求解', width=8, height=2, bg='white', font=('Arial', 12), command=hit2)
    # 添加求解最终解按钮
    b3 = tk.Button(window, text='所有解', width=8, height=2, bg='white', font=('Arial', 12), command=hit3)
    #添加文本框
    t = tk.Text(window,height=10,width=45)
    #添加滚动条
    sc = tk.Scrollbar(window)
    #关联文本框和滚动条
    sc.config(command=t.yview)
    t.config(yscrollcommand=sc.set)



    # 排版位置
    l1.place(x=50, y=height - 150, anchor='nw')
    n_in.place(x=240, y=height - 140, anchor='nw')
    b1.place(x=330, y=height - 140, anchor='nw')
    b2.place(x=80, y=height - 80, anchor='nw')
    b3.place(x=200, y=height - 80, anchor='nw')
    t.place(x=400,y=height-150,anchor='nw')
    sc.pack(side='right',fill=tk.Y)

    # loop
    window.mainloop()


if __name__ == '__main__':
    n = 0
    height = 800
    width = 800

    window()






