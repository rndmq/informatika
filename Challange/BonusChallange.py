from module.Doll import BuatBoneka
import module.datalawan as datalawan
import json
import sys
import time
import random
# CHALLANGE TASKS

global darah_user
darah_user = 1000
global darah_lawan
darah_lawan = 1000

list_kekuatan = ["Api", "Air", "Angin", "Bumi", "Listrik", "Es"]
list_aksi = ["attack", "skill", "defend"]

aksi_user = ""
aksi_lawan = ""
giliran = ""

powerUp_user = ""
powerUp_lawan = ""

kekuatan_damage_aku = 0
kekuatan_damage_lawan = 0

damage_aku = 0
damage_lawan = 0

cooldown_skill_user = 0
cooldown_skill_lawan = 0

burn_user = 0
burn_lawan = 0
freeze_user = 0
freeze_lawan = 0
shock_user = 0
shock_lawan = 0

efek_powerup_keuser = ""
efek_powerup_kelawan = ""


def hitung_damage(base_damage, aksi):
    if aksi == "attack":
        return base_damage
    elif aksi == "skill":
        return base_damage * 1.55
    elif aksi == "defend":
        return base_damage * 0.5
    return 0


def terapkan_powerup(damage, power_up):
    if power_up == "Api":
        return damage * 1.2
    elif power_up == "Air":
        return damage * 1.1
    elif power_up == "Angin":
        return damage * 1.15
    elif power_up == "Bumi":
        return damage * 1.25
    elif power_up == "Listrik":
        return damage * 1.3
    elif power_up == "Es":
        return damage * 1.4
    return damage


def pilih_powerup(label):
    pilihan = input(f"Pilih powerup {label} \n1. Api\n2. Air\n3. Angin\n4. Bumi\n5. Listrik\n6. Es: ")
    mapping = {
        "1": "Api",
        "2": "Air",
        "3": "Angin",
        "4": "Bumi",
        "5": "Listrik",
        "6": "Es"
    }
    return mapping.get(pilihan, "")


def update_status():
    return {
        "powerUp_user": pilih_powerup("user"),
        "powerUp_lawan": random.choice(list_kekuatan)
    }


def tampilkan_status_effects():
    print("\n=== INFO SKILL ===")
    print("1. Api -> skill membakar musuh tiap giliran.")
    print("2. Es -> skill membekukan musuh dan mengurangi damage lawan sebesar 25.")
    print("3. Listrik -> skill membuat musuh fokus terganggu dan damage lawan berkurang sedikit.")
    print("4. Air/Angin/Bumi -> skill memberi bonus damage besar dan efek pendukung.")
    print("=== SKILL memakai cooldown 2 giliran ===")

    if burn_lawan > 0:
        print("Lawan terbakar! HP lawan berkurang tiap giliran.")
    if freeze_lawan > 0:
        print("Lawan sedang beku, langkahnya terganggu, dan damage lawan berkurang 25.")
    if shock_lawan > 0:
        print("Lawan kewalahan fokus karena listrik.")


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
# Gunakan firepower sebagai basis damage per turn, dps tetap dipakai sebagai bonus ringan
kekuatan_damage_aku = firepower_aku + (damage_per_detik_aku * 0.05)
kekuatan_combat_aku = combateffectiveness_aku

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
kekuatan_damage_lawan = firepower_lawan + (dps_lawan * 0.05)


def main():
    global darah_user, darah_lawan, powerUp_user, powerUp_lawan
    global cooldown_skill_user, cooldown_skill_lawan
    global burn_user, burn_lawan, freeze_user, freeze_lawan, shock_user, shock_lawan
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

    info_skill = input("\nMau baca info skill dulu? (y/n): ").lower()
    if info_skill == "y":
        tampilkan_status_effects()
    else:
        print_lama("\nBaik, langsung masuk battle.")

    status_power = update_status()
    powerUp_user = status_power["powerUp_user"]
    powerUp_lawan = status_power["powerUp_lawan"]

    print_lama("\nBattle dimulai! Pilih aksi setiap giliran.")
    while darah_user > 0 and darah_lawan > 0:
        if cooldown_skill_user > 0:
            cooldown_skill_user -= 1
        if cooldown_skill_lawan > 0:
            cooldown_skill_lawan -= 1

        if burn_lawan > 0:
            darah_lawan -= 3
            print_lama("\nLawan terbakar! hp lawan berkurang 3.", jeda_titik=0.1)
            burn_lawan -= 1
        if freeze_lawan > 0:
            print_lama ("\nLawan sedang beku, geraknya terganggu, damage lawan berkurang 25.", jeda_titik=0.1)
            freeze_lawan -= 1
        if shock_lawan > 0:
            print_lama("\nLawan terguncang listrik, fokusnya menurun.", jeda_titik=0.1)
            shock_lawan -= 1

        aksi_user = input("Pilih aksi (attack/skill/defend): ").lower()
        if aksi_user not in list_aksi:
            print_lama("Aksi tidak valid. Gunakan attack, skill, atau defend.")
            continue

        aksi_lawan = random.choice(list_aksi)

        if freeze_lawan > 0:
            aksi_lawan = "defend"

        if aksi_user == "skill":
            if cooldown_skill_user == 0:
                cooldown_skill_user = 2
                damage_aku = hitung_damage(kekuatan_damage_aku, "skill")

                if powerUp_user == "Api":
                    burn_lawan = 2
                    print_lama("\nSkill kamu: Api! Musuh terbakar tiap giliran.", jeda_titik=0.1)
                elif powerUp_user == "Es":
                    freeze_lawan = 2
                    print_lama("\nSkill kamu: Es! Musuh dibekukan dan damage Serangan lawan turun 25.", jeda_titik=0.1)
                elif powerUp_user == "Listrik":
                    shock_lawan = 2
                    print_lama("\nSkill kamu: Listrik! Fokus musuh terganggu.", jeda_titik=0.1)
                else:
                    print_lama("\nSkill kamu digunakan tanpa elemen spesial.", jeda_titik=0.1)
            else:
                print_lama(f"\nSkill kamu masih dalam cooldown ({cooldown_skill_user} giliran tersisa).", jeda_titik=0.1)
                damage_aku = hitung_damage(kekuatan_damage_aku, "attack")
        else:
            damage_aku = hitung_damage(kekuatan_damage_aku, aksi_user)

        if aksi_lawan == "skill":
            if cooldown_skill_lawan == 0:
                cooldown_skill_lawan = 2
                damage_lawan = hitung_damage(kekuatan_damage_lawan, "skill")

                if powerUp_lawan == "Api":
                    burn_user = 2
                    print_lama("\nSkill lawan: Api! Kamu terbakar tiap giliran.", jeda_titik=0.1)
                elif powerUp_lawan == "Es":
                    freeze_user = 2
                    print_lama("\nSkill lawan: Es! Kamu dibekukan.", jeda_titik=0.1)
                elif powerUp_lawan == "Listrik":
                    shock_user = 2
                    print_lama("\nSkill lawan: Listrik! Fokus kamu terganggu.", jeda_titik=0.1)
                else:
                    print_lama("\nSkill lawan digunakan tanpa elemen spesial.", jeda_titik=0.1)
            else:
                damage_lawan = hitung_damage(kekuatan_damage_lawan, "attack")
        else:
            damage_lawan = hitung_damage(kekuatan_damage_lawan, aksi_lawan)

        if burn_user > 0:
            darah_user -= 3
            print_lama("\nKamu terbakar! HP kamu berkurang 3.", jeda_titik=0.1)
            burn_user -= 1
        if freeze_user > 0:
            print_lama("\nKamu sedang beku, aksi kamu terganggu, dan damage serangan kamu berkurang 25.", jeda_titik=0.1)
            freeze_user -= 1
        if shock_user > 0:
            print_lama("\nKamu kewalahan fokus karena listrik.", jeda_titik=0.1)
            shock_user -= 1

        if freeze_user > 0:
            damage_aku = max(0, damage_aku - 25)
        if freeze_lawan > 0:
            damage_lawan = max(0, damage_lawan - 25)

        damage_aku = terapkan_powerup(damage_aku, powerUp_user)
        damage_lawan = terapkan_powerup(damage_lawan, powerUp_lawan)

        if aksi_user != "defend":
            darah_lawan -= damage_aku
        if aksi_lawan != "defend":
            darah_user -= damage_lawan

        print_lama(f"\nAksi kamu: {aksi_user} | Aksi lawan: {aksi_lawan}", jeda_titik=0.1)
        print_lama(f"Damage kamu: {round(damage_aku, 2)} | Damage lawan: {round(damage_lawan, 2)}", jeda_titik=0.1)
        print_lama(f"Darah Kamu: {round(darah_user, 2)} | Darah Lawan: {round(darah_lawan, 2)}", jeda_titik=0.1)

    if darah_user > darah_lawan:
        print_lama("\nKamu menang!")
    else:
        print_lama("\nKamu kalah!")


main()
