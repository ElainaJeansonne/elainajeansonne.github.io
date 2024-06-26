import csv
import pandas as pd
import numpy as np
import math
import re
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from adjustText import adjust_text


df = pd.read_csv('C:/schoolwork/HD33077.csv', names=['year', 'theta', 'rho', 'component'])
df = df.dropna()
df = df.reset_index(drop=True)
df["x"] = df.loc[:,"rho"] * np.cos(df.loc[:,"theta"] * np.pi/180)
df["y"] = df.loc[:,"rho"] * np.sin(df.loc[:,"theta"] * np.pi/180)

try:
  new_filename = resource_filepath + "my_measurements_.csv"
  file = open(new_filename)
  new_content = file.readlines()  #creates a 2d list containing the content of the file

  new_df = pd.read_csv(new_filename, names=['year', 'theta', 'rho', 'component'])
  new_df["x"] = new_df.loc[:,"rho"] * np.cos(new_df.loc[:,"theta"] * np.pi/180)
  new_df["y"] = new_df.loc[:,"rho"] * np.sin(new_df.loc[:,"theta"] * np.pi/180)
except:
  pass

ax = df.plot(kind="scatter", x="x", y="y")
def get_plot_dict(df_dict, title, letter="", new_measurement=np.nan):
  # what do we need for a plot?
  # 1. plot title
  title = title

  # x and y values
  x = df_dict["x"]
  y = df_dict["y"]

  # 2. groups
  groups = df_dict.groupby('component')

  # 3. year
  year = df_dict['year'].to_list()

  # 4. component (for labeling)
  component = df_dict['component'].to_list()

  return {
      "title": title,
      "x": x,
      "y": y,
      "component": component,
      "groups": groups,
      "year": year,
      "origin_star": letter,
      "new_measurement": new_measurement }

def get_adjust_texts(plot_dict):
  zipped = zip(plot_dict["year"], plot_dict["x"], plot_dict["y"])
  ts = []
  ts_x = []
  ts_y = []
  #count = len(plot_dict["year"])

  for s, x_an, y_an in zipped:
    s = round(s)
    ts.append(plt.text(x_an, y_an, s, ha="left"))
    ts_x.append(x_an)
    ts_y.append(y_an)

  length = len(ts)
  num = round(length / 10)
  return ts, ts_x, ts_y

def loop_plot(plots):
    figs={}
    axs={}
    for idx,plot in enumerate(plots):
      # create subplots
      figs[idx]=plt.figure()
      axs[idx]=figs[idx].add_subplot(111)

      # set title of each plot, set axis labels
      axs[idx].set_title(plot["title"], y=1.2, pad=-30)
      axs[idx].title.set_size(18)
      axs[idx].set_xlabel('X (ArcSec)', fontsize=8)
      axs[idx].set_ylabel('Y (ArcSec)', fontsize=8)
       # get groups for each plot
      groups = plot["groups"]
      for name, group in groups:
        plt.gray()
        plt.plot(group.x, group.y, marker='o', linestyle='', markersize=3, label="Historical " + name)

      # STAR AT ORIGIN PLOT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
      #
      if "origin" in plot["title"]:
        # create a point at the origin, indicating the origin star location at [0,0]
        axs[idx].plot(0, 0, 'o')
        axs[idx].annotate(plot["origin_star"], xy=(0.5, 0.5))

        # center spines
        axs[idx].spines['left'].set_position('zero')
        axs[idx].spines['right'].set_color('none')
        axs[idx].spines['bottom'].set_position('zero')
        axs[idx].spines['top'].set_color('none')

        # create legend based on the groups of points, and new data
        plt.legend()

        # make the axes tick spacing equal
        plt.gca().set_box_aspect(1)
        plt.axis('equal')
        plt.grid()

        plt.savefig(figures_filepath + plot["title"], bbox_inches="tight")
    else:
        axs[idx].spines['right'].set_color('none')
        axs[idx].spines['top'].set_color('none')
        stepsize = 0.1

        ts, ts_x, ts_y = get_adjust_texts(plot)

        try:
          new_x = plot["new_measurement"][0]
          new_y = plot["new_measurement"][1]
          new_year = plot["new_measurement"][2]

          ts.append(plt.text(new_x, new_y, new_year, ha="left"))
          ts_x.append(new_x)
          ts_y.append(new_y)

          axs[idx].plot(new_x, new_y, '*', markersize=10, label="New " + plot["component"][0])
        except Exception:
          pass

        adjust_text(ts, x=ts_x, y=ts_y,
            only_move={'points':'xy', 'text':'y', 'objects':'y'},
            force_points=0.15
            #, arrowprops=dict(arrowstyle="->", color='black', lw=0.75)
            )

        # create legend based on the groups of points, and new data
        plt.legend()

        # make the axes tick spacing equal
        plt.gca().set_box_aspect(1)
        plt.axis('equal')
        plt.grid()

        plt.savefig(figures_filepath + plot["title"], bbox_inches="tight")



    return figs, axs
import string
import warnings

#get a list of alphabet letters
#
alphabet_list = list(string.ascii_uppercase)

# iterate through alphabet_list to create a new plot for each
# component with different stars at origin
#
plots = []
for letter, number in zip(alphabet_list, range(26)):
  #create a new df for each star centered at the origin
  df_curr = df[df['component'].str.startswith(letter)]

  unique_components = df_curr['component'].unique()
  if df_curr.empty:
    continue

  title = wds_id + " with " + letter + " at origin."
  plots.append(get_plot_dict(df_curr, title, letter=letter))

  for comp in unique_components:
    try:
      temp = new_df[new_df["component"] == comp]
      new_measurement = [float(temp['x']), float(temp['y']), round(float(temp['year']), 1)]
    except Exception:
      new_measurement = np.nan

    df_curr = df[df['component'] == comp]
    title = wds_id + " zoomed on " + comp
    plots.append(get_plot_dict(df_curr, title, new_measurement=new_measurement))

    figs, axs = loop_plot(plots)