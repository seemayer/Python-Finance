import finplot as fplt
from PyQt5.QtWidgets import QWidget,QGridLayout,QComboBox
import inspect
from pprint import pprint as pp

def create_ctrl_panel(win):
    panel = QWidget(win)
    panel.move(100, 0)
    win.scene().addWidget(panel)
    layout = QGridLayout(panel)

    panel.symbol = QComboBox(panel)
    [panel.symbol.addItem(i+'.L') for i in '888 ASCL ABF'.split()]
    panel.symbol.setCurrentIndex(1)
    layout.addWidget(panel.symbol, 0, 0)
    # panel.symbol.currentTextChanged.connect(change_asset)

    return panel

class control_panel(QWidget):
    def __init__(self, parent):
        super(control_panel, self).__init__(parent)
        self.move(100, 0)
        
        # layout = QGridLayout(panel)
        
        
        # parent.scene().addWidget(self)

    
        # self.move(100, 0)
        
        # panel = QWidget(win)
        # panel.move(100, 0)
        # win.scene().addWidget(panel)
        # layout = QGridLayout(panel)


# df = yfinance.download('AAPL', period = '1y')
ax = fplt.create_plot('Simple Control Panel Example')

win = ax.vb.win
ctrl_panel = create_ctrl_panel(win)
# cpanel = control_panel(win)
# win.scene().addWidget(cpanel)


# pp(inspect.getclasstree(inspect.getmro(mypanel)))
# pp(dir(ax))
# print(mypanel.__bases__)


# fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
# fplt.show()

# class CheckBoxList(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.window_width, self.window_height = 600,200
#         self.setMinimumSize(self.window_width, self.window_height)

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         self.checkBoxAll = QCheckBox('Select All')
#         self.checkBoxAll.setChecked(False)
#         self.checkBoxAll.stateChanged.connect(self.on_stateChanged)
#         layout.addWidget(self.checkBoxAll)

#         self.checkBoxA = QCheckBox('Select A')
#         self.checkBoxB = QCheckBox('Select B')
#         self.checkBoxC = QCheckBox('Select C')

#         self.checkBoxes = [self.checkBoxA, self.checkBoxB, self.checkBoxC]
#         for checkBox in self.checkBoxes:
#             layout.addWidget(checkBox)

#     def on_stateChanged(self, state):
#         for CheckBox in self.checkBoxes:
#             CheckBox.setCheckState(state)