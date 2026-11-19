cross = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

pattern = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

def calculate_mac(pattern, filter_data):
    score = 0.0
    
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score = score + pattern[row][col] * filter_data[row][col]
    
    return score
        
        
score_a = calculate_mac(pattern, cross)
score_b = calculate_mac(pattern, x_filter)

print("Score A:", score_a)
print("Score B:", score_b)

if abs(score_a - score_b) < 1e-9:
    print("판정: Undecided")
elif score_a > score_b:
    print("판정: A")
else:
    print("판정: B")
