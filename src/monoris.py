from tkinter import *
import time

####################
##### model

class Field:
    width = 10
    height = 20
    def __init__(self):
        u"""リストのリストを作る"""
        self.field = [[0 for i in range(Field.width)] for j in range(Field.height)]

    def is_filled_line(self, i):
        u"""i番目が埋まっているかどうか"""
        for value in self.field[i]:
            if value == 0:
                return False
        return True

    def erase_erasablelines(self):
        u"""消せる行を消去"""
        erasedlines = 0
        i = 0
        while i < len(self.field): # 消去できる行を消して
            if self.is_filled_line(i):
                del self.field[i]
                erasedlines += 1
            else:
                i += 1
        for i in range(erasedlines): # 先頭に空行を補充する
            self.field.insert(0, [0 for i in range(Field.width)])

    def pprint(self):
        u""" pretty printer (fieldデータをテキスト形式に整形して出力)"""
        output = "["
        is_firstline = True
        for line in self.field:
            if is_firstline:
                output += "["
                is_firstline = False
            else :
                output += " ["
            for value in line:
                output += str(value) + ", "
            output = output[:-2]
            output += "],\n"
        output = output[:-2] + "]"
        return output

class Block:
    def __init__(self, x, y, field):
        self.x = x
        self.y = y
        self.field = field

    def toString(self):
        return "position = (" + str(self.x) + ", " + str(self.y) + ")"

    def down(self):
        if self.y < Field.height - 1 and self.field[self.y+1][self.x] == 0:
            self.y += 1
            return True
        return False

    def left(self):
        if self.x != 0 and self.field[self.y][self.x-1] == 0:
            self.x -= 1
            return True
        return False

    def right(self):
        if self.x < Field.width - 1 and self.field[self.y][self.x+1] == 0:
            self.x += 1
            return True
        return False

    def fix(self):
        self.field[self.y][self.x] = 1

field = Field()

def insert_newblock():
    return Block(int(Field.width/2) - 1, 0, field.field)

currentblock = insert_newblock()

####################
##### view

# draw parameters
baseX = 80
baseY = 40
boxsize = 20
rdx = baseX + Field.width * boxsize # right down x
rdy = baseY + Field.height* boxsize # right down y

tk = Tk()
tk.title("monoris : or One Block Tetris")
canvas = Canvas(tk, width=600, height=600)
canvas.pack()

def draw_box(x, y):
    u"""四角形一個を描く"""
    x0, y0 = baseX + x * boxsize, baseY + y * boxsize
    canvas.create_rectangle(x0, y0, x0 + boxsize, y0 + boxsize, fill = "red")

def draw_Field(field):
    u"""固定されたFieldのブロックを描く"""
    for y, line in enumerate(field):
        for x, value in enumerate(line):
            if value == 1:
                draw_box(x, y)

def draw_block(block):
    u"""動いているブロックを描画"""
    draw_box(block.x, block.y)

####################
#### control

## parameters
downdelay = 10 # ブロックの落下遅延

def key_left(ev):
    currentblock.left()

def key_right(ev):
    currentblock.right()

def key_down(ev):
    currentblock.down()

tk.bind('<Left>', key_left)
tk.bind('<Right>', key_right)
tk.bind('<Down>', key_down)

####################
#### main routine
counter = downdelay

while True:
    # model
    if downdelay <= counter:
        down = currentblock.down()
        counter = 0
        if not down:
            currentblock.fix()
            field.erase_erasablelines()
            currentblock = insert_newblock()
    counter += 1

    # view
    canvas.delete("all")
    canvas.create_rectangle(baseX, baseY, rdx, rdy)
    draw_Field(field.field)
    draw_block(currentblock)

    # view for debug
    canvas.create_text(rdx + 100, baseY, text=currentblock.toString(), anchor="nw")
    canvas.create_text(rdx + 100, baseY + 30, text=field.pprint(), anchor="nw")

    #control
    time.sleep(0.05)
    tk.update()
