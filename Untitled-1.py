import random
from datetime import datetime, timedelta

class Node:
    def __init__(self, isim, mesafe, sure, ucret):
        self.isim = isim
        self.mesafe = mesafe
        self.sure = sure
        self.ucret = ucret * 2  # Fiyatı 2 katına çıkarıyoruz
        self.sonraki = None
        self.otobusler = []  # Her varış noktası için otobüs kalkış saatleri

    def otobus_kalkis_ekle(self, kalkis_saati, peron_numarasi):
        self.otobusler.append((kalkis_saati, peron_numarasi))

    def otobus_kalkislari_goster(self):
        print(f"\n{self.isim} varış noktasına kalkacak otobüslerin saatleri ve peron numaraları:")
        for i, (kalkis_saati, peron_numarasi) in enumerate(self.otobusler):
            varis_saati = otobus_gelme_suresi(self.mesafe, kalkis_saati)
            print(f"{i + 1}. Otobüs Kalkış Saati: {kalkis_saati.strftime('%H:%M')}, Varış Saati: {varis_saati.strftime('%H:%M')}, Peron: {peron_numarasi}")

class LinkedList:
    def __init__(self):
        self.baslangic = None

    def destinasyon_ekle(self, isim, mesafe, sure, ucret):
        yeni_node = Node(isim, mesafe, sure, ucret)
        if not self.baslangic:
            self.baslangic = yeni_node
        else:
            gecici = self.baslangic
            while gecici.sonraki:
                gecici = gecici.sonraki
            gecici.sonraki = yeni_node

    def destinasyonlari_goster(self):
        gecici = self.baslangic
        print("Mevcut varış noktaları:")
        index = 1
        while gecici:
            print(f"{index}. {gecici.isim} - Mesafe: {gecici.mesafe} km, Süre: {gecici.sure} dakika, Ücret: {gecici.ucret} TL")
            gecici.index = index  # Her düğüme bir sıra numarası ekliyoruz
            index += 1
            gecici = gecici.sonraki

    def destinasyon_bul_numaradan(self, numara):
        gecici = self.baslangic
        while gecici:
            if getattr(gecici, "index", None) == numara:
                return gecici
            gecici = gecici.sonraki
        return None

def temassiz_odeme(ucret):
    print(f"Temassız kart ile {ucret} TL ödeniyor...")
    return random.choice([True, False])

def manuel_odeme(ucret):
    while True:
        kart_numarasi = input("Lütfen kart numaranızı girin (16 haneli): ")
        if len(kart_numarasi) != 16 or not kart_numarasi.isdigit():
            print("Hata: Kart numarası 16 haneli olmalı ve sadece rakamlardan oluşmalı.")
            continue

        son_kullanim = input("Lütfen kartınızın son kullanım tarihini (AA/YY) girin: ")
        try:
            ay, yil = map(int, son_kullanim.split('/'))
            if ay < 1 or ay > 12:
                print("Hata: Ay değeri 01 ile 12 arasında olmalı.")
                continue
        except ValueError:
            print("Hata: girdiğiniz sayıları kontrol edip tekrar deneyiniz (AA/YY).")
            continue

        cvv = input("Lütfen kartınızın CVV numarasını girin (3 haneli): ")
        if len(cvv) != 3 or not cvv.isdigit():
            print("Hata: girdiğiniz sayılar hatalı lütfen 3 haneli cvv numarasını girip tekrar deneyiniz.")
            continue

        print(f"Kart bilgileriniz ile {ucret} TL ödeniyor...")
        print("Ödeme başarılı! Şimdi otobüse binebilirsiniz.")
        break  # Ödeme başarılı, işlemi bitir

def odeme_islemi(ucret):
    print("\u00d6deme Yöntemi: Temassız Kart")
    if temassiz_odeme(ucret):
        print("Temassız ödeme başarılı!")
    else:
        print("Temassız ödeme başarısız oldu. Kart bilgilerinizi girmeniz gerekiyor.")
        manuel_odeme(ucret)

def otobus_gelme_suresi(mesafe, kalkis_saati):
    # Kilometre başına 5 dakika hızla hesaplama
    sure = mesafe * 5
    varis_saati = kalkis_saati + timedelta(minutes=sure)
    return varis_saati

def otobus_geliyor_mu():
    if random.choice([True, False]):
        print("Otobüs geldi.")
    else:
        print("Otobüs gecikecek, gecikme için özür dileriz.")

def bilet_tarihi_ile_gecerliligi_kontrol_et(bilet_tarihi):
    bugun = datetime.now()
    if bilet_tarihi.date() == bugun.date():
        print("Bilet geçerli!")
        return True
    else:
        print(f"Bilet geçersiz! Bilet tarihi: {bilet_tarihi.strftime('%d/%m/%Y')}")
        return False

def odeme_yontemi_sor(ucret):
    # Ödeme yöntemini soruyoruz
    while True:
        secim = input("Ödeme yöntemi seçin (1: Temassız Kart, 2: Manuel Kart Bilgisi): ")
        if secim == "1":
            print("Temassız kart ile ödeme yapılacak...")
            if temassiz_odeme(ucret):
                print("Temassız ödeme başarılı!")
                break
            else:
                print("Temassız ödeme başarısız oldu. Kart bilgilerinizi girmeniz gerekiyor.")
                manuel_odeme(ucret)
                break
        elif secim == "2":
            manuel_odeme(ucret)
            break
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

def bilet_goster(bilet_bilgisi):
    """Bilet bilgisini çerçeveli şekilde göstermek için kullanılan fonksiyon"""
    bugun = datetime.now().strftime('%d/%m/%Y')  # Bugünün tarihini alıyoruz
    print("\n" + "=" * 40)
    print(f"            BİLET BİLGİLERİ")
    print("=" * 40)
    print(f"Tarih: {bugun}")
    print(f"Varış Noktası: {bilet_bilgisi['varis_noktasi']}")
    print(f"Kalkış Saati: {bilet_bilgisi['kalkis_saati']}")
    print(f"Peron: {bilet_bilgisi['peron']}")
    print(f"Ücret: {bilet_bilgisi['ucret']} TL")
    print("=" * 40)

def main():
    destinasyonlar = LinkedList()
    destinasyonlar.destinasyon_ekle("Beşiktaş", 12, 30, 96.0)
    destinasyonlar.destinasyon_ekle("Kadıköy", 20, 45, 160.0)
    destinasyonlar.destinasyon_ekle("Avcılar", 15, 40, 120.0)
    destinasyonlar.destinasyon_ekle("Beylikdüzü", 25, 50, 200.0)
    destinasyonlar.destinasyon_ekle("Üsküdar", 10, 25, 80.0)
    destinasyonlar.destinasyon_ekle("İncirli", 18, 35, 144.0)
    destinasyonlar.destinasyon_ekle("Mecidiyeköy", 8, 20, 64.0)
    destinasyonlar.destinasyon_ekle("Eminönü", 14, 28, 112.0)
    destinasyonlar.destinasyon_ekle("Taksim", 16, 32, 128.0)
    destinasyonlar.destinasyon_ekle("Bakırköy", 22, 50, 176.0)
    destinasyonlar.destinasyon_ekle("Levent", 9, 22, 72.0)

    kalkis_saati = datetime.strptime("08:00", "%H:%M")
    gecici = destinasyonlar.baslangic
    while gecici:
        for i in range(10):  # 10 otobüs ekleniyor
            peron_numarasi = random.randint(1, 10)  # Rastgele peron numarası
            gecici.otobus_kalkis_ekle(kalkis_saati + timedelta(minutes=10 * i), peron_numarasi)
        gecici = gecici.sonraki

    destinasyonlar.destinasyonlari_goster()

    try:
        secilen_numara = int(input("\nLütfen gideceğiniz varış noktasının numarasını girin: "))
        secilen = destinasyonlar.destinasyon_bul_numaradan(secilen_numara)
        if secilen:
            print(f"\nSeçtiğiniz varış noktası: {secilen.isim}")
            print(f"Mesafe: {secilen.mesafe} km")
            print(f"Süre: {secilen.sure} dakika")
            print(f"Ücret: {secilen.ucret} TL")
            secilen.otobus_kalkislari_goster()

            try:
                otobus_secimi = int(input("\nHangi otobüse binmek istersiniz? (1-10): "))
                if otobus_secimi < 1 or otobus_secimi > 10:
                    raise ValueError("Geçersiz otobüs seçimi.")
                secilen_otobus, peron_numarasi = secilen.otobusler[otobus_secimi - 1]
                varis_saati = otobus_gelme_suresi(secilen.mesafe, secilen_otobus)
                print(f"Seçtiğiniz otobüs kalkış saati: {secilen_otobus.strftime('%H:%M')}, Peron: {peron_numarasi}")
                print(f"Otobüs {varis_saati.strftime('%H:%M')}\'te varış noktasına ulaşacak.")
                
                # Bilet bilgilerini göstermek için dictionary oluşturuyoruz
                bilet_bilgisi = {
                    'varis_noktasi': secilen.isim,
                    'kalkis_saati': secilen_otobus.strftime('%H:%M'),
                    'peron': peron_numarasi,
                    'ucret': secilen.ucret
                }
                bilet_goster(bilet_bilgisi)

            except ValueError as e:
                print(e)
                return

            otobus_geliyor_mu()
            odeme_yontemi_sor(secilen.ucret)

            bilet_tarihi = datetime.now()
            if bilet_tarihi_ile_gecerliligi_kontrol_et(bilet_tarihi):
                print(f"Biletinizin tarihi: {bilet_tarihi.strftime('%d/%m/%Y')}")
            else:
                print("Bilet geçersiz olduğu için otobüse binilemez.")
        else:
            print("Seçtiğiniz numaraya karşılık gelen varış noktası bulunamadı. Lütfen tekrar deneyin.")
    except ValueError:
        print("Geçersiz giriş. Lütfen sadece numara girin.")

if __name__ == "__main__":
    main()
