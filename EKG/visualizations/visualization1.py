from threading import Thread
from model import Model
import sys
import numpy as np
import pandas as pd
import numpy as np
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash.html as html
import dash.dcc as dcc
 
 
#collor palette

# button_blue = #008CFF
# toggle_on_green = #36B37E
# checkbox_on_green = #36B37E
# checkbox_off_gray = #9C9C9C
# bg_2 = #363636



HTTP_PORT = 9999

class PlotComponent():
    def __init__(self, port = HTTP_PORT):
        """ Initialization. """
        super().__init__()
        self.port = port
        self.start_server()

    def start_server(self):
        """ Calling that method will result in listening of server at port HTTP_PORT. """
        self.thread = Thread(target=self._thread_target, daemon=True)
        self.thread.start() 

    def render(self):
        
        #card = self.chosed_card
        #part = self.active_graph
        
        card = 1
        part = 1
        

        
        
        if(card == 1):
            if(part == 1):
                self.baseline()
        
            elif(part == 2):
                self.Rpeaks()
        
            elif(part == 3):
                self.waves()
        
        elif(card == 2):
            if(part == 1):
                self.hrv1()
        
            elif(part == 2):
                self.hrv2()
        
            elif(part == 3):
                self.dfa()
        
        elif(card == 3):
            if(part == 1):
                self.heartClass()
        
            elif(part == 2):
                self.stSegment()

        
        else:
            self.ecgPlot()
        

    def _alg(self):
        
        self.M = Model()
        
        # Loading data from 0 to 10000 sample
        self.M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
        # launching "BaselineECGFilter"
        self.M.apply_algorythm(alg_name="BaselineECGFilter")
        # launching "RPeaksDetection"
        self.M.apply_algorythm(alg_name="RPeaksDetection")
        # launching "WAVES"
        self.M.apply_algorythm(alg_name="WAVES", algorythm="derivatives")
        # launching "HRV1"
        self.M.apply_algorythm(alg_name="HRV1")  
        # launching "DFA"
        self.M.apply_algorythm(alg_name="DFA")
        # launching "STSegment"
        #self.M.apply_algorythm(alg_name="STSegment")


    def _thread_target(self):
        self.render()
        
        
    def ecgPlot(self):
        self._alg()
        app = dash.Dash()
        
        dataecg = self.M.load_data_from_file("./dane/100.dat", left_slice=0, right_slice=10_000)
        dataecgX = np.arange(0, len(dataecg[0]), 1)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dataecgX,
            y=dataecg[0],
            name="Sygnał EKG"       # this sets its legend entry
            line=dict(color="#008CFF"),
            name="Sygnał EKG"# this sets its legend entry
            
        ))
        
        fig.update_layout(
            title="Wykres EKG",
            xaxis_title="Numer próbki",
            yaxis_title="Amplituda [µv]",
            showlegend=False,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#9C9C9C",
            xaxis_gridcolor="#9C9C9C",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#9C9C9C"
            )
        )

        fig.update_xaxes(rangeslider_visible=True)
        
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)
        
        
    def baseline(self):
        
        self._alg()
        app = dash.Dash()
        
        baseline = self.M.apply_algorythm(alg_name="BaselineECGFilter")
        baselineX = np.arange(0, len(baseline), 1)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=baselineX,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))
        
        
        fig.update_layout(
            title="Wykres baseline",
            xaxis_title="Numer próbki",
            yaxis_title="Amplituda [µv]",
            showlegend=False,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#9C9C9C",
            xaxis_gridcolor="#9C9C9C",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#9C9C9C"
            )
        )
        
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[-100, 300])
        
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)
        
        
    def Rpeaks(self):
        
        self._alg()
        app = dash.Dash()
        
        baseline = self.M.apply_algorythm(alg_name="BaselineECGFilter")
        baselineX = np.arange(0, len(baseline), 1)
        peaksR = self.M.apply_algorythm(alg_name="RPeaksDetection")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=baselineX,
            y=baseline,
            line=dict(color="#008CFF"),
            name="Baseline"
        ))
        
        fig.add_trace(go.Scatter(
            x=peaksR,
            y=baseline[peaksR],
            name="RPiki",
            mode='markers',
            marker=dict(color="#36B37E")
        ))
        
        fig.update_layout(
            title="Wykres baseline z zaznaczonymi R pikami",
            xaxis_title="Numer próbki",
            yaxis_title="Amplituda [µv]",
            showlegend=False,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#9C9C9C",
            xaxis_gridcolor="#9C9C9C",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#9C9C9C")
        )
        
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[-100, 300])
        
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)
        
        
    def waves(self):
        
        self._alg()
        app = dash.Dash()
        
        baseline = self.M.apply_algorythm(alg_name="BaselineECGFilter")
        baselineX = np.arange(0, len(baseline), 1)

        waves = self.M.apply_algorythm(alg_name="WAVES", algorythm="derivatives")

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
            line=dict(color="#008CFF"),
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
            title="Wykres waves",
            xaxis_title="Numer próbki",
            yaxis_title="Amplituda [µv]",
            legend_title="Legenda",
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#9C9C9C",
            xaxis_gridcolor="#9C9C9C",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#9C9C9C")
        )
        
        
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_yaxes(range=[-100, 300])
        
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)
 
 
    def hrv1(self):
        
        self._alg()
        app = dash.Dash()
        
        hrv1_all = self.M.apply_algorythm(alg_name="HRV1")
        hrv1_frequency_parameters = hrv1_all.get('frequency_parameters')
        hrv1 = hrv1_frequency_parameters.get('psd_chart')
        f = hrv1[0]
        pxx = hrv1[1]
        

        fig = go.Figure()
        
        
        fig.add_trace(go.Scatter(
            x=f,
            y=pxx,
            line=dict(color="#008CFF"),
            name="hrv1"
        ))
        
        fig.update_layout(
            title="Wykres hrv1",
            xaxis_title="Częstotliwość [Hz]",
            yaxis_title="Moc widma [ms^2]",
            showlegend=False,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#9C9C9C",
            xaxis_gridcolor="#9C9C9C",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#9C9C9C")
        )
        
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
        
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)
        
     
    def hrv2(self):
        pass
    
    
    def dfa(self):
        
        self._alg()
        app = dash.Dash()
        
        fig = go.Figure()
        
        dfa = self.M.apply_algorythm(alg_name="DFA")
        
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
            title="Wykres DFA",
            xaxis_title="log 10(n)",
            yaxis_title="log 10(F(n))",
            showlegend=False,
            paper_bgcolor ="#121212",
            plot_bgcolor ="#121212",
            yaxis_gridcolor="#9C9C9C",
            xaxis_gridcolor="#9C9C9C",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#9C9C9C")
        )
        
        fig.update_xaxes(type="log")
           
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)
        
        
    def heartClass(self):
        pass
    
    
    def stSegment(self):

        
        self._alg()
        app = dash.Dash()
        
        fig = go.Figure()
        
        stSegment = self.M.apply_algorythm(alg_name="STSegment")
        stSegments = self.stSegment['st_data']
        stSegmentPrint = stSegments[['start','end']]

        baseline = self.M.apply_algorythm(alg_name="BaselineECGFilter")
        baselineX = np.arange(0, len(baseline), 1)
    



        fig.update_layout(
            title="Wykres ",
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
           
        app.layout = html.Div(id = 'parent', children = [
            dcc.Graph(id = 'line_plot', figure=fig),
        ])
        app.run_server(port=HTTP_PORT)

if __name__ == '__main__':
    component = PlotComponent()