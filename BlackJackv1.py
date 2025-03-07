import random

def restore_deck():
    return [i % 13 + 1 for i in range(52)]

def shuffle_deck(deck):
    random.shuffle(deck)

def deal_card(deck):
    return deck.pop() if deck else None

def show_hand(hand):
    total = sum(hand)
    print(f"Hand: {hand} (Total: {total})")
    return total

def safe_chance(player_sum, deck):
    safe = sum(1 for card in deck if player_sum + card <= 21)
    return safe / len(deck) if deck else 0

def play_game(strategy, threshold):
    deck = restore_deck()
    shuffle_deck(deck)
    
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    
    print("Player's Turn:")
    player_sum = show_hand(player_hand)
    print(f"Dealer shows: {dealer_hand[0]}, ?")
    
    while player_sum < 21:
        if strategy == 's' and player_sum >= threshold:
            break
        elif strategy == 'c' and safe_chance(player_sum, deck) < threshold:
            break
        
        player_hand.append(deal_card(deck))
        player_sum = show_hand(player_hand)
    
    if player_sum > 21:
        print("Player busts! Dealer wins.")
        return "Dealer"
    
    print("Dealer's Turn:")
    dealer_sum = show_hand(dealer_hand)
    
    while dealer_sum < 17:
        dealer_hand.append(deal_card(deck))
        dealer_sum = show_hand(dealer_hand)
    
    if dealer_sum > 21 or player_sum > dealer_sum:
        print("Player wins!")
        return "Player"
    else:
        print("Dealer wins!")
        return "Dealer"

def main():
    strategy = input("Enter strategy (sum 's' or chance 'c'): ").strip()
    threshold = float(input("Enter threshold: "))
    games = int(input("Enter number of games: "))
    
    results = {"Player": 0, "Dealer": 0}
    for _ in range(games):
        winner = play_game(strategy, threshold)
        results[winner] += 1
    
    print(f"Final Results: Player {results['Player']} - Dealer {results['Dealer']}")

if __name__ == "__main__":
    main()
