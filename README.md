## Praktikum Rekayasa Perangkat Lunak (SSD1030) — **Pertemuan 9**

Perancangan Arsitektur, Mockup, dan Implementasi Standar Pengkodean (**Clean Code & SOLID**).

Aplikasi web sederhana untuk memprediksi kelulusan mahasiswa berdasarkan IPK dan total SKS, lalu menyimpan hasilnya ke database lokal dan menampilkannya sebagai riwayat.

<img width="1568" height="746" alt="image" src="https://github.com/user-attachments/assets/9f65c715-98ed-4d18-94ad-ed2cfdcdce0c" />
<img width="1568" height="744" alt="image" src="https://github.com/user-attachments/assets/3dce3eb4-f174-4b6b-ad89-6f2af863c826" />
<img width="1568" height="745" alt="image" src="https://github.com/user-attachments/assets/6fc62660-6662-45b8-b358-aada947802c3" />

## Fitur

- Form input: Nama Mahasiswa, IPK (0.0 – 4.0), dan Total SKS.
- Prediksi kelulusan otomatis dan penyimpanan data ke SQLite.
- Kartu status hasil prediksi dan tabel riwayat dengan lencana status.
- Navigasi menu: **Prediksi**, **Riwayat**, dan **Tentang**.
- Tampilan putih-biru mengikuti mockup Figma.

## Aturan Kelulusan

| Kondisi | Status |
| --- | --- |
| IPK ≥ 3.0 **dan** Total SKS ≥ 140 | Lulus Tepat Waktu |
| Selain itu | Tidak Lulus |

## Teknologi

- Python 3
- [Streamlit](https://streamlit.io/) — antarmuka web
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- SQLite — database lokal
- python-dotenv dan pandas

## Arsitektur (Layered, SOLID — Single Responsibility)

```
Praktikum_RPL_9/
├── app.py                      # View Layer: UI Streamlit & Dependency Injection
├── views/
│   └── components.py           # View Layer: potongan HTML tampilan
├── services/
│   └── service.py              # Service Layer: logika bisnis (aturan kelulusan)
├── repositories/
│   └── repository.py           # Repository Layer: simpan/ambil data
├── models/
│   └── model.py                # Model Layer: struktur tabel database
├── styles/
│   └── style.css               # Gaya tampilan
├── .streamlit/config.toml      # Tema Streamlit
├── .env                        # Konfigurasi database
└── requirements.txt
```

Alur data: `View (app.py)` → `Service` (hitung status) → `Repository` (simpan/ambil) → `Model` (tabel `mahasiswa`).

## Cara Menjalankan

1. Clone repo dan masuk ke foldernya:

   ```bash
   git clone https://github.com/USERNAME/Praktikum_RPL_9.git
   cd Praktikum_RPL_9
   ```

2. Instal library:

   ```bash
   pip install -r requirements.txt
   ```

3. Pastikan file `.env` berisi:

   ```
   DATABASE_URL=sqlite:///data_prediksi.db
   ```

4. Jalankan aplikasi:

   ```bash
   streamlit run app.py
   ```

Browser akan terbuka otomatis. Isi form lalu klik **Prediksi & Simpan**.

## Penerapan Clean Code & SOLID

| Aspek | Penerapan |
| --- | --- |
| SRP | Empat layer terpisah: model, repository, service, dan view. |
| Naming | Nama variabel dan fungsi deskriptif (`tentukan_kelulusan`, `simpan_data`, `BATAS_IPK_MINIMAL`). |
| Functions | Fungsi pendek dan fokus pada satu tugas. |
| Konstanta | Batas IPK dan SKS didefinisikan sebagai konstanta, tanpa magic number. |
| Integrasi UI | Streamlit berjalan, data tersimpan, dan tabel riwayat tampil. |

## Mockup

Mockup dirancang di Figma dengan dua kondisi: **Form Kosong** dan **Hasil Prediksi**. Tambahkan gambar ke folder `docs/` lalu tampilkan di sini:

```markdown
![Form Kosong](docs/mockup-state-1.png)
![Hasil Prediksi](docs/mockup-state-2.png)
```

## Penulis

Praktikum RPL 9 — Mata kuliah Rekayasa Perangkat Lunak (SSD1030).
