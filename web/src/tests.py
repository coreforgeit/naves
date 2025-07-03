import requests


def test_add_row():
    url = "http://localhost/api/add-row"  # Адрес твоего API (проверь порт!)
    data = {
        'row': {
            "id": 4,
            "sport": "Хоккей",
            "tournament": "НХЛ",
            # "tournament": " ",
            "match": "Детройт - Юта",
            "date": "2026-05-23T21:00:00.000Z",
            "is_top_match": "да",
            "coefficient": "Ничья: 3.65\n\nПобеда хозяев: 1.75\n\nПобеда гостей: 5.20",
            "prediction": "Флуминенсе забил только в одном матче КЧМ, но умеет сушить игру – 0 пропущенных в четырех из пяти последних  матчей.",
            "bet": "Амур победит в ОТ",
            "image": "https://dumpster.cdn.sports.ru/c/cc/6d5798e4cce2cab5de5a2528d09a2.jpg",
            "broadcast": "нет",
            "row_number": 5
        }
    }

    response = requests.post(url, json=data)
    print("Status code:", response.status_code)
    print("Response:", response.json())
    assert response.status_code == 201
    print(response.json())


def test_add_rows():
    url = "http://localhost/api/add-rows"
    data = {
        "rows": [
            {
                "id": 1,
                "sport": "Футбол",
                "tournament": "АПЛ",
                "match": "Ливерпуль - Арсенал",
                "date": "2026-05-20T21:00:00.000Z",
                "is_top_match": "да",
                "coefficient": "Ничья: 3.65\n\nПобеда хозяев: 1.75\n\nПобеда гостей: 5.20",
                "prediction": "Флуминенсе забил только в одном матче КЧМ, но умеет сушить игру – 0 пропущенных в четырех из пяти последних  матчей.",
                "bet": "Ливерпуль победит",
                "image": "https://dumpster.cdn.sports.ru/c/cc/6d5798e4cce2cab5de5a2528d09a2.jpg",
                "broadcast": "https://www.sports.ru/",
                "row_number": 2
            },
            {
                "id": 2,
                "sport": "Хоккей",
                "tournament": "КХЛ",
                "match": "Амур - Куньлунь",
                "date": "2026-05-21T21:00:00.000Z",
                "is_top_match": "нет",
                "coefficient": "Ничья: 3.65\n\nПобеда хозяев: 1.75\n\nПобеда гостей: 5.20",
                "prediction": "Флуминенсе забил только в одном матче КЧМ, но умеет сушить игру – 0 пропущенных в четырех из пяти последних  матчей.",
                "bet": "Амур победит в ОТ",
                "image": "https://dumpster.cdn.sports.ru/c/cc/6d5798e4cce2cab5de5a2528d09a2.jpg",
                "broadcast": "https://www.sports.ru/",
                "row_number": 3
            },
            {
                "id": 3,
                "sport": "Футбол",
                "tournament": "Лига Чемпионов",
                "match": "Барселона - Реал Мадрид",
                "date": "2026-05-22T21:00:00.000Z",
                "is_top_match": "да",
                "coefficient": "Ничья: 3.65\n\nПобеда хозяев: 1.75\n\nПобеда гостей: 5.20",
                "prediction": "Интер выиграл группу, но это не была легкая прогулка – есть ощущение, что возрастной состав докатывает сезон на ободах. Не видно и встряски, которая явно нужна финалисту ЛЧ: Кристиан Киву пока ничего не поменял после Индзаги. \n\nНе удивительно, что самыми яркими выглядят братья Эспозито, которые прошлый сезон провели в аренде.\n\nЕще одно доказательство кризиса: Интер не выигрывал три матча подряд с марта – непривычно долго для самой стабильной команды Италии последних лет.",
                "bet": "Будет ничья",
                "image": "https://dumpster.cdn.sports.ru/c/cc/6d5798e4cce2cab5de5a2528d09a2.jpg",
                "broadcast": "нет",
                "row_number": 4
            },
            {
                "id": 4,
                "sport": "Хоккей",
                "tournament": "НХЛ",
                "match": "Детройт - Юта",
                "date": "2026-05-23T21:00:00.000Z",
                "is_top_match": "да 7",  # <-- Некорректное значение, тут будет ошибка
                "coefficient": "Ничья: 3.65\n\nПобеда хозяев: 1.75\n\nПобеда гостей: 5.20",
                "prediction": "Флуминенсе забил только в одном матче КЧМ, но умеет сушить игру – 0 пропущенных в четырех из пяти последних  матчей.",
                "bet": "Амур победит в ОТ",
                "image": "https://dumpster.cdn.sports.ru/c/cc/6d5798e4cce2cab5de5a2528d09a2.jpg",
                "broadcast": "нет",
                "row_number": 5
            }
        ]
    }

    response = requests.post(url, json=data)
    print("Status code:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_add_row()
    # test_add_rows()
