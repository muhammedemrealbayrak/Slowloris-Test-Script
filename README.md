# 🚀 High-Performance Asyncio Slowloris DoS Simulator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Bu proje, web sunucularının eşzamanlı bağlantı sınırlarını ve yavaş HTTP isteklerine (Slowloris) karşı duyarlılığını ölçmek amacıyla geliştirilmiş yüksek performanslı bir **dayanıklılık test aracıdır**. 

Geleneksel senkron soket yönetimindeki darboğazları gidermek için tamamen **asenkron (asynchronous)** mimari ve düşük seviyeli **TCP soket optimizasyonları** kullanılarak geliştirilmiştir.

---

## ✨ Özellikler

*   **Asenkron Mimari (`asyncio`):** Binlerce TCP bağlantısı tek bir iş parçacığında (thread) birbirini engellemeden asenkron olarak oluşturulur ve yönetilir.
*   **TCP Soket Optimizasyonları:** 
    *   `SO_KEEPALIVE` etkinleştirilerek soketlerin işletim sistemi seviyesinde canlı kalması sağlanmıştır.
    *   `TCP_NODELAY` (Nagle algoritmasının kapatılması) ile küçük kontrol paketlerinin arabelleğe alınmadan sunucuya anında ulaşması sağlanır.
*   **Dinamik Keep-Alive Sinyalleri:** Sabit süreler yerine 5-10 saniye aralığında rastgele sürelerle gönderilen HTTP başlıkları sayesinde güvenlik duvarlarının (WAF) basit zaman deseni analizleri aşılır.
*   **Kendini İyileştiren Havuz (Self-Healing Pool):** Düşen veya sunucu tarafından kapatılan soketler otomatik tespit edilerek 1 saniye içinde yenisiyle değiştirilir ve bağlantı havuzu sabit tutulur.
*   **Dinamik İzleme:** Arka planda çalışan izleyici sayesinde her 5 saniyede bir güncel aktif soket sayısı terminale yazdırılır.

---

## 🛠️ Kurulum

Proje hiçbir harici kütüphaneye bağımlı değildir, sadece standart Python kütüphanelerini kullanır.

# 1. Depoyu bilgisayarınıza indirin:
git clone https://github.com/muhammedemrealbayrak/Slowloris-Test-Script.git
cd Slowloris-Test-Script
