from __future__ import division, print_function
import numpy as np
import pandas as pd
import pygal
from datetime import datetime

data = pd.read_csv('btown/2016-first-quarter-citations.csv')
data = data.dropna(how='any')
ages = data['Cited Person Age']
ages = ages[ages < 100]
ages = np.asarray(ages, int)
freq, bins = np.histogram(ages, bins=np.max(ages) - np.min(ages))
plot_data = []
for i in range(len(freq)):
    plot_data.append([freq[i], bins[i], bins[i] + 1])
hist = pygal.Histogram(title = "Citations by age")
hist.add('Citations',plot_data)
hist.render_to_file('age_citation.svg')