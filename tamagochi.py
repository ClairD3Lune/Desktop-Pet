import time
import random
import json
import os
from datetime import datetime, timedelta

class Tamagotchi:
    def __init__(self, name, stage="baby", hunger=50, energy=50, mood="neutral", level=1, exp=0, nap_until=None):
        self.name = name
        self.stage = stage
        self.hunger = hunger
        self.energy = energy
        self.mood = mood
        self.level = level
        self.exp = exp
        self.nap_until = nap_until  # real time nap tracking

    def show_status(self):
        print(f"\n✨ {self.name}'s Stats ✨")
        print(f"🌱 Stage: {self.stage}")
        print(f"❤️ Mood: {self.mood}")
        print(f"🍖 Hunger: {self.hunger}/100")
        print(f"⚡ Energy: {self.energy}/100")
        print(f"⭐ Level: {self.level} | XP: {self.exp}/100")

        if self.is_napping():
            print("🛌 Status: Napping... shhh 🪫")
            self.show_ascii()
            return  # early return, don't talk or react

        self.say_something()
        self.show_ascii()

    def is_napping(self):
        if self.nap_until:
            wake_time = datetime.fromisoformat(self.nap_until)
            now = datetime.now()
            if now < wake_time:
                remaining = wake_time - now
                minutes, seconds = divmod(remaining.total_seconds(), 60)
                print(f"🛌 {self.name} is sleeping for {int(minutes)}m {int(seconds)}s more.")
                return True
            else:
                self.nap_until = None  # nap's over
                print(f"🌞 {self.name} woke up well-rested!")
                self.energy =min(100, self.energy + random.randint(10, 40))
        return False

    def show_ascii(self):
        if self.is_napping():
            print(r"""
  ( -_-) Zzz
  (\__/)    
 ( – w – ) 
  /　づ     """)
        elif self.stage == "baby":
            print(r"""
  (\__/)
  (•ㅅ•)   
  / 　 づ
""")
        elif self.stage == "teen":
            print(r"""
  ʕ•́ᴥ•̀ʔっ
 (   ⊃⊃ )
""")
        elif self.stage == "eldritch abomination":
            print(r"""
   ☉･‿･☉  
  /█\▕█▕
 /  \    \
 [RUN]
""")

    def say_something(self):
        mood_quotes = {
            "hungry": "🍔 Feed me or I *will* riot.",
            "tired": "🛌 Zzz... why am I even awake?",
            "ecstatic": "✨ I feel ALIVE!!",
            "cosmically unstable": "👁 I have seen beyond the veil.",
            "happy": "😊 You’re the best, Pookie <3",
            "bored": "🚒 This is LAME.",
            "neutral": "¯\\_(ツ)_/¯ meh.",
            "energetic": "⚡ LET’S GOOOOOO!!!"
        }
        print(f"\n🔨 {self.name} says: \"{mood_quotes.get(self.mood, '...')}\"")

    def feed(self):
        if self.is_napping():
            print("You can't wake it up to feed it, that's rude 😤")
            return
        self.hunger = min(100, self.hunger + 20)
        print("You gave it a mysterious snack... 🍖")
        self.update_mood()

    def nap(self):
        if self.is_napping():
            print("It's already snoozing 💩 Let it rest, bestie.")
            return
        nap_duration = timedelta(minutes=0.1)  # Change to hours if needed
        self.nap_until = (datetime.now() + nap_duration).isoformat()
        print(f"\nPutting {self.name} to sleep. 🛌 It'll wake up soon.")
        self.update_mood()

    def pet(self):
        if self.is_napping():
            print("Petting a sleeping creature... suspicious 😳")
        else:
            print("A gentle pat 💐🫡 It liked that.")
        self.mood = random.choice(["happy", "ecstatic", "bored"])

    def dungeon(self):
        if self.is_napping():
            print("Let it nap! Dungeons can wait. 😤")
            return
        print("Marching into the dungeon like a legend. 🚡️")
        enemies = ["slime", "goblin", "shadow being", "your ex"]
        enemy = random.choice(enemies)
        print(f"A wild {enemy} appears!")

        time.sleep(1)
        outcome = random.choices(["win", "lose"], weights=[0.7, 0.3])[0]

        if outcome == "win":
            gain = random.randint(15, 30)
            print(f"Slayed the {enemy}! +{gain} XP 💪")
            self.exp += gain
            if self.exp >= 100:
                self.level += 1
                self.exp = 0
                print("🎉 LEVEL UP!!! 🎉")
                self.evolve()
        else:
            print(f"Oof, the {enemy} bonked your pet. -15 energy")
            self.energy = max(0, self.energy - 15)
        self.update_mood()

    def evolve(self):
        if self.level >= 3 and self.stage == "baby":
            self.stage = "teen"
            print("✨ Your pet evolved into a rebellious teen!")
        elif self.level >= 6 and self.stage == "teen":
            self.stage = "eldritch abomination"
            print("😨 It has transcended... it now whispers in ancient tongues.")

    def update_mood(self):
        if self.hunger < 30:
            self.mood = "hungry"
        elif self.energy < 30:
            self.mood = "tired"
        elif self.level >= 6:
            self.mood = "cosmically unstable"
        else:
            self.mood = random.choice(["happy", "neutral", "bored", "energetic"])

    def save(self):
        data = self.__dict__
        with open(f"{self.name}.json", "w") as f:
            json.dump(data, f)
        print("📂 Saved! Don't lose me, Pookie!")

    @staticmethod
    def load(name):
        if os.path.exists(f"{name}.json"):
            with open(f"{name}.json", "r") as f:
                data = json.load(f)
                return Tamagotchi(**data)
        return None

# Main game loop
def main():
    print("🎮 Welcome to Terminal Tamagotchi V2: Sassy Sleeper Edition")
    name = input("Name your Tamagotchi (or type to load): ").strip()

    tama = Tamagotchi.load(name)
    if tama:
        print(f"Welcome back, {name}! 😎")
    else:
        tama = Tamagotchi(name)
        print(f"✨ New digital child created: {name}")

    while True:
        tama.show_status()

        if tama.is_napping():
            print("😤 Let it finish its nap before doing anything else!")
            time.sleep(2)  # pause for drama
            continue

        print("\nActions: [1] Feed [2] Nap [3] Pet [4] Dungeon [5] Save [6] Quit")
        choice = input("> ").strip()

        if choice == "1":
            tama.feed()
        elif choice == "2":
            tama.nap()
        elif choice == "3":
            tama.pet()
        elif choice == "4":
            tama.dungeon()
        elif choice == "5":
            tama.save()
        elif choice == "6":
            print("👋 Bye bye! May it not devour the world while you sleep.")
            tama.save()
            break
        else:
            print("Nope. Invalid. Try again, Pooks.")

if __name__ == "__main__":
    main()