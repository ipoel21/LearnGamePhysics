# Analisis Detail Bouncing Ball: Fisika, Logic, dan Perbandingan V1 vs V2

Dokumen ini menjelaskan isi `bouncingBall.py` secara rinci. Fokus pembahasannya adalah:

- apa yang dipelajari dari sisi fisika
- apa yang dipelajari dari sisi logika pemrograman
- bagaimana cara kerja `v1`
- bagaimana cara kerja `v2`
- apa perbedaan inti antara keduanya
- kenapa `v2` lebih bagus sebagai implementasi

## Gambaran Umum

File `bouncingBall.py` berisi dua fungsi:

- `runV1()` pada baris 4
- `runV2()` pada baris 70

Kedua fungsi sama-sama membuat simulasi bola yang bergerak vertikal, terkena gravitasi, menyentuh lantai, lalu memantul. Perbedaan besarnya ada pada cara pantulan dimodelkan.

## Pembahasan Fisika

### 1. Posisi dan kecepatan vertikal

Simulasi ini hanya berfokus pada gerak di sumbu `y`. Posisi horizontal `x` tetap, sedangkan `y` berubah terus.

Artinya:

- bola tidak bergerak ke kanan atau kiri
- seluruh perhatian diarahkan ke gerak naik-turun

Ini adalah bentuk paling sederhana dari simulasi fisika, tetapi sangat baik untuk belajar dasar-dasarnya.

### 2. Percepatan gravitasi

Di `v1`, gravitasi disimpan dalam variabel:

```python
grafity = 980
```

Di `v2`, gravitasi ditulis:

```python
gravity = 980
```

Makna `980` di sini dapat dipahami sebagai percepatan vertikal dalam satuan pixel per detik kuadrat. Ini bukan satuan fisika dunia nyata secara literal, tetapi representasi numerik yang cocok untuk layar.

Konsep pentingnya:

- gravitasi bukan langsung memindahkan posisi
- gravitasi terlebih dahulu menambah kecepatan jatuh

Itulah kenapa rumusnya bukan `y += gravity`, tetapi:

```python
velocity_y += gravity * dt
```

### 3. Integrasi waktu sederhana

Kedua versi memakai pendekatan numerik sederhana:

```python
velocity_y += gravity * dt
y += velocity_y * dt
```

Ini adalah pola **semi-implicit Euler** sederhana yang sangat umum dipakai untuk game kecil dan prototyping.

Maknanya:

1. hitung perubahan kecepatan karena gravitasi
2. gunakan kecepatan terbaru untuk mengubah posisi

Pendekatan ini cukup stabil untuk simulasi sederhana seperti bouncing ball.

### 4. Delta time (`dt`)

Kedua versi memakai:

```python
dt = clock.tick(165) / 1000
```

`clock.tick(165)` mengembalikan waktu antar frame dalam milidetik, lalu dibagi 1000 agar menjadi detik.

Kenapa ini penting:

- jika komputer cepat, frame bisa sangat rapat
- jika komputer lebih lambat, jarak antar frame bisa lebih besar
- tanpa `dt`, gerak bola akan berbeda antar komputer

Dengan `dt`, perhitungan fisika didasarkan pada waktu nyata, bukan jumlah frame.

### 5. Lantai sebagai batas gerak

Di `v1`:

```python
floor_y = HEIGHT - 25
```

Di `v2`:

```python
floor_y = HEIGHT - radius
```

Karena `y` adalah pusat lingkaran, maka bola menyentuh lantai saat pusatnya berada di `HEIGHT - radius`.

Di sinilah `v2` lebih kuat:

- ia menghubungkan posisi lantai dengan ukuran bola
- jika radius diganti, lantai tetap benar

Sedangkan `v1` memakai angka literal `25`, yang kebetulan sama dengan radius. Ini bekerja, tetapi tidak fleksibel.

### 6. Tumbukan dan respons tumbukan

Saat bola sudah mencapai lantai:

```python
if y >= floor_y:
    y = floor_y
```

Langkah ini punya dua fungsi:

- mendeteksi collision
- memperbaiki posisi agar bola tidak tenggelam ke bawah lantai

Setelah itu, tiap versi memberi respons yang berbeda.

## Cara Kerja V1

### Inti ide V1

`v1` membuat bola memantul dengan cara:

- saat menyentuh lantai, kecepatan di-reset ke `0`
- nilai `jump_power` dikurangi menjadi `80%` dari sebelumnya
- bola diberi kecepatan ke atas lagi dari `jump_power` yang sudah dikurangi

Bagian kuncinya ada di baris 50 sampai 59.

### Alur logika V1

1. Program membaca input.
2. Jika `SPACE` ditekan saat bola di lantai, `velocity_y` diisi `jump_power`.
3. Setiap frame, gravitasi menambah `velocity_y`.
4. Posisi `y` diperbarui.
5. Jika menyentuh lantai:
   - `velocity_y` di-set ke `0`
   - posisi dikunci ke `floor_y`
   - jika `loop_jump` masih aktif, `jump_power *= 0.8`
   - `velocity_y = jump_power`
6. Bola naik lagi dengan tenaga lebih kecil.

### Kelebihan V1

- mudah dipahami untuk tahap awal
- cocok sebagai eksperimen pertama
- menunjukkan konsep decay atau redaman
- cukup baik untuk membangun intuisi tentang loop dan state

### Kekurangan V1

#### 1. Pantulan tidak berasal dari kecepatan tumbukan aktual

Ini kelemahan terbesarnya.

Pada fisika sederhana, pantulan seharusnya bergantung pada kecepatan saat benda mengenai lantai. Namun di `v1`, kecepatan tumbukan tidak dipakai untuk menghitung pantulan. Program justru menggunakan `jump_power` yang disimpan dari awal lalu dikurangi manual.

Akibatnya:

- sistem terasa lebih scripted
- hubungan sebab-akibat fisik kurang natural
- pantulan tidak benar-benar merepresentasikan "energi saat impact"

#### 2. Ada state tambahan yang sebenarnya tidak wajib

`loop_jump` dipakai untuk menghentikan proses pantulan saat `jump_power >= -1`.

Ini bekerja, tetapi menambah kompleksitas yang bisa dihindari dengan pendekatan lain yang lebih langsung.

#### 3. Ada variabel tidak terpakai

Pada baris 45 dan 46:

```python
pre_y = y
pre_v_y = velocity_y
```

Kedua variabel ini tidak dipakai lagi. Ini biasanya tanda bahwa:

- ada ide debug atau eksperimen yang belum dibersihkan
- kode masih berada di fase eksplorasi

#### 4. Penamaan kurang rapi

Ada typo `grafity` dan judul window `"Belajar Grafitasi"`.

Ini tidak merusak program, tetapi mengurangi keterbacaan dan kesan rapih pada kode.

#### 5. Ketergantungan pada angka literal

`floor_y = HEIGHT - 25` bekerja hanya karena `radius = 25`.

Kalau radius diganti dan angka `25` lupa diperbarui, collision akan salah.

## Cara Kerja V2

### Inti ide V2

`v2` memperlakukan pantulan sebagai hasil langsung dari kecepatan saat tumbukan.

Saat bola menyentuh lantai:

- posisi diperbaiki ke `floor_y`
- jika kecepatan jatuh masih cukup besar, arah kecepatan dibalik
- besar kecepatannya dikurangi dengan faktor `bounce`
- jika terlalu kecil, gerakan dihentikan

Bagian kuncinya ada di baris 111 sampai 121.

### Alur logika V2

1. Program membaca input.
2. Jika `SPACE` ditekan saat bola berada di lantai, `velocity_y = jump_power`.
3. Setiap frame, gravitasi menambah `velocity_y`.
4. Posisi `y` diperbarui dari `velocity_y`.
5. Jika menyentuh lantai:
   - `y = floor_y`
   - jika `abs(velocity_y) > 50`, pantulkan:
     ```python
     velocity_y = -velocity_y * bounce
     ```
   - jika tidak, `velocity_y = 0`
6. Bola memantul makin kecil sampai akhirnya diam.

### Kenapa pendekatan ini lebih baik

#### 1. Pantulan berbasis kecepatan impact

Ini poin paling penting.

Nilai pantulan tidak lagi diambil dari "stok tenaga lompat", tetapi dari kondisi fisik sesaat sebelum tumbukan. Secara logika dan fisika, ini jauh lebih masuk akal.

#### 2. Parameter fisika lebih eksplisit

Di `v2` ada:

- `gravity`
- `jump_power`
- `bounce`

Masing-masing punya peran yang jelas:

- `gravity`: percepatan jatuh
- `jump_power`: impuls awal ke atas
- `bounce`: rasio kehilangan energi saat memantul

Ini membuat tuning perilaku jauh lebih mudah.

#### 3. Threshold kecil mencegah jitter

Tanpa ambang `abs(velocity_y) > 50`, bola bisa terus memantul sangat kecil atau bergetar karena error numerik kecil.

Threshold ini adalah keputusan praktis yang sangat umum dalam game development.

#### 4. Floor position lebih adaptif

`floor_y = HEIGHT - radius` jauh lebih aman daripada menulis angka tetap.

#### 5. Visual debugging lebih baik

`v2` menggambar garis lantai, sehingga:

- area collision terlihat jelas
- pemain bisa langsung memahami permukaan tempat bola memantul

## Perbandingan V1 vs V2 Secara Detail

### 1. Sumber energi pantulan

`v1`:

- memakai `jump_power` yang terus dikurangi
- pantulan tidak dihitung dari impact yang terjadi saat itu

`v2`:

- memakai `velocity_y` saat menabrak lantai
- pantulan adalah hasil langsung dari tumbukan

Kesimpulan: `v2` lebih fisikal, `v1` lebih scripted.

### 2. Cara menghentikan pantulan

`v1`:

- berhenti saat `jump_power >= -1`
- artinya yang dipantau adalah besar tenaga lompat yang tersisa

`v2`:

- berhenti saat `abs(velocity_y) <= 50`
- artinya yang dipantau adalah kondisi gerak aktual

Kesimpulan: `v2` lebih berbasis state nyata dari objek.

### 3. Keterbacaan kode

`v1` masih terasa seperti kode belajar:

- ada variabel sisa debug
- ada typo
- ada angka literal

`v2` lebih mudah dibaca karena:

- nama variabel lebih baik
- alur update diberi komentar
- collision dan pantulan lebih jelas

### 4. Skalabilitas

Jika nanti ingin menambah fitur seperti:

- banyak bola
- slider gravitasi
- gesekan udara
- collision antar objek

`v2` lebih mudah dikembangkan karena model mental kodenya lebih konsisten.

## Kenapa V2 Lebih Bagus

Secara keseluruhan, `v2` lebih bagus karena:

1. lebih dekat ke model fisika sederhana yang benar
2. lebih mudah dijelaskan secara sebab-akibat
3. lebih rapi secara struktur
4. lebih mudah di-tuning
5. lebih aman saat ukuran objek berubah
6. lebih siap dijadikan dasar pengembangan berikutnya

Kalau `v1` menjawab pertanyaan "bagaimana membuat bola terlihat memantul?", maka `v2` menjawab pertanyaan yang lebih baik: "bagaimana memodelkan pantulan dengan logika yang lebih masuk akal?"

## Hal-Hal Penting yang Dipelajari dari Sisi Logic

### 1. Event handling

Input keyboard dibaca dari event loop `pygame`. Ini melatih pemahaman bahwa game bersifat event-driven.

### 2. State management

Program menyimpan state penting seperti:

- posisi
- kecepatan
- status running
- parameter fisika

Seluruh perilaku game muncul dari perubahan state ini dari frame ke frame.

### 3. Update order matters

Urutan update sangat penting:

1. baca input
2. update kecepatan
3. update posisi
4. cek collision
5. render

Jika urutannya diacak, hasilnya bisa terasa salah atau glitch.

### 4. Guard condition

`SPACE` hanya boleh bekerja saat bola di tanah. Ini adalah contoh guard condition untuk mencegah aksi yang tidak valid.

### 5. Numerical stability

Simulasi real-time hampir selalu perlu aturan praktis seperti:

- clamp position
- speed threshold
- frame time normalization

`v2` menunjukkan kesadaran yang lebih baik terhadap stabilitas numerik dibanding `v1`.

## Catatan Kecil yang Masih Bisa Di-improve dari V2

Walaupun `v2` lebih baik, masih ada beberapa hal yang bisa ditingkatkan:

### 1. Debug print sebaiknya dihapus atau dijadikan opsional

Baris 117 sampai 119 mencetak nilai velocity setiap pantulan. Ini berguna saat belajar, tetapi untuk versi lebih bersih sebaiknya:

- dihapus, atau
- dikontrol dengan flag debug

### 2. Bisa dibuat lebih modular

Kalau project berkembang, logika bola bisa dipindahkan ke class seperti `Ball`.

### 3. Bisa ditambah konstanta bernama

Misalnya threshold `50` bisa dijadikan:

```python
min_bounce_speed = 50
```

Ini membuat maksud angka tersebut lebih jelas.

## Kesimpulan Akhir

Project ini sangat bagus untuk belajar dasar game physics karena mengajarkan hubungan langsung antara:

- percepatan
- kecepatan
- posisi
- collision
- bounce
- damping

`v1` penting karena menunjukkan proses belajar dan eksperimen pribadi. Dari versi ini terlihat pemahaman dasar sudah terbentuk: ada gravitasi, ada update posisi, ada pantulan bertahap, dan ada ide menghentikan gerakan.

`v2` lebih bagus karena membawa ide yang sama ke bentuk yang lebih matang. Pantulan tidak lagi "diatur manual" dari sisa tenaga lompat, tetapi muncul dari kecepatan tumbukan yang sedang terjadi. Inilah alasan utama `v2` terasa lebih benar, lebih bersih, dan lebih layak dijadikan versi utama.
