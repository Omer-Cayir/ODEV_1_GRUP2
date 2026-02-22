import tkinter as tk
from tkinter import ttk
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DTMFGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("DTMF Sinyal Sentezi")
        self.root.geometry("900x500")
        
        # --- PARAMETRELER ---
        # fs: Saniyedeki örnek sayısı (Nyquist kriterine uygun seçildi) 
        self.fs = 44100  
        # duration: Bir tuş sesinin ne kadar süreceği (0.3 saniye) 
        self.duration = 0.3  
        
        # --- DTMF FREKANS TABLOSU ---
        # Her tuş, bir düşük ve bir yüksek frekansın birleşimidir 
        self.dtmf_map = {
            '1': (500, 1100), '2': (500, 1300), '3': (500, 1500), 'A': (500, 1700),
            '4': (600, 1100), '5': (600, 1300), '6': (600, 1500), 'B': (600, 1700),
            '7': (700, 1100), '8': (700, 1300), '9': (700, 1500), 'C': (700, 1700),
            '*': (800, 1100), '0': (800, 1300), '#': (800, 1500), 'D': (800, 1700)
        }
        
        self.setup_ui()

    def setup_ui(self):
        # Üst Panel: Basılan tuş ve frekans bilgilerini yazı olarak gösterir
        self.info_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.lbl_status = tk.Label(self.info_frame, text="Bir tuşa basın...", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.lbl_status.pack()
        
        self.lbl_freqs = tk.Label(self.info_frame, text="Frekanslar: - Hz + - Hz", font=("Arial", 11), bg="#f0f0f0", fg="blue")
        self.lbl_freqs.pack()

        self.main_container = tk.Frame(self.root)
        self.main_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Sol Panel: 4x4 Numpad (Telefon tuş takımı) tasarımı
        self.button_frame = tk.LabelFrame(self.main_container, text=" Tuş Takımı ", padx=10, pady=10)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], 
                ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]
        
        # İç içe döngü ile butonları ekrana dizer
        for r, row in enumerate(keys):
            for c, char in enumerate(row):
                btn = tk.Button(self.button_frame, text=char, width=6, height=3,
                                font=("Arial", 12, "bold"),
                                command=lambda ch=char: self.play_dtmf(ch))
                btn.grid(row=r, column=c, padx=3, pady=3)

        # Sağ Panel: Sinyalin grafiğini çizdireceğimiz Matplotlib alanı 
        self.plot_frame = tk.LabelFrame(self.main_container, text=" Sinyal Grafiği ", padx=5, pady=5)
        self.plot_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def play_dtmf(self, char):
        # 1. Tuşa ait frekans değerlerini tablodan al
        f_low, f_high = self.dtmf_map[char]
        
        # 2. Arayüzdeki yazı başlıklarını güncelle
        self.lbl_status.config(text=f"Basılan Tuş: {char}")
        self.lbl_freqs.config(text=f"Düşük Frekans: {f_low} Hz | Yüksek Frekans: {f_high} Hz")
        
        # 3. Sinyal Oluşturma (Matematiksel Modelleme) 
        # Zaman ekseni oluşturulur (0'dan duration süresine kadar)
        t = np.linspace(0, self.duration, int(self.fs * self.duration), endpoint=False)
        # İki sinüs dalgası toplanır ve 0.5 ile çarpılarak normalizasyon yapılır (clipping önleme) 
        signal = 0.5 * (np.sin(2 * np.pi * f_low * t) + np.sin(2 * np.pi * f_high * t))
        
        # 4. Sesi Hoparlörden Çal 
        sd.play(signal, self.fs)
        
        # 5. Görselleştirme (Grafiği Güncelle) 
        self.ax.clear()
        # Sinyalin tamamı yerine sadece ilk 400 örneği çizdirerek dalga formunu net gösterir
        self.ax.plot(t[:400], signal[:400], color='red') 
        self.ax.set_title(f"{char} Tuşu Birleşik Sinyal")
        self.ax.set_xlabel("Zaman (s)")
        self.ax.set_ylabel("Genlik")
        self.ax.grid(True)
        self.canvas.draw() # Grafiği ekrana yansıt

if __name__ == "__main__":
    root = tk.Tk()
    app = DTMFGenerator(root)
    root.mainloop() # Programı başlat ve kullanıcı kapatana kadar açık tut