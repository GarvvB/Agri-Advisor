import random

class FarmSimulator:
    def __init__(self, nitrogen, phosphorus, potassium, ph):
        self.n = nitrogen
        self.p = phosphorus
        self.k = potassium
        self.ph = ph
        self.moisture = 60

    def simulate_day(self, temp, humidity, rain):
        evap = temp * 0.08
        uptake = random.uniform(0.5, 1.2)

        self.moisture += rain * 0.6 - evap
        self.moisture = max(10, min(self.moisture, 100))

        self.n -= uptake * 0.8
        self.p -= uptake * 0.5
        self.k -= uptake * 0.6

        self.ph += random.uniform(-0.05, 0.05)

        return {
            "nitrogen": round(self.n,2),
            "phosphorus": round(self.p,2),
            "potassium": round(self.k,2),
            "ph": round(self.ph,2),
            "moisture": round(self.moisture,2)
        }
