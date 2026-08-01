# 1.	firepower (besar damage untuk sekali attack), 
# 2.	rate of fire (berapa banyak attack yang bisa dilakukan dalam satu menit), 
# 3.	accuracy (kemampuan untuk melakukan attack dengan akurat), 
# 4.	evasion (kemampuan untuk menghindari serangan musuh).
def DataBoneka():
   print("=== CLASSIC MODE ===")
   print("=== minta attribute boneka ===")
   try:
    nama_boneka = str(input("Masukkan nama boneka: "))
    firepower = int(input("Masukkan firepower: "))
    rate_of_fire = int(input("Masukkan rate of fire: "))
    accuracy = int(input("Masukkan accuracy: "))
    evasion = int(input("Masukkan evasion: "))
    damage_per_detik = round((firepower * rate_of_fire) / 60, 2)
    combateffectiveness = int((30 * firepower) + (40 * (rate_of_fire ** 2) / 120) + (15 * (accuracy + evasion)))
    print("\n### SUCCESS ###")
    print("Nama boneka: ", nama_boneka + "\nFirepower: ", firepower, "\nRate of Fire: ", rate_of_fire, "\nAccuracy: ", accuracy, "\nEvasion: ", evasion, "\nDamage per Detik: ", damage_per_detik, "\nCombat Effectiveness: ", combateffectiveness)
   except ValueError:
        print("Input harus berupa angka untuk firepower, rate of fire, accuracy, dan evasion. Silakan coba lagi.")
DataBoneka()