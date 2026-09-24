#!/usr/bin/env python3
"""
Akademik Feodalizm CLI & Veri Simülatörü
Öğrenciler, araştırmacılar ve araştırmacılar için komut satırı analiz, dilekçe üretme ve risk değerlendirme aracı.
"""
import os
import sys
import json
import csv
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERILER_DIR = os.path.join(BASE_DIR, "veriler")
DILEKCELER_DIR = os.path.join(BASE_DIR, "dilekce-sablonlari")

def print_banner():
    print("=" * 72)
    print("  AKADEMİK FEODALİZM VE GÜÇ ASİMETRİSİ ARAŞTIRMA SİMÜLATÖRÜ (CLI)")
    print("  Demokratik Üniversite & Açık Bilim Girişimi - 2026")
    print("=" * 72)

def calculate_risk_interactive():
    print("\n[?] FAKÜLTE FEODALİZM RİSK DEĞERLENDİRME TESTİ")
    print("-" * 55)
    questions = [
        ("Sınav kâğıtları açık cevap anahtarı/barem olmaksızın okunuyor ve kâğıt gösterilmiyor mu?", 20),
        ("Şikâyet edilen öğretim üyesini aynı fakültedeki mesai arkadaşı profesörler mi soruşturuyor?", 25),
        ("Asistanlar/öğrenciler hocanın şahsi işleri ve angaryaları için baskı altında tutuluyor mu?", 20),
        ("Kadro ilanlarında tek bir adayın tez başlığını tarif eden kişiye özel şartlar var mı?", 15),
        ("Hak arayan öğrenciler 'dersi geçemezsin / mezun olamazsın' misillemesiyle tehdit ediliyor mu?", 20)
    ]
    total_score = 0
    for idx, (q, weight) in enumerate(questions, 1):
        while True:
            ans = input(f"{idx}. {q} (e/h) [+{weight} Puan]: ").strip().lower()
            if ans in ['e', 'evet', 'y', 'yes']:
                total_score += weight
                break
            elif ans in ['h', 'hayir', 'hayır', 'n', 'no']:
                break
            else:
                print("Lütfen 'e' veya 'h' yazınız.")
    
    print("\n" + "=" * 55)
    print(f"HESAPLANAN FEODALİZM RİSK ENDEKSİ: {total_score} / 100")
    if total_score >= 70:
        print("DURUM: [KRİTİK] Aşırı Feodal Ortam & Yüksek Mobbing Riski!")
        print("Tavsiye: Tüm iletişimleri yazılı yapın, delil toplayın ve bağımsız yargı yoluna hazırlanın.")
    elif total_score >= 40:
        print("DURUM: [ORTA] Bürokrasi Zırhı ve Keyfiyet Riski.")
        print("Tavsiye: Hak arama dilekçelerinde Bilgi Edinme Kanunu ve Danıştay içtihatlarını kullanın.")
    else:
        print("DURUM: [DÜŞÜK] Nispeten Demokratik ve Şeffaf Akademik Ortam.")
    print("=" * 55)

def list_and_search_chronology(keyword=None, year=None):
    csv_path = os.path.join(VERILER_DIR, "universite-akademik-mobbing-ve-intihar-kronolojisi.csv")
    if not os.path.exists(csv_path):
        print("[!] Kronoloji dosyası bulunamadı.")
        return
    print(f"\n[*] AKADEMİK MOBBİNG VE OLAY KRONOLOJİSİ SORGULAMA")
    print("-" * 75)
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if year and str(row['yil']) != str(year):
                continue
            if keyword:
                kw = keyword.lower()
                row_str = " ".join(row.values()).lower()
                if kw not in row_str:
                    continue
            count += 1
            print(f"[{row['yil']}] - {row['sehir']} | Olay: {row['olay_turu']}")
            print(f"  Mağdur: {row['magdur_profili']}")
            print(f"  Baskı:  {row['akademik_baski_faktoru']}")
            print(f"  Sonuç:  {row['resmi_islem_ve_akibet']}")
            print(f"  Kaynak: {row['kaynak_kategorisi']}\n")
        print(f"[+] Toplam {count} vaka listelendi.")

def list_countries_matrix():
    json_path = os.path.join(VERILER_DIR, "ulke-akademik-mevzuatlari.json")
    if not os.path.exists(json_path):
        print("[!] JSON dosyası bulunamadı.")
        return
    with open(json_path, "r", encoding="utf-8") as f:
        countries = json.load(f)
    print("\n" + "=" * 80)
    print(f"{'Ülke':<22} | {'Model':<30} | {'Asimetri':<8} | {'Cezasızlık':<10} | {'Ombudsman':<10}")
    print("-" * 80)
    for c in countries:
        omb = "Var" if c['denetim_ve_sikayet']['bagimsiz_ombudsman'] else "Yok"
        print(f"{c['ulke']:<22} | {c['model'][:30]:<30} | {c['guc_asimetrisi']['skor_1_10']:<8} | %{c['denetim_ve_sikayet']['sikayet_cezasizlik_orani_yuzde']:<9} | {omb:<10}")
    print("=" * 80)

def generate_petition(template_num, uni, fak, ders, output_file=None):
    template_files = {
        1: "01_sinav-kagidi-ve-barem-inceleme-talebi.md",
        2: "02_bagimsiz-dis-juri-itiraz-dilekcesi.md",
        3: "03_akademik-mobbing-ve-gorevi-kotuye-kullanma-sikayeti.md",
        4: "04_tez-danismani-degisikligi-talep-dilekcesi.md",
        5: "05_savcilik-suc-duyurusu-taslagi.md",
        6: "06_bilgi-edinme-kanunu-kapsaminda-juri-ve-mulakat-tutanaklari-talebi.md"
    }
    fname = template_files.get(template_num, "01_sinav-kagidi-ve-barem-inceleme-talebi.md")
    path = os.path.join(DILEKCELER_DIR, fname)
    if not os.path.exists(path):
        print(f"[!] Şablon dosyası bulunamadı: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Custom replacements
    content = content.replace("[ÜNİVERSİTE ADI]", uni.upper())
    content = content.replace("[Üniversite Adı]", uni)
    content = content.replace("[FAKÜLTE ADI]", fak.upper())
    content = content.replace("[Fakülte Adı]", fak)
    content = content.replace("[Ders Adı ve Kodu]", ders)
    content = content.replace("[Ders Adı]", ders)
    content = content.replace("[Ders Kodu] - [Ders Adı]", ders)
    
    print("\n--- ÜRETİLEN DİLEKÇE METNİ ---")
    print(content)
    print("------------------------------")
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"[+] Dilekçe başarıyla kaydedildi: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Akademik Feodalizm CLI & Veri Simülatörü")
    parser.add_argument("--test", action="store_true", help="İnteraktif Feodalizm Risk Testini Başlat")
    parser.add_argument("--kronoloji", action="store_true", help="Mobbing ve Vaka Kronolojisini Listele")
    parser.add_argument("--ara", type=str, help="Kronoloji içinde arama terimi")
    parser.add_argument("--yil", type=str, help="Kronoloji için yıl filtresi")
    parser.add_argument("--ulkeler", action="store_true", help="Ülkeler Karşılaştırma Matrisini Listele")
    parser.add_argument("--dilekce", type=int, choices=[1,2,3,4,5,6], help="Dilekçe Şablon Numarası (1-6)")
    parser.add_argument("--uni", type=str, default="Ankara Üniversitesi", help="Üniversite Adı")
    parser.add_argument("--fak", type=str, default="Mühendislik Fakültesi", help="Fakülte Adı")
    parser.add_argument("--ders", type=str, default="BIL101 Algoritmalar", help="Ders Kodu/Adı")
    parser.add_argument("--kaydet", type=str, help="Üretilen dilekçenin kaydedileceği dosya yolu")
    
    args = parser.parse_args()
    print_banner()
    
    if args.test:
        calculate_risk_interactive()
    elif args.kronoloji or args.ara or args.yil:
        list_and_search_chronology(keyword=args.ara, year=args.yil)
    elif args.ulkeler:
        list_countries_matrix()
    elif args.dilekce:
        generate_petition(args.dilekce, args.uni, args.fak, args.ders, args.kaydet)
    else:
        list_countries_matrix()
        print("\n[İpucu] İnteraktif risk testi için: python scripts/academic_simulator.py --test")
        print("[İpucu] Dilekçe üretmek için: python scripts/academic_simulator.py --dilekce 1 --uni 'Ege Üniv' --fak 'Tıp Fak' --ders 'Anatomi'")
        print("[İpucu] Kronoloji sorgulamak için: python scripts/academic_simulator.py --kronoloji --ara 'Danıştay'")

if __name__ == "__main__":
    main()
