from re import sub as regex_replace
from datasets import load_dataset, Dataset
from tqdm import tqdm

total_letter_counter: int = 0

# 카타가나 - 히라가나 사전 만들기 / 히라가나 - 개수 사전 만들기 / 모든 히라가나가 담긴 리스트 만들기
KATA_TO_HIRA: dict[str, str] = {}
hira_counter: dict[str, int] = {}
HIRA_LIST: list[str] = []
# 히라가나 유니코드 범위: 12353 ~ 12438
# 카타가나 유니코드 시작점: 12449 / 히라가나와 1대 1로 대응됨
for hira_unicode in range(12353, 12439):
    hira = chr(hira_unicode)
    KATA_TO_HIRA[chr(12449 + (hira_unicode - 12353))] = hira
    hira_counter[hira] = 0
    HIRA_LIST.append(hira)

kanji_counter: dict[str, int] = {
    chr(kanji_unicode): 0 for kanji_unicode in range(19968, 40911)
}
# 일본어 데이터셋 불러오기
print("Start Loading Dataset...")
dataset: Dataset = load_dataset("izumi-lab/llm-japanese-dataset", revision="main")
print("Done.")
try:
    for data in tqdm(dataset["train"]):
        string: str = ''.join(data[key] for key in data if data[key] not in ['', None])
        string: list = list(string)
        for i, letter in enumerate(string):
            string[i] = KATA_TO_HIRA.get(letter, letter)
        string: str = ''.join(string)
        string = regex_replace("[^ぁ-ん一-龯]", "", string)

        for letter in string:
            total_letter_counter += 1
            if letter in hira_counter:
                hira_counter[letter] += 1
            else:
                kanji_counter[letter] += 1
finally:
    not_used_kanji: list[str] = []
    for key in list(kanji_counter):
        if kanji_counter[key] == 0:
            del kanji_counter[key]
            not_used_kanji.append(key)

    with open("./result_kanji.txt", "wt+", encoding="UTF8") as file:
        file.write(f"---RESULT(total {total_letter_counter} letter)---\n")

        frequency: dict[int, str] = {}
        for hira, value in hira_counter.items():
            file.write(f"{hira}: {value}\n")
            frequency[hira_counter[hira]] = hira

        for kanji, value_ in kanji_counter.items():
            file.write(f"{kanji}: {value_}\n")
            frequency[kanji_counter[kanji]] = kanji

        file.write("---Sort by frequency order---\n")
        for freq in list(reversed(sorted(frequency))):
            file.write(f"{frequency[freq]}: {freq}\n")

        file.write(f"\nNot used Kanji: {', '.join(list(not_used_kanji))}\n")
        file.write("---END---\n\n\n")

    print("Result is saved in 'result_kanji.txt'")
