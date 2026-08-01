import random
# CUMA MODULE
def generate_musuh():
    
    list_musuh = [
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
    }
]
    musuh = random.choice(list_musuh)
    return musuh