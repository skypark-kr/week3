def read_matrix(name):
    matrix = []

    print(name, "입력(3줄)")

    for row in range(3):
        while True:
            text = input(f"{row+1} 행 입력: ")
            values = text.split()
            
            if len(values) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                continue
            try: 
                numbers = []
                for value in values:
                    numbers.append(float(value))

            except ValueError:
                print("숫자만 입력하세요")
                continue
            matrix.append(numbers)
            break
    return matrix


def calculate_mac(pattern, filter_data):
    score = 0.0
    
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score = score + pattern[row][col] * filter_data[row][col]
    
    return score
        
filter_a = read_matrix("필터 A")
filter_b = read_matrix("필터 B")

print("필터 저장 완료")
print("A: ", filter_a)
print("B: ", filter_b)
pattern = read_matrix("패턴")

print("패턴 입력 완료!")
print("MAC 계산을 시작합니다.")   
    
score_a = calculate_mac(pattern, filter_a)
score_b = calculate_mac(pattern, filter_b)

print("Score A:", score_a)
print("Score B:", score_b)

if abs(score_a - score_b) < 1e-9:
    print("판정: Undecided")
elif score_a > score_b:
    print("판정: A")
else:
    print("판정: B")
