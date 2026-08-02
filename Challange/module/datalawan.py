import random

# CUMA MODULE
def generate_lawan(user_power=0, difficulty=1):
    list_lawan = [
        {
         "nama": "Hans", "firepower": 60, "rate_of_fire": 85, "accuracy": 70, "evasion": 20
         },
        {
         "nama": "Grobin", "firepower": 75, "rate_of_fire": 60, "accuracy": 80, "evasion": 30
         },
        {
         "nama": "Oscar", "firepower": 50, "rate_of_fire": 90, "accuracy": 65, "evasion": 25
         },
        {
         "nama": "Morgan", "firepower": 80, "rate_of_fire": 70, "accuracy": 75, "evasion": 15
         },
        {
         "nama": "Darren", "firepower": 55, "rate_of_fire": 95, "accuracy": 60, "evasion": 35
         },
        {
         "nama": "Nicho", "firepower": 95, "rate_of_fire": 55, "accuracy": 70, "evasion": 20
         },
        {
         "nama": "Yemima", "firepower": 85, "rate_of_fire": 65, "accuracy": 85, "evasion": 10
         },
        {
         "nama": "Rebbeca", "firepower": 45, "rate_of_fire": 100, "accuracy": 55, "evasion": 40
         },
        {
         "nama": "Michelle", "firepower": 90, "rate_of_fire": 50, "accuracy": 75, "evasion": 15
         },
        {
         "nama": "Shiva", "firepower": 70, "rate_of_fire": 80, "accuracy": 70, "evasion": 30
         },
        {
         "nama": "Kezia", "firepower": 65, "rate_of_fire": 75, "accuracy": 80, "evasion": 25
         },
        {
         "nama": "Julieta", "firepower": 88, "rate_of_fire": 60, "accuracy": 90, "evasion": 10
         },
        {
         "nama": "Devina", "firepower": 100, "rate_of_fire": 40, "accuracy": 65, "evasion": 5
         },
        {
         "nama": "Ethan", "firepower": 50, "rate_of_fire": 85, "accuracy": 85, "evasion": 45
         }
    ]

    lawan = random.choice(list_lawan)

    # Scaling dinamis agar musuh tidak terlalu statis.
    # Semakin kuat user dan semakin tinggi difficulty, semakin tinggi scaling musuh.
    difficulty_scale = {1: 1.0, 2: 1.15, 3: 1.30}[difficulty]

    if user_power > 0:
        scale = (0.9 + (user_power / 1000) * 0.45 + random.uniform(0.05, 0.20)) * difficulty_scale
        rof_scale = (0.95 + (user_power / 1000) * 0.20 + random.uniform(0.0, 0.15)) * difficulty_scale
    else:
        scale = (1.0 + random.uniform(0.0, 0.12)) * difficulty_scale
        rof_scale = (1.0 + random.uniform(0.0, 0.08)) * difficulty_scale

    lawan["firepower"] = int(min(130, lawan["firepower"] * scale))
    lawan["rate_of_fire"] = int(min(130, lawan["rate_of_fire"] * rof_scale))
    lawan["accuracy"] = int(min(100, lawan["accuracy"] + (user_power / 350) + (difficulty * 2)))
    lawan["evasion"] = int(min(100, lawan["evasion"] + (user_power / 500) + (difficulty * 3)))

    return lawan
