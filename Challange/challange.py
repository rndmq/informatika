from module.Doll import BuatBoneka
import module.datalawan as datalawan
import json
import sys
import time
# CHALLANGE TASKS


def print_lama(teks, jeda_biasa=0.01, jeda_titik=0.6):
# bonus visual cerita ajah.
    for karakter in teks:
        sys.stdout.write(karakter)
        sys.stdout.flush()
        
        if karakter == ".":
            time.sleep(jeda_titik)
        else:
            time.sleep(jeda_biasa)
    print()


# ======= MINTA DATA DARI USER =======
nama_boneka_aku = str(input("Masukkan nama boneka: "))
firepower_aku = int(input("Masukkan firepower: "))
rate_of_fire_aku = int(input("Masukkan rate of fire: "))
accuracy_aku = int(input("Masukkan accuracy: "))
evasion_aku = int(input("Masukkan evasion: "))
damage_per_detik_aku = round((firepower_aku * rate_of_fire_aku) / 60, 2)
combateffectiveness_aku = int((30 * firepower_aku) + (40 * (rate_of_fire_aku ** 2) / 120) + (15 * (accuracy_aku + evasion_aku)))

# total punya user
punya_user = BuatBoneka(f"{nama_boneka_aku}", firepower_aku, rate_of_fire_aku, accuracy_aku, evasion_aku)
kekuatan_damage_aku, kekuatan_combat_aku = damage_per_detik_aku, combateffectiveness_aku

# Musuh
lawan_terpilih = datalawan.generate_lawan()
firepower_lawan = lawan_terpilih["firepower"]
rate_of_fire_lawan = lawan_terpilih["rate_of_fire"]
accuracy_lawan = lawan_terpilih["accuracy"]
evasion_lawan = lawan_terpilih["evasion"]
dps_lawan = round((firepower_lawan * rate_of_fire_lawan) / 60, 2)
ce_lawan = int((30 * firepower_lawan) + (40 * (rate_of_fire_lawan ** 2) / 120) + (15 * (accuracy_lawan + evasion_lawan)))
lawan_terpilih["damage per detik lawan"] = dps_lawan
lawan_terpilih["combat effectiveness lawan"] = ce_lawan


def main():
    auto = False
    print("Selamat datang di ranked!")
    data_boneka = punya_user
    print("\nData boneka yang telah kamu custom:")
    print_lama(json.dumps(data_boneka, indent=4), jeda_biasa=0.02, jeda_titik=0.4)
    print_lama("\n[INFO INTEL] Kamu mendapatkan kabar dari agen intel Badan Intelijen "
                   "Kerajaan Dōruzufurontorain yang menyamar sebagai tukang cilok di dekat "
                   "markas Mercury. Ternyata Mercury juga memiliki Tactical Doll yang "
                   "berjaga di sekitar markasnya...\n", jeda_biasa=0.03, jeda_titik=0.6)
    print("\nData lawan yang telah menghadang kamu:")
    print_lama(json.dumps(lawan_terpilih, indent=4), jeda_biasa=0.02, jeda_titik=0.4)
    tanya_user = input("\nApakah kamu mau menggunakan system otomatis\n 1: Ya\n 2: Tidak\nPilihan Kamu: ")

    if tanya_user == "1":
        auto = True
        print("\nSystem otomatis telah diaktifkan!")
    else:
        auto = False
        print("\nSystem otomatis dihentikan!")

    global status
    if kekuatan_damage_aku >= dps_lawan and kekuatan_combat_aku >= ce_lawan:
        status = "Menang"
    else:
        status = "Kalah"

    User_response = ""

    if not auto:
        User_response = input("\nApakah kamu mau melawan Tacticall Doll ini? (y/n): ")

        if User_response.lower() == "y" and status == "Kalah":
          print(f"\nKamu {status} melawan Tacticall Doll ini!")
          print("Seharusnya kamu kabur!")
        elif User_response.lower() == "y" and status == "Menang":
          print(f"\nKamu {status} melawan Tacticall Doll ini!")
          print("Selamat kamu menang!")
        elif User_response.lower() == "n":
          print("\nKamu memilih untuk kabur dari Tacticall Doll ini!")
        else:
          print("\nInput tidak valid. Harusnya memasukkan data \"y\" atau \"n\".")

    # BAGIAN OTOMATIS
    pesan_dari_bot = ""
    tanya_user_mengenaiBot = ""


    # OTOMATIS
    if auto:
      if status == "Menang":
        time.sleep(0.25)
        print_lama("...")
        pesan_dari_bot = "[SYSTEM] kamu menang! Ayo kita lawan diaa"
        print_lama(pesan_dari_bot)
        User_response = str(input("\nApakah kamu mau melawan Tacticall Doll ini? (y/n): "))
        if User_response.lower() == "y":
          pesan_dari_bot = "Kamu menuruti saran untuk melawan Tacticall Doll ini!"
          print_lama(pesan_dari_bot)
          print(f"\nKamu {status} melawan Tacticall Doll ini!")
          print_lama("Selamat kamu menang! 🎉")
        elif User_response.lower() == "n":
          pesan_dari_bot = "kamu memilih untuk tidak mengikuti bot & kabur dari Tacticall Doll ini!"
          print_lama(pesan_dari_bot)
        else:
          pesan_dari_bot = "[SYSTEM] input tidak valid. Harusnya memasukkan data \"y\" atau \"n\"."
          print(pesan_dari_bot)
          tanya_user_mengenaiBot = str(input("\nApakah kamu mau kabur dari Tacticall Doll ini? (y/n): "))
          if tanya_user_mengenaiBot.lower() == "y":
            pesan_dari_bot = "Kamu menuruti saran bot untuk kabur dari Tacticall Doll ini!"
            print_lama(pesan_dari_bot)
          elif tanya_user_mengenaiBot.lower() == "n":
            pesan_dari_bot = "Kamu nekat melawan meski bot menyarankan kabur!"
            print_lama(pesan_dari_bot)
          else:
            print("[SYSTEM] input tidak valid.")

      else:  # status == "Kalah"
        time.sleep(0.25)
        print_lama("...")
        pesan_dari_bot = "[SYSTEM] kamu kalah! Sebaiknya kita kabur ajaa"
        print_lama(pesan_dari_bot)
        User_response = str(input("\nApakah kamu mau kabur dari Tacticall Doll ini? (y/n): "))
        if User_response.lower() == "y":
          pesan_dari_bot = "Kamu menuruti saran bot untuk kabur dari Tacticall Doll ini!"
          print_lama(pesan_dari_bot)
        elif User_response.lower() == "n":
          pesan_dari_bot = "Kamu nekat melawan meski bot menyarankan kabur!"
          print_lama(pesan_dari_bot)
          print(f"\nKamu {status} melawan Tacticall Doll ini!")
        else:
          pesan_dari_bot = "[SYSTEM] input tidak valid. Harusnya memasukkan data \"y\" atau \"n\"."
          print(pesan_dari_bot)
          tanya_user_mengenaiBot = str(input("\nApakah kamu mau kabur dari Tacticall Doll ini? (y/n): "))
          if tanya_user_mengenaiBot.lower() == "y":
            pesan_dari_bot = "Kamu menuruti saran bot untuk kabur dari Tacticall Doll ini!"
            print_lama(pesan_dari_bot)
          elif tanya_user_mengenaiBot.lower() == "n":
            pesan_dari_bot = "Kamu nekat melawan meski bot menyarankan kabur!"
            print_lama(pesan_dari_bot)
          else:
            print("[SYSTEM] input tidak valid.")
          
          
main()