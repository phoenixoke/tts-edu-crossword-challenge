# TTS EDU: Crossword Challenge

Think - Solve - Complete - Win

Game teka-teki silang interaktif untuk Bahasa Indonesia kelas 7 (Fase D), materi **Teks Prosedur**. Dibuat untuk Papan Interaktif Digital (PID), laptop, tablet, dan HP.

## Cara pakai

Buka `index.html` di Chrome atau Edge. Tidak perlu server atau internet. Untuk GitHub Pages, aktifkan Pages dari branch `main` dan game langsung bisa diakses lewat tautan.

## Isi

- 10 paket bertahap (Pemanasan sampai Grand Finale), 7 sampai 14 kata per paket, 99 kata total.
- Setiap grid divalidasi otomatis saat game dibuka: nomor, panjang kata, huruf persilangan, dan keterhubungan grid.
- Mode Individu, Kelompok (dengan batas waktu diskusi opsional), dan Battle.
- Skor: +100 per kata benar, +300 paket selesai, +200 tanpa bantuan, +100 sebelum waktu habis. Jawaban salah tidak mengurangi skor.
- Bantuan: Hint Letter, Show Clue, Clear Word, Reveal Word.
- Panel guru: timer (5/7/10 menit atau kustom), kesulitan, bantuan, urutan pembukaan paket, kunci jawaban, hasil, reset skor, suara, layar penuh.
- Leaderboard, lencana pencapaian, ekspor CSV, dan cetak ringkasan.
- Progres tersimpan di penyimpanan lokal browser perangkat yang dipakai.

## Folder `source`

- `bank.py`: bank kata dan petunjuk per paket.
- `gen.py`: penyusun grid. Menolak susunan yang membuat deretan huruf tanpa petunjuk.
- `template.html` dan `build.py`: kerangka game dan perakit file tunggal.

Ilustrasi halaman pembuka dibuat dengan Gemini.

Game Design by prooflendi
