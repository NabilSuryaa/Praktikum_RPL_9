"""Komponen tampilan (HTML kecil) untuk View Layer.

Hanya membangun potongan HTML; tidak ada logika bisnis atau akses database.
"""
from html import escape

STATUS_LULUS = "Lulus Tepat Waktu"


def _kelas_badge(status: str) -> str:
    return "badge-lulus" if status == STATUS_LULUS else "badge-tidak"


def navbar_brand() -> str:
    return '<div class="brand"><span class="brand-dot"></span>PrediksiKu</div>'


def hero(judul: str, deskripsi: str) -> str:
    return (
        '<div class="chip">Praktikum RPL 9 • Clean Code &amp; SOLID</div>'
        f'<h1 class="hero-title">{escape(judul)}</h1>'
        f'<p class="hero-desc">{escape(deskripsi)}</p>'
    )


def kartu_status_menunggu() -> str:
    return (
        '<div class="status-card">'
        '<div class="status-icon icon-wait">•••</div>'
        '<div><div class="status-title">Menunggu input</div>'
        '<div class="status-sub">Isi form lalu tekan Prediksi &amp; Simpan untuk melihat status.</div>'
        "</div></div>"
    )


def kartu_status_hasil(hasil: dict, batas_ipk: float, batas_sks: int) -> str:
    lulus = hasil["status"] == STATUS_LULUS
    kelas = "icon-ok" if lulus else "icon-bad"
    simbol = "✓" if lulus else "✕"
    kalimat = "dinyatakan " + hasil["status"] + ("!" if lulus else ".")
    op_ipk = "≥" if hasil["ipk"] >= batas_ipk else "<"
    op_sks = "≥" if hasil["sks"] >= batas_sks else "<"
    detail = (
        f'IPK {hasil["ipk"]:.2f} {op_ipk} {batas_ipk} dan '
        f'Total SKS {hasil["sks"]} {op_sks} {batas_sks}. Data berhasil disimpan.'
    )
    return (
        f'<div class="status-card {"card-ok" if lulus else "card-bad"}">'
        f'<div class="status-icon {kelas}">{simbol}</div>'
        f'<div><div class="status-title">{escape(hasil["nama"])} {escape(kalimat)}</div>'
        f'<div class="status-sub">{escape(detail)}</div></div></div>'
    )


def tabel_riwayat(baris: list[dict], judul: str = "Riwayat Prediksi") -> str:
    if baris:
        isi = "".join(
            "<tr>"
            f'<td>{escape(b["Nama"])}</td><td>{b["IPK"]:.2f}</td><td>{b["SKS"]}</td>'
            f'<td><span class="badge {_kelas_badge(b["Status"])}">{escape(b["Status"])}</span></td>'
            "</tr>"
            for b in baris
        )
    else:
        isi = '<tr><td colspan="4" class="kosong">Belum ada riwayat prediksi.</td></tr>'
    return (
        '<div class="card">'
        f'<div class="card-head"><span class="card-title">{escape(judul)}</span>'
        f'<span class="count-pill">{len(baris)} data</span></div>'
        '<table class="tabel"><thead><tr><th>Nama</th><th>IPK</th><th>SKS</th><th>Status</th></tr></thead>'
        f"<tbody>{isi}</tbody></table></div>"
    )


def halaman_tentang() -> str:
    return (
        '<div class="card"><div class="card-head"><span class="card-title">Tentang Aplikasi</span></div>'
        '<p class="about">PrediksiKu menentukan kelulusan mahasiswa berdasarkan aturan: '
        "<b>IPK ≥ 3.0</b> dan <b>Total SKS ≥ 140</b> dinyatakan <i>Lulus Tepat Waktu</i>. "
        "Dibangun dengan arsitektur layered (View, Service, Repository, Model) "
        "menggunakan Streamlit dan SQLAlchemy.</p></div>"
    )
