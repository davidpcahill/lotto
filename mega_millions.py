from random import SystemRandom, sample

# Virtual balls
white_balls = set([1,2,3,4,5,6,7,8,9,10,
               11,12,13,14,15,16,17,18,19,20,
               21,22,23,24,25,26,27,28,29,30,
               31,32,33,34,35,36,37,38,39,40,
               41,42,43,44,45,46,47,48,49,50,
               51,52,53,54,55,56,57,58,59,60,
               61,62,63,64,65,66,67,68,69,70])

red_balls = set([1,2,3,4,5,6,7,8,9,10,
             11,12,13,14,15,16,17,18,19,20,
             21,22,23,24,25])

print("Adding entropy to seeder.")
seeder = SystemRandom()

# Create quick pick ticket
print("Selecting quick pick for odds test.")
qp_numbers = seeder.sample(list(white_balls), 5)
qp_meganumber = seeder.sample(list(red_balls), 1)
# Sort quick pick
qp_numbers.sort()
# Show quick pick
print("[QP Test]:", str(qp_numbers), str(qp_meganumber))

# Test odds
# TODO: see if using numpy, set, compare, etc is more efficient.
# TODO: Add check for duplicate drawings (from previous)
print("Performing odds test...")
draw_count = 0
loss = 0
zero_and_mega = 0
one_and_mega = 0
two_and_mega = 0
three_of_five = 0
three_of_five_and_mega = 0
four_of_five = 0
four_of_five_and_mega = 0
five_of_five = 0
five_of_five_and_mega = 0

while True:

    # Reset matches
    white_match_count = 0
    mega_match_count = 0

    # Draw numbers
    white_draws = seeder.sample(list(white_balls), 5)
    red_draw = seeder.sample(list(red_balls), 1)

    # Sort white draws
    white_draws.sort()

    # Increase count
    draw_count += 1

    # Check draw for winners and count matches
    for white_number in white_draws:
        for qp_number in qp_numbers:
            if qp_number == white_number:
                white_match_count += 1
    # Mega check
    if qp_meganumber == red_draw:
        mega_match_count = 1

    # Match logic counters
    # none of 5, only Mega
    if (white_match_count == 0) & (mega_match_count == 1):
        zero_and_mega += 1
    # Any 1 of 5 and Mega
    elif (white_match_count == 1) & (mega_match_count == 1):
        one_and_mega += 1
    # Any 2 of 5 and Mega
    elif (white_match_count == 2) & (mega_match_count == 1):
        two_and_mega += 1
    # Any 3 of 5
    elif (white_match_count == 3) & (mega_match_count == 0):
        three_of_five += 1
    # Any 3 of 5 and Mega
    elif (white_match_count == 3) & (mega_match_count == 1):
        three_of_five_and_mega += 1
    # Any 4 of 5
    elif (white_match_count == 4) & (mega_match_count == 0):
        four_of_five += 1
    # Any 4 of 5 and Mega
    elif (white_match_count == 4) & (mega_match_count == 1):
        four_of_five_and_mega += 1
    # All 5 of 5
    elif (white_match_count == 5) & (mega_match_count == 0):
        five_of_five += 1
    # All 5 of 5 and Mega
    elif (white_match_count == 5) & (mega_match_count == 1):
        five_of_five_and_mega += 1
    else:
        loss += 1

    if draw_count % 1000000 == 0:
        print("{:,}".format(draw_count), "Simulated Drawings...")
        print("Current Statistics:")
        print("Loss:", "{:,}".format(loss))
        print("0 + Mega:", "{:,}".format(zero_and_mega))
        print("1 + Mega:", "{:,}".format(one_and_mega))
        print("2 + Mega:", "{:,}".format(two_and_mega))
        print("3 of 5:", "{:,}".format(three_of_five))
        print("3 of 5 + Mega:", "{:,}".format(three_of_five_and_mega))
        print("4 of 5:", "{:,}".format(four_of_five))
        print("4 of 5 + Mega:", "{:,}".format(four_of_five_and_mega))
        print("5 of 5:", "{:,}".format(five_of_five))
        print("5 of 5 + Mega:", "{:,}".format(five_of_five_and_mega))
        print("-------------------------------")

    if draw_count > 1000000000:
        print("Test complete. Draw count over 1 billion.")
        break
