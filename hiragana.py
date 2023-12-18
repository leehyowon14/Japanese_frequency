from re import sub as regex_replace
from datasets import load_dataset, Dataset
from requests import get as http_get
from tqdm import tqdm

total_letter_counter: int = 0

# 카타가나 - 히라가나 사전 만들기 / 히라가나 - 개수 사전 만들기 / 모든 히라가나가 담긴 리스트 만들기
KATA_TO_HIRA: dict[str, str] = {}
hira_counter: dict[str, int] = {}
HIRA_LIST: list[str] = []
# 히라가나 유니코드 시작점: 12353
# 히라가나 유니코드 종료점: 12438
# 카타가나 유니코드 시작점: 12449
for hira_unicode in range(12353, 12439):
    hira = chr(hira_unicode)
    KATA_TO_HIRA[chr(12449 + (hira_unicode - 12353))] = hira
    hira_counter[hira] = 0
    HIRA_LIST.append(hira)

# 일본어 데이터셋 불러오기
print("Start Loading Dataset...")
dataset: Dataset = load_dataset("izumi-lab/llm-japanese-dataset", revision="main")
print("Done.")
try:
    for data in tqdm(dataset["train"]):
        string: str = ''.join(data[key] for key in data if data[key] not in ['', None])
        # 모든 글자 히라가나로 바꾼 후 히라가나만 남기기
        res: list = list(http_get(
            f"https://learn-language.tokyo/api/toHiraganaKanjiKatakana?text={string}&toLang=toFuriganaNormal",
            timeout=30
        ).text)
        for i, letter in enumerate(res):
            res[i] = KATA_TO_HIRA.get(letter, letter)
        res: str = ''.join(res)
        res = regex_replace("[^ぁ-ん]", "", res)

        for letter in res:
            total_letter_counter += 1
            hira_counter[letter] += 1
finally:
    with open("./result.txt", "wt+", encoding="UTF8") as file:
        file.write(f"---RESULT(total {total_letter_counter} letter)---\n")
        frequency: dict[int, str] = {}
        for hira, value in hira_counter.items():
            file.write(f"{hira}: {value}\n")
            frequency[hira_counter[hira]] = hira

        file.write("---Sort by frequency order---\n")
        for freq in list(reversed(sorted(frequency))):
            file.write(f"{frequency[freq]}: {freq}\n")
        file.write("---END---\n\n\n")

    print("Result is saved in 'result.txt'")
