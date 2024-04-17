import matplotlib.pyplot as plt
import numpy as np

from sklearn import linear_model

to_minutes = lambda s: int(s[0])*60 + int(s[2:4])

durations_str = ["2:00", "2:05", "2:10", "2:15", "2:20", "2:25", "2:30", "2:35", "2:40", "2:45", "2:50", "2:55", "3:00"]
durations = np.array(list(map(to_minutes, durations_str)))
people_count_for_durations = np.array([17260, 16945, 16631, 16319, 16010, 15702, 15397, 15094, 14793, 14496, 14201, 13910, 13622])

prices = np.array([0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4])
people_count_for_prices = np.array([21251, 20516, 19727, 18898, 18046, 17183, 16319, 15466, 14629, 13815, 13037, 12293, 11549, 10912, 10286])

frequencies = np.array([45, 42, 39, 36, 33, 30, 27, 24, 21])
people_count_for_frequencies = np.array([16421, 16401, 16378, 16351, 16319, 16281, 16235, 16177, 16102])

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)

# linreg1 = linear_model.LinearRegression().fit(durations.reshape(-1, 1), people_count_for_durations.reshape(-1, 1))

ax1.bar(durations_str, people_count_for_durations)
ax1.set_xlabel('Продолжительность поездки')
ax1.set_ylabel('Пассажиропоток')
ax1.set_ylim((10000, 22000))

# linreg2 = linear_model.LinearRegression().fit(prices.reshape(-1, 1), people_count_for_prices.reshape(-1, 1))

ax2.bar(prices, people_count_for_prices)
ax2.set_xlabel('Ценовой тариф')
ax2.set_ylabel('Пассажиропоток')
ax2.set_ylim((10000, 22000))


# linreg3 = linear_model.LinearRegression().fit(frequencies.reshape(-1, 1), people_count_for_frequencies.reshape(-1, 1))

ax3.bar(frequencies, people_count_for_frequencies)
ax3.set_xlabel('Частота сообщений, пар/сутки')
ax3.set_ylabel('Пассажиропоток')
ax3.set_ylim((10000, 22000))


plt.show()
