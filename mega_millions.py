from random import SystemRandom

# Virtual balls
white_balls = list(range(1, 71))
red_balls = list(range(1, 26))

print("Adding entropy to seeder.")
seeder = SystemRandom()

# Create quick pick ticket
print("Selecting quick pick for odds test.")
qp_numbers = set(seeder.sample(white_balls, 5))
qp_meganumber = seeder.choice(red_balls)
print("[QP Test]:", sorted(qp_numbers), [qp_meganumber])

# Test odds
print("Performing odds test...")
draw_count = 0
results = {
    "loss": 0,
    "0 + Mega": 0,
    "1 + Mega": 0,
    "2 + Mega": 0,
    "3 of 5": 0,
    "3 of 5 + Mega": 0,
    "4 of 5": 0,
    "4 of 5 + Mega": 0,
    "5 of 5": 0,
    "5 of 5 + Mega": 0
}

def print_ascii_distribution(results, total_draws):
    max_value = max(results.values())
    graph_width = 50  # width of the graph in characters

    print("\nASCII Distribution Graph:")
    for key, value in sorted(results.items(), key=lambda x: x[1], reverse=True):  # Sort by value
        bar_length = int((value / max_value) * graph_width)
        print(f"{key: <15}: {value: >10,} | {'*' * bar_length}")

    winning_draws = total_draws - results['loss']
    winning_percentage = (winning_draws / total_draws) * 100
    print(f"\nWinning Percentage: {winning_percentage:.2f}%")
    print("{:,} Simulated Drawings...".format(draw_count))
    print("-------------------------------")


while True:
    draw_count += 1
    white_draws = set(seeder.sample(white_balls, 5))
    red_draw = seeder.choice(red_balls)

    white_match_count = len(qp_numbers.intersection(white_draws))
    mega_match_count = 1 if qp_meganumber == red_draw else 0

    # Match logic counters
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
    elif white_match_count == 5 and mega_match_count == 1:
        match_key = "5 of 5 + Mega"
        print(f"JACKPOT! 5 of 5 + Mega achieved after {draw_count:,} draws!")
    else:
        match_key = "loss"

    results[match_key] += 1

    if draw_count % 1000000 == 0:
        print("{:,}".format(draw_count), "Simulated Drawings...")
        for key, value in results.items():
            print(f"{key}:", "{:,}".format(value))
        print("-------------------------------")
        print_ascii_distribution(results, draw_count)

    if draw_count > 1000000000:
        print("Test complete. Draw count over 1 billion.")
        break
