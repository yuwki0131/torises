from tkinter import *
import time

####################
##### model

# parameters
mapwidth = 10
mapheight = 20

class Field:
    width = 10
    height = 20
    def __init__(self):
        u"""リストのリスト(ブロックが動くフィールド)を作る"""
        self.field = [[0 for i in range(Field.width)]
                      for j in range(Field.height)]

    def is_filled_line(self, i):
        u"""i番目が埋まっているかどうか"""
        for value in self.field[i]:
            if value == 0:
                return False
        return True

    def erase_erasablelines(self):
        u"""消せる行(=並んでいる行)を消去"""
        erasedlines = 0
        i = 0
        while i < len(self.field): # 消去できる行をすべて消して
            if self.is_filled_line(i):
                del self.field[i]
                erasedlines += 1
            else:
                i += 1
        for i in range(erasedlines): # 先頭に空行を補充する
            self.field.insert(0, [0 for i in range(Field.width)])

def clockwise(lss):
    u"""行列(リストのリスト)を時計回りに回転"""
    newlist = list()
    for a in zip(*lss):#     xs, ys, zs = lss; zip(xs, ys, zs)
        ls = list(a)
        ls.reverse()
        newlist.append(ls)
    return newlist

class Block:
    blocksize = 3
    def __init__(self, x, y, field):
        self.x = x
        self.y = y
        self.block = [[0, 1, 0],
                      [0, 1, 0],
                      [0, 0, 0]]
        self.field = field

    def tostring(self):
        position_data = "position = (" + str(self.x) + ", " + str(self.y) + ")"
        block_data = pprint(self.block)
        return position_data + "\n" + block_data

    def turn_clockwise(self):
        u"""ブロックを回転(時計回り)させる"""
        oldblock = self.block
        self.block = clockwise(self.block)
        # 0~1マス移動して回転させられるなら、0~1マス移動
        for (add_x, add_y) in [(0, 0), (1, 0), (0, -1), (-1, 0)]:
            self.x, self.y = (self.x + add_x, self.y + add_y)
            if not self.hit():
                return True
            self.x, self.y = (self.x - add_x, self.y - add_y)
        # 回転失敗
        self.block = oldblock
        return False

    def in_field(self, x, y):
        u"""指定した(x,y)がフィール内"""
        return 0 <= x < Field.width and 0 <= y < Field.height

    def hit(self):
        x0, y0 = self.x, self.y
        for y in range(self.blocksize):
            for x in range(self.blocksize):
                if self.block[y][x] == 1:
                    if not self.in_field(x0 + x, y0 + y):
                        return True # フィールド外
                    if self.field[y0 + y][x0 + x] == 1:
                        return True # フィールド上のブロックと接触
        return False

    def down(self):
        self.y += 1
        if not self.hit():
            return True
        self.y -= 1
        return False

    def left(self):
        self.x -= 1
        if not self.hit():
            return True
        self.x += 1
        return False

    def right(self):
        self.x += 1
        if not self.hit():
            return True
        self.x -= 1
        return False

    def fix(self):
        for y, bline in enumerate(self.block):
            for x, v in enumerate(bline):
                if v == 1:
                    self.field[self.y + y][self.x + x] = 1

field = Field()

def insert_newblock():
    return Block(int(Field.width/2) - 2, 0, field.field)

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
tk.title("doris : or Two Block Tetris")
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
    x0, y0 = block.x, block.y
    for y, line in enumerate(block.block):
        for x, value in enumerate(line):
            if value == 1:
                draw_box(x0 + x, y0 + y)

def pprint(field):
    u""" pretty printer (fieldデータをテキスト形式に整形して出力)"""
    output = "["
    is_firstline = True
    for line in field:
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

Field.pprint = pprint
Block.pprint = pprint

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

def key_up(ev):
    currentblock.turn_clockwise()

tk.bind('<Left>', key_left)
tk.bind('<Right>', key_right)
tk.bind('<Down>', key_down)
tk.bind('<Up>', key_up)

####################
#### main routine
counter = downdelay

while True:
    if downdelay <= counter:
        counter = 0
        # model
        down = currentblock.down()
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
    canvas.create_text(rdx + 100, baseY, text=currentblock.tostring(), anchor="nw")
    canvas.create_text(rdx + 100, baseY + 80, text=pprint(field.field), anchor="nw")

    #control
    time.sleep(0.05)
    tk.update()
