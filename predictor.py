import random
from typing import List, Tuple

def analyze_last_10(results: List[str]) -> Tuple[int, int]:
    """
    results: list of 10 strings, each 'B' or 'S'
             'B' = Big, 'S' = Small
    returns: (big_count, small_count)
    """
    if len(results) != 10:
        raise ValueError("You must provide exactly 10 results.")
    
    big_count = sum(1 for r in results if r.upper() == 'B')
    small_count = sum(1 for r in results if r.upper() == 'S')
    
    if big_count + small_count != 10:
        raise ValueError("Results must only contain 'B' or 'S'.")
    
    return big_count, small_count


def compute_prob_big(big_count: int, small_count: int) -> float:
    """
    Compute probability of 'Big' based on imbalance.
    Biases towards the side that appeared less.
    """
    if big_count == small_count:
        return 0.5  # perfectly balanced, no bias
    
    diff = abs(big_count - small_count)
    # each unit of imbalance shifts probability by 0.05, capped at 0.2
    bias = min(0.2, 0.05 * diff)
    
    if small_count > big_count:
        # Small dominated, so increase chance of Big
        p_big = 0.5 + bias
    else:
        # Big dominated, so decrease chance of Big
        p_big = 0.5 - bias
    
    return p_big


def predict_next(results: List[str], seed: int = None):
    """
    Main function:
      - takes last 10 'B'/'S'
      - uses seed (optional) for reproducible pseudo-randomness
      - prints prediction: next Big/Small and a number 0–9
    """
    if seed is not None:
        random.seed(seed)  # deterministic if you repeat same seed
    
    big_count, small_count = analyze_last_10(results)
    p_big = compute_prob_big(big_count, small_count)
    
    # Decide Big/Small
    draw = random.random()
    next_is_big = draw < p_big
    size_pred = 'Big' if next_is_big else 'Small'
    
    # Now choose a number consistent with Big/Small:
    # often in these games 0–4 = Small, 5–9 = Big
    if next_is_big:
        number_pred = random.randint(5, 9)
    else:
        number_pred = random.randint(0, 4)
    
    # You can add your own color logic; here I just make it random:
    color_pred = random.choice(['Red', 'Green'])
    
    # Pack everything in a dictionary
    prediction = {
        "big_count_last_10": big_count,
        "small_count_last_10": small_count,
        "prob_big": round(p_big, 3),
        "random_draw": round(draw, 3),
        "predicted_size": size_pred,
        "predicted_number": number_pred,
        "predicted_color": color_pred
    }
    
    return prediction


if __name__ == "__main__":
    # EXAMPLE USAGE:
    # last 10 outcomes, from oldest to newest, as 'B' or 'S'
    last_10 = ['S', 'S', 'B', 'S', 'B', 'S', 'S', 'B', 'S', 'S']
    
    # choose any seed you like; using 123 here
    result = predict_next(last_10, seed=123)
    
    print("Analysis & Prediction:")
    for k, v in result.items():
        print(f"{k}: {v}")
