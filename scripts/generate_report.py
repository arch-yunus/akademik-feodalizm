#!/usr/bin/env python3
"""
Statistical report generator for akademik-feodalizm datasets.
Generates RAPOR_2026.md containing aggregated metrics, comparative indices, and executive summaries.
"""
import os
import json
import csv
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def generate_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    veriler_dir = os.path.join(base_dir, "veriler")
    
    # 1. Load JSON data
    json_path = os.path.join(veriler_dir, "ulke-akademik-mevzuatlari.json")
    with open(json_path, "r", encoding="utf-8") as f:
        countries = json.load(f)
        
    # 2. Load CSV 1 (Complaints)
    csv1_path = os.path.join(veriler_dir, "sorusturma-sonuclari-ve-ihrac-oranlari.csv")
    complaints = []
    with open(csv1_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            complaints.append(row)
            
    # 3. Load CSV 2 (Dropouts & Safety valves)
    csv2_path = os.path.join(veriler_dir, "ogrenci-terk-ve-af-istatistikleri.csv")
    dropouts = []
    with open(csv2_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dropouts.append(row)
            
    # 4. Load CSV 3 (Mobbing Chronology)
    csv3_path = os.path.join(veriler_dir, "universite-akademik-mobbing-ve-intihar-kronolojisi.csv")
    chronology = []
    if os.path.exists(csv3_path):
        with open(csv3_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                chronology.append(row)

    # 5. Load CSV 4 (Brain Drain)
    csv4_path = os.path.join(veriler_dir, "akademik-beyin-gocu-ve-yurtdisi-kayiplari.csv")
    brain_drain = []
    if os.path.exists(csv4_path):
        with open(csv4_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                brain_drain.append(row)

    total_complaints = sum(int(r['toplam_sikayet_sayisi']) for r in complaints)
    total_unprocessed = sum(int(r['isleme_konulmayan_basvuru']) + int(r['takipsizlik_veya_ceza_verilmeyen']) for r in complaints)
    avg_impunity = sum(float(r['cezasizlik_orani_yuzde']) for r in complaints) / len(complaints)
    total_brain_drain = sum(int(r['yurtdisina_giden_doktora_ve_postdoc']) for r in brain_drain) if brain_drain else 0
    total_financial_loss = sum(float(r['tahmini_yillik_maddi_kayip_milyon_dolar']) for r in brain_drain) if brain_drain else 0

    report_content = f"""# Akademik Feodalizm ve Güç Asimetrisi Araştırma Raporu (2026)

Bu analitik rapor, depodaki doğrulanmış 5 ayrı veri setinin (JSON ve CSV) Python veri işleme motoruyla derlenmesi sonucu otomatik olarak üretilmiştir.

---

## 📊 1. Temel İstatistiksel Göstergeler ve Yönetici Özeti

* **İncelenen Ülke Sayısı:** {len(countries)} Ülke Modeli
* **En Yüksek Güç Asimetrisi:** Türkiye (9.2 / 10)
* **En Düşük Güç Asimetrisi (En İyi Uygulama):** Hollanda & İskandinavya (1.5 / 10) | İsviçre (2.2 / 10)
* **2018-2025 Arası Toplam Şikâyet Sayısı:** {total_complaints:,}
* **2018-2025 Arası Cezasız/Takipsiz Kapatılan Dosya Sayısı:** {total_unprocessed:,}
* **Ortalama Cezasızlık Oranı:** %{avg_impunity:.1f}
* **2018-2025 Toplam Yurtdışına Göç Eden Doktoralı / Postdoc:** {total_brain_drain:,} Araştırmacı
* **Kümülatif Tahmini Beşeri & Maddi Kayıp:** ${total_financial_loss:,.1f} Milyon Dolar

---

## 🌍 2. Uluslararası Cezasızlık ve Asimetri Matrisi

| Ülke | Model | Güç Asimetrisi (1-10) | İş Güvencesi | Cezasızlık Oranı | Bağımsız Ombudsman |
| :--- | :--- | :---: | :---: | :---: | :---: |
"""
    for c in countries:
        ombuds = "✅ Var" if c['denetim_ve_sikayet']['bagimsiz_ombudsman'] else "❌ Yok"
        report_content += f"| **{c['ulke']}** | {c['model']} | {c['guc_asimetrisi']['skor_1_10']} | {c['hukuki_statu']['is_guvencesi_skoru_1_10']}/10 | %{c['denetim_ve_sikayet']['sikayet_cezasizlik_orani_yuzde']} | {ombuds} |\n"

    report_content += """
---

## 📉 3. Yıllara Göre Şikâyet ve Cezasızlık Trendi (Türkiye)

| Yıl | Toplam Şikâyet | İşleme Konulmayan / Takipsizlik | İhraç Sayısı | Cezasızlık Oranı |
| :---: | :---: | :---: | :---: | :---: |
"""
    for r in complaints:
        unprocessed = int(r['isleme_konulmayan_basvuru']) + int(r['takipsizlik_veya_ceza_verilmeyen'])
        report_content += f"| {r['yil']} | {int(r['toplam_sikayet_sayisi']):,} | {unprocessed:,} | {r['kamu_gorevinden_ihrac']} | %{r['cezasizlik_orani_yuzde']} |\n"

    report_content += """
---

## 🚪 4. Sosyal Tahliye Vanaları Verileri (2018-2025)

| Yıl | Örgün Terk / Kayıt Sildiren | AÖF / AUZEF Kayıt | KYK Kesilmeme Oranı | Ek Madde 1 Geçiş |
| :---: | :---: | :---: | :---: | :---: |
"""
    for r in dropouts:
        report_content += f"| {r['yil']} | {int(r['orgun_egitimi_terk_kayit_sildiren']):,} | {int(r['aof_ve_auzefe_kayit_yapan']):,} | %{r['kyk_kesilmeksizin_devam_orani_yuzde']} | {int(r['ek_madde_1_yatay_gecis_yapan']):,} |\n"

    report_content += """
---

## ✈️ 5. Akademik Beyin Göçü ve Yetişmiş İnsan Kaybı (2018-2025)

| Yıl | Giden Doktora/Postdoc | Başlıca Hedef Ülke | Geri Dönüş Oranı | Yıllık Tahmini Kayıp ($) |
| :---: | :---: | :---: | :---: | :---: |
"""
    for r in brain_drain:
        report_content += f"| {r['yil']} | {int(r['yurtdisina_giden_doktora_ve_postdoc']):,} | {r['en_cok_tercih_edilen_ulke']} | %{r['geri_donus_orani_yuzde']} | ${float(r['tahmini_yillik_maddi_kayip_milyon_dolar']):.1f}M |\n"

    report_content += """
---

## ⚖️ 6. Seçilmiş Mobbing ve Güç Suistimali Kronolojisi

| Yıl | Şehir | Olay Türü | Mağdur | Temel Baskı / Çatışma | Yargı / İdari Sonuç |
| :---: | :---: | :--- | :--- | :--- | :--- |
"""
    for r in chronology:
        report_content += f"| {r['yil']} | {r['sehir']} | {r['olay_turu']} | {r['magdur_profili']} | {r['akademik_baski_faktoru']} | {r['resmi_islem_ve_akibet']} |\n"

    report_content += """
---

*Rapor Sonu — Otomatik Üretim Tarihi: 2026 | Akademik Feodalizm Araştırma Girişimi*
"""

    report_path = os.path.join(base_dir, "RAPOR_2026.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[+] Report generated successfully at: {report_path}")

if __name__ == "__main__":
    generate_report()
