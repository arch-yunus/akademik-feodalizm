# Katkıda Bulunma Rehberi (KATKI.md)

Bu araştırma deposu, yükseköğretim sistemlerindeki yapısal güç asimetrilerini, kürsü feodalizmini ve idari denetimsizliği tarafsız, veriye dayalı ve karşılaştırmalı bir perspektifle belgelemeyi amaçlayan açık kaynaklı bir çalışmadır.

Topluluk katkılarını memnuniyetle kabul ediyoruz.

---

## 1. Katkı Alanları

Katkılarınızı aşağıdaki ana kategoriler altında sunabilirsiniz:

1. **Veri Setleri (`veriler/`):**
   - YÖK, TÜİK, üniversite denetim raporları, OECD ve UNESCO veri tabanlarından doğrulanabilir istatistikler.
   - Disiplin soruşturmaları, mobbing başvuruları, af kanunları ve terk oranları verileri.
   - Yeni ülkelerin karşılaştırmalı mevzuat ve gösterge parametreleri (`ulke-akademik-mevzuatlari.json`).

2. **Analiz ve Kuramsal Metinler (`analizler/`):**
   - Eğitim sosyolojisi, kurumsal iktisat, kamu yönetimi ve hukuk perspektifinden derinlemesine incelemeler.
   - Somut mekanizmaların (kürsü tekeli, notlandırma keyfiyeti, tahliye vanaları) analitik dökümü.

3. **Alıntılar ve Emsal Belgeler (`alintilar-ve-dokumanlar/`):**
   - Literatür alıntıları (Weber, Bourdieu, Freire, Foucault, Veblen vb.).
   - Danıştay ve İdare Mahkemesi emsal kararları (özellikle not iptalleri, soruşturma açılmaması itirazları, mobbing tazminatları).
   - Kişisel verilerden tamamen arındırılmış, anonimleştirilmiş dilekçe ve bürokratik oyalama örnekleri.

4. **Mevzuat Arşivi (`mevzuat-arsivi/`):**
   - İlgili ülkelerin yükseköğretim kanunları, disiplin tüzükleri ve ombudsmanlık yönergeleri.

---

## 2. Araştırma ve Etik Kuralları

Bu çalışmanın güvenilirliğini ve yasal meşruiyetini korumak için aşağıdaki kurallara kesinlikle uyulmalıdır:

- **Kişisel Verilerin Korunması (KVKK & GDPR):** Hiçbir akademisyenin, idarecinin veya öğrencinin gerçek adı, unvanı, üniversite/bölüm adı hedef gösterilerek paylaşılamaz. Tüm vakalar ve belgeler anonimleştirilmelidir (örn: *Hoca A, Öğrenci B, X Üniversitesi*).
- **Hakaret ve İftira Yasağı:** Amaç kişileri hedef almak değil; kurumsal, yapısal ve yasal mekanizmaları ve sistemik açıkları analiz etmektir.
- **Doğrulanabilirlik:** Eklenen istatistiki veriler ve mahkeme kararları resmi kaynaklara (Resmî Gazete, Danıştay Karar Sorgu, YÖK İstatistikleri, OECD Education at a Glance) dayandırılmalıdır.

---

## 3. Katkı Süreci (Git & PR)

1. Depoyu forklayın (`Fork`).
2. Yeni ve açıklayıcı bir dal (branch) açın:
   ```bash
   git checkout -b ozellik/yeni-emsal-karar-ekleme
   ```
3. İlgili dizinde dosyanızı oluşturun veya güncelleyin.
4. Veri formatının doğruluğunu test edin:
   ```bash
   python scripts/validate_data.py
   ```
5. Değişikliklerinizi açık bir commit mesajıyla kaydedin:
   ```bash
   git commit -m "feat(emsal): 2024 danistay not iptali karari eklendi"
   ```
6. Dalınızı pushlayın ve ana depoya **Pull Request** açın.

---

## 4. Dosya ve Veri Standartları

- Tüm Markdown dosyaları `UTF-8` kodlamasında ve GitHub Flavored Markdown standartlarında olmalıdır.
- JSON dosyaları 2 boşluk girintili, geçerli JSON syntax'ına sahip olmalıdır.
- CSV dosyaları `UTF-8` ve virgül (`,`) ayracı ile yapılandırılmalıdır.

Katkılarınız için teşekkür ederiz!
