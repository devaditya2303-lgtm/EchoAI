print("✨ Welcome to AstroAI – Your Cosmic Guide ✨\n")

# Step 1: Collect user details
name = input("What's your name, cosmic traveler? ")
date_of_birth = input("Enter your date of birth (DD-MM-YYYY): ")
time_of_birth = input("Enter your birth time (HH:MM, optional): ")
place_of_birth = input("Enter your birth place: ")
zodiac = input("Enter your Zodiac/Rashi (optional): ")
nakshatra = input("Enter your Nakshatra (optional): ")

# Step 2: Cosmic greetings
print(f"\nHello {name}! Let’s see what the stars say about you 🌠")

# Step 3: Simple astrology (demo)
if zodiac:
    print(f"Your Zodiac sign {zodiac} suggests you are brave and adventurous!")
else:
    print("You didn’t provide your Zodiac, but the stars still shine for you ✨")

if nakshatra:
    print(f"Your Nakshatra {nakshatra} shows mystical energy and creativity!")

print("\n🔮 Have a magical day! 🌌")
