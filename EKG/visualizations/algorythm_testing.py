from re import X
from tkinter import Y
from model import Model
M = Model()


# Loading data from 0 to 10000 sample
M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
# launching "BaselineECGFilter"
M.apply_algorythm(alg_name="BaselineECGFilter")
# launching "RPeaksDetection"
M.apply_algorythm(alg_name="RPeaksDetection")
# launching "WAVES"
M.apply_algorythm(alg_name="WAVES", algorythm="discreate wavelet transform")
# launching "HRV1"
M.apply_algorythm(alg_name="HRV1")
# launching "DFA"
M.apply_algorythm(alg_name="DFA")
# launching "STSegment"
M.apply_algorythm(alg_name="STSegment")

# launching "HRV2"
M.apply_algorythm(alg_name="HRV2")

M.apply_algorythm(alg_name="HeartClass")


from os import sin, cos


