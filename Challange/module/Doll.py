# 1.	firepower (besar damage untuk sekali attack), 
# 2.	rate of fire (berapa banyak attack yang bisa dilakukan dalam satu menit), 
# 3.	accuracy (kemampuan untuk melakukan attack dengan akurat), 
# 4.	evasion (kemampuan untuk menghindari serangan musuh).

# HCUMA MODULE
def BuatBoneka(nama_boneka, firepower, rate_of_fire, accuracy, evasion):
  try:
     firepower = int(firepower)
     rate_of_fire = int(rate_of_fire)
     accuracy = int(accuracy)
     evasion = int(evasion)
        
     damage_per_detik = round((firepower * rate_of_fire) / 60, 2)
     combateffectiveness = int((30 * firepower) + (40 * (rate_of_fire ** 2) / 120) + (15 * (accuracy + evasion)))
        
     return {
      "nama": nama_boneka,
      "firepower": firepower,
      "rate_of_fire": rate_of_fire,
      "accuracy": accuracy,
      "evasion": evasion,
      "damage per detik": damage_per_detik,
      "combat effectiveness": combateffectiveness
        }
  except ValueError:
     return None
