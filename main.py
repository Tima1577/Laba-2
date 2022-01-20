import csv
import requests
from bs4 import BeautifulSoup

print('Какой жанр вас интересует? Отвечайте на ангийском, пожалуйста')
tags = input().split(",")
print('Какая минимальная оценка?')
Rating = (input())
print('Какое минимальное количество оценок?')
number_of_votes = (input())
print('Каких предупреждений не должно быть?')
content_warning = input().split(",")
print('Какой тип?')
type_anime = input()
print('Какое минимально количество эпизодов?')
episodes = input()
print('Закончено? Если да то ответье True, если нет то False')
finish = input()
answer = []
final_answer = []
a = []

with open('anime.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for i in tags:
            if i in row['Tags']:
                answer.append(row)
    for row in answer[:]:
        if row['Rating Score'] == 'Unknown':
            answer.remove(row)
            continue
        if not(float(Rating) <= float(row['Rating Score'])):
            answer.remove(row)
    for row in answer[:]:
        if row['Number Votes'] == 'Unknown':
            answer.remove(row)
            continue
        if not(float(number_of_votes) <= float(row['Number Votes'])):
            answer.remove(row)
    for row in answer[:]:
        for i in content_warning:
            if i in row['Content Warning']:
                answer.remove(row)
                break
    for row in answer[:]:
        if row['Type'] == 'Unknown':
            answer.remove(row)
            continue
        if not(row['Type'] == type_anime):
            answer.remove(row)
    for row in answer[:]:
        if row['Episodes'] == 'Unknown':
            answer.remove(row)
            continue
        if not(float(episodes) <= float(row['Episodes'])):
            answer.remove(row)
    for row in answer[:]:
        if not(row['Finished'] == finish):
            answer.remove(row)
    for row in answer:
        a = [float(row['Rating Score']), (row['Name']), (row['Url'])]
        final_answer.append(a)
print(answer)
final_answer.sort()
final_answer.reverse()

f = open('answer.txt', 'w', encoding='utf-8')
for i in range(min(5, len(final_answer))):
    response = requests.get(final_answer[i][2])
    soup = BeautifulSoup(response.text, 'html.parser')
    img = requests.get("https://www.anime-planet.com/" + soup.find('img', class_='screenshots')['src'])
    img_file = open(str(i + 1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    f.write(final_answer[i][2] + ': ' + final_answer[i][1] + '\n')
for i in range(min(5, len(final_answer)), len(final_answer)):
    f.write(final_answer[i][2] + ': ' + final_answer[i][1] + '\n')
f.close()
