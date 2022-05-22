import pandas as pd
import numpy as numpy
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go


#-------------------------------------------------------------------------
#ekran 1 ekg, baseline, R, waves

baseline = M.apply_algorythm(alg_name="BaselineECGFilter")
baselineX = np.arange(0, len(baseline), 1)

dataecg = M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
dataecgX = np.arange(0, len(dataecg[0]), 1)

peaksR = M.apply_algorythm(alg_name="RPeaksDetection")



fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dataecgX,
    y=dataecg[0],
    name="Sygnał EKG"       # this sets its legend entry
))


fig.add_trace(go.Scatter(
    x=baselineX,
    y=baseline,
    name="Baseline"
))

fig.add_trace(go.Scatter(
    x=peaksR,
    y=baseline[peaksR],
    name="RPiki",
    mode='markers'
))

fig.update_layout(
    title="Wykres EKG",
    xaxis_title="Numer próbki",
    yaxis_title="Amplituda [µv]",
    legend_title="Legenda",
    template="plotly_dark",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig.update_xaxes(rangeslider_visible=True)

fig.show()



#------------------------
#wawes


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

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=baselineX,
    y=baseline,
    name="Baseline"
))

fig.add_trace(go.Scatter(
    x=waves_R_Peaks,
    y=baseline[waves_R_Peaks],
    name="RPiki",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_S_Peaks,
    y=baseline[waves_S_Peaks],
    name="SPiki",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_QRS_Offsets,
    y=baseline[waves_QRS_Offsets],
    name="QRS offset",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_T_Peaks,
    y=baseline[waves_T_Peaks],
    name="TPiki",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_ECG_T_Offsets,
    y=baseline[waves_ECG_T_Offsets],
    name="T offset",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_P_Peaks,
    y=baseline[waves_P_Peaks],
    name="PPiki",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_Q_Peaks,
    y=baseline[waves_Q_Peaks],
    name="QPiki",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_QRS_Onsets,
    y=baseline[waves_QRS_Onsets],
    name="QRS onset",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_P_Onsets,
    y=baseline[waves_P_Onsets],
    name="P onset",
    mode='markers'
))

fig.add_trace(go.Scatter(
    x=waves_P_Offsets,
    y=baseline[waves_P_Offsets],
    name="P offset",
    mode='markers'
))



fig.update_layout(
    title="Wykres EKG",
    xaxis_title="Numer próbki",
    yaxis_title="Amplituda [µv]",
    legend_title="Legenda",
    template="plotly_dark",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)


fig.update_xaxes(rangeslider_visible=True)

fig.show()

