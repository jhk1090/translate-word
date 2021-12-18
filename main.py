import requests
import time
import asyncio
from functools import partial
from bs4 import BeautifulSoup
import os

progress:int = 0
progress_init:int = 100
count:int = 0
count_init:int = 0
saved_storage:dict = {}
keywords:list = []
keywords_init = 0
success = 0
error = 0

async def analyze(url, keyword):  # 코루틴 정의
    global progress, saved_storage, count, error, success
    isSuccessful = False
    cycle = 0
    isInexistCheck = False
    isInexistWord = False
    selector:str = "#mArticle > div.search_cont > div:nth-child(3) > div:nth-child(2) > div.cleanword_type > ul.list_search > li > span.txt_search"
    while not isSuccessful:
        # 요청 시작
        loop = asyncio.get_event_loop()
        request = partial(requests.get, url, headers={
            'user-agent': 'Mozilla/5.0'})
        res = await loop.run_in_executor(None, request)
        soup = BeautifulSoup(res.text, 'html.parser')
        if not isInexistCheck:
            isInexistWord = len(soup.select('strong.tit_info')) == 0
            isInexistCheck = True
        # 재요청 여부
        if len(soup.select(selector)) == 0:
            if (isInexistWord) and (cycle <= 20):
                cycle += 1
                continue
            else:
                isSuccessful = True
                progress += progress_init
                count += 1
                keywords.remove(keyword)
                error += 1
                print(f'{keyword} 실패, {progress:.3f}% 진행 ({count}/{count_init})')
                return '데이터 없음'
        target_list =  []
        for i in soup.select(selector):
            target_list.append(i.text)
        target_stringify = ', '.join([str(elem) for elem in target_list])
        # 응답
        isSuccessful = True
        progress += progress_init
        count += 1
        success += 1
        keywords.remove(keyword)
        print(f'{keyword} 성공, {progress:.3f}% 진행 ({count}/{count_init})')
        saved_storage[keyword] = target_stringify
        return target_stringify

async def receive_input():
    global progress_init, count_init, keywords, keywords_init
    inputwords = input('\
키워드를 입력해주세요\n\
(* abc순 정렬이 권장되고, 키워드는 스페이스로 구분됩니다.) >>\
\n')
    inputwords = inputwords.strip()
    keywords = inputwords.split(' ')
    keywords.sort()
    keywords_init = len(keywords)
    progress_init = 100 / keywords_init
    count_init = keywords_init

async def main():
    base_url = 'https://dic.daum.net/search.do?q={keyword}'
    os.system('cls')
    print("=====================================================")
    await receive_input()
    print("=====================================================")
    futures = [asyncio.ensure_future(analyze(
        base_url.format(keyword=keyword), keyword)) for keyword in keywords]
    result = await asyncio.gather(*futures)
    print("=====================================================")
    print("잠시만 기다려주세요.. ")
    isNewlinePrint = input("결과를 줄바꿈하실건가요? (기본값 y, y/n) >>> ")
    if isNewlinePrint != 'n':
        for i in result:
            print(i)
    else:
        for idx, i in enumerate(result):
            if idx == len(result) - 1:
                print(i)
            else:
                print(i, end="|")
    print("=====================================================")

if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.stop()
        print("=====================================================")
        print("잠시만 기다려주세요.. ")
        saved_storage = dict(sorted(saved_storage.items()))
        isNewlinePrint = input("결과를 줄바꿈하실건가요? (기본값 y, y/n) >>> ")
        if isNewlinePrint != 'n':
            for idx, (key, value) in enumerate(saved_storage.items()):
                print(value)
        else:
            for idx, (key, value) in enumerate(saved_storage.items()):
                if idx == len(saved_storage) - 1:
                    print(value)
                else:
                    print(value, end="|")
        print("=====================================================")
        print(f"결과가 비정상적으로 반환되었습니다. (총 진행도: {progress:.3f}%)")
        print(f"진행중이었던 키워드는 총 {len(keywords)}개입니다.")
        print("다음과 같습니다:")
        for idx, i in enumerate(keywords):
            if idx == len(keywords) - 1:
                print(i)
            else:
                print(i, end=", ")
        print("=====================================================")
    end = time.time()
    print(f'[성공: {success}, 실패: {error}, 미반환: {len(keywords)}], 총계: {keywords_init}')
    print(f'{end-start:.4f}초 소요됨')