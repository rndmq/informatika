from Doll import BuatBoneka
import datamusuh as datamusuh
import json
import sys
import time
# CHALLANGE TASKS

import sys
import time

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
lawan_terpilih = datamusuh.generate_musuh()
firepower_musuh = lawan_terpilih["firepower"]
rate_of_fire_musuh = lawan_terpilih["rate_of_fire"]
accuracy_musuh = lawan_terpilih["accuracy"]
evasion_musuh = lawan_terpilih["evasion"]
dps_musuh = round((firepower_musuh * rate_of_fire_musuh) / 60, 2)
ce_musuh = int((30 * firepower_musuh) + (40 * (rate_of_fire_musuh ** 2) / 120) + (15 * (accuracy_musuh + evasion_musuh)))
lawan_terpilih["damage per detik musuh"] = dps_musuh
lawan_terpilih["combat effectiveness musuh"] = ce_musuh


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
    print("\nData musuh yang telah menghadang kamu:")
    print_lama(json.dumps(lawan_terpilih, indent=4), jeda_biasa=0.02, jeda_titik=0.4)
    tanya_user = input("\nApakah kamu mau menggunakan system otomatis\n 1: Ya\n 2: Tidak\nPilihan Kamu: ")

    if tanya_user == "1":
        auto = True
        print("\nSystem otomatis telah diaktifkan!")
    else:
        auto = False
        print("\nSystem otomatis dihentikan!")

    global status
    if kekuatan_damage_aku >= dps_musuh and kekuatan_combat_aku >= ce_musuh:
        status = "Menang"
    else:
        status = "Kalah"

    User_response = ""

    if not auto:
        User_response = input("\nApakah kamu mau melawan musuh ini? (y/n): ")

        if User_response.lower() == "y" and status == "Kalah":
          print(f"\nKamu {status} melawan musuh ini!")
          print("Seharusnya kamu kabur!")
        elif User_response.lower() == "y" and status == "Menang":
          print(f"\nKamu {status} melawan musuh ini!")
          print("Selamat kamu menang!")
        elif User_response.lower() == "n":
          print("\nKamu memilih untuk kabur dari musuh ini!")
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
        User_response = str(input("\nApakah kamu mau melawan musuh ini? (y/n): "))
        if User_response.lower() == "y":
          pesan_dari_bot = "Kamu menuruti saran untuk melawan musuh ini!"
          print_lama(pesan_dari_bot)
          print(f"\nKamu {status} melawan musuh ini!")
          print_lama("Selamat kamu menang! 🎉")
        elif User_response.lower() == "n":
          pesan_dari_bot = "kamu memilih untuk tidak mengikuti bot & kabur dari musuh ini!"
          print_lama(pesan_dari_bot)
        else:
          pesan_dari_bot = "[SYSTEM] input tidak valid. Harusnya memasukkan data \"y\" atau \"n\"."
          print(pesan_dari_bot)
          tanya_user_mengenaiBot = str(input("\nApakah kamu mau kabur dari musuh ini? (y/n): "))
        if tanya_user_mengenaiBot.lower() == "y":
          pesan_dari_bot = "Kamu menuruti saran bot untuk kabur dari musuh ini!"
          print_lama(pesan_dari_bot)
          
main()
