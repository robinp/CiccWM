import winop_w32 as winop

import layout

class Row:

    def __init__(self, winInfo):
        self.winInfo = winInfo

    def getWinInfo(self):
        return self.winInfo

class Column:

    def __init__(self):
        self.rows =  []
        self.act_row = None
        self.layout = layout.DistributingLayout()

    def hasRows(self):
        return len(self.rows) > 0

    def setLayout(self, layout):
        self.layout = layout

    def getActRow(self):
        if self.act_row is None:
            return None
        else:
            return self.rows[self.act_row]

    def detachActRow(self):
        row = self.getActRow()
        if row is not None:
            if self.act_row != 0:
                self.cycleUp()
            self.rows.remove(row)
        return row

    def setWidth(self, w):
        self.width = w
        return self

    def setLeft(self, x):
        self.left = x
        return self

    def getWidth(self):
        return self.width

    def getLeft(self):
        return self.left

    def addRow(self, row):
        if self.act_row is not None:
            self.rows.insert(self.act_row + 1, row)
            self.act_row += 1
        else:
            self.rows.append(row)
            self.act_row = 0

    def cycleUp(self):
        print("cycling up")
        self.act_row = self.getUpRowId_()

    def getUpRowId_(self):
        ret = None
        if self.act_row is not None:
            ret = self.act_row - 1
            if ret == -1:
                ret += len(self.rows)
        return ret

    def cycleDown(self):
        print("cycling down")
        self.act_row = self.getDownRowId_()

    def getDownRowId_(self):
        ret = None
        if self.act_row is not None:
            ret = self.act_row + 1
            if ret == len(self.rows):
                ret -= len(self.rows)
        return ret

    def shiftUp(self):
        print("shifting up")
        up, act = self.getUpRowId_(), self.act_row
        r = self.rows
        # swap
        r[act], r[up] = r[up], r[act]
        self.cycleUp()

    def shiftDown(self):
        print("shifting down")
        down, act = self.getDownRowId_(), self.act_row
        r = self.rows
        # swap
        r[act], r[down] = r[down], r[act]
        self.cycleDown()

    def refreshFocus(self):
        self.rows[self.act_row].getWinInfo().getWin().doFocus()

    def doLayout(self):
        self.layout.doLayout(self.rows, self.act_row, 
                self.getLeft(), self.getWidth())


class Columns:

    def __init__(self):
        self.cols = [Column()]
        self.act_col = 0
        self.resizeCols_()

    def getActCol_(self):
        return self.cols[self.act_col]

    def addAsRow(self, winInfo):
        self.getActCol_().addRow(Row(winInfo))

    def setActColLayout(self, layout):
        self.getActCol_().setLayout(layout)

    def cycleUpActCol(self):
        self.getActCol_().cycleUp()
        self.getActCol_().refreshFocus()
    
    def cycleDownActCol(self):
        self.getActCol_().cycleDown()
        self.getActCol_().refreshFocus()

    def cycleRight(self):
        print "cycling right"
        self.act_col += 1
        if self.act_col >= len(self.cols):
            self.act_col -= len(self.cols)

        self.getActCol_().refreshFocus()

    def cycleLeft(self):
        print "cycling left"
        self.act_col -= 1
        if self.act_col == -1:
            self.act_col += len(self.cols)

        self.getActCol_().refreshFocus()

    def shiftUpActWin(self):
        self.getActCol_().shiftUp()

    def shiftDownActWin(self):
        self.getActCol_().shiftDown()

    def shiftRightActWin(self):
        row = self.getActCol_().detachActRow()
        if row is None:
            return

        rcol = self.getRightCol_()
        rcol.addRow(row)

        ec = self.getEmptyColumn()
        if ec is not None:
            self.cols.remove(ec)
            # compensate shift caused by remove
            # this will be undoed by cycleRight
            self.act_col -= 1
        self.resizeCols_()
        self.cycleRight()

    def shiftLeftActWin(self):
        row = self.getActCol_().detachActRow()
        if row is None:
            return

        lcol = self.getLeftCol_()
        lcol.addRow(row)

        ec = self.getEmptyColumn()
        if ec is not None:
            self.cols.remove(ec)
        self.resizeCols_()
        self.cycleLeft()

    def getEmptyColumn(self):
        empties = filter(lambda c: not c.hasRows(), self.cols)
        if len(empties) > 1:
            raise Exception("more than one empty column!")
        elif len(empties) == 1:
            return empties[0]
        return None

    def getRightCol_(self):
        if self.act_col + 1 == len(self.cols):
            # create new column
            self.cols.append(Column())
        
        return self.cols[self.act_col + 1]

    def getLeftCol_(self):
        if self.act_col == 0:
            # create new column
            self.cols.insert(0, Column())
            # compensate shift
            self.act_col += 1
        
        return self.cols[self.act_col - 1]

    def resizeCols_(self):
        W, _ = winop.Winop().getScreenSize()
        def fib():
            # skip first step
            a, b = 1, 1
            while True:
                yield b
                a, b = b, a + b
        _, props = zip(*(zip(range(len(self.cols)), fib())))

        col_sizes = map(lambda p: int(1.0 * p / sum(props) * W), reversed(props))
        left = 0
        for col, size in zip(self.cols, col_sizes):
            col.setLeft(left).setWidth(size)
            left += size

    def doLayout(self):
        for col in self.cols:
            col.doLayout()

        s = ""
        for col in self.cols:
            s += "|" + str(len(col.rows))
        s += "|"
        print(s)
        
        s = ""
        for col in self.cols:
            s += " " + str(col.act_row)
        print(s)
        
        print(" " * (1 + self.act_col * 2) + "^")

