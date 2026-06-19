import sys

SAPTAWARA = {
    "Ahad": 5, "Minggu": 5, "Senin": 4, "Selasa": 3,
    "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9
}

PANCAWARA = {
    "Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 6
}

COMPATIBILITY_MAP = {
    1: ("Pegat", "Prone to separation; highest risk classification"),
    2: ("Ratu", "Harmonious, respected; socially well-regarded couple"),
    3: ("Jodho", "Ideally matched; considered a natural soulmate pairing"),
    4: ("Topo", "Hardship and perseverance; challenges overcome together"),
    5: ("Tinari", "Fortunate; blessed with ease and luck"),
    6: ("Padu", "Prone to conflict; frequent disagreements expected"),
    7: ("Sujanan", "Prone to infidelity; trust issues anticipated"),
    8: ("Pesthi", "Highest long-term harmony; the most auspicious class")
}

def bersihkan_dan_urai_weton(input_str):
    """
    Mengurai string input menjadi komponen Hari dan Pasaran yang valid.
    Mendukung format 'Hari Pasaran', 'hari-pasaran', dll.
    """
    # Ganti tanda hubung dengan spasi dan pisahkan kata
    tokens = input_str.replace("-", " ").strip().split()
    
    if len(tokens) != 2:
        return None
    
    # Standarisasi huruf kapital di awal kata
    part1, part2 = tokens[0].capitalize(), tokens[1].capitalize()
    
    # Cek skenario normal: Part1 = Hari, Part2 = Pasaran
    if part1 in SAPTAWARA and part2 in PANCAWARA:
        hari = "Ahad" if part1 == "Minggu" else part1
        return (hari, part2)
    
    # Cek skenario terbalik: Part1 = Pasaran, Part2 = Hari
    if part1 in PANCAWARA and part2 in SAPTAWARA:
        hari = "Ahad" if part2 == "Minggu" else part2
        return (hari, part1)
        
    return None

def dapatkan_input_weton(prompt):
    """Meminta input weton dari user secara berulang sampai valid."""
    while True:
        user_input = input(prompt)
        hasil_urai = bersihkan_dan_urai_weton(user_input)
        if hasil_urai:
            return hasil_urai
        print("[!] Format salah atau Weton tidak dikenal. Contoh input valid: 'Senin Pon' atau 'Kamis-Legi'. Coba lagi.")

def hitung_simulasi_matchmaking(nama1, weton1, nama2, weton2):
    hari1, pasaran1 = weton1
    hari2, pasaran2 = weton2
    
    # 1. Hitung Nilai Neptu Individu
    neptu1 = SAPTAWARA[hari1] + PANCAWARA[pasaran1]
    neptu2 = SAPTAWARA[hari2] + PANCAWARA[pasaran2]
    
    # 2. Binary Accumulation (Total Neptu)
    t_gabungan = neptu1 + neptu2
    
    # 3. Klasifikasi Kompatibilitas Modulo 8 (T ≡ R mod 8)
    r = t_gabungan % 8
    if r == 0:
        r = 8  # Reinterpretasi nilai residu 0 menjadi perwakilan kelas 8
        
    kategori, interpretasi = COMPATIBILITY_MAP[r]
    
    # 4. Optimasi Hari Pernikahan Modulo 5
    # Formula: H_nikah ≡ (3 - T) (mod 5) -> Mencari target sisa nilai weton nikah
    target_residue = (3 - t_gabungan) % 5
    
    daftar_hari_pernikahan_cocok = []
    for h, ns in SAPTAWARA.items():
        if h == "Minggu": continue # Hindari duplikasi karena 'Ahad' sudah dihitung
        for p, np in PANCAWARA.items():
            if (ns + np) % 5 == target_residue:
                daftar_hari_pernikahan_cocok.append(f"{h} {p} (Neptu: {ns + np})")
                
    return {
        "neptu1": neptu1,
        "neptu2": neptu2,
        "t_gabungan": t_gabungan,
        "r": r,
        "kategori": kategori,
        "interpretasi": interpretasi,
        "target_residue": target_residue,
        "hari_pernikahan": daftar_hari_pernikahan_cocok
    }


def main():
    print("="*60)
    print("  SIMULASI OPTIMASI ALGORITMA PERJODOHAN WETON JAVANESE  ")
    print("        Berbasis Teori Himpunan & Aritmatika Modular     ")
    print("="*60)
    
    # Mengambil Input Data Orang Pertama
    nama1 = input("\nMasukkan Nama Orang ke-1           : ").strip()
    weton1 = dapatkan_input_weton("Masukkan Weton Orang ke-1 (H-P)    : ")
    
    # Mengambil Input Data Orang Kedua
    nama2 = input("\nMasukkan Nama Orang ke-2           : ").strip()
    weton2 = dapatkan_input_weton("Masukkan Weton Orang ke-2 (H-P)    : ")
    
    # Jalankan Perhitungan
    hasil = hitung_simulasi_matchmaking(nama1, weton1, nama2, weton2)
    
    print("\n" + "="*50)
    print("           HASIL EVALUASI KOMPATIBILITAS          ")
    print("="*50)
    print(f"• Neptu {nama1} ({weton1[0]} {weton1[1]}) : {hasil['neptu1']}")
    print(f"• Neptu {nama2} ({weton2[0]} {weton2[1]}) : {hasil['neptu2']}")
    print(f"• Total Akumulasi Neptu (T)      : {hasil['t_gabungan']}")
    print(f"• Nilai Residu Kongruensi (R)    : {hasil['r']} (T mod 8)")
    print(f"• KATEGORI KESERASIAN            : \033[1;32m{hasil['kategori']}\033[0m")
    print(f"  [Interpretasi]: {hasil['interpretasi']}")
    print("-"*50)
    print("      DAFTAR KORDINAT WETON PERNIKAHAN IDEAL      ")
    print("      (Berdasarkan Nilai Target Gedhong/Wealth)    ")
    print("-"*50)
    print(f"Target Rumus: (T + H_nikah) ≡ 3 (mod 5)")
    print(f"Hasil Sisa Target Komplemen: {hasil['target_residue']}")
    print(f"Pilihan Weton Hari Pernikahan yang Cocok:")
    
    for idx, hari in enumerate(hasil['hari_pernikahan'], 1):
        print(f"  {idx}. {hari}")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program dihentikan secara paksa oleh pengguna.")
        sys.exit(0)