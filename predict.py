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

md = to_minutes("2:15")
mp = 1.0
mf = 33

# строим нашу линейную модель
X = np.array(
    [[d, mp, mf] for d in durations] + [[md, p, mf] for p in prices] + [[md, mp, f] for f in frequencies]
)
Y = np.concatenate(
    [people_count_for_durations, people_count_for_prices, people_count_for_frequencies]
).reshape(-1, 1)
linreg = linear_model.LinearRegression().fit(X, Y)
print(linreg.coef_, linreg.intercept_)

# строим графики
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(8, 9))

x = np.array([[durations[0], mp, mf], [durations[-1], mp, mf]])
y = linreg.predict(x)
ax1.plot(x[:, 0], y, label='Линейная модель', color='orange')
ax1.scatter(durations, people_count_for_durations, label='Исходные данные')
ax1.set_xlabel('Продолжительность поездки')
ax1.set_ylabel('Пассажиропоток')
ax1.set_ylim((10000, 22000))
ax1.legend()

x = np.array([[md, prices[0], mf], [md, prices[-1], mf]])
y = linreg.predict(x)
ax2.plot(x[:, 1], y, label='Линейная модель', color='orange')
ax2.scatter(prices, people_count_for_prices, label='Исходные данные')
ax2.set_xlabel('Ценовой тариф')
ax2.set_ylabel('Пассажиропоток')
ax2.set_ylim((10000, 22000))
ax2.legend()

x = np.array([[md, mp, frequencies[0]], [md, mp, frequencies[-1]]])
y = linreg.predict(x)
ax3.plot(x[:, 2], y, label='Линейная модель', color='orange')
ax3.scatter(frequencies, people_count_for_frequencies, label='Исходные данные')
ax3.set_xlabel('Частота сообщений, пар/сутки')
ax3.set_ylabel('Пассажиропоток')
ax3.set_ylim((10000, 22000))
ax3.legend()

plt.savefig('linear_model_results.png')
plt.show()
