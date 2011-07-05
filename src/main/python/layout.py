import winop_w32 as winop

class DistributingLayout:

    def doLayout(self, rows, active_idx, left, width): 

        total_w, total_h = winop.Winop().getScreenSize()
        last_y = 0

        for idx, row in enumerate(rows):
            win = row.getWinInfo().getWin()
            height = int(total_h / len(rows))
            win.prepareSize((width, height))
            win.preparePos((left, last_y))
            win.applyOps()

            last_y = last_y + height

class MaxingLayout:

    def doLayout(self, rows, active_idx, left, width):
        total_w, total_h = winop.Winop().getScreenSize()
        act_row = rows[active_idx]
        win = act_row.getWinInfo().getWin()
        
        win.prepareSize((width, total_h))
        win.preparePos((left, 0))
        win.applyOps()
