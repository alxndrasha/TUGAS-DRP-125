import pandas as pd

df = pd.read_csv("world_bank_data_2025.csv")
print("Ukuran awal:", df.shape)
print("Contoh format country_id:", df["country_id"].unique()[:10])

# 1. Hapus tahun 2025 karena datanya kosong semua
df_clean = df[df["year"] <= 2024].copy()

# 2. Hapus negara/wilayah yang > 80% datanya kosong (seperti British Virgin Islands & Gibraltar)
indikator = df_clean.select_dtypes(include="float64").columns
rasio_kosong = df_clean.groupby("country_id")[indikator].apply(
    lambda g: g.isna().mean().mean()
)
negara_valid = rasio_kosong[rasio_kosong <= 0.80].index
df_clean = df_clean[df_clean["country_id"].isin(negara_valid)].copy()

# 3. Hapus kolom yang terlalu banyak kosong (> 70%, yaitu Public Debt)
kolom_drop = df_clean.columns[df_clean.isna().mean() > 0.70].tolist()
df_clean = df_clean.drop(columns=kolom_drop)
print("Kolom dihapus:", kolom_drop)

# 4. Urutkan data & isi celah 1 tahun yang bolong di tengah (interpolasi linear per negara)
df_clean = df_clean.sort_values(["country_id", "year"]).reset_index(drop=True)
kolom_float = df_clean.select_dtypes(include="float64").columns
df_clean[kolom_float] = df_clean.groupby("country_id")[kolom_float].transform(
    lambda s: s.interpolate(method="linear", limit=1, limit_area="inside")
)

# 5. Tambah kolom turunan agar angka lebih mudah dibaca di dashboard
df_clean["GDP (Billion USD)"] = (df_clean["GDP (Current USD)"] / 1e9).round(2)
df_clean["Fiscal Balance (% of GDP)"] = (
    df_clean["Government Revenue (% of GDP)"] - df_clean["Government Expense (% of GDP)"]
).round(2)

print("\nUkuran setelah cleaning:", df_clean.shape)
print("Jumlah negara tersisa :", df_clean["country_id"].nunique())
print("Rentang tahun tersisa  :", df_clean["year"].min(), "-", df_clean["year"].max())

# 6. Simpan hasil cleaning ke file CSV baru
df_clean.to_csv("world_bank_clean.csv", index=False)
print("\nFile 'world_bank_clean.csv' berhasil dibuat!")