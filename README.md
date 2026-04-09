# Üretim Toplantı Analiz Sistemi

Bu proje, günlük üretim toplantıları için kullanılan Excel verisini otomatik olarak analiz eden, özetleyen ve görselleştiren bir Flask uygulamasıdır.

Amaç, dağınık ve yoruma açık ham veriyi birkaç saniye içinde:

- okunabilir bir yönetim özetine,
- parametre bazlı performans kartlarına,
- kritik ve olumlu çıkarımlara,
- trend grafiklerine,
- isteğe bağlı AI değerlendirmesine

dönüştürmektir.

## Proje Ne Yapar?

Sistem, yüklenen Excel dosyasındaki üretim verilerini okuyup aşağıdaki işleri yapar:

1. Excel içindeki `Veriler` sayfasını işler.
2. Tarih sütunlarını otomatik bulur.
3. Veriyi analiz için uygun uzun formata çevirir.
4. Hedef satırlarını gerçekleşen satırlarla eşleştirir.
5. Her parametre için:
   - güncel değer,
   - ortalama,
   - maksimum,
   - minimum,
   - hedef,
   - hedefe göre karşılaştırma
   üretir.
6. Günlük toplantı mantığına göre yorumlanacak günü otomatik seçer:
   - İSG / Kalite / Üretim için veri olan son gün
   - Planlama için veri olan son gün
7. Kural bazlı çıkarımlar üretir:
   - kritik durumlar,
   - olumlu performanslar,
   - hedef altı / hedef üstü durumlar
8. Her parametre için trend grafiği oluşturur.
9. İstenirse Ollama üzerinden yönetici diliyle kısa AI değerlendirmesi üretir.

## Bu Sistem Neyi Bulur?

Sistem yalnızca sayıları göstermiyor; verideki anlamlı durumları bulup toplantı için aksiyona çevrilebilir hale getiriyor.

Bulduğu başlıca durumlar:

- İSG tarafında kaza var mı, yok mu
- Kalite tarafında hurda oranı hedefin üstünde mi altında mı
- Üretim tarafında gerçekleşen miktarlar hedefe ulaştı mı
- Planlama tarafında stok ve eksik yükler kritik eşikleri aştı mı
- Hangi parametreler olumlu gidiyor
- Hangi parametreler müdahale istiyor
- Hangi alanlar toplantıda önce konuşulmalı

Örnek olarak sistem şu tip çıktılar üretebilir:

- `Demir-Çelik Hurda % | Hedefin üstünde`
- `Bronz Döküm Kg | Hedefin altında`
- `Taşlama Stoğu Ton | 22.9T > 20T`
- `Kümülatif kaza sayısı | Sıfır kaza`

## Ne İşe Yarar?

Bu proje özellikle sabah üretim toplantılarında zaman kazandırır.

Normalde mühendis veya planlama ekibi:

- Excel dosyasını açar,
- doğru günü seçer,
- hedefleri kontrol eder,
- kritik sapmaları arar,
- grafik üretir,
- toplantıda hangi konulara öncelik verileceğini belirler.

Bu sistem bu süreci otomatikleştirir.

Sağladığı faydalar:

- Ham veriyi hızlı okunur hale getirir
- Toplantı öncesi hazırlık süresini kısaltır
- Kritik sapmaları otomatik yakalar
- Olumlu performansı da görünür kılar
- Tüm parametreleri tek ekranda toplar
- Trendleri görsel olarak gösterir
- AI özeti ile yönetim diliyle kısa değerlendirme sunar

## Beklenen Veri Yapısı

Sistem, Excel içinde `Veriler` adında bir sayfa bekler.

Beklenen temel kolon yapısı:

| Kategori | Parametre | 2026-03-01 | 2026-03-02 | ... |
|----------|-----------|------------|------------|-----|
| Kalite   | Bronz Hurda % | 0.4 | 0.5 | ... |
| Kalite   | Bronz Hurda Hedefi % | 0.5 | 0.5 | ... |
| Üretim   | Bronz Döküm Kg | 1200 | 1300 | ... |

Kurallar:

- İlk sütun `Kategori`
- İkinci sütun `Parametre`
- Sonraki sütunlar tarih kolonları
- Hedef satırları varsa sistem bunları otomatik eşleştirir

## Desteklenen Kategori Mantığı

Sistem şu kategorileri özellikle tanır:

- İSG
- Kalite
- Üretim
- Planlama

Bu kategoriler için farklı analiz mantıkları uygulanır.

### İSG

- Kaza var mı yok mu kontrol edilir
- Sıfır kaza olumlu kayıt olarak işlenir
- Kaza varsa kritik kayıt oluşturulur

### Kalite

- Gerçekleşen değer hedefle kıyaslanır
- Hedefin üstü kritik, altı olumlu olarak işaretlenir

### Üretim

- Gerçekleşen miktar hedefle kıyaslanır
- Hedef altı kritik, hedef üstü olumlu olarak işaretlenir

### Planlama

- Tanımlı eşikler üzerinden aksiyon üretilir
- Örneğin:
  - Taşlama Stoğu Ton
  - Kumlama Stoğu Ton
  - Döküm eksiği
  - Mevcut sipariş
  - Fatura bekleyen hazır ürün

## Uygulama Ekranında Neler Var?

Sonuç ekranı dört ana bölümden oluşur:

### 1. Genel Sonuç

Üstte toplantı tarihi ve özet bilgi görünür:

- Kaç parametre analiz edildi
- Kaç çıkarım üretildi
- Kaç grafik üretildi
- AI özeti hazır mı

### 2. İnceleme

Her parametre için kart gösterilir:

- kategori
- parametre adı
- son tarih
- güncel değer
- ortalama
- maksimum
- minimum
- hedef
- hedefe göre karşılaştırma

Bu bölüm, sunumdaki “Genel Veri Özeti” mantığının web arayüzündeki karşılığıdır.

### 3. Çıkarımlar

Toplantıda konuşulması gereken yorumlar burada görünür.

Her kartta:

- kategori
- durum etiketi (`Kritik`, `İyi`, vb.)
- parametre
- ilişki bilgisi (`Hedefin altında`, `Hedefin üstünde`, `Sıfır kaza`, vb.)
- sayısal karşılaştırma
- yorum / aksiyon metni

### 4. Grafikler

Her parametre için ayrı trend grafiği bulunur.

Grafiklerde:

- gerçekleşen değer çizgisi
- varsa hedef çizgisi
- kategori etiketi
- grafik sırası

Grafikler sağ / sol butonlarıyla kart kart gezilebilir.

### 5. AI Değerlendirme

Ollama aktifse sistem kısa yönetici yorumu üretir.

Bu bölüm:

- rapor özeti,
- değerlendirme,
- öncelikli aksiyonlar

biçiminde gösterilir.

## Filtreleme Özellikleri

Arayüzde üç ana bölümde filtre vardır:

### İnceleme filtresi

- kategoriye göre filtreleme
- parametre adına göre arama

### Çıkarımlar filtresi

- kategoriye göre filtreleme
- duruma göre filtreleme (`Kritik`, `Olumlu`, vb.)
- yorum veya parametre adına göre arama

### Grafik filtresi

- kategoriye göre filtreleme
- grafik başlığına göre arama

## Mimari

Projede aktif olarak kullanılan ana dosyalar:

- [app.py](app.py)
  Flask uygulaması, dosya yükleme, sonuç sayfası ve AI HTML dönüşümü

- [analysis_engine.py](analysis_engine.py)
  Veri hazırlama, hedef eşleştirme, toplantı günü seçimi, yorum üretimi, özet kartları ve grafik üretimi

- [ollama_client.py](ollama_client.py)
  Ollama istemcisi ve AI prompt oluşturma

- [templates/index.html](templates/index.html)
  Başlangıç / yükleme ekranı

- [templates/result.html](templates/result.html)
  Sonuç ekranı

- [static/dashboard.css](static/dashboard.css)
  Tüm görsel tema ve bileşen stilleri

Not:

- `analyzer.py` dosyası repoda duruyor olsa da uygulamanın aktif analiz motoru `analysis_engine.py` dosyasıdır.

## Kurulum

### 1. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 2. İsteğe bağlı `.env` ayarları

AI özeti kullanmak istiyorsanız `.env` içinde Ollama ayarları tanımlanmalıdır:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=your-model-name
```

Bu ayarlar yoksa analiz ekranı yine çalışır; sadece AI özeti boş kalabilir.

### 3. Uygulamayı başlatın

```bash
python app.py
```

## Kullanım Akışı

1. Uygulamayı açın
2. Excel dosyasını yükleyin
3. Sistem dosyayı analiz etsin
4. Sonuç ekranında:
   - İnceleme
   - Çıkarımlar
   - Grafikler
   - AI değerlendirme
   bölümlerini kullanın
5. Gerekirse filtrelerle sonucu daraltın

## Projenin Toplantıdaki Karşılığı

Bu sistem aslında bir “rapor görüntüleyici” değil, toplantı asistanıdır.

Yani şunları aynı anda yapar:

- veriyi temizler
- hedefleri bağlar
- önemli günü seçer
- kritik ve olumlu durumları bulur
- sunum mantığında özet çıkarır
- trendleri gösterir
- yöneticinin konuşacağı dili hazırlar

Bu nedenle sistemin çıktısı sadece sayı listesi değil, karar destek ekranıdır.

## Özet

Bu proje:

- üretim Excel’ini okur,
- hedefleri eşleştirir,
- günlük toplantı gününü doğru seçer,
- tüm parametreleri özetler,
- kritik ve olumlu çıkarımlar üretir,
- grafiklerle trend gösterir,
- AI desteğiyle yönetici değerlendirmesi sunar.

Kısacası, sabah toplantısı için ham veri dosyasını okunabilir ve aksiyon alınabilir bir dijital rapora dönüştürür.
