## Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu) 
---
# 1. Metro Ağı Rota Planlayıcısı

Bu projede, Ankara'daki metro hatları üzerinde bir metro ağı simülasyonu gerçekleştirilmiştir. Kullanıcıların belirli bir başlangıç ve varış istasyonu arasında en az aktarmalı veya en hızlı rotayı bulmalarını sağlayan algoritmalar entegre edilmiştir. Ek olarak, metro ağı ve bulunan rotalar matplotlib ve NetworkX kütüphaneleri ile görsel olarak sunulmuştur.

# 2. Kullanılan Teknolojiler ve Kütüphaneler

-> collections:  
  --> defaultdict: Hat bazlı istasyonları organize etmek için kullanıldı.  
  --> deque: BFS algoritmasında kuyruk veri yapısı olarak kullanıldı.  

-> heapq: A* algoritması için öncelik kuyruğu (priority queue) olarak kullanıldı. En düşük maliyetli rotayı öncelikli seçer.  

-> matplotlib.pyplot: Rotaların ve metro ağının grafiksel olarak gösterimi için kullanıldı.  

-> networkx: Metro ağının çoklu yönlü grafik yapısı ile modellenmesi ve görselleştirilmesi sağlandı.


# 3. Algoritmaların Çalışma Mantığı

📌 Temel Prensip:  
BFS, başlangıç noktasından itibaren bir grafın tüm komşularını, sonra onların komşularını (yani seviyeye göre) sırayla ziyaret eder. Her bir düğümün hedefe olan uzaklığı eşitse (örneğin, bir gridde her hareketin maliyeti eşitse), BFS en kısa yolu bulur.

🔧 Nasıl Çalışır?

Kuyruğa (deque) başlangıç istasyonu ekler.

Her adımda, mevcut istasyonun komşularını kontrol eder.

Daha önce gidilmemiş istasyonlar kuyruk sonuna eklenir.

Hedef istasyona ulaşılırsa o ana kadarki yol dönülür.  

Örnek:  
![image](https://github.com/user-attachments/assets/80037444-83f1-4efd-a795-086900225534)

Başlangıçta 0 ziyaret edilir → Output: [0]  

0'ın komşuları sırayla kuyruğa eklenir: 2, 3, 1  

Kuyruktan ilk eleman 2 çıkarılır ve ziyaret edilir → Output: [0, 2]  

2'nin komşusu olan 4 kuyruğa eklenir  

Sıradaki eleman 3 ziyaret edilir → Output: [0, 2, 3]  

Sıradaki eleman 1 ziyaret edilir → Output: [0, 2, 3, 1]  

Son olarak kuyruktaki 4 ziyaret edilir → Output: [0, 2, 3, 1, 4]  

---


A* (A Yıldız) Algoritması - En Hızlı Rota

📌 Temel Prensip:  
A* algoritması, BFS gibi düğümleri genişletir ama bunu daha akıllı bir şekilde yapar. Hedefe daha yakın olan düğümleri öncelikli olarak arar. Bunu bir heuristic (sezgisel) ile sağlar. En kısa ve en verimli yolu bulmaya çalışır.  

🔧 Nasıl Çalışır?

A* algoritması, her düğüm için şu maliyet fonksiyonunu kullanır: f(n) = g(n) + h(n)  

g(n): Başlangıçtan şu ana kadar olan gerçek maliyet (örneğin, adım sayısı), genellikle Manhattan mesafesi, Euclidean mesafesi, ya da başka uygun bir heuristic fonksiyon olabilir.
h(n): Hedefe olan tahmini maliyet (heuristic), değeri en düşük olan düğüm ilk olarak genişletilir.  

Örnek:

![image](https://github.com/user-attachments/assets/21f4f6a5-7d42-4371-906d-9814eec585e3)

#### s Düğümünden Başla:  
s'in komşuları: a (3), b (2)  

Hesaplayalım:  
f(a) = g(a) + h(a) = 3 + 3 = 6  
f(b) = 2 + 3 = 5  

En küçük f değeri b, yani b seçilir.  

#### b Düğümünden Devam Et:  
b'nin komşuları: a (3), c (5), d (3)  
g(b) = 2 olduğu için:  
g(a) = 2 + 3 = 5, f(a) = 5 + 3 = 8  
g(c) = 2 + 5 = 7, f(c) = 7 + 0 = 7  
g(d) = 2 + 3 = 5, f(d) = 5 + 0 = 5  

Şimdi olası yollar:  
a → 8
c → 7
d → 5

En küçük f = 5, d seçilir.  

#### Hedefe Ulaşıldı:  
d düğümüne ulaşıldı. Bu yol izlenmiştir:  
s → b → d
Toplam maliyet: s → b (2) + b → d (3) = 5

---

# 4. Örnek Kullanım ve Test Sonuçları

Örnek Kullanım: 

![1a](https://github.com/user-attachments/assets/1cd055c6-0a3e-4374-bb7b-cca9b12acef7)


Metro Simülasyonunun Görselleştirilmesi:  
Aşağıda belirlenen üç farklı senaryo için en az aktarma yapılan ve en hızlı rotalar grafiklerle gösterilmiş ve detaylarıyla açıklanmıştır.  

1. AŞTİ'den OSB'ye  
En Az Aktarmalı Rota  
Rota: AŞTİ → Kızılay → Kızılay (aktarma) → Ulus → Demetevler → OSB  

Görsel: ![2a](https://github.com/user-attachments/assets/d6d15809-c17e-4219-b5d0-7cbf6ce75b49)

En Hızlı Rota  
Rota: AŞTİ → Kızılay → Kızılay (aktarma) → Ulus → Demetevler → OSB  

Süre: 25 dakika  

Görsel: ![3a](https://github.com/user-attachments/assets/f74aba83-c79f-467b-b4de-2543e39cab85)

---

2. Batıkent'ten Keçiören'e  
En Az Aktarmalı Rota  
Rota: Batıkent → Demetevler → Gar → Keçiören  

Görsel:![4a](https://github.com/user-attachments/assets/4c5cddce-e081-4712-801e-d69815005df6)


En Hızlı Rota  
Rota: Batıkent → Demetevler → Gar → Keçiören  

Süre: 21 dakika  

Görsel:![5a](https://github.com/user-attachments/assets/7da157a0-1370-4e1a-b272-ed14cada330d)


---

3. Keçiören'den AŞTİ'ye  
En Az Aktarmalı Rota  
Rota: Keçiören → Gar → Gar (aktarma) → Sıhhiye → Kızılay → AŞTİ  

Görsel:![6a](https://github.com/user-attachments/assets/61302001-9d8d-4971-bf78-8808655e834d)

En Hızlı Rota  
Rota: Keçiören → Gar → Gar (aktarma) → Sıhhiye → Kızılay → AŞTİ  

Süre: 19 dakika  

Görsel:![7a](https://github.com/user-attachments/assets/822da784-6957-4778-b61a-844f6195919f)

---

# 5. Projeyi Geliştirme Fikirleri

Gerçek Zamanlı Trafik Verisi: A* algoritması, anlık trafik veya bekleme süreleri ile entegre edilebilir.  
Farklı Hesaplama Modları: Engelli dostu rota, az yürüme mesafesi, minimum yırıma gibi tercihler eklenebilir.  
