from threading import Thread
from model import Model
import numpy as np
import dash
import plotly.graph_objects as go
import dash.html as html
import dash.dcc as dcc
from enum import Enum
import pandas as pd 
import plotly.express as px
from numpy import pi, sin, cos
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngineWidgets import QWebEngineView




HTTP_PORT = 9999
INTERVAL = 2 #update interval (s)

class PlotTypes(Enum):
    DEFAULT = 1
    BASELINE = 2
    RPEAKS = 3
    WAVES = 4
    WAVES_DISCRETE = 5
    HRV_1 = 6
    HRV_2 = 7
    HRV_2_HISTOGRAM = 8
    DFA = 9
    ST_SEGMENT = 10
    HEARTCLASS = 11
    HEARTCLASS_HISTOGRAM = 12

        
class PlotComponent():
    types = PlotTypes
    def __init__(self, port = HTTP_PORT):
        """ Initialization. """
        super().__init__()
        self.port = port
        self.fs = 360
        self.start_server()
        self.choosePlot(self.types.DEFAULT)
        


    def start_server(self):
        """ Calling that method will result in listening of server at port HTTP_PORT. """
        self.thread = Thread(target=self._thread_target, daemon=True)
        self.thread.start()       
        

    def choosePlot(self, plot_type, ):
        if plot_type not in PlotTypes:
            raise Exception('type does not exist')
        self.showingPlot = plot_type
   
        if self.showingPlot == PlotTypes.BASELINE:
            self.baseline()
        elif self.showingPlot == PlotTypes.DFA:
            self.dfa()
        elif self.showingPlot == PlotTypes.HRV_1:
            self.hrv1()
        elif self.showingPlot == PlotTypes.HRV_2:
            self.hrv2()
        elif self.showingPlot == PlotTypes.HRV_2_HISTOGRAM:
            self.hrv2_histogram()
        elif self.showingPlot == PlotTypes.RPEAKS:
            self.Rpeaks()
        elif self.showingPlot == PlotTypes.WAVES:
            self.waves()
        elif self.showingPlot == PlotTypes.WAVES_DISCRETE:
            self.waves_discrete()
        elif self.showingPlot == PlotTypes.HEARTCLASS:
            self.heartClass()
        elif self.showingPlot == PlotTypes.HEARTCLASS_HISTOGRAM:
            self.heartClass_histogram()
        elif self.showingPlot == PlotTypes.ST_SEGMENT:
            self.stSegment()
        elif self.showingPlot == PlotTypes.DEFAULT:
            self.ecgPlot(None)



    def first_render(self):
        self.app = dash.Dash()
        fig = go.Figure()
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])

        self.app.run_server(port = self.port)


    def _thread_target(self):
        self.first_render()
        
        
    def ecgPlot(self, dataecg):
        
        # dataecg = self.M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
        if dataecg is None:
            dataecg = np.zeros((1,100))
        dataecgX = np.arange(0, len(dataecg[0]), 1)
        
        dataecgx = dataecgX /self.fs

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dataecgx,
            y=dataecg[0],
            line=dict(color="#008CFF"),
            name="Ecg signal"# this sets its legend entry
            
        ))
        
        fig.update_layout(
            xaxis_title="Time [s]",
            yaxis_title="Amplitude [µv]",
            yaxis=dict(zeroline=False),
            showlegend=True,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C"
            )
        )

        fig.update_xaxes(rangeslider_visible=True)
        
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
        
        
    def baseline(self, baseline):
    
        baselineX = np.arange(0, len(baseline), 1)
        baselinex = baselineX / self.fs

        boarder_top = max(baseline)
        boarder_bot = min(baseline)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=baselinex,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))
        
        
        fig.update_layout(
            xaxis_title="Time [s]",
            yaxis_title="Amplitude [µv]",
            showlegend=True,
            yaxis=dict(zeroline=False),
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C"
            )
        )
        
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[boarder_bot, boarder_top])
        
        print("Update baseline graph")
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
        
        
    def Rpeaks(self, baseline, peaksR):
    
        baselineX = np.arange(0, len(baseline), 1)
        baselinex = baselineX / self.fs
        peaksRx = peaksR / self.fs
        boarder_top = max(baseline)
        boarder_bot = min(baseline)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=baselinex,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))
        
        fig.add_trace(go.Scatter(
            x=peaksRx,
            y=baseline[peaksR],
            name="R Peaks",
            mode='markers',
            marker=dict(color="#36B37E")
        ))
        
        fig.update_layout(
            xaxis_title="Time [s]",
            yaxis_title="Amplitude [µv]",
            showlegend=True,
            yaxis=dict(zeroline=False),
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C")
        )
        
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[boarder_bot, boarder_top])

        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
        
        
    def waves(self, baseline, waves):
        
        baselineX = np.arange(0, len(baseline), 1)
        baselinex = baselineX / self.fs
        
        boarder_top = max(baseline)
        boarder_bot = min(baseline)

        waves_R_Peaks = waves['ECG_R_Peaks'] 
        waves_S_Peaks = waves['ECG_S_Peaks'] 
        waves_QRS_offsets = waves['ECG_QRS_Offsets'] 
        waves_T_Peaks = waves['ECG_T_Peaks'] 
        waves_ECG_T_offsets = waves['ECG_T_Offsets'] 
        waves_P_Peaks = waves['ECG_P_Peaks'] 
        waves_Q_Peaks = waves['ECG_Q_Peaks'] 
        waves_QRS_Onsets = waves['ECG_QRS_Onsets'] 
        waves_P_Onsets = waves['ECG_P_Onsets'] 
        waves_P_offsets = waves['ECG_P_Offsets'] 
        

        

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=baselinex,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))

        fig.add_trace(go.Scatter(
            x=waves_R_Peaks / self.fs,
            y=baseline[waves_R_Peaks],
            name="R peaks",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_S_Peaks / self.fs,
            y=baseline[waves_S_Peaks],
            name="S peaks",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_QRS_offsets / self.fs,
            y=baseline[waves_QRS_offsets],
            name="QRS ofet",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_T_Peaks / self.fs,
            y=baseline[waves_T_Peaks],
            name="T peaks",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_ECG_T_offsets / self.fs,
            y=baseline[waves_ECG_T_offsets],
            name="T offset",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_P_Peaks / self.fs,
            y=baseline[waves_P_Peaks],
            name="P peaks",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_Q_Peaks / self.fs,
            y=baseline[waves_Q_Peaks],
            name="Q peaks",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_QRS_Onsets / self.fs,
            y=baseline[waves_QRS_Onsets],
            name="QRS onset",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_P_Onsets / self.fs,
            y=baseline[waves_P_Onsets],
            name="P onset",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_P_offsets / self.fs,
            y=baseline[waves_P_offsets],
            name="P offset",
            mode='markers'
        ))
        
        
        fig.update_layout(
            xaxis_title="Time [s]",
            yaxis_title="Amplitude [µv]",
            legend_title="Legend",
            paper_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C")
        )
        
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[boarder_bot, boarder_top])
        
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
 
 
    def waves_discrete(self, baseline, waves):
        
        baselineX = np.arange(0, len(baseline), 1)
        baselinex = baselineX / self.fs
        
        boarder_top = max(baseline)
        boarder_bot = min(baseline)

        waves_QRS_offsets = waves['ECG_QRS_Offsets'] 
        waves_ECG_T_offsets = waves['ECG_T_Offsets'] 
        waves_QRS_Onsets = waves['ECG_QRS_Onsets'] 
        waves_P_Onsets = waves['ECG_P_Onsets'] 
        waves_P_offsets = waves['ECG_P_Offsets'] 


        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=baselinex,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))


        fig.add_trace(go.Scatter(
            x=waves_QRS_offsets / self.fs,
            y=baseline[waves_QRS_offsets],
            name="QRS ofet",
            mode='markers'
        ))


        fig.add_trace(go.Scatter(
            x=waves_ECG_T_offsets / self.fs,
            y=baseline[waves_ECG_T_offsets],
            name="T ofet",
            mode='markers'
        ))


        fig.add_trace(go.Scatter(
            x=waves_QRS_Onsets / self.fs,
            y=baseline[waves_QRS_Onsets],
            name="QRS onset",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_P_Onsets / self.fs,
            y=baseline[waves_P_Onsets],
            name="P onset",
            mode='markers'
        ))

        fig.add_trace(go.Scatter(
            x=waves_P_offsets / self.fs,
            y=baseline[waves_P_offsets],
            name="P ofet",
            mode='markers'
        ))


        fig.update_layout(
            xaxis_title="Time [s]",
            yaxis_title="Amplitude [µv]",
            legend_title="Legend",
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C")
        )


        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[boarder_bot, boarder_top])
 
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
 
 

    def hrv1(self, hrv1_all):

        
        hrv1_frequency_parameters = hrv1_all.get('frequency_parameters')
        hrv1 = hrv1_frequency_parameters.get('psd_chart')
        f = hrv1[0]
        pxx = hrv1[1]
        
        hf = [0.4]
        lf = [0.15]
        vlf = [0.04]
        ulf = [0.003]
        a = [hf, lf, vlf, ulf]
        y = [1]
        

        fig = go.Figure()
        
        
        fig.add_trace(go.Scatter(
            x=f,
            y=pxx,
            line=dict(color="#008CFF"),
            name="hrv1"
        ))
        
        fig.add_vline(x=0.4, line_width=3, line_dash="dash", line_color="#36B37E", name="hf")
        fig.add_vline(x=0.15, line_width=3, line_dash="dash", line_color="#36B37E", name="lf")
        fig.add_vline(x=0.04, line_width=3, line_dash="dash", line_color="#36B37E", name="vlf")
        fig.add_vline(x=0.003, line_width=3, line_dash="dash", line_color="#36B37E", name="ulf")
        
        fig.add_trace(go.Scatter(
            x=hf,
            y=y,
            name="hf (0.4)",
            mode='markers',
            marker=dict(color="#36B37E")
        ))

        fig.add_trace(go.Scatter(
            x=lf,
            y=y,
            name="lf (0.15)",
            mode='markers',
            marker=dict(color="#36B37E")
        ))
        fig.add_trace(go.Scatter(
            x=vlf,
            y=y,
            name="vlf (0.04)",
            mode='markers',
            marker=dict(color="#36B37E")
        ))
        fig.add_trace(go.Scatter(
            x=ulf,
            y=y,
            name="ulf (0.003)",
            mode='markers',
            marker=dict(color="#36B37E")
        ))
                
        
        fig.update_layout(
            xaxis_title="Frequency [Hz]",
            yaxis_title="Frequency spectrum [ms^2]",
            showlegend=True,
            paper_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C")
        )
        
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
        self.hrv1_plot = fig
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
   
  
    def hrv2(self, hrv2):
    
        poincare = hrv2.get('Poincare')
        rri = poincare.get('RRi')
        rri1 = poincare.get('RRi1')


        elipse = hrv2.get('Pincare_par')
        x_center = elipse.get('xpoint')
        y_center = elipse.get('ypoint')
        sd1 = float(elipse.get('SD1'))
        sd2 = float(elipse.get('Sd2'))
        angle = elipse.get('angle')


        def ellipse(x_center=0, y_center=0, ax1 = [1, 0],  ax2 = [0,1], a=1, b =1,  N=100):

            t = np.linspace(0, 2*pi, N)
            
            xs = a * cos(t)
            ys = b * sin(t)
            R = np.array([ax1, ax2]).T
            xp, yp = np.dot(R, [xs, ys])
            x = xp + x_center 
            y = yp + y_center
            return x, y

        x, y = ellipse(x_center=x_center, y_center=y_center, 
                        ax1 =[cos(pi/6), sin(pi/6)],  ax2=[-sin(pi/6),cos(pi/6)],
                        a=sd1, b =sd2)



        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=rri,
            y=rri1,
            name="poincare ",
            mode='markers',
            marker=dict(color="#008CFF")
            
        ))

        fig.add_scatter(
                    x=x,
                    y=y,
                    mode = 'lines',
                    line=dict(color="#36B37E")
        )

        fig.update_layout(
            xaxis_title="Time [s] [ms]",
            yaxis_title="Time [s] [ms]",
            showlegend=True,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C"
            )
        )
        self.hrv2_eclipse_plot = fig
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
    

    def hrv2_histogram(self, hrv2):

        hrv2_h = hrv2.get("Histogram")
        hrv2_x = hrv2_h.get('data')
        hrv2_y = hrv2_h.get('bins')
        begin_xy = hrv2_h.get('begin_xy')
        end_xy = hrv2_h.get('end_xy')
        top_xy = hrv2_h.get('top_xy')

        x = []
        x.append(begin_xy[0])
        x.append(top_xy[0])
        x.append(end_xy[0])

        y = []
        y.append(begin_xy[1])
        y.append(top_xy[1])
        y.append(end_xy[1])
        
        fig = go.Figure()

        fig.add_trace(go.Histogram(
                    x=hrv2_x,
                    nbinsx=hrv2_y,
                    name="histogram",
                    marker_color="#008CFF"
                ))

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            name="triangle",
            line=dict(color="#36B37E"),
        ))



        fig.update_layout(
            showlegend=True,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            yaxis=dict(zeroline=False),
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C"
            )
        )
        self.hrv2_histogram_plot = fig
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])


    def dfa(self, dfa):
        
        fig = go.Figure()
        
        fluct = dfa['alpha_1']['Fluctuations']
        fluctfit = dfa['alpha_1']['Fluct_poly']
        scales = dfa['alpha_1']['Windows']
        alpha = dfa['alpha_1']['Alpha']


        alpha2 = dfa['alpha_2']['Alpha']
        fluct2 = dfa['alpha_2']['Fluctuations']
        fluctfit2 = dfa['alpha_2']['Fluct_poly']
        scales2 = dfa['alpha_2']['Windows']
        
        
        fig.add_trace(go.Scatter(
            x=scales,
            y=fluct,
            mode='markers',
            marker=dict(color="#5900b3")     
        ))
        
        fig.add_trace(go.Scatter(
            x=scales2,
            y=fluct2,
            mode='markers',
            marker=dict(color="#cc0099")
        ))
        
        fig.add_trace(go.Scatter(
            x=scales,
            y=fluctfit,
            line=dict(color="#008CFF"),
            name=r'$\alpha_1$ = %0.2f'%alpha       # this sets its legend entry
        ))
        
        fig.add_trace(go.Scatter(
            x=scales2,
            y=fluctfit2,
            line=dict(color="#36B37E"),
            name=r'$\alpha_2$ = %0.2f'%alpha2       # this sets its legend entry
        ))
        
        
        
        fig.update_layout(
            xaxis_title="log 10(n)",
            yaxis_title="log 10(F(n))",
            showlegend=True,
            paper_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C")
        )
        
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
        self.dfa_plot = fig
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
           
   
    def heartClass(self, ht_all):
        
        ht = ht_all.get('morphology_vectors')
        sv = ht.get('Supraventricular')
        v = ht.get('Ventricular')
        u = ht.get('Unclassifiable')

        X_1 = [first for [first, second, third] in sv]
        Y_1 = [second for [first, second, third] in sv]
        Z_1 = [third for [first, second, third] in sv]

        X_2 = [first for [first, second, third] in v]
        Y_2 = [second for [first, second, third] in v]
        Z_2 = [third for [first, second, third] in v]

        X_3 = [first for [first, second, third] in u]
        Y_3 = [second for [first, second, third] in u]
        Z_3 = [third for [first, second, third] in u]

        X = X_1 + X_2 + X_3
        Y = Y_1 + Y_2 + Y_3
        Z = Z_1 + Z_2 + Z_3

        color_1 = ['Supraventricular'] * len(X_1)
        color_2 = ['Ventricular'] * len(X_2)
        color_3 = ['Unclassifiable'] * len(X_3)
        color = color_1 + color_2 + color_3

        df = pd.DataFrame(list(zip(X, Y, Z, color)), columns =['ratio shape', 'ratio velocity', 'number of samples 40','Legend'])
        
        fig = px.scatter_3d(
            df,
            x='ratio shape',
            y='ratio velocity', 
            z='number of samples 40',
            color='Legend',
            template = 'plotly_dark'
        )

        fig.update_layout(
            showlegend=True,
            paper_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C")
        )
        self.heartclass_plot = fig
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = False ), 
        ])
        
        
    def heartClass_histogram(self, ht_all):
        
        count = ht_all.get('morphology_count')
        sv = count.get('Supraventricular')
        v = count.get('Ventricular')
        u = count.get('Unclassifiable')

        hist = []
        names = ['Supraventricular', 'Ventricular', 'Unclassifiable']
        hist.append(sv)
        hist.append(v)
        hist.append(u)



        fig = go.Figure()
        fig.add_trace(go.Bar(x=names, 
                            y=hist,
                            marker_color="#008CFF",
        ))

        fig.update_layout(
            showlegend=True,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#515151",
            yaxis=dict(zeroline=False),
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C"
            )
        )
        self.heartclass_histogram_plot = fig
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
        
        
    def stSegment(self, baseline, st):
        

        stSegment = st.get('st_data') 
        stStart = stSegment.get('start') 
        stEnd = stSegment.get('end') 


        stAll = []

        baselinex = np.arange(0, len(baseline), 1)
        # baselinex = baselineX / self.fs 
        
        boarder_top = max(baseline)
        boarder_bot = min(baseline)

        for i, ii in zip(stStart, stEnd):
            a = [i,ii]
            stAll.append(a)

              
        fig =go.Figure()


        fig.add_trace(go.Scatter(
            x=baselinex,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))


        for i in stAll:
            fig.add_trace(go.Scatter(
                x=i,
                y=baseline[i],
                mode='markers'
                
            ))


        fig.update_layout(
            xaxis_title="Time [s]",
            yaxis_title="Amplitude [µv]",
            showlegend=True,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis=dict(zeroline=False),
            yaxis_gridcolor="#515151",
            xaxis_gridcolor="#515151",
            font=dict(
                family="Shell",
                size=18,
                color="#9C9C9C"
            )
        )

        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[boarder_bot, boarder_top])

        
        self.app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id='live-update-graph', figure = fig, animate = True ), 
        ])
        

if __name__ == '__main__':
    component = PlotComponent()
    component.choosePlot(PlotComponent.types.BASELINE)
    
