from random import SystemRandom

# Virtual balls
white_balls = list(range(1, 71))
red_balls = list(range(1, 26))

# Initialize counters for each number drawn
white_ball_counts = {num: 0 for num in white_balls}
red_ball_counts = {num: 0 for num in red_balls}

seeder = SystemRandom()


def get_manual_numbers():
    while True:
        try:
            numbers = input(
                "Enter 5 unique white ball numbers (1-70) separated by spaces: "
            ).split()
            if len(numbers) != 5 or not all(1 <= int(num) <= 70 for num in numbers):
                raise ValueError
            mega = int(input("Enter a Mega Ball number (1-25): "))
            if not 1 <= mega <= 25:
                raise ValueError
            return set(map(int, numbers)), mega
        except ValueError:
            print("Invalid input. Please try again.")


def display_odds():
    print("\nStatistical Odds of Winning:")
    odds = [
        ("5 of 5 + Mega", "302,575,350"),
        ("5 of 5", "12,607,306"),
        ("4 of 5 + Mega", "931,001"),
        ("4 of 5", "38,792"),
        ("3 of 5 + Mega", "14,547"),
        ("3 of 5", "606"),
        ("2 of 5 + Mega", "693"),
        ("1 of 5 + Mega", "89"),
        ("0 of 5 + Mega", "37"),
    ]
    for game, odd in odds:
        print(f"{game: <15}: 1 in {odd}")
    print("\n")


def print_ascii_distribution(results, total_draws):
    max_value = max(results.values())
    graph_width = 50

    for key, value in sorted(results.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((value / max_value) * graph_width)
        print(f"{key: <15}: {value: >10,} | {'*' * bar_length}")

    winning_draws = total_draws - results["Losses"]
    winning_percentage = (winning_draws / total_draws) * 100
    print(f"Winning Percentage: {winning_percentage:.2f}%")
    print("{:,} Simulated Drawings...".format(draw_count))
    print("-------------------------------")


display_odds()

print("Select your option:")
print("1. Enter numbers manually.")
print("2. Quick Pick single random set.")
print("3. Quick Pick all draws randomly.")

choice = input("Enter your choice (1/2/3): ")

if choice == "1":
    qp_numbers, qp_meganumber = get_manual_numbers()
elif choice == "2":
    qp_numbers = set(seeder.sample(white_balls, 5))
    qp_meganumber = seeder.choice(red_balls)
else:
    qp_numbers = None
    qp_meganumber = None

print(
    "[Selected Numbers]:",
    sorted(qp_numbers) if qp_numbers else "Random each draw",
    [qp_meganumber] if qp_meganumber else "Random each draw",
)

print("Performing odds test...")
draw_count = 0
results = {
    "Losses": 0,
    "0 + Mega": 0,
    "1 + Mega": 0,
    "2 + Mega": 0,
    "3 of 5": 0,
    "3 of 5 + Mega": 0,
    "4 of 5": 0,
    "4 of 5 + Mega": 0,
    "5 of 5": 0,
    "5 of 5 + Mega": 0,
}

while True:
    if choice == "3":
        qp_numbers = set(seeder.sample(white_balls, 5))
        qp_meganumber = seeder.choice(red_balls)

    draw_count += 1
    white_draws = set(seeder.sample(white_balls, 5))
    red_draw = seeder.choice(red_balls)

    white_match_count = len(qp_numbers.intersection(white_draws))
    mega_match_count = 1 if qp_meganumber == red_draw else 0

    for num in white_draws:
        white_ball_counts[num] += 1
    red_ball_counts[red_draw] += 1

    match_key = None
    if white_match_count == 0 and mega_match_count == 1:
        match_key = "0 + Mega"
    elif white_match_count == 1 and mega_match_count == 1:
        match_key = "1 + Mega"
    elif white_match_count == 2 and mega_match_count == 1:
        match_key = "2 + Mega"
    elif white_match_count == 3 and mega_match_count == 0:
        match_key = "3 of 5"
    elif white_match_count == 3 and mega_match_count == 1:
        match_key = "3 of 5 + Mega"
    elif white_match_count == 4 and mega_match_count == 0:
        match_key = "4 of 5"
    elif white_match_count == 4 and mega_match_count == 1:
        match_key = "4 of 5 + Mega"
    elif white_match_count == 5 and mega_match_count == 0:
        match_key = "5 of 5"
        print(f"HIT! 5 of 5 achieved after {draw_count:,} draws!")
        print(
            f"Picked: {sorted(qp_numbers)} [{qp_meganumber}] | Drawn: {sorted(white_draws)} [{red_draw}]"
        )
    elif white_match_count == 5 and mega_match_count == 1:
        match_key = "5 of 5 + Mega"
        print(f"JACKPOT! 5 of 5 + Mega achieved after {draw_count:,} draws!")
        print(
            f"Picked: {sorted(qp_numbers)} [{qp_meganumber}] | Drawn: {sorted(white_draws)} [{red_draw}]"
        )
    else:
        match_key = "Losses"

    results[match_key] += 1

    if draw_count % 1000000 == 0:
        print_ascii_distribution(results, draw_count)

    if draw_count % 10000000 == 0:
        print("White Ball Distribution:")
        max_white_count = max(white_ball_counts.values())
        for num, count in sorted(white_ball_counts.items()):
            bar_length = int((count / max_white_count) * 50)
            print(f"{num:2} | {count: >7,} | {'*' * bar_length}")
        print("-------------------------------")
        print("Red Ball Distribution:")
        max_red_count = max(red_ball_counts.values())
        for num, count in sorted(red_ball_counts.items()):
            bar_length = int((count / max_red_count) * 50)
            print(f"{num:2} | {count: >7,} | {'*' * bar_length}")

    if draw_count > 1000000000:
        print("Test complete. Draw count over 1 billion.")
        break
