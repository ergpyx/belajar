# Belajar Kosakata dan Bunpou

Folder ini menyimpan data belajar dari N5 sampai N1. Halaman hasil ada di `dist/index.html`.

## Struktur

```
belajar/
├── data/
│   ├── kotoba/     # file kosakata, misalnya kotoba-n5.json, kotoba-n4.json, ...
│   └── bunpou/     # file pola bunpou, misalnya bunpou-n5.json, bunpou-n4.json, ...
├── template/
│   └── reader.html # tampilan halaman, jangan diubah kecuali tahu apa yang diubah
├── build.py        # menggabungkan semua data menjadi satu halaman
└── dist/
    └── index.html  # hasil build, siap dibuka atau diterbitkan
```

## Penamaan file

Tingkat JLPT diambil dari nama file, jadi nama harus mengikuti pola ini:

- `kotoba-n5.json`, `kotoba-n4.json`, ..., `kotoba-n1.json`
- `bunpou-n5.json`, `bunpou-n4.json`, ..., `bunpou-n1.json`

Satu tingkat boleh punya lebih dari satu file, misalnya `kotoba-n5-bab1.json` dan `kotoba-n5-bab2.json`. Semua file dengan tingkat yang sama digabung.

File yang namanya tidak punya tingkat akan dilewati dan diberi peringatan saat build.

## Cara menambah data

1. Taruh file JSON di `data/kotoba/` atau `data/bunpou/` dengan nama yang benar.
2. Jalankan `python3 build.py`.
3. Buka `dist/index.html`.

Build akan menampilkan jumlah kosakata dan pola per tingkat, serta memberi peringatan untuk `id` ganda atau pola tanpa `grammar_point`.

## Format kosakata (`data/kotoba/*.json`)

Berupa daftar (array). Setiap entri:

| Field | Wajib | Keterangan |
|---|---|---|
| `id` | ya | angka unik, tidak boleh sama antar file |
| `word` | ya | penulisan kanji atau kana |
| `reading` | ya | bacaan dalam kana |
| `furigana` | tidak | misalnya `食[た]べる` |
| `pos` | tidak | daftar kelas kata, misalnya `["Noun"]` |
| `senses` | tidak | daftar arti: `{"n": 1, "meanings": ["..."], "notes": ["..."]}` |
| `tags` | tidak | daftar tag bebas |

Field `level` diisi otomatis dari nama file.

## Format bunpou (`data/bunpou/*.json`)

Berupa daftar (array). Setiap pola:

| Field | Wajib | Keterangan |
|---|---|---|
| `id` | ya | angka unik |
| `grammar_point` | ya | nama pola, misalnya `～です` |
| `romaji` | tidak | |
| `jlpt_level` | tidak | diisi otomatis dari nama file jika kosong |
| `meaning` | tidak | arti pola dalam bahasa Indonesia |
| `usage_notes` | tidak | daftar catatan |
| `connection_rule` | tidak | daftar cara menyambung |
| `conjugations` | tidak | daftar `{"label", "polite", "plain"}` |
| `examples` | tidak | daftar `{"japanese", "furigana", "translation"}` |

## Data dummy

`kotoba-n5.json`, `kotoba-n4.json`, `bunpou-n5.json`, dan `bunpou-n4.json` hanya contoh. Hapus atau ganti dengan data Anda.
