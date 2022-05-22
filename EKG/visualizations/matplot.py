import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from algorythm_testing import *

#-------------------------------------------------------------------------
#collor palette

button_blue = #008CFF
toggle_on_green = #36B37E
checkbox_on_green = #36B37E
checkbox_off_gray = #9C9C9C
bg_2 = #363636



#-------------------------------------------------------------------------
#ecg plot
dataecg = M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)

plt.style.use('dark_background')
plt.plot(dataecg[0], color="#008CFF")
plt.title("sygnał EKG")
plt.grid(color="#363636")
plt.xlabel("Numer próbki")
plt.ylabel("Amplituda [µv]")
plt.show()


#-------------------------------------------------------------------------
# R peaks

baseline = M.apply_algorythm(alg_name="BaselineECGFilter")
peaksR = M.apply_algorythm(alg_name="RPeaksDetection")

plt.style.use('dark_background')
plt.xlim(0,1000)
plt.ylim(-100, 300)
plt.plot(baseline, color="#008CFF")
plt.plot(peaksR, baseline[peaksR], "x", color="w") # dodać zmienna z t pików oraz z wartościa, piki zaznaczone przez x
plt.title("sygnał z zaznaczonymi R pikami")
plt.grid(color="#363636")
plt.xlabel("Numer próbki")
plt.ylabel("Amplituda [µv]")
plt.show()

#-------------------------------------------------------------------------
#baseline plot ekran 1  part 1

baseline = M.apply_algorythm(alg_name="BaselineECGFilter")

plt.style.use('dark_background')
plt.plot(baseline, color="#008CFF")
plt.title("sygnał baseline")
plt.grid(color="#363636")
plt.xlabel("Numer próbki")
plt.ylabel("Amplituda [µv]")
plt.show()


#-------------------------------------------------------------------
#raw ekg + baseline + RPekas    ekran 1 part 2

dataecg = M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
baseline = M.apply_algorythm(alg_name="BaselineECGFilter")
peaksR = M.apply_algorythm(alg_name="RPeaksDetection")


plt.style.use('dark_background')

fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(left = 0.3, bottom = 0.25)
p, = ax.plot(dataecg[0], color = 'w', label = 'raw')
plt.grid(color="#363636")
plt.xlabel("Numer próbki")
plt.ylabel("Amplituda [µv]")
p1, = ax.plot(baseline, color = '#008CFF', label = 'baseline', visible = False)
p2, = ax.plot(peaksR, baseline[peaksR], "x", color="w", visible = False)

plots = [p, p1, p2]
activated = [True, False, False]
labels = ['raw', 'baseline', 'RPeaks']

#instance axes
ax_check = plt.axes([0.03, 0.5, 0.15, 0.15]) #x,y pos/ width, height
ax_slider = plt.axes([0.3, 0.05, 0.5, 0.1])

#instance button
plot_button = CheckButtons(ax_check, labels, activated )
plot_slider = RangeSlider(ax_slider, valmin=0, valmax=len(baseline), valinit=(0, len(baseline)), label='zakres', color="#008CFF")
 
#display/hide plots
def show_plot(label):
    index = labels.index(label)
    plots[index].set_visible(not plots[index].get_visible())
    fig.canvas.draw()

def window_size(val):
    ax.set_xlim(val[0], val[1])


plot_button.on_clicked(show_plot) 
plot_slider.on_changed(window_size)
plt.grid()
plt.show()


#--------------------------------------------------------------
#  waves  okno 1   part 3



baseline = M.apply_algorythm(alg_name="BaselineECGFilter")
baselineX = np.arange(0, len(baseline), 1)

waves = M.apply_algorythm(alg_name="WAVES", algorythm="derivatives")

waves_R_Peaks = waves['ECG_R_Peaks']
waves_S_Peaks = waves['ECG_S_Peaks']
waves_QRS_Offsets = waves['ECG_QRS_Offsets']
waves_T_Peaks = waves['ECG_T_Peaks']
waves_ECG_T_Offsets = waves['ECG_T_Offsets']
waves_P_Peaks = waves['ECG_P_Peaks']
waves_Q_Peaks = waves['ECG_Q_Peaks']
waves_QRS_Onsets = waves['ECG_QRS_Onsets']
waves_P_Onsets = waves['ECG_P_Onsets']
waves_P_Offsets = waves['ECG_P_Offsets']


plt.style.use('dark_background')

fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(left = 0.3, bottom = 0.25)
p, = ax.plot(baseline, color = '#008CFF', label = 'baseline')
p1, = ax.plot(waves_R_Peaks, baseline[waves_R_Peaks], "x")
p2, = ax.plot(waves_S_Peaks, baseline[waves_S_Peaks], "x")
p3, = ax.plot(waves_QRS_Offsets, baseline[waves_QRS_Offsets], "x")
p4, = ax.plot(waves_T_Peaks, baseline[waves_T_Peaks], "x")
p5, = ax.plot(waves_ECG_T_Offsets, baseline[waves_ECG_T_Offsets], "x")
p6, = ax.plot(waves_P_Peaks, baseline[waves_P_Peaks], "x")
p7, = ax.plot(waves_Q_Peaks, baseline[waves_Q_Peaks], "x")
p8, = ax.plot(waves_QRS_Onsets, baseline[waves_QRS_Onsets], "x")
p9, = ax.plot(waves_P_Onsets, baseline[waves_P_Onsets], "x")
p10, = ax.plot(waves_P_Offsets, baseline[waves_P_Offsets], "x")

plots = [p, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
activated = [True, True, True, True, True, True, True, True, True, True]
labels = ['baseline', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

#instance axes
ax_check = plt.axes([0.03, 0.5, 0.15, 0.4]) #x,y pos/ width, height
ax_slider = plt.axes([0.3, 0.05, 0.5, 0.1])

#instance button
plot_button = CheckButtons(ax_check, labels, activated )
plot_slider = RangeSlider(ax_slider, valmin=0, valmax=len(baseline), valinit=(0, len(baseline)), label='zakres', color="#008CFF")
 
#display/hide plots
def show_plot(label):
    index = labels.index(label)
    plots[index].set_visible(not plots[index].get_visible())
    fig.canvas.draw()

def window_size(val):
    ax.set_xlim(val[0], val[1])


plot_button.on_clicked(show_plot) 
plot_slider.on_changed(window_size)
plt.grid(color="#363636")
plt.xlabel("Numer próbki")
plt.ylabel("Amplituda [µv]")
plt.show()

#-------------------------------------------------------------------------
#HRV1 ekran 2  part 1

hrv1 = M.apply_algorythm(alg_name="HRV1") 
print(hrv1)

plt.figure()
plt.plot(f, pxx)
plt.yscale("log")
plt.xscale("log")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Moc widma [ms^2]")
plt.show()



#-------------------------------------------------------------------------
#HRV2 ekran 2  part 2







#-------------------------------------------------------------------------
#DFA ekran 2  part 3

dfa = M.apply_algorythm(alg_name="DFA")
plt.style.use('dark_background')

fluct = dfa['alpha_1']['Fluctuations']
fluctfit = dfa['alpha_1']['Fluct_poly']
scales = dfa['alpha_1']['Windows']
alpha = dfa['alpha_1']['Alpha']


alpha2 = dfa['alpha_2']['Alpha']
fluct2 = dfa['alpha_2']['Fluctuations']
fluctfit2 = dfa['alpha_2']['Fluct_poly']
scales2 = dfa['alpha_2']['Windows']

plt.style.use('dark_background')
plt.loglog(scales, fluct, 'bo')
plt.loglog(scales2, fluct2, 'bo')
plt.loglog(scales, fluctfit, 'r', label=r'$\alpha_1$ = %0.2f'%alpha, color="")
plt.loglog(scales2, fluctfit2, 'r', label=r'$\alpha_2$ = %0.2f'%alpha2, color="")
plt.title('DFA')
plt.xlabel(r'$\log{10}$(n)')
plt.ylabel(r'$\log{10}$(F(n))')
plt.legend()
plt.show()


#----------------------------------------------------------------
#ST segment ekran 3  part 1

stSegment = M.apply_algorythm(alg_name="STSegment")
stSegments = stSegment['st_data']
stSegmentsStart = stSegments['start']
stSegmentsStop = stSegments['end']
print(stSegmentsStart)
print(stSegmentsStop)

#----------------------------------------------------------------
#Heart Class ekran 3  part 2