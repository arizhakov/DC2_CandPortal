#==============================================================================
# import plotly.plotly as py
# import plotly.graph_objs as go
# 
# data = [
#         go.Heatmap(
#             z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
#             x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
#             y=['Morning', 'Afternoon', 'Evening']
#         )
#         ]
# py.iplot(data, filename='labelled-heatmap')
# 
#==============================================================================
import numpy as np
import numpy.random
import matplotlib.pyplot as plt

x = np.random.randn(100000)
y = np.random.randn(100000)
plt.hist2d(x,y,bins=100);
