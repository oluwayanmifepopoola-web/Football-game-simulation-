import random
import time

# --- CONSTANTS ---
STARTING_COINS = 10000
INITIAL_PLAYERS = 5
MAX_OVR = 100

# --- PLAYER CLASS ---

class Player:
    """Represents a single player card in the FC Mobile game."""
    def __init__(self, name, ovr, position):
        self.name = name
        self.ovr = ovr
        self.position = position
        self.level = 1

    def __str__(self):
        """Returns a string representation of the player."""
        return f"⚽ {self.name} ({self.position}) | OVR: {self.ovr} | Lv: {self.level}"

    def get_training_cost(self):
        """Calculates the cost to upgrade the player's level (and OVR)."""
        # Training cost scales based on the current level
        return self.level * 1000

    def apply_training(self):
        """Increases the player's level and overall rating."""
        if self.ovr < MAX_OVR:
            self.level += 1
            # OVR increases by a small random amount to simulate card variance
            self.ovr = min(MAX_OVR, self.ovr + random.randint(1, 2))
            return True
        return False

# --- CLUB MANAGER CLASS ---

class ClubManager:
    """Manages the overall club state, including finances and roster."""
    def __init__(self, club_name):
        self.club_name = club_name
        self.coins = STARTING_COINS
        self.roster = []
        self.match_history = []

    def get_team_ovr(self):
        """Calculates the average OVR of the current roster."""
        if not self.roster:
            return 0
        return sum(player.ovr for player in self.roster) // len(self.roster)

    def display_status(self):
        """Prints the current club status."""
        print("\n" + "="*50)
        print(f"       *** {self.club_name} FC - CLUB STATUS ***")
        print("="*50)
        print(f"💰 Coins: {self.coins:,}")
        print(f"⭐ Team OVR: {self.get_team_ovr()}")
        print(f"👥 Roster Size: {len(self.roster)} Players")
        print(f"📊 Match Record: {len([r for r in self.match_history if r == 'Win'])}W - {len([r for r in self.match_history if r == 'Draw'])}D - {len([r for r in self.match_history if r == 'Loss'])}L")
        print("="*50)

    def display_roster(self):
        """Lists all players in the roster."""
        if not self.roster:
            print("\nYour roster is empty. Go sign some players!")
            return

        print("\n--- Current Roster ---")
        self.roster.sort(key=lambda p: p.ovr, reverse=True)
        for i, player in enumerate(self.roster):
            print(f"[{i+1:02d}] {player}")

    def add_player(self, player):
        """Adds a player to the roster."""
        self.roster.append(player)
        print(f"\n✅ Signed {player.name}! Welcome to the club.")

    def remove_player(self, index):
        """Sells a player from the roster."""
        if 0 <= index < len(self.roster):
            player = self.roster.pop(index)
            sale_price = player.ovr * 100 # Simple formula for selling price
            self.coins += sale_price
            print(f"\n💰 Sold {player.name} for {sale_price:,} Coins.")
        else:
            print("❌ Invalid player index.")

# --- GAME LOGIC FUNCTIONS ---

def generate_player(min_ovr, max_ovr):
    """Generates a random player card."""
    first_names = ["Leo", "Cristiano", "Kylian", "Erling", "Virgil", "Kevin", "Harry", "Karim", "Robert", "Luka"]
    last_names = ["Messi", "Ronaldo", "Mbappe", "Haaland", "Van Dijk", "De Bruyne", "Kane", "Benzema", "Lewandowski", "Modric"]
    positions = ["ST", "RW", "LW", "CM", "CDM", "CB", "LB", "GK"]

    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    ovr = random.randint(min_ovr, max_ovr)
    position = random.choice(positions)
    return Player(name, ovr, position)

def scout_players(club):
    """Allows the user to scout and buy new players."""
    print("\n" + "="*50)
    print("           *** SCOUTING MARKET ***")
    print("="*50)

    # Offer different tiers of scouting packs
    packs = {
        "1": {"name": "Bronze Pack (Low OVR)", "cost": 500, "min_ovr": 60, "max_ovr": 75},
        "2": {"name": "Silver Pack (Mid OVR)", "cost": 2500, "min_ovr": 70, "max_ovr": 85},
        "3": {"name": "Gold Pack (High OVR)", "cost": 7500, "min_ovr": 80, "max_ovr": 95}
    }

    while True:
        print(f"\nYour Coins: {club.coins:,}")
        print("Choose a pack to open:")
        for key, pack in packs.items():
            print(f"[{key}] {pack['name']} - Cost: {pack['cost']:,} Coins")
        print("[0] Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == '0':
            break

        if choice in packs:
            pack = packs[choice]
            if club.coins >= pack['cost']:
                club.coins -= pack['cost']
                print(f"\nOpening {pack['name']}...")
                time.sleep(1)

                new_player = generate_player(pack['min_ovr'], pack['max_ovr'])
                club.add_player(new_player)
                
            else:
                print("❌ Insufficient coins!")
        else:
            print("❌ Invalid choice.")
        print("-" * 20)

def train_player(club):
    """Allows the user to train a player to increase their OVR."""
    if not club.roster:
        print("\n❌ You need players to train them! Go scouting first.")
        return

    club.display_roster()
    print("\n--- Player Training ---")

    while True:
        try:
            choice = input("Enter the number of the player to train (0 to cancel): ")
            if choice == '0':
                return

            index = int(choice) - 1
            if 0 <= index < len(club.roster):
                player = club.roster[index]
                cost = player.get_training_cost()

                if player.ovr == MAX_OVR:
                    print(f"❌ {player.name} is already at max OVR ({MAX_OVR}) and cannot be trained further.")
                    return

                if club.coins >= cost:
                    confirm = input(f"Train {player.name} for {cost:,} Coins? (y/n): ").lower()
                    if confirm == 'y':
                        club.coins -= cost
                        old_ovr = player.ovr
                        player.apply_training()
                        print(f"\n⬆️ {player.name} trained successfully!")
                        print(f"   Level: {player.level} | OVR: {old_ovr} -> {player.ovr}")
                    break
                else:
                    print(f"❌ Insufficient coins! Training cost is {cost:,} Coins.")
                    break
            else:
                print("❌ Invalid number. Please enter a number from the list.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def sell_player_market(club):
    """Allows the user to sell a player from their roster."""
    if not club.roster:
        print("\n❌ Your roster is empty.")
        return

    club.display_roster()
    print("\n--- Player Selling Market ---")

    while True:
        try:
            choice = input("Enter the number of the player to sell (0 to cancel): ")
            if choice == '0':
                return

            index = int(choice) - 1
            if 0 <= index < len(club.roster):
                player = club.roster[index]
                sale_price = player.ovr * 100
                confirm = input(f"Sell {player.name} for {sale_price:,} Coins? (y/n): ").lower()
                if confirm == 'y':
                    club.remove_player(index)
                break
            else:
                print("❌ Invalid number. Please enter a number from the list.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def simulate_match(club):
    """Simulates a match against a random opponent."""
    print("\n" + "="*50)
    print("             *** MATCH DAY ***")
    print("="*50)

    # Generate random opponent stats
    opponent_ovr = random.randint(club.get_team_ovr() - 10, club.get_team_ovr() + 10)
    opponent_name = random.choice(["River Plate", "Boca Juniors", "AC Milan", "Bayern Munich", "PSG", "Liverpool"])
    opponent_name += f" ({opponent_ovr})"

    print(f"📅 Your Team OVR: {club.get_team_ovr()} | Opponent: {opponent_name}")
    print("\nSimulating match...")
    time.sleep(2)

    # Determine match outcome based on OVR difference
    ovr_diff = club.get_team_ovr() - opponent_ovr
    result = "Draw"
    score = "1-1"
    coins_reward = 1000

    if ovr_diff > 5:
        # Strong chance of winning
        if random.random() < 0.7:
            result = "Win"
            score = f"{random.randint(2, 4)}-{random.randint(0, 1)}"
            coins_reward = 3000
        else:
            result = "Draw"
            score = f"{random.randint(1, 2)}-{random.randint(1, 2)}"
            coins_reward = 1500
    elif ovr_diff < -5:
        # Strong chance of losing
        if random.random() < 0.6:
            result = "Loss"
            score = f"{random.randint(0, 1)}-{random.randint(2, 4)}"
            coins_reward = 500
        else:
            result = "Draw"
            score = f"{random.randint(1, 2)}-{random.randint(1, 2)}"
            coins_reward = 1000
    else:
        # Evenly matched
        rand_val = random.random()
        if rand_val < 0.4:
            result = "Win"
            score = f"{random.randint(1, 3)}-{random.randint(0, 2)}"
            coins_reward = 2000
        elif rand_val < 0.8:
            result = "Draw"
            score = f"{random.randint(0, 2)}-{random.randint(0, 2)}"
            coins_reward = 1250
        else:
            result = "Loss"
            score = f"{random.randint(0, 2)}-{random.randint(1, 3)}"
            coins_reward = 750

    # Apply rewards and record history
    club.coins += coins_reward
    club.match_history.append(result)

    print("\n--- Match Result ---")
    if result == "Win":
        print(f"🎉 VICTORY! You defeated {opponent_name} with a score of {score}.")
    elif result == "Draw":
        print(f"🤝 DRAW! You tied with {opponent_name}. Score: {score}.")
    else:
        print(f"😔 DEFEAT! You lost to {opponent_name}. Score: {score}.")

    print(f"💰 Coins Earned: {coins_reward:,}")

# --- MAIN GAME LOOP ---

def main():
    """Main function to run the FC Mobile Simulator."""
    print("=" * 50)
    print("   WELCOME TO FC MOBILE: ULTIMATE TEAM SIMULATOR")
    print("=" * 50)

    club_name = input("Enter your Club Name: ")
    club = ClubManager(club_name)

    # Initial roster setup
    print("\nBuilding initial roster...")
    for _ in range(INITIAL_PLAYERS):
        player = generate_player(min_ovr=65, max_ovr=80)
        club.add_player(player)

    while True:
        club.display_status()
        print("\n--- Main Menu ---")
        print("[1] View Roster")
        print("[2] Scout & Sign Players (Market)")
        print("[3] Train Players (Improve OVR)")
        print("[4] Sell Players")
        print("[5] Play Match (Simulation)")
        print("[0] Exit Game")

        choice = input("Enter action number: ")

        if choice == '1':
            club.display_roster()
            input("\nPress Enter to continue...")
        elif choice == '2':
            scout_players(club)
        elif choice == '3':
            train_player(club)
        elif choice == '4':
            sell_player_market(club)
        elif choice == '5':
            if len(club.roster) < 5:
                print("\n❌ You need at least 5 players to field a team!")
                input("\nPress Enter to continue...")
                continue
            simulate_match(club)
            input("\nPress Enter to continue...")
        elif choice == '0':
            print("\nThank you for playing the FC Mobile Simulator! Goodbye.")
            break
        else:
            print("❌ Invalid choice. Please select a valid number.")

if __name__ == "__main__":
    main()

