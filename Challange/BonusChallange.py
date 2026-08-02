from module.Doll import BuatBoneka
import module.datalawan as datalawan
import json
import sys
import time
import random
# CHALLANGE TASKS

global darah_user
darah_user = 1500
global darah_lawan
darah_lawan = 1000

difficulty = 1

list_kekuatan = ["Api", "Air", "Angin", "Bumi", "Listrik", "Es"]
list_aksi = ["attack", "skill", "defend", "powerups"]

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
cooldown_defend_lawan = 0
cooldown_powerup_user = 0
cooldown_powerup_lawan = 0

boost_user = 0
boost_lawan = 0

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
        return 0
    elif aksi == "powerups":
        return 0
    return 0


def hitung_peluang_defend(evasion, accuracy, mode_bonus=0):
    return min(0.95, max(0.15, (((evasion * 0.7) + (accuracy * 0.3)) / 100) + mode_bonus))


def pilih_aksi_lawan(aksi_user, evasion_lawan, accuracy_lawan, accuracy_aku, evasion_aku, cooldown_defend, difficulty):
    #fungsi biar ai ga murni random..
    defend_bias = {1: 0.20, 2: 0.32, 3: 0.45}[difficulty]
    skill_bias = {1: 0.18, 2: 0.30, 3: 0.44}[difficulty]

    if cooldown_defend > 0:
        return "attack"

    if aksi_user == "skill" and evasion_lawan >= 70 and random.random() < defend_bias:
        return "defend"

    if accuracy_lawan >= accuracy_aku and evasion_lawan >= evasion_aku:
        return "skill"

    if evasion_lawan >= 75 and random.random() < defend_bias:
        return "defend"

    if accuracy_lawan >= 80 and random.random() < skill_bias:
        return "skill"

    return "attack"


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


def tampilkan_info_battle(mode):
    mode_info = {1: "Easy", 2: "Medium", 3: "Hard"}[mode]
    print_lama(f"\n[INFO MODE] Mode aktif: {mode_info}", jeda_biasa=0.02, jeda_titik=0.3)
    print_lama("[INFO BALANCE] Stat kamu dibatasi dengan cap dinamis, bukan statis. Jadi angka tidak melonjak terlalu besar.", jeda_biasa=0.02, jeda_titik=0.3)
    print_lama("[INFO BALANCE] HP user ikut tumbuh dari kekuatan awal, supaya battle tetap seimbang dan tidak terlalu cepat mati.", jeda_biasa=0.02, jeda_titik=0.3)
    print_lama("[INFO BALANCE] Lawan memakai AI yang menyesuaikan evasion, accuracy, defend, counter attack, dan crit berdasarkan difficulty.", jeda_biasa=0.02, jeda_titik=0.3)


def pilih_mode():
    while True:
        print_lama("\nPilih mode: 1 = Easy, 2 = Medium, 3 = Hard", jeda_biasa=0.02, jeda_titik=0.2)
        pilihan = input("Mode battle (1/2/3): ").strip()
        if pilihan in {"1", "2", "3"}:
            return int(pilihan)
        print_lama("[SYSTEM] Pilihan tidak valid. Masukkan 1, 2, atau 3.", jeda_biasa=0.02, jeda_titik=0.2)


def get_mode_settings(mode):
    return {
        1: {"enemy_scale": 1.00, "hp_scale": 1.00, "defend_bonus": 0.04, "counter_chance": 0.10, "crit_chance": 0.05},
        2: {"enemy_scale": 1.25, "hp_scale": 1.35, "defend_bonus": 0.15, "counter_chance": 0.16, "crit_chance": 0.12},
        3: {"enemy_scale": 1.45, "hp_scale": 1.50, "defend_bonus": 0.22, "counter_chance": 0.24, "crit_chance": 0.16},
    }[mode]


def cek_crit(base_damage, crit_chance, actor):
    if random.random() < crit_chance:
        print_lama(f"\n[CRIT] {actor} mendapat crit! Damage meningkat.", jeda_titik=0.1)
        return round(base_damage * 1.75, 2)
    return base_damage


def cek_counter_attack(damage, counter_chance, actor):
    if random.random() < counter_chance:
        print_lama(f"\n[COUNTER] {actor} melakukan counter attack!", jeda_titik=0.1)
        return round(damage * 0.55, 2)
    return 0


def normalisasi_stat(nilai, batas_bawah, batas_atas):
    return max(batas_bawah, min(batas_atas, nilai))


def dynamic_cap(raw_value, base_cap, growth_rate, max_extra):
    extra = min(max_extra, raw_value * growth_rate)
    return min(base_cap + extra, base_cap + max_extra)


def normalisasi_input(firepower, rate_of_fire, accuracy, evasion):
    firepower_cap = dynamic_cap(firepower, 100, 0.03, 20)
    rate_cap = dynamic_cap(rate_of_fire, 120, 0.02, 20)
    accuracy_cap = dynamic_cap(accuracy, 100, 0.015, 10)
    evasion_cap = dynamic_cap(evasion, 100, 0.015, 10)

    firepower = normalisasi_stat(firepower, 1, int(firepower_cap))
    rate_of_fire = normalisasi_stat(rate_of_fire, 1, int(rate_cap))
    accuracy = normalisasi_stat(accuracy, 0, int(accuracy_cap))
    evasion = normalisasi_stat(evasion, 0, int(evasion_cap))
    return firepower, rate_of_fire, accuracy, evasion


def hitung_bonus_stat(raw_firepower, raw_rate_of_fire, raw_accuracy, raw_evasion):
    firepower_bonus = max(0, raw_firepower - 100)
    rate_bonus = max(0, raw_rate_of_fire - 120)
    accuracy_bonus = max(0, raw_accuracy - 100)
    evasion_bonus = max(0, raw_evasion - 100)

    bonus_ai = round((accuracy_bonus * 0.35) + (evasion_bonus * 0.35) + (firepower_bonus * 0.10), 2)
    bonus_hp = round((firepower_bonus * 0.9) + (rate_bonus * 0.35), 2)
    bonus_tactical = round((accuracy_bonus * 0.2) + (evasion_bonus * 0.2) + (rate_bonus * 0.1), 2)
    return bonus_ai, bonus_hp, bonus_tactical


def hitung_kekuatan_user(firepower, rate_of_fire, accuracy, evasion):
    damage_per_detik = round((firepower * rate_of_fire) / 60, 2)
    combateffectiveness = int((30 * firepower) + (40 * (rate_of_fire ** 2) / 120) + (15 * (accuracy + evasion)))
    kekuatan_awal = round((firepower * 0.55) + (damage_per_detik * 0.25) + (combateffectiveness * 0.20), 2)
    return damage_per_detik, combateffectiveness, kekuatan_awal


def hitung_darah_user(kekuatan_awal):
    return round(1200 + (kekuatan_awal * 2.0), 2)


# ======= MINTA DATA DARI USER =======
difficulty = pilih_mode()
mode_settings = get_mode_settings(difficulty)

nama_boneka_aku = str(input("Masukkan nama boneka: "))
raw_firepower_aku = int(input("Masukkan firepower: "))
raw_rate_of_fire_aku = int(input("Masukkan rate of fire: "))
raw_accuracy_aku = int(input("Masukkan accuracy: "))
raw_evasion_aku = int(input("Masukkan evasion: "))
firepower_aku, rate_of_fire_aku, accuracy_aku, evasion_aku = normalisasi_input(
    raw_firepower_aku,
    raw_rate_of_fire_aku,
    raw_accuracy_aku,
    raw_evasion_aku
)
bonus_ai_aku, bonus_hp_aku, bonus_tactical_aku = hitung_bonus_stat(
    raw_firepower_aku,
    raw_rate_of_fire_aku,
    raw_accuracy_aku,
    raw_evasion_aku
)
damage_per_detik_aku, combateffectiveness_aku, kekuatan_damage_aku = hitung_kekuatan_user(firepower_aku, rate_of_fire_aku, accuracy_aku, evasion_aku)
darah_user = hitung_darah_user(kekuatan_damage_aku) + bonus_hp_aku

def tambah_darah_lawan(darah_lawan_saatini):
    _, _, kekuatan_user = hitung_kekuatan_user(
        firepower_aku,
        rate_of_fire_aku,
        accuracy_aku,
        evasion_aku
    )
    return round(min(5000, darah_lawan_saatini + (kekuatan_user * 4.2 * mode_settings["hp_scale"])), 2)

# total punya user
punya_user = BuatBoneka(f"{nama_boneka_aku}", firepower_aku, rate_of_fire_aku, accuracy_aku, evasion_aku)
kekuatan_combat_aku = combateffectiveness_aku

# Musuh
lawan_terpilih = datalawan.generate_lawan(kekuatan_damage_aku + bonus_ai_aku, difficulty)
firepower_lawan = lawan_terpilih["firepower"]
rate_of_fire_lawan = lawan_terpilih["rate_of_fire"]
accuracy_lawan = lawan_terpilih["accuracy"]
evasion_lawan = lawan_terpilih["evasion"]
dps_lawan = round((firepower_lawan * rate_of_fire_lawan) / 60, 2)
ce_lawan = int((30 * firepower_lawan) + (40 * (rate_of_fire_lawan ** 2) / 120) + (15 * (accuracy_lawan + evasion_lawan)))
lawan_terpilih["damage per detik lawan"] = dps_lawan
lawan_terpilih["combat effectiveness lawan"] = ce_lawan
kekuatan_damage_lawan = round((firepower_lawan * 0.55) + (dps_lawan * 0.25) + (ce_lawan * 0.20), 2)


def main():
    global darah_user, darah_lawan, powerUp_user, powerUp_lawan
    global cooldown_skill_user, cooldown_skill_lawan, cooldown_defend_lawan
    global cooldown_powerup_user, cooldown_powerup_lawan
    global burn_user, burn_lawan, freeze_user, freeze_lawan, shock_user, shock_lawan
    global boost_user, boost_lawan
    print("Selamat datang di ranked!")
    data_boneka = punya_user
    print("\nData boneka yang telah kamu custom:")
    print_lama(json.dumps(data_boneka, indent=4), jeda_biasa=0.02, jeda_titik=0.4)
    print_lama(f"\nKekuatan awal kamu: {kekuatan_damage_aku}", jeda_biasa=0.02, jeda_titik=0.4)
    print_lama(f"\nDarah kamu saat ini: {darah_user}", jeda_biasa=0.02, jeda_titik=0.4)
    print_lama(f"\nKepintaran AI yang dialihkan: {bonus_ai_aku}", jeda_biasa=0.02, jeda_titik=0.4)
    print_lama(f"\nBonus darah yang dialihkan: {bonus_hp_aku}", jeda_biasa=0.02, jeda_titik=0.4)
    tampilkan_info_battle(difficulty)
    print_lama("\n[INFO INTEL] Kamu mendapatkan kabar dari agen intel Badan Intelijen "
               "Kerajaan Dōruzufurontorain yang menyamar sebagai tukang cilok di dekat "
               "markas Mercury. Ternyata Mercury juga memiliki Tactical Doll yang "
               "berjaga di sekitar markasnya...\n", jeda_biasa=0.03, jeda_titik=0.6)
    print("\nData lawan yang telah menghadang kamu:")
    print_lama(json.dumps(lawan_terpilih, indent=4), jeda_biasa=0.02, jeda_titik=0.4)

# pastiin darah lawan lebih tinggi dari user, biar adil, karna human vs random.
    darah_lawan = tambah_darah_lawan(darah_lawan)
    print_lama(f"\nHP awal kamu: {round(darah_user, 2)}", jeda_biasa=0.02, jeda_titik=0.3)
    print_lama(f"HP awal lawan: {round(darah_lawan, 2)}", jeda_biasa=0.02, jeda_titik=0.3)

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
        if cooldown_defend_lawan > 0:
            cooldown_defend_lawan -= 1
        if cooldown_powerup_user > 0:
            cooldown_powerup_user -= 1
        if cooldown_powerup_lawan > 0:
            cooldown_powerup_lawan -= 1

        if boost_user > 0:
            print_lama("\nKamu sedang dalam mode power up. Damage berikutnya akan naik!", jeda_titik=0.1)
            boost_user -= 1
        if boost_lawan > 0:
            print_lama("\nLawan sedang menguatkan diri. Damage berikutnya lawan naik!", jeda_titik=0.1)
            boost_lawan -= 1

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

        aksi_user = input("Pilih aksi (attack/skill/defend/powerups): ").lower()
        if aksi_user not in list_aksi:
            print_lama("Aksi tidak valid. Gunakan attack, skill, defend, atau powerups.")
            continue

        aksi_lawan = pilih_aksi_lawan(aksi_user, evasion_lawan, accuracy_lawan, accuracy_aku, evasion_aku, cooldown_defend_lawan, difficulty)

        if aksi_lawan == "defend":
            cooldown_defend_lawan = 2

        if freeze_lawan > 0:
            aksi_lawan = "defend"

        if aksi_user == "powerups":
            if cooldown_powerup_user == 0:
                cooldown_powerup_user = 2
                boost_user = 2
                damage_aku = hitung_damage(kekuatan_damage_aku, "powerups")
                print_lama("\nKamu memakai power up! Damage kamu akan naik di giliran berikutnya.", jeda_titik=0.1)
            else:
                print_lama(f"\nPower up kamu masih dalam cooldown ({cooldown_powerup_user} giliran tersisa).", jeda_titik=0.1)
                damage_aku = hitung_damage(kekuatan_damage_aku, "attack")
        elif aksi_user == "skill":
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

        if aksi_lawan == "powerups":
            if cooldown_powerup_lawan == 0:
                cooldown_powerup_lawan = 2
                boost_lawan = 2
                damage_lawan = hitung_damage(kekuatan_damage_lawan, "powerups")
                print_lama("\nLawan memakai power up! Damage lawan akan naik di giliran berikutnya.", jeda_titik=0.1)
            else:
                damage_lawan = hitung_damage(kekuatan_damage_lawan, "attack")
        elif aksi_lawan == "skill":
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

        #chance defendse bwt jdi 0
        defend_rate_lawan = hitung_peluang_defend(evasion_lawan, accuracy_lawan, mode_settings["defend_bonus"])
        defend_rate_user = hitung_peluang_defend(evasion_aku, accuracy_aku, mode_settings["defend_bonus"] * 0.8)

        if aksi_lawan == "defend":
            if random.random() < defend_rate_lawan:
                damage_aku = 0
                print_lama("\nLawan mengelak serangan kamu, tetapi ia tetap terkena efek kejut dari serangan kamu!", jeda_titik=0.1)
            else:
                print_lama("\nLawan mengangkat pertahanan, tapi serangan kamu masih mengenai target.", jeda_titik=0.1)

        if aksi_user == "defend":
            damage_lawan = 0 if random.random() < defend_rate_user else damage_lawan

        if boost_user > 0:
            damage_aku = round(damage_aku * 1.25, 2)
        if boost_lawan > 0:
            damage_lawan = round(damage_lawan * 1.25, 2)

        damage_aku = terapkan_powerup(damage_aku, powerUp_user)
        damage_lawan = terapkan_powerup(damage_lawan, powerUp_lawan)

        damage_aku = cek_crit(damage_aku, mode_settings["crit_chance"], "Kamu")
        damage_lawan = cek_crit(damage_lawan, mode_settings["crit_chance"], "Lawan")

        counter_lawan = cek_counter_attack(damage_aku, mode_settings["counter_chance"], "Lawan")
        if counter_lawan > 0:
            darah_user -= counter_lawan

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
