import pandas as pd

df = pd.read_csv("world_bank_data_2025.csv")

print(df.shape)

print(df.head())

# cek kesehatan data
df.info()

# 1. gabungkan jumlah & persentase data kosong dalam satu tabel terurut
cek_kosong = pd.DataFrame({
    "jumlah_kosong": df.isnull().sum(),
    "persen_kosong (%)": (df.isnull().mean() * 100).round(2),
})
print("\n--- Ringkasan Data Kosong ---")
print(cek_kosong[cek_kosong["jumlah_kosong"] > 0].sort_values(by="persen_kosong (%)", ascending=False))

# 2. cek duplikasi baris dan kombinasi unik negara-tahun
print("\n--- Cek Duplikat ---")
print("Duplikat baris penuh   :", df.duplicated().sum())
print("Duplikat negara & tahun:", df.duplicated(subset=["country_id", "year"]).sum())

# 3. cek cakupan entitas negara dan rentang periode
kolom_pertama = df.columns[0]
print("\n--- Cakupan Negara & Tahun ---")
print(f"Total {kolom_pertama} unik :", df[kolom_pertama].nunique())
print("Total country_id unik  :", df["country_id"].nunique())
print(f"Rentang tahun          : {df['year'].min()} - {df['year'].max()}")

# 4. ringkasan statistik otomatis untuk seluruh kolom float64
print("\n--- Statistik Deskriptif Indikator ---")
indikator = df.select_dtypes(include="float64")
print(indikator.describe().T[["count", "mean", "50%", "min", "max"]].round(2))

# 5. cek anomali nilai negatif pada indikator yang seharusnya >= 0
kolom_non_negatif = [
    "GDP (Current USD)",
    "GDP per Capita (Current USD)",
    "Unemployment Rate (%)",
    "Public Debt (% of GDP)",
]
print("\n--- Cek Anomali Nilai Negatif ---")
print((df[kolom_non_negatif] < 0).sum())
# 6. cek distribusi kelengkapan data per tahun
print("\n--- Kelengkapan Data per Tahun (Indikator Utama) ---")
cek_tahun = df.groupby("year")[
    ["GDP (Current USD)", "Inflation (CPI %)", "Unemployment Rate (%)", "Public Debt (% of GDP)"]
].count()
print(cek_tahun)

# 7. cek konsistensi format teks pada kolom negara
print("\n--- Cek Konsistensi Penulisan Negara ---")
spasi_nama = (df[kolom_pertama].str.strip() != df[kolom_pertama]).sum()
kode_tidak_3_huruf = (df["country_id"].str.len() != 3).sum()
print("Spasi berlebih pada nama negara :", spasi_nama)
print("Kode country_id bukan 3 huruf   :", kode_tidak_3_huruf)

# 8. cek 10 negara dengan total data kosong terbanyak
print("\n--- 10 Negara dengan Data Paling Banyak Kosong ---")
kosong_per_baris = df[indikator.columns].isna().sum(axis=1)
kosong_per_negara = kosong_per_baris.groupby(df[kolom_pertama]).sum().sort_values(ascending=False)
print(kosong_per_negara.head(10))

# 9. cek sampel nilai ekstrem (outlier) untuk membedakan krisis ekonomi vs salah input
print("\n--- Sampel Nilai Ekstrem (Outlier) ---")
print("Top 3 Inflasi Tertinggi:")
print(df.nlargest(3, "Inflation (CPI %)")[[kolom_pertama, "year", "Inflation (CPI %)"]])

print("\nTop 3 Pertumbuhan PDB Terendah:")
print(df.nsmallest(3, "GDP Growth (% Annual)")[[kolom_pertama, "year", "GDP Growth (% Annual)"]])