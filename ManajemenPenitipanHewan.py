import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json


# Class
class Hewan:
    def __init__(self, nama_pemilik, nama_hewan, jenis, tanggal_masuk, rencana_keluar):
        self.nama_pemilik = nama_pemilik
        self.nama_hewan = nama_hewan
        self.jenis = jenis
        self.tanggal_masuk = datetime.strptime(tanggal_masuk, "%Y-%m-%d")
        
        self.rencana_keluar = None
        if rencana_keluar:
            self.rencana_keluar = datetime.strptime(rencana_keluar, "%Y-%m-%d")

        self.tanggal_keluar_aktual = None

    def keluar(self, tanggal_keluar_aktual):
        self.tanggal_keluar_aktual = tanggal_keluar_aktual


#simpan data
def simpan_data():
    data = []
    for h in queue_hewan:
        data.append({
            "nama_pemilik": h.nama_pemilik,
            "nama_hewan": h.nama_hewan,
            "jenis": h.jenis,
            "tanggal_masuk": h.tanggal_masuk.strftime("%Y-%m-%d"),
            "rencana_keluar": h.rencana_keluar.strftime("%Y-%m-%d") if h.rencana_keluar else None
        })

    with open("data_penitipan.json", "w") as f:
        json.dump(data, f, indent=4)


#muat data
def muat_data():
    try:
        with open("data_penitipan.json", "r") as f:
            data = json.load(f)

        for item in data:
            hewan = Hewan(
                item["nama_pemilik"],
                item["nama_hewan"],
                item["jenis"],
                item["tanggal_masuk"],
                item["rencana_keluar"]
            )
            queue_hewan.append(hewan)

        queue_hewan.sort(key=lambda x: (x.jenis, x.tanggal_masuk))
        update_listbox()

    except FileNotFoundError:
        pass


# Queue
queue_hewan = []

# Function Tambah Hewan
def tambah_hewan():
    nama_pemilik = entry_pemilik.get()
    nama_hewan = entry_hewan.get()
    jenis = jenis_var.get()
    tanggal_masuk = entry_masuk.get()
    rencana_keluar = entry_rencana.get()

    if not nama_pemilik or not nama_hewan or not tanggal_masuk:
        messagebox.showwarning("Peringatan", "Nama Pemilik, Hewan, dan Tanggal Masuk harus diisi!")
        return

    for h in queue_hewan:
        if h.nama_hewan.lower() == nama_hewan.lower():
            messagebox.showwarning("Duplikat", f"Hewan dengan nama '{nama_hewan}' sudah ada dalam daftar!")
            return

    try:
        hewan = Hewan(nama_pemilik, nama_hewan, jenis, tanggal_masuk, rencana_keluar)
    except ValueError:
        messagebox.showerror("Error", "Format tanggal salah! Gunakan YYYY-MM-DD.")
        return

    queue_hewan.append(hewan)
    queue_hewan.sort(key=lambda x: (x.jenis, x.tanggal_masuk))

    messagebox.showinfo("Berhasil", f"Hewan {nama_hewan} berhasil ditambahkan.")

    entry_pemilik.delete(0, tk.END)
    entry_hewan.delete(0, tk.END)
    entry_masuk.delete(0, tk.END)
    entry_masuk.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_rencana.delete(0, tk.END)

    update_listbox()

# Function Keluarkan Hewan
def keluarkan_hewan():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Peringatan", "Pilih hewan yang akan dikeluarkan!")
        return

    index = selected_index[0]
    hewan = queue_hewan[index]

    tanggal_aktual = datetime.now().strftime("%Y-%m-%d")
    hewan.keluar(tanggal_aktual)

    pesan = f"Hewan {hewan.nama_hewan} resmi dikeluarkan.\nTanggal Dikeluarkan: {tanggal_aktual}"
    messagebox.showinfo("Sukses Dikeluarkan", pesan)

    queue_hewan.pop(index)
    update_listbox()


# Update Listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for hewan in queue_hewan:
        tgl_masuk_str = hewan.tanggal_masuk.strftime('%Y-%m-%d')
        if hewan.rencana_keluar:
            tgl_rencana_str = hewan.rencana_keluar.strftime('%Y-%m-%d')
            info_keluar = f"Sampai: {tgl_rencana_str}"
        else:
            info_keluar = "Durasi: -"

        display_text = f"[{hewan.jenis}] {hewan.nama_hewan} ({hewan.nama_pemilik}) | Masuk: {tgl_masuk_str} | {info_keluar}"
        listbox.insert(tk.END, display_text)

        if hewan.jenis == "Air":
            listbox.itemconfig(tk.END, {'bg': 'cyan'})
        else:
            listbox.itemconfig(tk.END, {'bg': 'light green'})


#close window
def on_closing():
    simpan_data()
    root.destroy()


#guizaQ                                                                         
root = tk.Tk()
root.title("Penitipan Hewan")
root.geometry("500x500")

warna_bg = "#FF6B35"
warna2 = "#4169E1"
warna3 = "#F25C05"
warna4 = "#EEF4ED"

root.configure(bg=warna_bg)

frame_form = tk.Frame(root, bg=warna_bg)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nama Pemilik:", bg=warna_bg).grid(row=0, column=0, sticky="e", padx=5, pady=2)
entry_pemilik = tk.Entry(frame_form)
entry_pemilik.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Nama Hewan:", bg=warna_bg).grid(row=1, column=0, sticky="e", padx=5, pady=2)
entry_hewan = tk.Entry(frame_form)
entry_hewan.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_form, text="Jenis Hewan:", bg=warna_bg).grid(row=2, column=0, sticky="e", padx=5, pady=2)
frame_radio = tk.Frame(frame_form, bg=warna_bg)
frame_radio.grid(row=2, column=1, sticky="w")

jenis_var = tk.StringVar(value="Darat")
tk.Radiobutton(frame_radio, text="Darat", variable=jenis_var, value="Darat", bg=warna_bg, fg='light green').pack(side="left")
tk.Radiobutton(frame_radio, text="Air", variable=jenis_var, value="Air", bg=warna_bg, fg='cyan').pack(side="left")

tk.Label(frame_form, text="Tanggal Masuk (YYYY-MM-DD):", bg=warna_bg).grid(row=3, column=0, sticky="e", padx=5, pady=2)
entry_masuk = tk.Entry(frame_form)
entry_masuk.grid(row=3, column=1, padx=5, pady=2)
entry_masuk.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(frame_form, text="Rencana Keluar (YYYY-MM-DD):", bg=warna_bg).grid(row=4, column=0, sticky="e", padx=5, pady=2)
entry_rencana = tk.Entry(frame_form)
entry_rencana.grid(row=4, column=1, padx=5, pady=2)
tk.Label(frame_form, text="(Opsional)", bg=warna_bg, font=("Arial", 8)).grid(row=4, column=2, sticky="w")

frame_buttons = tk.Frame(root, bg=warna_bg)
frame_buttons.pack(pady=5)
tk.Button(frame_buttons, text="Tambah Hewan", command=tambah_hewan, bg="white").pack(side="left", padx=5)
tk.Button(frame_buttons, text="Keluarkan Hewan", command=keluarkan_hewan, bg="white").pack(side="left", padx=5)

tk.Label(root, text="Daftar Hewan & Jadwal:", bg=warna4, font=("Arial", 10, "bold")).pack(pady=(10, 0))
listbox = tk.Listbox(root, width=90, height=15, bg=warna2)
listbox.pack(pady=5, padx=10)


muat_data()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
