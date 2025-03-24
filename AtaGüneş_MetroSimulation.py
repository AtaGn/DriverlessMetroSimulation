from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import matplotlib.pyplot as plt
import networkx as nx

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur
          
          Bu fonksiyonu tamamlayın:
          1. Başlangıç ve hedef istasyonların varlığını kontrol edin
          2. BFS algoritmasını kullanarak en az aktarmalı rotayı bulun
          3. Rota bulunamazsa None, bulunursa istasyon listesi döndürün
          4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın
          
          İpuçları:
          - collections.deque kullanarak bir kuyruk oluşturun, HINT: kuyruk = deque([(baslangic, [baslangic])])
          - Ziyaret edilen istasyonları takip edin
          - Her adımda komşu istasyonları keşfedin
        """

        # Başlangıç ve hedef istasyon sistemde yoksa rota aranmaz
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        # Başlangıç ve hedef istasyon nesneleri alınır
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # BFS için kuyruk yapısı kullanılır. 
        # Her eleman (şu anki istasyon, o ana kadar olan rota) şeklindedir
        kuyruk = deque([(baslangic, [baslangic])])

        # Ziyaret edilen istasyonlar kümesi: Aynı istasyonu tekrar ziyaret etmeyi engeller
        ziyaret_edilen = {baslangic}

        # Kuyruk boşalana kadar döngü devam eder
        while kuyruk:
            # Kuyruğun başından bir istasyon ve o ana kadarki rotası alınır
            mevcut, yol = kuyruk.popleft()

            # Hedef istasyona ulaşıldıysa, o ana kadarki yol doğrudan döndürülür
            if mevcut == hedef:
                return yol

            # Mevcut istasyonun komşuları (bağlantılı istasyonlar) döngüyle kontrol edilir
            for komsu, sure in mevcut.komsular:
                # Komşu daha önce ziyaret edilmemişse
                if komsu not in ziyaret_edilen:
                    ziyaret_edilen.add(komsu)  # Ziyaret edildi olarak işaretle
                    # Kuyruğa yeni komşuyu ve güncellenmiş rotayı ekle
                    kuyruk.append((komsu, yol + [komsu]))

        # Kuyruk tamamen boşaldıysa ve hedefe ulaşılmadıysa rota bulunamamıştır
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur
          
          Bu fonksiyonu tamamlayın:
          1. Başlangıç ve hedef istasyonların varlığını kontrol edin
          2. A* algoritmasını kullanarak en hızlı rotayı bulun
          3. Rota bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) tuple'ı döndürün
          4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın
          
          İpuçları:
          - heapq modülünü kullanarak bir öncelik kuyruğu oluşturun, HINT: pq = [(0, id(baslangic), baslangic, [baslangic])]
          - Ziyaret edilen istasyonları takip edin
          - Her adımda toplam süreyi hesaplayın
          - En düşük süreye sahip rotayı seçin
          """

        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # Öncelikli kuyruk: (toplam_sure, istasyon_id, istasyon_nesnesi, rota)
        # id(istasyon) burada heapq sıralamada eşitlik durumlarını çözmek için kullanılır
        pq = [(0, id(baslangic), baslangic, [baslangic])]

        # Ziyaret edilen istasyonlar ve en kısa süreyi takip etmek için sözlük
        ziyaret_edilen: Dict[str, int] = {baslangic.idx: 0}

        # Kuyruk boşalana kadar döngü devam eder
        while pq:
            toplam_sure, _, mevcut, yol = heapq.heappop(pq)

            # Hedef istasyona ulaşıldıysa rota ve süre döndürülür
            if mevcut == hedef:
                return (yol, toplam_sure)

            # Mevcut istasyonun tüm komşuları kontrol edilir
            for komsu, sure in mevcut.komsular:
                yeni_sure = toplam_sure + sure

                # Komşuya daha önce gidilmediyse veya daha kısa sürede ulaşılıyorsa güncelle
                if komsu.idx not in ziyaret_edilen or yeni_sure < ziyaret_edilen[komsu.idx]:
                    ziyaret_edilen[komsu.idx] = yeni_sure
                    heapq.heappush(pq, (yeni_sure, id(komsu), komsu, yol + [komsu]))

        # Hedefe ulaşan bir yol bulunamadıysa
        return None

    def ciz_rota(self, rota: List[Istasyon], baslik: str, index: int):
        """
        Verilen istasyon listesini (rota) ve tüm metro ağını 2D olarak çizer.
        Her hattı farklı renklerle, aktarma bağlantılarını ise kesikli çizgiyle gösterir.
        Kullanıcıya açık, kolay okunabilir bir görselleştirme sağlar.
        """

        # Çoklu yönlü bir grafik yapısı oluştur (aynı iki istasyon arasında birden fazla bağlantı olabilir)
        G = nx.MultiDiGraph()

        # Her istasyonun çizim için sabit bir (x, y) pozisyonu tanımlanır
        positions = {
            "K1": (0, 0), "K2": (1, 0), "K3": (2, 0), "K4": (3, 0),
            "M1": (0, -1), "M2": (1, -1), "M3": (2, -1), "M4": (3, -1),
            "T1": (0, 1), "T2": (1, 1), "T3": (2, 1), "T4": (3, 1)
        }

        # Her hattın istasyon sıralaması ve aktarma bağlantıları
        hatlar = {
            "Kırmızı Hat": ("K1", "K2", "K3", "K4"),
            "Mavi Hat": ("M1", "M2", "M3", "M4"),
            "Turuncu Hat": ("T1", "T2", "T3", "T4"),
            "Aktarma": [("K1", "M2"), ("K3", "T2"), ("M4", "T3")]
        }

        # Her hattın çizimde kullanılacak rengi
        colors = {
            "Kırmızı Hat": "red",
            "Mavi Hat": "blue",
            "Turuncu Hat": "orange",
            "Aktarma": "green"
        }

        # Tüm hatlar için bağlantılar (kenarlar) grafiğe eklenir
        for hat, stations in hatlar.items():
            if hat != "Aktarma":
                # Aynı hat içindeki istasyonları birbirine bağla
                for i in range(len(stations) - 1):
                    G.add_edge(stations[i], stations[i + 1], color=colors[hat], weight=2)
            else:
                # Aktarma hatları özel stil (kesikli çizgi) ile bağlanır
                for s1, s2 in stations:
                    G.add_edge(s1, s2, color=colors[hat], weight=1, style='dashed')

        # Tüm istasyon düğümleri grafa eklenir, etiketleri de istasyon adları olarak ayarlanır
        for node in positions:
            G.add_node(node, label=self.istasyonlar[node].ad)

        # Görselleştirme başlatılır
        plt.figure(figsize=(10, 5))

        # Düğümler (istasyon noktaları) çizilir – gri renkte
        nx.draw_networkx_nodes(G, positions, node_size=600, node_color="lightgray")

        # Her düğüme (istasyona) istasyon ismi etiketi eklenir
        labels = {k: self.istasyonlar[k].ad for k in positions}
        nx.draw_networkx_labels(G, positions, labels=labels, font_size=9)

        # Her kenar (bağlantı) tipi için ilgili stil ve renk ile çizim yapılır
        for u, v, k, data in G.edges(keys=True, data=True):
            style = data.get('style', 'solid')  # Stil belirtilmemişse varsayılan olarak düz çizgi
            nx.draw_networkx_edges(
                G, positions, edgelist=[(u, v)],
                edge_color=data['color'],
                width=data['weight'],
                style=style
            )

        # Verilen rota üzerindeki bağlantılar (kenarlar) siyah ve kalın çizilir
        path_edges = [(rota[i].idx, rota[i + 1].idx) for i in range(len(rota) - 1)]
        nx.draw_networkx_edges(
            G, positions, edgelist=path_edges,
            edge_color='black', width=3, style='solid'
        )

        # Grafik başlığı ve düzenlemeler
        plt.title(baslik)          # Grafiğin üstüne başlık eklenir
        plt.axis('off')            # Koordinat eksenleri gizlenir
        plt.tight_layout()         # Grafik öğeleri arasında boşluk bırakmadan sıkı yerleşim yapılır

        return plt                 # Oluşturulan grafik döndürülür (isteğe bağlı olarak kaydedilebilir veya gösterilebilir)


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 

    senaryolar = [
        ("M1", "K4", "AŞTİ -> OSB"),
        ("T1", "T4", "Batıkent -> Keçiören"),
        ("T4", "M1", "Keçiören -> AŞTİ")
    ]

    cizimler = []
    for i, (b, h, ad) in enumerate(senaryolar):
        rota1 = metro.en_az_aktarma_bul(b, h)
        if rota1:
            cizimler.append(metro.ciz_rota(rota1, f"{ad} - En Az Aktarma", i * 2 + 1))
        rota2 = metro.en_hizli_rota_bul(b, h)
        if rota2:
            rota, sure = rota2
            cizimler.append(metro.ciz_rota(rota, f"{ad} - En Hızlı", i * 2 + 2))

    for plt_obj in cizimler:
        plt_obj.show()
