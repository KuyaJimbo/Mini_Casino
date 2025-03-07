import random

def restore_deck():
    return [(i % 13) + 1 for i in range(52)]

def shuffle_deck(deck):
    random.shuffle(deck)

def deal_card(deck):
    if not deck:
        deck = restore_deck()
        shuffle_deck(deck)
    return deck.pop(), deck

def hand_value(hand):
    return sum(hand)

def safe_chance(player_sum, deck):
    safe = sum(1 for card in deck if player_sum + card <= 21)
    return safe / len(deck) if deck else 0

def play_game(strategy, threshold):
    deck = restore_deck()
    shuffle_deck(deck)
    
    player_hand = []
    dealer_hand = []
    
    for _ in range(2):
        card, deck = deal_card(deck)
        player_hand.append(card)
        card, deck = deal_card(deck)
        dealer_hand.append(card)
    
    while hand_value(player_hand) < 21:
        if strategy == 's' and hand_value(player_hand) >= threshold:
            break
        if strategy == 'c' and safe_chance(hand_value(player_hand), deck) < threshold:
            break
        card, deck = deal_card(deck)
        player_hand.append(card)
    
    while hand_value(dealer_hand) < 17:
        card, deck = deal_card(deck)
        dealer_hand.append(card)
    
    return hand_value(player_hand), hand_value(dealer_hand)


strategy = input("Enter strategy (s for SUM, c for CHANCE): ")
threshold = float(input("Enter threshold: "))
games = int(input("Enter number of games to simulate: "))

player_wins, dealer_wins, ties = 0, 0, 0

for _ in range(games):
    player_score, dealer_score = play_game(strategy, threshold)
    
    if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
        dealer_wins += 1
    elif dealer_score > 21 or player_score > dealer_score:
        player_wins += 1
    else:
        ties += 1

print(f"Results after {games} games:")
print(f"Player Wins: {player_wins}")
print(f"Dealer Wins: {dealer_wins}")
print(f"Ties: {ties}")
