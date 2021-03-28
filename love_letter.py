import time
import random
from collections import Counter
from colorama import init, Fore

init()

n_players = 4
full_deck = [1] * 7 + [2] * 2 + [3] * 2 + [4] * 2 + [5] * 2 + [6, 7, 8]

names = ['Вася', 'Петя', 'Дядя Федор', 'Повар', 'Пикачу', 'Капитошка', 'Моряк Папай', 'Шляпокот', 'Овощной пацан', 'Геннадий', 'Петрович', 'Альбус Дамблдор', 'Алеша Попович', 'Доктор Кто', 'Салат Цезарь', 'Соус Тартар', 'Велоцираптор', 'Боб Строитель', 'Гордон Фример', 'Халк', 'Котопес', 'Манчкин 99 Уровня', 'Джимми Нейтрон', 'Шерлок Холмс', 'Ленин', 'Чубакка', 'СуперСтас', 'Соник', 'Морфиус', 'Росомаха', 'Бакалавр Йода', 'Родион Раскольников', 'Булка с Корицей', 'Чеширский Кот', 'Супер Умный Бот v1.16', 'Илон Маск']
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.YELLOW, Fore.RED, Fore.MAGENTA]
end_color = Fore.RESET
your_color = Fore.LIGHTBLUE_EX

random.shuffle(names)
random.shuffle(colors)
you = 0

deck = []
discards = []
protected = set()
dead = set()
n_round = 1
max_rounds = 3
scores = Counter()


def is_you(player):
    return player == you


def get_name(player, case=0):
    if is_you(player):
        if case == 1:
            return f'{your_color}Вас{end_color}'
        elif case == 2:
            return f'{your_color}Вами{end_color}'
        return f'{your_color}Вы{end_color}'
    return f'{colors[player]}{names[player]}{end_color}'


def get_alive_players():
    return [i for i in range(n_players) if i not in dead]


def get_possible_aims(player, card=None):
    return [i for i in range(n_players) if i not in dead and i not in protected and (i != player or card == 5)]


def show_alive_players():
    alive_players = get_alive_players()
    if len(alive_players) >= 2:
        alive_names = [get_name(i) for i in alive_players]
        print(f"Остались только {', '.join(alive_names[:-1])} и {alive_names[-1]}")
    elif is_you(alive_players[0]):
        print(f"Остались только {get_name(you)}")
    else:
        print(f'Остался только {get_name(alive_players[0])}')


def is_the_end():
    if n_players - len(dead) == 1:
        winner = list(set(cards) - dead)[0]
        if is_you(winner):
            print(f'{get_name(you)} победили')
        else:
            print(f'Побеждает {get_name(winner)}')
        scores[winner] += 1
        return True
    if not deck:
        print('Колода закончилась.')
        alive = get_alive_players()
        for player in alive:
            print(f'У {get_name(player, 1)} карта {cards[player]}')
        highest = max(cards[player] for player in alive)
        max_players = [player for player in alive if cards[player] == highest]
        if len(max_players) > 1:
            print(f'Игроков с наибольшей картой ({highest}) несколько, поэтому ничья')
        else:
            player = max_players[0]
            if is_you(player):
                print(f'У {get_name(you, 1)} наибольшая карта ({highest}), поэтому {get_name(you)} побеждаете')
            else:
                print(f'У {get_name(player)} наибольшая карта ({highest}), поэтому он побеждает')
            scores[player] += 1
        return True


def kill(player):
    card, cards[player] = cards[player], None
    if card:
        if is_you(player):
            print(f'{get_name(you)} выбываете из игры и сбрасываете карту {card}')
        else:
            print(f'Игрок {get_name(player)} выбывает из игры и сбрасывает карту {card}')
        discards.append(card)
    else:
        if is_you(player):
            print(f'{get_name(you)} выбываете из игры')
        else:
            print(f'Игрок {get_name(player)} выбывает из игры')

    dead.add(player)
    show_alive_players()


def drop(player):
    card = cards[player]
    if is_you(player):
        print(f'{get_name(you)} сбрасываете карту {card}')
    else:
        print(f'Игрок {get_name(player)} сбрасывает карту {card}')
    if card == 8:
        cards[player] = None
        kill(player)
    cards[player] = deck.pop()
    discards.append(card)


def move_guard(player, guess, dest):
    if dest is None:
        print(f'{get_name(player)} сбрасывает Стражницу, потому что остальные игроки под защитой Служанки')
        return
    if is_you(player):
        print(f'{get_name(you)} думаете, что {get_name(dest)} - {guess}')
    else:
        print(f'{get_name(player)} думает, что {get_name(dest)} - {guess}')
    if guess == cards[dest]:
        print(f'{get_name(you)} угадали!' if is_you(player) else f'{get_name(player)} угадал')
        kill(dest)
    else:
        print(f'{get_name(you)} не угадали' if is_you(player) else f'{get_name(player)} не угадал')


def move_priest(player, dest):
    if dest is None:
        print(f'{get_name(player)} сбрасывает Священника, потому что остальные игроки под защитой Служанки')
        return
    if is_you(player):
        print(f'{get_name(player)} играете Священника против {get_name(dest, 1)}')
        print(f'{get_name(dest)} показывает карту {cards[dest]}')
    elif is_you(dest):
        print(f'{get_name(player)} играет Священника против {get_name(you, 1)}')
        print(f'{get_name(dest)} показываете карту {cards[dest]}')
    else:
        print(f'{get_name(player)} играет Священника против {get_name(dest, 1)}')
        print(f'{get_name(dest)} показывает свою карту {get_name(player, 1)}')


def move_baron(player, dest):
    if dest is None:
        print(f'{get_name(player)} сбрасывает Барона, потому что остальные игроки под защитой Служанки')
        return
    if is_you(player):
        print(f'{get_name(you)} играете Барона против {get_name(dest, 1)}')
        print(f'У игрока {get_name(dest)} карта {cards[dest]}')
    elif is_you(dest):
        print(f'{get_name(player)} играет Барона против {get_name(you, 1)}')
        print(f'У {get_name(dest, 1)} карта {cards[dest]}')
    else:
        print(f'{get_name(player)} играет Барона против {get_name(dest, 1)}')
    if cards[player] < cards[dest]:
        kill(player)
    elif cards[player] > cards[dest]:
        kill(dest)
    else:
        print('Одиннаковые карты, ничего не происходит.')


def move_maid(player):
    if is_you(player):
        print(f'{get_name(you)} играете Служанку')
    else:
        print(f'{get_name(player)} играет Служанку')
    protected.add(player)


def move_prince(player, dest):
    if dest is None:
        print(f'{get_name(player)} сбрасывает Принца, потому что остальные игроки под защитой Служанки')
        return
    if is_you(player):
        print(f'{get_name(you)} играете Принца против {get_name(dest, 1)}')
    elif is_you(dest):
        print(f'{get_name(player)} играет Принца против {get_name(you, 1)}')
    else:
        print(f'{get_name(player)} играет Принца против {get_name(dest, 1)}')
    drop(dest)


def move_king(player, dest):
    if dest is None:
        print(f'{get_name(player)} сбрасывает Короля, потому что остальные игроки под защитой Служанки')
        return
    if is_you(player):
        print(f'{get_name(you)} меняетесь картами с {get_name(dest)}')
    elif is_you(dest):
        print(f'{get_name(player)} меняется картами с {get_name(you, 2)}')
    else:
        print(f'{get_name(player)} меняется картами с {get_name(dest)}')
    cards[player], cards[dest] = cards[dest], cards[player]


def move_countess(player):
    if is_you(player):
        print(f'{get_name(you)} играете Графиню')
    else:
        print(f'{get_name(player)} играет Графиню')


def move_princess(player):
    if is_you(player):
        print(f'{get_name(you)} сбрасываете Принцессу')
    else:
        print(f'{get_name(player)} сбрасывает Принцессу')
    kill(player)


moves = {
    1: move_guard,
    2: move_priest,
    3: move_baron,
    4: move_maid,
    5: move_prince,
    6: move_king,
    7: move_countess,
    8: move_princess,
}


def promt(new, old):
    print(f'Ваши карты {new} и {old}')
    while True:
        choice = input('Выберите карту: ')
        try:
            choice = int(choice)
        except:
            pass
        if choice not in (new, old):
            print(f'Можно выбрать только {new} или {old}')
            continue
        if choice == 1:
            return choice, promt_guard()
        elif choice == 5 and max(new, old) == 7:
            print('Нужно сбросить карту 7, если на руке карта 5 или 6')
        elif choice in (2, 3, 5, 6):
            return choice, promt_dest(choice)
        return choice, {}


def promt_guard():
    while True:
        try:
            aims = get_possible_aims(you)
            aims_names = [f'{get_name(player)} ({player})' for player in aims]
            string = input(f'Выберите игрока и угадайте карту - {", ".join(aims_names)}: ')
            dest, guess = [int(part) for part in string.strip().replace(', ', ' ').replace(',', ' ').split(' ')]
            if guess not in range(2, 9):
                print('Можно угадывать только карты 2-8')
                continue
            if is_you(dest):
                print(f'Вы не можете выбрать себя')
            elif dest in protected:
                print(f'Игрок {dest} не может быть выбран, он под защитой Служанки')
            elif dest in dead:
                print(f'Игрок {dest} не может быть выбран, он выбыл из игры')
            elif dest not in aims:
                print('Нужно ввести номер игрока')
            else:
                return {'dest': dest, 'guess': guess}
        except:
            print('Ввести нужно два числа через пробел или запятую')


def promt_dest(card):
    while True:
        aims = get_possible_aims(you, card)
        aims_names = [f'{get_name(player)} ({player})' for player in aims]
        string = input(f'Выберите игрока - {", ".join(aims_names)}: ')
        try:
            dest = int(string)
        except:
            print('Нужно ввести номер игрока')
            continue
        if dest in dead:
            print(f'Игрок {dest} уже выбыл из игры')
        elif dest in protected:
            print(f'Игрок {dest} находится под защитой Служанки')
        elif dest not in aims:
            print('Нужно ввести номер игрока')
        else:
            return {'dest': dest}


def move_bot(player, card1, card2):
    time.sleep(2)
    card = random.choice([card1, card2])
    if card == 8:
        card = min(card1, card2)
    if card == 7 and min(card1, card2) in (5, 6):
        card = min(card1, card2)
    aims = get_possible_aims(player)
    if not aims:
        aim = None
    else:
        aim = random.choice(aims)
    if card == 1:
        possible_cards = Counter(full_deck) - Counter(discards) - Counter([card1, card2])
        possible = random.choice([card for card in possible_cards.elements() if card != 1])
        return card, {'dest': aim, 'guess': possible}
    if card in (2, 3, 5, 6):
        return card, {'dest': aim}
    return card, {}


def move(player):
    time.sleep(1)
    print('='*24)
    print('Ваш ход' if is_you(player) else f'Сейчас ходит {get_name(player)}')
    if player in protected:
        protected.remove(player)
    new, old = deck.pop(), cards[player]
    if is_you(player):
        choice, kwargs = promt(new, old)
    else:
        choice, kwargs = move_bot(player, new, old)
    cards[player] = old if choice == new else new
    moves[choice](player, **kwargs)
    discards.append(choice)


def play_round():
    global deck, out_card, cards, discards, protected, dead
    deck = full_deck.copy()
    random.shuffle(deck)
    out_card = deck.pop()
    cards = {i: deck.pop() for i in range(n_players)}
    discards.clear()
    protected.clear()
    dead.clear()
    player = 0
    while deck:
        if is_the_end():
            return
        if player in dead:
            player = (player + 1) % n_players
            continue
        print(f'Осталось в колоде {len(deck) * "|"} {len(deck)} карт')
        if discards:
            print(f"Сброс: {','.join(map(str, discards))}")
        move(player)
        player = (player + 1) % n_players
    is_the_end()


def show_scores():
    print()
    print('Счет:')
    for player, score in scores.most_common():
        print(f'{get_name(player)} - {score}')


print('Играют в игру:', ', '.join(get_name(i) for i in range(n_players-1)), 'и', get_name(n_players-1))

while n_round <= max_rounds:
    print()
    print(f'Новый раунд {n_round}/{max_rounds}')
    play_round()
    n_round += 1

show_scores()
