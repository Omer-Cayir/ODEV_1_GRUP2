import numpy as np
import matplotlib.pyplot as plt

# 1. Parametrelerin Tanımlanması
f1 = 52.5   # Hz
f2 = 105    # Hz
f3 = 1050   # Hz

# Örnekleme frekansı: En yüksek frekansın (1050 Hz) yaklaşık 10 katı (Pürüzsüzlük için)
fs = 10000 
t_basla = 0
t_bitis = 0.1  # 100 milisaniye (52.5 Hz'in yaklaşık 5 periyodunu görmek için yeterli)

# 2. Zaman Dizisinin ve Sinyallerin Oluşturulması
t = np.linspace(t_basla, t_bitis, int(fs * (t_bitis - t_basla)))

# Her bir sinüs dalgasının oluşturulması
y1 = np.sin(2 * np.pi * f1 * t)
y2 = np.sin(2 * np.pi * f2 * t)
y3 = np.sin(2 * np.pi * f3 * t)

# Sinyallerin Toplamı
y_toplam = y1 + y2 + y3

# 3. Grafik Çizimi
plt.figure(figsize=(12, 6))

# Üstte tekil sinyallerden bir örnek (Kıyaslama için)
plt.subplot(2, 1, 1)
plt.plot(t, y1, label=f"{f1} Hz", alpha=0.7)
plt.plot(t, y2, label=f"{f2} Hz", alpha=0.7)
plt.title("Bireysel Sinyaller")
plt.legend()
plt.grid(True)

# Altta toplam sinyal
plt.subplot(2, 1, 2)
plt.plot(t, y_toplam, color='black', label="Toplam Sinyal")
plt.title(f"Sinyallerin Toplamı ({f1} + {f2} + {f3} Hz)")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Genlik")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()