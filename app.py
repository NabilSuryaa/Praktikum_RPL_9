import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.model import Base
from repositories.repository import MahasiswaRepository
from services.service import PrediksiService
from views import components

# 1. Konfigurasi halaman web
st.set_page_config(page_title="PrediksiKu", page_icon="🎓", layout="wide")

MENU = ["Prediksi", "Riwayat", "Tentang"]


def muat_css():
    """Memuat gaya tampilan dari styles/style.css."""
    file_css = Path(__file__).parent / "styles" / "style.css"
    st.markdown(f"<style>{file_css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_resource
def inisialisasi_database():
    load_dotenv()
    engine = create_engine(
        os.getenv("DATABASE_URL", "sqlite:///data_prediksi.db"),
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def ubah_data_ke_baris(data_db) -> list[dict]:
    return [
        {"Nama": d.nama, "IPK": d.ipk, "SKS": d.sks, "Status": d.status_kelulusan}
        for d in reversed(data_db)  # terbaru di atas
    ]


def proses_prediksi(nama: str, ipk: float | None, sks: int | None):
    """Validasi, prediksi lewat service, simpan lewat repository."""
    if nama.strip() == "":
        st.warning("⚠️ Nama tidak boleh kosong!")
        return
    if ipk is None or sks is None:
        st.warning("⚠️ IPK dan Total SKS wajib diisi!")
        return
    status = service.tentukan_kelulusan(ipk, sks)
    repo.simpan_data(nama.strip(), ipk, sks, status)
    st.session_state["hasil"] = {"nama": nama.strip(), "ipk": ipk, "sks": sks, "status": status}
    st.toast("Data berhasil disimpan!")


def tampilkan_form():
    with st.form("form_input"):
        st.markdown('<div class="card-title">Data Mahasiswa</div>', unsafe_allow_html=True)
        nama = st.text_input("Nama Mahasiswa", placeholder="Contoh: Budi Santoso")
        ipk = st.number_input(
            "IPK (0.0 - 4.0)", min_value=0.0, max_value=4.0, value=None, step=0.01, format="%.2f", placeholder="0.00"
        )
        sks = st.number_input("Total SKS", min_value=0, value=None, step=1, placeholder="0")
        tombol_proses = st.form_submit_button("Prediksi & Simpan")
    if tombol_proses:
        proses_prediksi(nama, ipk, None if sks is None else int(sks))


def tampilkan_hasil(baris: list[dict]):
    hasil = st.session_state.get("hasil")
    if hasil:
        st.markdown(components.kartu_status_hasil(hasil, service.BATAS_IPK_MINIMAL, service.BATAS_SKS_MINIMAL), unsafe_allow_html=True)
    else:
        st.markdown(components.kartu_status_menunggu(), unsafe_allow_html=True)
    st.markdown(components.tabel_riwayat(baris), unsafe_allow_html=True)


muat_css()
db_session = inisialisasi_database()
repo = MahasiswaRepository(db_session)
service = PrediksiService()

# 2. Navigasi atas (logo + menu)
kolom_logo, kolom_menu = st.columns([3, 2])
kolom_logo.markdown(components.navbar_brand(), unsafe_allow_html=True)
with kolom_menu:
    menu = st.radio("Menu", MENU, horizontal=True, label_visibility="collapsed", key="menu")

# 3. Isi halaman
if menu == "Prediksi":
    kiri, kanan = st.columns([1.1, 1.4], gap="large")
    with kiri:
        st.markdown(
            components.hero(
                "Sistem Prediksi Kelulusan",
                "Masukkan data mahasiswa, sistem akan menentukan kelulusan dan menyimpannya ke database.",
            ),
            unsafe_allow_html=True,
        )
        tampilkan_form()
    with kanan:  # dirender setelah form agar langsung memuat data terbaru
        tampilkan_hasil(ubah_data_ke_baris(repo.ambil_semua_data()))
elif menu == "Riwayat":
    st.markdown(components.tabel_riwayat(ubah_data_ke_baris(repo.ambil_semua_data())), unsafe_allow_html=True)
else:
    st.markdown(components.halaman_tentang(), unsafe_allow_html=True)
