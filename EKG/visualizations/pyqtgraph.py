import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np



#----------------------------------------------------------------------------------
#basic ECG
dataecg = M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
sizeX = np.arange(0, len(dataecg[0]), 1)


app =QApplication(sys.argv)
pg.plot(x = sizeX, y = dataecg[0])
status = app.exec_()
sys.exit(status)



#------------------------------------------------------------------------------------
#baseline

baseline = M.apply_algorythm(alg_name="BaselineECGFilter")

app =QApplication(sys.argv)
pg.plot(baseline)
status = app.exec_()
sys.exit(status)

#------------------------------------------------------------------------------------
#dataecg + baseline na jednym

dataecg = M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
sizeX = np.arange(0, len(dataecg[0]), 1)
baseline = M.apply_algorythm(alg_name="BaselineECGFilter")


app = QApplication(sys.argv)
win = pg.plot(title = "wykres")

dataecgPlot = win.plot(x = sizeX, y = dataecg[0], pen ="white")
baselinePlot = win.plot(baseline, pen='blue')

status = app.exec_()
sys.exit(status)


#------------------------------------------------------------------------------------
#Rpeaks

peaksR = M.apply_algorythm(alg_name="RPeaksDetection")
baseline = M.apply_algorythm(alg_name="BaselineECGFilter")


app = QApplication(sys.argv)
win = pg.plot(title = "wykres")

peaksR = win.plot(peaksR, baseline[peaksR], pen=None, symbol='t')
baselinePlot = win.plot(baseline, pen='blue')

status = app.exec_()
sys.exit(status)

#-------------------------------------------------------------------------------------
#wszystko na 1

peaksR = M.apply_algorythm(alg_name="RPeaksDetection")
baseline = M.apply_algorythm(alg_name="BaselineECGFilter")
dataecg = M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
sizeX = np.arange(0, len(dataecg[0]), 1)

app = QApplication(sys.argv)
win = pg.plot(title = "wykres")

peaksR = win.plot(peaksR, baseline[peaksR], pen=None, symbol='t')
baselinePlot = win.plot(baseline, pen='blue')
dataecgPlot = win.plot(x = sizeX, y = dataecg[0], pen ="green")

status = app.exec_()
sys.exit(status)
