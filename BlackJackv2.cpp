#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <ctime>

std::vector<int> restore_deck() {
    std::vector<int> deck;
    for (int i = 0; i < 52; i++) {
        deck.push_back((i % 13) + 1);
    }
    return deck;
}

void shuffle_deck(std::vector<int>& deck) {
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(deck.begin(), deck.end(), g);
}

std::pair<int, std::vector<int>> deal_card(std::vector<int>& deck) {
    if (deck.empty()) {
        deck = restore_deck();
        shuffle_deck(deck);
    }
    int card = deck.back();
    deck.pop_back();
    return {card, deck};
}

int hand_value(const std::vector<int>& hand) {
    return std::accumulate(hand.begin(), hand.end(), 0);
}

double safe_chance(int player_sum, const std::vector<int>& deck) {
    if (deck.empty()) return 0;
    
    int safe_cards = 0;
    for (int card : deck) {
        if (player_sum + card <= 21) {
            safe_cards++;
        }
    }
    return static_cast<double>(safe_cards) / deck.size();
}

std::pair<int, int> play_game(char strategy, double threshold) {
    std::vector<int> deck = restore_deck();
    shuffle_deck(deck);
    
    std::vector<int> player_hand;
    std::vector<int> dealer_hand;
    
    for (int i = 0; i < 2; i++) {
        auto [card, new_deck] = deal_card(deck);
        deck = new_deck;
        player_hand.push_back(card);
        
        auto [dealer_card, newer_deck] = deal_card(deck);
        deck = newer_deck;
        dealer_hand.push_back(dealer_card);
    }
    
    while (hand_value(player_hand) < 21) {
        if (strategy == 's' && hand_value(player_hand) >= threshold) {
            break;
        }
        if (strategy == 'c' && safe_chance(hand_value(player_hand), deck) < threshold) {
            break;
        }
        auto [card, new_deck] = deal_card(deck);
        deck = new_deck;
        player_hand.push_back(card);
    }
    
    while (hand_value(dealer_hand) < 17) {
        auto [card, new_deck] = deal_card(deck);
        deck = new_deck;
        dealer_hand.push_back(card);
    }
    
    return {hand_value(player_hand), hand_value(dealer_hand)};
}

int main() {
    char strategy;
    double threshold;
    int games;
    
    std::cout << "Enter strategy (s for SUM, c for CHANCE): ";
    std::cin >> strategy;
    
    std::cout << "Enter threshold: ";
    std::cin >> threshold;
    
    std::cout << "Enter number of games to simulate: ";
    std::cin >> games;
    
    int player_wins = 0, dealer_wins = 0, ties = 0;
    
    for (int i = 0; i < games; i++) {
        auto [player_score, dealer_score] = play_game(strategy, threshold);
        
        if (player_score > 21 || (dealer_score <= 21 && dealer_score > player_score)) {
            dealer_wins++;
        } else if (dealer_score > 21 || player_score > dealer_score) {
            player_wins++;
        } else {
            ties++;
        }
    }
    
    std::cout << "Results after " << games << " games:" << std::endl;
    std::cout << "Player Wins: " << player_wins << std::endl;
    std::cout << "Dealer Wins: " << dealer_wins << std::endl;
    std::cout << "Ties: " << ties << std::endl;
    
    return 0;
}
