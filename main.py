import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

temp_dry = np.arange(30,39,0.5)
def temp_wet(dry_temp, hp):
    temp_wet = dry_temp*np.arctan(0.152*(hp+8.3136)**(1/2))+np.arctan(dry_temp+hp)-np.arctan(hp-1.6763)+0.00391838*(hp)**(3/2)*np.arctan(0.0231*hp)-4.686
    temp_wet = np.round(temp_wet,2)
    return temp_wet
def tzk(temp_dry, hp, v=0):
    _temp_wet = temp_wet(temp_dry,hp)
    return _temp_wet *0.6 + temp_dry * 0.4 - v

def tzk_temps(temp_dry, temp_wet, v=0):
    return temp_wet *0.6 + temp_dry * 0.4 - v

v = [0,0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
data = np.array([tzk(
    _temp_dry,
    hp = 60,
    v = _v
) for _v in v for _temp_dry in temp_dry]).reshape(len(v),-1).transpose()

tzk_df = pd.DataFrame(
    data = data,
    index = temp_dry,
    columns = np.arange(0,4.5,0.5)
    )
tzk_df.index.name = 'temp'
tzk_df.columns.name = 'v'


from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput, PreText, BoxAnnotation, ColorPicker
from bokeh.plotting import figure

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler

#output_notebook()

tzk_df.columns = tzk_df.columns.astype(str)
tzk_df_ = tzk_df.reset_index().to_dict(orient= "list")
source = ColumnDataSource(data=tzk_df_)

tzk_CDS = ColumnDataSource(data=dict(x=[34], y=[28]))

mid_box = BoxAnnotation(bottom=30, top=32, fill_alpha=0.1, fill_color='yellow')
bottom_box = BoxAnnotation(bottom=26, top=30, fill_alpha=0.1, fill_color='green')

p = figure(title="tutuł", height=300, width=600, x_range=(30,38), y_range=(22,34),
           background_fill_color='#efefef')
p.add_layout(mid_box)
p.add_layout(bottom_box)

numlines=len(tzk_df.columns)
     
def tzk_temps(temp_dry, temp_wet, v=0):
    return temp_wet *0.6 + temp_dry * 0.4 - v  

def tg(temp_dry, temp_wet, v):
    for temp in np.linspace(60,20,100):
        if tzk_temps(temp, temp_wet, v) <= 32:
            temp = np.round(temp,1)
            break
    return temp


# plotting the graph  
p.multi_line(
    xs = [tzk_df.index.values]*numlines, 
    ys = [tzk_df[name].values for name in tzk_df])  

f = p.scatter("x", "y", source=tzk_CDS, color="black",name="my")

ts = Slider(title="ts", value=34, start=28, end=38, step=1)
tw = Slider(title="tw", value=28, start=18, end=38, step=1)
v = Slider(title="v", value=2, start=0, end=4, step=0.1)

extra_txt = PreText(text="""""", width=250, height=100)

def update_data(attrname, old, new):
    ts_ = ts.value
    tw_ = tw.value
    v_ = v.value
    tzk_ = tzk_temps(ts_, tw_, v= v_)
    tzk_CDS.data = dict(x=[ts_], y=[tzk_])
    if tzk_>= 32:
        f.glyph.line_color = "red"
        f.glyph.fill_color = "red"
    else:
        f.glyph.line_color = "black"
        f.glyph.fill_color = "black"      

    p.title.text = f"Tzk = {tzk_:.1f}"
    extra_txt.text = f"t graniiczna: {tg(ts_,tw_,v_)}"


curdoc().add_root(row(column(ts,tw,v,extra_txt), p, width=800))
ts.on_change('value', update_data)
tw.on_change('value', update_data)
v.on_change('value', update_data)
