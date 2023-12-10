일본어 빈도수 분석 프로그램
---
#### 일본어의 발음별 빈도수를 분석합니다.
[해당 데이터셋](https://huggingface.co/datasets/izumi-lab/llm-japanese-dataset)에 있는 모든 일본어 데이터를 사용하여 일본어의 발음별 빈도수를 분석합니다.

### hiragana.py
- **발음별** 빈도수 분석이기에 카타가나는 히라가나로 치환되어 기록됩니다.
- [해당 웹사이트](https://learn-language.tokyo/ja/kanji-hiragana-katakana)를 이용하여 한자를 히라가나로 바꾸어서 기록합니다.
- `result.txt`파일에 분석 결과를 지정합니다
- 프로그램 실행 도중 `CTRL + C`를 눌러 탈출하여도 분석한 만큼의 결과를 `result.txt`에 저장합니다

### include_kanji.py
- 한자를 히라가나로 바꾸지 않고 기록하는 빈도수 분석 프로그램입니다.
- `hiragana.py`와 마찬가지로 카타가나는 히라가나로 치환되어 기록됩니다.
- 유니코드의 특성상, 상용한자와 표외한자를 제외한 한자도 분석됩니다.
- 사용되지 않은 한자는 `Not used Kanji`로 따로 분류되어 한줄로 기록됩니다.
- `result_kanji.txt`파일에 분석 결과를 지정합니다
- 프로그램 실행 도중 `CTRL + C`를 눌러 탈출하여도 분석한 만큼의 결과를 `result_kanji.txt`에 저장합니다

---
Developed by. leehyowon14