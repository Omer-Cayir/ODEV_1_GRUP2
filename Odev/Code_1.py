import numpy as np
import matplotlib.pyplot as plt

# Parametreler
f = 1050       # Frekans (Hz)
fs = 2100      # Örnekleme hızı (Saniyede kaç nokta ölçüldüğü)
t_son = 0.01    # Çizilecek süre (0.05 saniye = 50 ms)

# Zaman ekseni (0'dan 0.05'e kadar noktalar oluşturur)
t = np.linspace(0, t_son, int(fs * t_son))

# Sinyal denklemi
y = np.sin(2 * np.pi * f * t)

# Grafik oluşturma
plt.figure(figsize=(10, 4))
plt.plot(t, y)
plt.title(f"{f} Hz Sinüs Sinyali")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Genlik")
plt.grid(True)
plt.show()