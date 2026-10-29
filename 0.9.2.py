import os
import sys
import json
import random
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

VERSION = "v0.9.2"
CRIT_CHANCE = 0.15
CRIT_MULT = 2.0

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except Exception:
    SOUND_ENABLED = False

LANG = "ru"
FULLSCREEN = False
MUSIC_ENABLED = True
SOUNDS_ENABLED = True
MUSIC_VOLUME = 0.5
SOUNDS_VOLUME = 0.7
MUSIC_CHOICE = "random"

SETTINGS_FILE = "settings.json"
SAVE_FILE = "save.json"
SOUNDS = {}
GAME_START_TIME = time.time()

GAME_MUSIC_TRACKS = [
    {"file": "game_music1.ogg", "weight": 70},
    {"file": "game_music2.ogg", "weight": 30},
]

def pick_random_game_music():
    files = [t["file"] for t in GAME_MUSIC_TRACKS]
    weights = [t["weight"] for t in GAME_MUSIC_TRACKS]
    return random.choices(files, weights=weights, k=1)[0]

def play_current_game_music():
    fname = pick_random_game_music() if MUSIC_CHOICE == "random" else MUSIC_CHOICE
    play_music(fname)

def load_settings():
    global LANG, FULLSCREEN, MUSIC_ENABLED, SOUNDS_ENABLED, MUSIC_VOLUME, SOUNDS_VOLUME, MUSIC_CHOICE
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            LANG = data.get("lang", "ru")
            FULLSCREEN = data.get("fullscreen", False)
            MUSIC_ENABLED = data.get("music_enabled", True)
            SOUNDS_ENABLED = data.get("sounds_enabled", True)
            MUSIC_VOLUME = data.get("music_volume", 0.5)
            SOUNDS_VOLUME = data.get("sounds_volume", 0.7)
            MUSIC_CHOICE = data.get("music_choice", "random")
        except Exception:
            pass

def save_settings():
    data = {"lang": LANG, "fullscreen": FULLSCREEN,
            "music_enabled": MUSIC_ENABLED, "sounds_enabled": SOUNDS_ENABLED,
            "music_volume": MUSIC_VOLUME, "sounds_volume": SOUNDS_VOLUME,
            "music_choice": MUSIC_CHOICE}
    try:
        tmp = SETTINGS_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, SETTINGS_FILE)
    except Exception:
        pass

def load_sounds():
    if not SOUND_ENABLED:
        return
    sound_files = {"attack": "attack.wav", "heal": "heal.wav", "fireball": "fireball.wav",
                   "heal_spell": "heal_spell.wav", "hit": "hit.wav", "victory": "victory.wav",
                   "death": "death.wav", "levelup": "levelup.wav", "move": "move.wav",
                   "rest": "rest.wav", "shop": "shop.wav", "click": "click.wav",
                   "crit": "crit.wav"}
    for key, filename in sound_files.items():
        path = resource_path(os.path.join("sounds", filename))
        if os.path.exists(path):
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(SOUNDS_VOLUME)
                SOUNDS[key] = snd
            except Exception:
                pass

def update_sounds_volume():
    for key in SOUNDS:
        try:
            SOUNDS[key].set_volume(SOUNDS_VOLUME)
        except Exception:
            pass

def play_sound(key):
    if SOUND_ENABLED and SOUNDS_ENABLED and key in SOUNDS:
        try:
            SOUNDS[key].play()
        except Exception:
            pass

def play_music(filename, loop=True):
    if not SOUND_ENABLED or not MUSIC_ENABLED:
        return
    path = resource_path(os.path.join("sounds", filename))
    if os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1 if loop else 0)
        except Exception:
            pass

def update_music_volume():
    if SOUND_ENABLED:
        try:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
        except Exception:
            pass

def stop_music():
    if SOUND_ENABLED:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass


TEXTS = {
    "ru": {
        "title": "The World Manile", "new_game": "Новая игра", "load_game": "Загрузить игру",
        "settings": "Настройки", "help": "Помощь", "quit": "Выйти", "back": "Назад", "save": "Сохранить",
        "language": "Язык", "fullscreen": "Полный экран", "music": "Музыка", "sounds": "Звуки",
        "on": "Вкл", "off": "Выкл",
        "music_volume": "Громкость музыки", "sounds_volume": "Громкость звуков",
        "music_choice": "Музыка в игре", "music_random": "Случайно",
        "track_1": "Трек 1", "track_2": "Трек 2", "listen": "Слушать",
        "reset_save": "Сбросить сохранение", "reset_confirm": "Ты уверен? Весь прогресс будет удалён!",
        "apply": "Применить", "hp": "HP", "mana": "Мана", "potions": "Зелья", "gold": "Золото",
        "level": "Уровень", "exp": "Опыт", "location": "Локация", "enemy": "Враг", "phase": "Фаза",
        "attack": "Атака", "heal": "Лечиться", "fireball": "Огн. шар", "heal_spell": "Исцеление",
        "inventory": "Инвентарь", "forward": "Вперёд", "back_btn": "Назад", "rest": "Отдых",
        "talk": "Говорить", "shop": "Магазин", "craft": "Крафт", "map": "Карта",
        "empty_inventory": "Пусто.", "use": "Использовать",
        "game_over": "Игра окончена", "victory": "ТЫ ПОБЕДИЛ ПОВЕЛИТЕЛЯ БЕЗДНЫ! Спасён мир!",
        "epilogue": "Эпилог: Ты стал легендой. Мир свободен.",
        "death": "Ты погиб... Игра окончена.", "no_potions": "Нет зелий!", "no_mana": "Недостаточно маны!",
        "enemy_dead": "Враг мёртв! Иди дальше.", "kill_first": "Сначала убей врага!",
        "level_up": "*** УРОВЕНЬ ПОВЫШЕН! Теперь {} уровень! HP +20, мана +10. ***",
        "exp_gain": "Получено {} опыта.", "loot_drop": "🎁 С врага упало: {}!",
        "no_loot": "Ничего не выпало.", "found_gold": "Найдено {} золота.",
        "you_dealt": "⚔️ Ты нанёс {} урона!",
        "you_dealt_crit": "⚡ КРИТ! Ты нанёс {} урона!",
        "enemy_attacks": "💢 {} атакует! -{} HP.",
        "you_healed": "💚 Вылечил {} HP. Осталось зелий: {}",
        "heal_outside": "💚 Ты отдохнул и вылечил {} HP. Осталось зелий: {}",
        "fireball_cast": "🔥 Огненный шар! Урон {}.",
        "heal_cast": "✨ Магическое исцеление +{} HP.", "move_forward": "Ты перешёл в {}. Встречай {}!",
        "move_back": "Ты вернулся в {}.", "arrived": "Ты пришёл в {}.",
        "load_save": "Игра загружена. Продолжаем в {}.", "welcome": "Добро пожаловать в The World Manile!",
        "forest": "Мрачный лес", "cave": "Пещера теней", "castle": "Заброшенный замок",
        "dungeon": "Подземелье", "volcano": "Вулкан", "village": "Деревня",
        "city": "Город", "citadel": "Цитадель", "ruins": "Древние руины",
        "goblin": "Гоблин", "wolf": "Волк", "troll": "Тролль", "bear": "Пещерный медведь",
        "ghost_knight": "Призрачный рыцарь", "vampire": "Вампир", "skeleton": "Скелет-воин",
        "necromancer": "Некромант", "fire_elemental": "Огненный элементаль",
        "lord_of_abyss": "Повелитель Бездны", "gargoyle": "Горгулья", "dark_mage": "Тёмный маг",
        "stone_guardian": "Каменный страж",
        "merchant": "Торговец", "elder": "Старейшина", "guard": "Стражник", "quest_giver": "Квестодатель",
        "rest_heal": "Ты отдохнул и восстановил {} HP и {} маны.",
        "quest_talk": "{}: {}", "shop_buy": "Ты купил {} за {} золота.",
        "not_enough_gold": "У тебя нет {} золота.", "shop_menu": "Добро пожаловать в магазин!",
        "shop_only_city": "Магазин только в городе!",
        "shop_buy_btn": "Купить", "shop_price": "Цена", "shop_your_gold": "Твоё золото",
        "shop_discount": "Скидка", "shop_cant_afford": "Недостаточно золота!",
        "stats_title": "Статистика", "stats_short": "Стата", "stats_playtime": "Время игры: {}",
        "stats_kills": "Убито врагов: {}", "stats_potions_used": "Использовано зелий: {}",
        "stats_best_damage": "Лучший урон: {}", "stats_quests_done": "Квестов выполнено: {}",
        "stats_achievements": "Достижений: {}/{}", "stats_crits": "Критических ударов: {}",
        "stats_reputation": "Репутация:",
        "rep_village": "Деревня", "rep_city": "Город", "rep_citadel": "Цитадель",
        "rep_gain": "📜 +{} репутации с {}",
        "rep_neutral": "Нейтральный", "rep_friendly": "Дружелюбный",
        "rep_honored": "Уважаемый", "rep_exalted": "Прославленный",
        "help_text": "THE WORLD MANILE — пошаговая RPG.\n\nЦЕЛЬ: Прокачайся, выполняй квесты и победи Повелителя Бездны.\n\nБОЙ: Атака (15% крит x2), магия, лечение, свои Аркимы.\n\nКВЕСТЫ: говори с NPC.\nРЕПУТАЦИЯ: скидки в магазинах.\nКРАФТ: создавай предметы.\nАРКИМЫ: создавай свои заклинания (кулдаун 2 хода).\nКАРТА: кликни на соседнюю локацию для перехода.",
        "big_potion": "Большое зелье", "magic_amulet": "Магический амулет",
        "sword": "Меч +5", "ring": "Кольцо защиты",
        "elixir_mana": "Эликсир маны", "crown": "Корона власти",
        "mega_potion": "Мега-зелье", "legendary_sword": "Легендарный меч",
        "archmage_crown": "Корона архимага",
        "passive_item": "Пассивный предмет.", "no_enemies": "Здесь нет врагов.",
        "no_shop_here": "Здесь нет магазина!", "no_talk": "Здесь некогда болтать!",
        "nobody_here": "Здесь никого нет.", "cannot_rest": "Нельзя отдыхать в бою!",
        "path_closed": "Путь закрыт.", "invalid_choice": "Неверный выбор.",
        "where_to": "Куда идём?", "nowhere_back": "Некуда возвращаться.",
        "reset_done": "Сохранение удалено.", "save_quit": "Сохранить игру перед выходом?",
        "quit_title": "Выход", "save_msg": "Игра сохранена.",
        "peaceful_location": "Мирная локация",
        "craft_title": "Создание предметов", "craft_ingredients": "Нужно:",
        "craft_result": "Результат:", "craft_btn": "Создать",
        "craft_success": "✅ Создано: {}!", "craft_fail": "❌ Не хватает ингредиентов!",
        "map_title": "Карта мира", "map_you_here": "Ты здесь",
        "map_click_hint": "Кликни на соседнюю локацию для перехода",
        "tutorial_title": "Обучение", "tut_next": "Далее", "tut_skip": "Пропустить", "tut_start": "Начать игру",
        "tut_1": "Добро пожаловать в The World Manile!\n\nТы — герой, избранный судьбой. Мир погрузился во тьму, и только ты можешь остановить Повелителя Бездны.\n\nПуть начинается в деревне. Удачи!",
        "tut_2": "Статус игрока (верх экрана):\n\n• HP — здоровье.\n• Мана — для магии.\n• Зелья — восстанавливают HP.\n• Золото — для магазина.\n• Уровень и Опыт — растут за победы.",
        "tut_3": "Бой и криты:\n\n• Атака — базовый удар (15% шанс крита x2).\n• Лечиться — тратит 1 зелье.\n\n⚠️ Кнопка «Лечиться» работает ВЕЗДЕ!",
        "tut_4": "Магия:\n\n• Огн. шар — 20 маны, 30–60 урона.\n• Исцеление — 15 маны, 20–40 HP.",
        "tut_5": "Инвентарь, крафт и карта:\n\n• Инвентарь — используй предметы.\n• Крафт — создавай предметы.\n• Карта — кликни на соседнюю локацию для перехода.",
        "tut_6": "Локации и репутация:\n\n• 9 локаций, 3 фракции.\n• Убивай врагов — получай репутацию!\n• Живые NPC реагируют на твои действия.",
        "tut_7": "✨ АРКИМЫ — твои заклинания:\n\n• Создаются в мирных зонах (кнопка «Аркимы»).\n• База (Удар/Пронзание/Вытягивание) + Стихия (Огонь/Лёд/Молния/Бездна).\n• В бою — кнопка «Своё заклинание».\n• ⚠️ После каста — кулдаун 2 хода!\n\nУдачи, герой!",
        "quest_new": "📜 Новый квест: {}", "quest_progress_fmt": "📜 {}: {}/{}",
        "quest_done": "✅ Квест '{}' выполнен! +{} опыта, +{} золота.",
        "quest_already": "Все квесты у этого NPC выполнены.",
        "quest_finish_first": "Сначала закончи текущий квест.",
        "ach_unlocked": "🏆 Достижение: {}",
        "ach_goblin_slayer": "Убийца гоблинов (10 гоблинов)",
        "ach_blade_master": "Мастер клинка (100 урона за удар)",
        "ach_rich": "Богач (500 золота)",
        "ach_legend": "Легенда (победа над боссом)",
        "ach_quest_master": "Мастер квестов (3 квеста)",
        "ach_craftsman": "Ремесленник (первый крафт)",
        "ach_crit_master": "Мастер критов (10 критов)",
        "ach_explorer": "Исследователь (все 9 локаций)",
        "ach_collector": "Коллекционер (5 разных предметов)",
        "ach_survivor": "Живучий (выжить с 1 HP)",
        "ach_rep_master": "Дипломат (макс. репутация)",
        "boss_phase2": "Повелитель Бездны: «Ты силён, смертный… Но это лишь начало!»",
        "boss_phase3": "Повелитель Бездны: «Я — сама Бездна! ТЫ НЕ ПОБЕДИШЬ!»",
        "boss_intro": "Повелитель Бездны: «Кто осмелился войти в мои владения?»",
        "boss_poison": "💀 Яд Бездны отнимает {} HP!",
        "victory_title": "ПОБЕДА!",
        "victory_text": "Мир спасён. Ты — легенда The World Manile.\n\nИтоговая статистика:\nУровень: {}\nУбито врагов: {}\nКвестов выполнено: {}\nДостижений: {}/{}\nЛучший урон: {}\nВремя игры: {}",
        "new_game_plus": "Новая игра+", "continue": "Вернуться в меню",
        "ng_plus_start": "Новая игра+: ты сохраняешь уровень и достижения!",
        "story_forest": "🌲 Мрачный лес. Ветер шепчет проклятия.",
        "story_cave": "🕳️ Пещера теней. С потолка капает вода.",
        "story_castle": "🏰 Заброшенный замок. Здесь когда-то жили короли.",
        "story_ruins": "🗿 Древние руины. Камни помнят битвы.",
        "story_dungeon": "⚰️ Подземелье. Запах сырости и смерти.",
        "story_volcano": "🌋 Вулкан. Здесь всё дышит огнём.",
        "npc_dialog_title": "Разговор",
        "npc_choice_talk": "Поговорить",
        "npc_choice_quest": "Взять квест",
        "npc_choice_shop": "Торговать",
        "npc_choice_leave": "Уйти",
        "npc_quest_already": "У этого NPC больше нет квестов.",
        "npc_quest_active": "У тебя уже есть активный квест.",
        "npc_memory_first": "Ты впервые здесь? Я тебя запомню.",
        "npc_memory_back": "А, снова ты! Рад видеть.",
        "npc_memory_frequent": "Опять ты? Мы уже почти друзья!",
        "npc_react_goblin": "Слышал, ты чистишь лес от гоблинов. Респект!",
        "npc_react_rich": "Говорят, у тебя золота куры не клюют. Одолжишь?",
        "npc_react_hero": "Ты — герой, о котором говорят легенды!",
        "npc_react_boss": "Ты победил Повелителя Бездны? Не верю своим ушам!",
        "npc_rep_low": "Сначала докажи, что достоин.",
        "npc_rep_high": "Для тебя — особые условия.",
        "npc_intro_elder": "Старейшина: Здравствуй, путник. Наша деревня страдает от монстров.",
        "npc_intro_merchant": "Торговец: Заходи, у меня лучший товар в округе!",
        "npc_intro_guard": "Стражник: Стою на посту. А ты кто такой?",
        "npc_intro_quest_giver": "Квестодатель: У меня много дел — есть работа для тебя.",
        "npc_smalltalk_elder": "Старейшина: Раньше тут было спокойно. Потом пришла тьма.",
        "npc_smalltalk_merchant": "Торговец: Цены растут, монстры крепчают. Тяжёлые времена.",
        "npc_smalltalk_guard": "Стражник: В замке поселились призраки. Не суйся туда без подготовки.",
        "npc_smalltalk_quest_giver": "Квестодатель: Информация — тоже товар. Но для тебя бесплатно.",
        "arkims": "Аркимы",
        "arkim_workshop": "Мастерская Аркимов",
        "arkim_create": "Создать арким",
        "arkim_use": "Своё заклинание",
        "arkim_name_prompt": "Назови своё заклинание:",
        "arkim_no_spells": "У тебя пока нет своих заклинаний.",
        "arkim_created": "✨ Создано заклинание: {}",
        "arkim_deleted": "Заклинание удалено.",
        "arkim_only_peaceful": "Аркимы создаются только в мирных зонах!",
        "arkim_no_spells_in_combat": "Нет созданных заклинаний!",
        "arkim_cast": "✨ {} — {} урона!",
        "arkim_cast_crit": "⚡ КРИТ! {} — {} урона!",
        "arkim_effect_burn": "🔥 Враг горит! +{} урона",
        "arkim_effect_freeze": "❄️ Враг заморожен! Пропустит ход.",
        "arkim_effect_stun": "⚡ Враг оглушён! Пропустит ход.",
        "arkim_effect_steal": "💜 Украдено {} HP!",
        "arkim_mana_cost": "Мана: {}",
        "arkim_damage": "Урон: {}",
        "arkim_delete_btn": "Удалить",
        "arkim_select_base": "База",
        "arkim_select_element": "Стихия",
        "arkim_strike": "Удар",
        "arkim_pierce": "Пронзание",
        "arkim_drain": "Вытягивание",
        "arkim_fire": "Огонь",
        "arkim_ice": "Лёд",
        "arkim_lightning": "Молния",
        "arkim_void": "Бездна",
        "arkim_cooldown_msg": "⏳ Кулдаун! Подожди ход.",
        "arkim_cooldown_status": "🔮 Кулдаун аркима: {}",
    },
    "en": {
        "title": "The World Manile", "new_game": "New Game", "load_game": "Load Game",
        "settings": "Settings", "help": "Help", "quit": "Quit", "back": "Back", "save": "Save",
        "language": "Language", "fullscreen": "Fullscreen", "music": "Music", "sounds": "Sounds",
        "on": "On", "off": "Off",
        "music_volume": "Music volume", "sounds_volume": "Sounds volume",
        "music_choice": "Game music", "music_random": "Random",
        "track_1": "Track 1", "track_2": "Track 2", "listen": "Listen",
        "reset_save": "Reset save", "reset_confirm": "Are you sure? All progress will be deleted!",
        "apply": "Apply", "hp": "HP", "mana": "Mana", "potions": "Potions", "gold": "Gold",
        "level": "Level", "exp": "EXP", "location": "Location", "enemy": "Enemy", "phase": "Phase",
        "attack": "Attack", "heal": "Heal", "fireball": "Fireball", "heal_spell": "Heal Spell",
        "inventory": "Inventory", "forward": "Forward", "back_btn": "Back", "rest": "Rest",
        "talk": "Talk", "shop": "Shop", "craft": "Craft", "map": "Map",
        "empty_inventory": "Empty.", "use": "Use",
        "game_over": "Game Over", "victory": "YOU DEFEATED THE LORD OF THE ABYSS!",
        "epilogue": "Epilogue: You became a legend.", "death": "You died... Game Over.",
        "no_potions": "No potions!", "no_mana": "Not enough mana!",
        "enemy_dead": "Enemy is dead! Move on.", "kill_first": "Kill the enemy first!",
        "level_up": "*** LEVEL UP! Level {}! HP +20, mana +10. ***", "exp_gain": "Gained {} EXP.",
        "loot_drop": "🎁 Loot: {}!", "no_loot": "Nothing dropped.", "found_gold": "Found {} gold.",
        "you_dealt": "⚔️ Dealt {} damage!",
        "you_dealt_crit": "⚡ CRIT! Dealt {} damage!",
        "enemy_attacks": "💢 {} attacks! -{} HP.",
        "you_healed": "💚 Healed {} HP. Potions: {}",
        "heal_outside": "💚 You rested and healed {} HP. Potions: {}",
        "fireball_cast": "🔥 Fireball! {} damage.",
        "heal_cast": "✨ Heal +{} HP.", "move_forward": "You moved to {}. Meet {}!",
        "move_back": "You went back to {}.", "arrived": "You arrived at {}.",
        "load_save": "Save loaded. Continue in {}.", "welcome": "Welcome to The World Manile!",
        "forest": "Dark Forest", "cave": "Cave of Shadows", "castle": "Abandoned Castle",
        "dungeon": "Dungeon", "volcano": "Volcano", "village": "Village",
        "city": "City", "citadel": "Citadel", "ruins": "Ancient Ruins",
        "goblin": "Goblin", "wolf": "Wolf", "troll": "Troll", "bear": "Cave Bear",
        "ghost_knight": "Ghost Knight", "vampire": "Vampire", "skeleton": "Skeleton Warrior",
        "necromancer": "Necromancer", "fire_elemental": "Fire Elemental",
        "lord_of_abyss": "Lord of the Abyss", "gargoyle": "Gargoyle", "dark_mage": "Dark Mage",
        "stone_guardian": "Stone Guardian",
        "merchant": "Merchant", "elder": "Elder", "guard": "Guard", "quest_giver": "Quest Giver",
        "rest_heal": "You rested: +{} HP, +{} mana.", "quest_talk": "{}: {}",
        "shop_buy": "Bought {} for {} gold.", "not_enough_gold": "You don't have {} gold.",
        "shop_menu": "Welcome to the shop!", "shop_only_city": "Shop only in the city!",
        "shop_buy_btn": "Buy", "shop_price": "Price", "shop_your_gold": "Your gold",
        "shop_discount": "Discount", "shop_cant_afford": "Not enough gold!",
        "stats_title": "Statistics", "stats_short": "Stats", "stats_playtime": "Playtime: {}",
        "stats_kills": "Enemies killed: {}", "stats_potions_used": "Potions used: {}",
        "stats_best_damage": "Best damage: {}", "stats_quests_done": "Quests completed: {}",
        "stats_achievements": "Achievements: {}/{}", "stats_crits": "Critical hits: {}",
        "stats_reputation": "Reputation:",
        "rep_village": "Village", "rep_city": "City", "rep_citadel": "Citadel",
        "rep_gain": "📜 +{} reputation with {}",
        "rep_neutral": "Neutral", "rep_friendly": "Friendly",
        "rep_honored": "Honored", "rep_exalted": "Exalted",
        "help_text": "THE WORLD MANILE — turn-based RPG.\n\nGOAL: Level up, complete quests, defeat the Lord of the Abyss.\n\nCOMBAT: Attack (15% crit x2), magic, heal, custom Arkims.\n\nQUESTS: talk to NPCs.\nREPUTATION: shop discounts.\nCRAFT: create items.\nARKIMS: create custom spells (2-turn cooldown).\nMAP: click adjacent location to travel.",
        "big_potion": "Big Potion", "magic_amulet": "Magic Amulet",
        "sword": "Sword +5", "ring": "Ring of Protection",
        "elixir_mana": "Mana Elixir", "crown": "Crown of Power",
        "mega_potion": "Mega Potion", "legendary_sword": "Legendary Sword",
        "archmage_crown": "Archmage Crown",
        "passive_item": "Passive item.", "no_enemies": "No enemies here.",
        "no_shop_here": "No shop here!", "no_talk": "No time to talk!",
        "nobody_here": "Nobody here.", "cannot_rest": "Can't rest in combat!",
        "path_closed": "Path closed.", "invalid_choice": "Invalid choice.",
        "where_to": "Where to?", "nowhere_back": "Nowhere to go back.",
        "reset_done": "Save deleted.", "save_quit": "Save game before quitting?",
        "quit_title": "Quit", "save_msg": "Game saved.",
        "peaceful_location": "Peaceful location",
        "craft_title": "Crafting", "craft_ingredients": "Needed:",
        "craft_result": "Result:", "craft_btn": "Craft",
        "craft_success": "✅ Created: {}!", "craft_fail": "❌ Not enough ingredients!",
        "map_title": "World Map", "map_you_here": "You are here",
        "map_click_hint": "Click an adjacent location to travel",
        "tutorial_title": "Tutorial", "tut_next": "Next", "tut_skip": "Skip", "tut_start": "Start Game",
        "tut_1": "Welcome to The World Manile!\n\nYou are the chosen hero. The world has fallen into darkness. Only you can stop the Lord of the Abyss.\n\nYour journey begins in the village. Good luck!",
        "tut_2": "Player status (top):\n\n• HP — health.\n• Mana — for magic.\n• Potions — restore HP.\n• Gold — for shops.\n• Level & EXP — grow from victories.",
        "tut_3": "Combat & crits:\n\n• Attack — basic hit (15% crit x2).\n• Heal — uses 1 potion.\n\n⚠️ Heal works ANYWHERE!",
        "tut_4": "Magic:\n\n• Fireball — 20 mana, 30–60 dmg.\n• Heal Spell — 15 mana, 20–40 HP.",
        "tut_5": "Inventory, craft, map:\n\n• Inventory — use items.\n• Craft — create items.\n• Map — click adjacent location to travel.",
        "tut_6": "Locations & Reputation:\n\n• 9 locations, 3 factions.\n• Kill enemies — gain reputation!\n• Living NPCs react to you.",
        "tut_7": "✨ ARKIMS — your custom spells:\n\n• Created in peaceful zones (Arkims button).\n• Base (Strike/Pierce/Drain) + Element (Fire/Ice/Lightning/Void).\n• In combat — Custom Spell button.\n• ⚠️ After cast — 2-turn cooldown!\n\nGood luck, hero!",
        "quest_new": "📜 New quest: {}", "quest_progress_fmt": "📜 {}: {}/{}",
        "quest_done": "✅ Quest '{}' completed! +{} EXP, +{} gold.",
        "quest_already": "All quests from this NPC are done.",
        "quest_finish_first": "Finish current quest first.",
        "ach_unlocked": "🏆 Achievement: {}",
        "ach_goblin_slayer": "Goblin Slayer (10 goblins)",
        "ach_blade_master": "Blade Master (100 damage in one hit)",
        "ach_rich": "Rich (500 gold)",
        "ach_legend": "Legend (defeat the boss)",
        "ach_quest_master": "Quest Master (3 quests)",
        "ach_craftsman": "Craftsman (first craft)",
        "ach_crit_master": "Crit Master (10 crits)",
        "ach_explorer": "Explorer (all 9 locations)",
        "ach_collector": "Collector (5 different items)",
        "ach_survivor": "Survivor (survive with 1 HP)",
        "ach_rep_master": "Diplomat (max reputation)",
        "boss_phase2": "Lord of the Abyss: \"You are strong, mortal… But this is just the beginning!\"",
        "boss_phase3": "Lord of the Abyss: \"I AM the Abyss! YOU CANNOT WIN!\"",
        "boss_intro": "Lord of the Abyss: \"Who dares enter my domain?\"",
        "boss_poison": "💀 Abyss poison drains {} HP!",
        "victory_title": "VICTORY!",
        "victory_text": "The world is saved. You are a legend of The World Manile.\n\nFinal stats:\nLevel: {}\nEnemies killed: {}\nQuests: {}\nAchievements: {}/{}\nBest damage: {}\nPlaytime: {}",
        "new_game_plus": "New Game+", "continue": "Back to Menu",
        "ng_plus_start": "New Game+: you keep your level and achievements!",
        "story_forest": "🌲 Dark Forest. The wind whispers curses.",
        "story_cave": "🕳️ Cave of Shadows. Water drips.",
        "story_castle": "🏰 Abandoned Castle. Kings once lived here.",
        "story_ruins": "🗿 Ancient Ruins. Stones remember battles.",
        "story_dungeon": "⚰️ Dungeon. Smell of damp and death.",
        "story_volcano": "🌋 Volcano. Everything breathes fire.",
        "npc_dialog_title": "Dialogue",
        "npc_choice_talk": "Talk",
        "npc_choice_quest": "Take quest",
        "npc_choice_shop": "Trade",
        "npc_choice_leave": "Leave",
        "npc_quest_already": "This NPC has no more quests.",
        "npc_quest_active": "You already have an active quest.",
        "npc_memory_first": "First time here? I'll remember you.",
        "npc_memory_back": "Ah, you again! Good to see you.",
        "npc_memory_frequent": "You again? We're almost friends!",
        "npc_react_goblin": "Heard you're clearing goblins from the forest. Respect!",
        "npc_react_rich": "They say you're swimming in gold. Lend some?",
        "npc_react_hero": "You're a hero of legend!",
        "npc_react_boss": "You defeated the Lord of the Abyss? Unbelievable!",
        "npc_rep_low": "First prove yourself.",
        "npc_rep_high": "For you — special terms.",
        "npc_intro_elder": "Elder: Greetings, traveler. Our village suffers from monsters.",
        "npc_intro_merchant": "Merchant: Come in, I have the best goods around!",
        "npc_intro_guard": "Guard: On duty. Who are you?",
        "npc_intro_quest_giver": "Quest Giver: I have much work — there's a job for you.",
        "npc_smalltalk_elder": "Elder: It used to be peaceful here. Then darkness came.",
        "npc_smalltalk_merchant": "Merchant: Prices rise, monsters grow stronger. Hard times.",
        "npc_smalltalk_guard": "Guard: Ghosts have settled in the castle. Don't go without preparation.",
        "npc_smalltalk_quest_giver": "Quest Giver: Information is also a commodity. But free for you.",
        "arkims": "Arkims",
        "arkim_workshop": "Arkim Workshop",
        "arkim_create": "Create Arkim",
        "arkim_use": "Custom Spell",
        "arkim_name_prompt": "Name your spell:",
        "arkim_no_spells": "You have no custom spells yet.",
        "arkim_created": "✨ Spell created: {}",
        "arkim_deleted": "Spell deleted.",
        "arkim_only_peaceful": "Arkims can only be created in peaceful zones!",
        "arkim_no_spells_in_combat": "No custom spells created!",
        "arkim_cast": "✨ {} — {} damage!",
        "arkim_cast_crit": "⚡ CRIT! {} — {} damage!",
        "arkim_effect_burn": "🔥 Enemy burns! +{} damage",
        "arkim_effect_freeze": "❄️ Enemy frozen! Skips a turn.",
        "arkim_effect_stun": "⚡ Enemy stunned! Skips a turn.",
        "arkim_effect_steal": "💜 Stole {} HP!",
        "arkim_mana_cost": "Mana: {}",
        "arkim_damage": "Damage: {}",
        "arkim_delete_btn": "Delete",
        "arkim_select_base": "Base",
        "arkim_select_element": "Element",
        "arkim_strike": "Strike",
        "arkim_pierce": "Pierce",
        "arkim_drain": "Drain",
        "arkim_fire": "Fire",
        "arkim_ice": "Ice",
        "arkim_lightning": "Lightning",
        "arkim_void": "Void",
        "arkim_cooldown_msg": "⏳ Cooldown! Wait a turn.",
        "arkim_cooldown_status": "🔮 Arkim cooldown: {}",
    }
}

def t(key):
    if key in TEXTS[LANG]:
        return TEXTS[LANG][key]
    return key


ARKIMS = {
    "strike": {"type": "base", "name_key": "arkim_strike", "damage": 20, "mana": 20},
    "pierce": {"type": "base", "name_key": "arkim_pierce", "damage": 30, "mana": 35},
    "drain":  {"type": "base", "name_key": "arkim_drain",  "damage": 15, "mana": 28, "heal": 12},
    "fire":      {"type": "element", "name_key": "arkim_fire",      "bonus_dmg": 8, "mana": 8,  "effect": "burn",   "chance": 0.30},
    "ice":       {"type": "element", "name_key": "arkim_ice",       "bonus_dmg": 4, "mana": 7,  "effect": "freeze", "chance": 0.25},
    "lightning": {"type": "element", "name_key": "arkim_lightning", "bonus_dmg": 6, "mana": 10, "effect": "stun",   "chance": 0.20},
    "void":      {"type": "element", "name_key": "arkim_void",      "bonus_dmg": 5, "mana": 9,  "effect": "steal",  "chance": 0.30},
}

BASE_ARKIMS = ["strike", "pierce", "drain"]
ELEMENT_ARKIMS = ["fire", "ice", "lightning", "void"]


ITEMS = {
    "sword":           {"type": "passive", "bonus_attack": 5},
    "ring":            {"type": "passive", "bonus_defence": 3},
    "crown":           {"type": "passive", "bonus_max_hp": 10},
    "big_potion":      {"type": "consumable", "heal": 30},
    "magic_amulet":    {"type": "consumable", "mana": 20},
    "elixir_mana":     {"type": "consumable", "mana": 30},
    "mega_potion":     {"type": "consumable", "heal": 80},
    "legendary_sword": {"type": "passive", "bonus_attack": 15, "bonus_defence": 5},
    "archmage_crown":  {"type": "passive", "bonus_max_hp": 20, "bonus_max_mana": 30},
}

RECIPES = [
    {"result": {"id": "mega_potion", "count": 1},
     "ingredients": [{"id": "big_potion", "count": 3}]},
    {"result": {"id": "legendary_sword", "count": 1},
     "ingredients": [{"id": "sword", "count": 1}, {"id": "ring", "count": 1}]},
    {"result": {"id": "archmage_crown", "count": 1},
     "ingredients": [{"id": "crown", "count": 1}, {"id": "elixir_mana", "count": 2}]},
]

REP_FACTIONS = {
    "village": {"location": 6, "name_key": "rep_village"},
    "city":    {"location": 7, "name_key": "rep_city"},
    "citadel": {"location": 8, "name_key": "rep_citadel"},
}

LOCATION_FACTION = {
    1: "village", 2: "village",
    3: "city", 9: "city",
    4: "citadel", 5: "citadel",
}

QUESTS = {
    "goblin_hunt": {"npc": "elder", "location": 6, "enemy": "goblin", "target": 3,
                    "exp": 30, "gold": 20, "faction": "village",
                    "name": {"ru": "Проблема в лесу", "en": "Forest Problem"},
                    "desc": {"ru": "Убей 3 гоблина", "en": "Kill 3 goblins"}},
    "wolf_hunt": {"npc": "quest_giver", "location": 7, "enemy": "wolf", "target": 3,
                  "exp": 40, "gold": 30, "faction": "city",
                  "name": {"ru": "Волчья угроза", "en": "Wolf Threat"},
                  "desc": {"ru": "Убей 3 волка", "en": "Kill 3 wolves"}},
    "skeleton_clear": {"npc": "elder", "location": 8, "enemy": "skeleton", "target": 2,
                       "exp": 60, "gold": 50, "faction": "citadel",
                       "name": {"ru": "Зачистка подземелья", "en": "Dungeon Clear"},
                       "desc": {"ru": "Убей 2 скелета", "en": "Kill 2 skeletons"}},
    "bear_hunt": {"npc": "elder", "location": 6, "enemy": "bear", "target": 3,
                  "exp": 50, "gold": 40, "faction": "village",
                  "name": {"ru": "Медвежья охота", "en": "Bear Hunt"},
                  "desc": {"ru": "Убей 3 медведей", "en": "Kill 3 bears"}},
    "troll_hunt": {"npc": "merchant", "location": 6, "enemy": "troll", "target": 3,
                   "exp": 55, "gold": 45, "faction": "village",
                   "name": {"ru": "Троллья напасть", "en": "Troll Menace"},
                   "desc": {"ru": "Убей 3 троллей", "en": "Kill 3 trolls"}},
    "vampire_hunt": {"npc": "guard", "location": 7, "enemy": "vampire", "target": 2,
                     "exp": 70, "gold": 60, "faction": "city",
                     "name": {"ru": "Вампирская угроза", "en": "Vampire Threat"},
                     "desc": {"ru": "Убей 2 вампиров", "en": "Kill 2 vampires"}},
    "gargoyle_hunt": {"npc": "quest_giver", "location": 7, "enemy": "gargoyle", "target": 3,
                      "exp": 80, "gold": 70, "faction": "city",
                      "name": {"ru": "Каменные стражи", "en": "Stone Sentinels"},
                      "desc": {"ru": "Убей 3 горгульи", "en": "Kill 3 gargoyles"}},
    "fire_hunt": {"npc": "elder", "location": 8, "enemy": "fire_elemental", "target": 2,
                  "exp": 100, "gold": 80, "faction": "citadel",
                  "name": {"ru": "Огненная буря", "en": "Fire Storm"},
                  "desc": {"ru": "Убей 2 огненных элементаля", "en": "Kill 2 fire elementals"}},
}

ACHIEVEMENTS = {
    "goblin_slayer": {"name_key": "ach_goblin_slayer"},
    "blade_master":  {"name_key": "ach_blade_master"},
    "rich":          {"name_key": "ach_rich"},
    "legend":        {"name_key": "ach_legend"},
    "quest_master":  {"name_key": "ach_quest_master"},
    "craftsman":     {"name_key": "ach_craftsman"},
    "crit_master":   {"name_key": "ach_crit_master"},
    "explorer":      {"name_key": "ach_explorer"},
    "collector":     {"name_key": "ach_collector"},
    "survivor":      {"name_key": "ach_survivor"},
    "rep_master":    {"name_key": "ach_rep_master"},
}


player_hp = 100; player_max_hp = 100
potions = 3
mana = 50; mana_max = 50
gold = 50
level = 1; exp = 0; exp_to_next = 50
location = 6
enemy_name = "goblin"; enemy_hp = 60
game_over = False
inventory = []
attack_bonus = 0; defence_bonus = 0
stats_kills = 0; stats_potions_used = 0; stats_best_damage = 0
stats_crafts = 0; stats_crits = 0
active_quest = None
quest_progress = {}
completed_quests = []
location_history = []
achievements_unlocked = []
enemy_kill_counts = {}
boss_phase = 1
boss_poison_turns = 0
boss_defeated = False
story_shown = []
visited_locations = set()

reputation = {"village": 0, "city": 0, "citadel": 0}
npc_memory = {}
custom_spells = []
enemy_frozen_turns = 0
arkim_cooldown = 0

def get_npc_talks(npc_name):
    return npc_memory.get(npc_name, {}).get("talks", 0)

def inc_npc_talks(npc_name):
    if npc_name not in npc_memory:
        npc_memory[npc_name] = {"talks": 0}
    npc_memory[npc_name]["talks"] += 1

def get_rep(faction):
    return reputation.get(faction, 0)

def add_rep(faction, amount):
    if faction in reputation:
        reputation[faction] += amount

def get_rep_level(faction):
    r = get_rep(faction)
    if r >= 20: return 3
    if r >= 10: return 2
    if r >= 5: return 1
    return 0

def get_rep_label(faction):
    lvl = get_rep_level(faction)
    return [t("rep_neutral"), t("rep_friendly"), t("rep_honored"), t("rep_exalted")][lvl]

def get_discount(faction):
    lvl = get_rep_level(faction)
    return [0.0, 0.10, 0.20, 0.30][lvl]

locations_data = {
    1: {"name": "forest", "type": "combat", "enemies": ["goblin", "wolf"], "connected": [2, 6], "story": "story_forest"},
    2: {"name": "cave", "type": "combat", "enemies": ["troll", "bear"], "connected": [1, 3], "story": "story_cave"},
    3: {"name": "castle", "type": "combat", "enemies": ["ghost_knight", "vampire", "gargoyle"], "connected": [2, 9, 7], "story": "story_castle"},
    9: {"name": "ruins", "type": "combat", "enemies": ["stone_guardian", "gargoyle"], "connected": [3, 4], "story": "story_ruins"},
    4: {"name": "dungeon", "type": "combat", "enemies": ["skeleton", "necromancer", "dark_mage"], "connected": [9, 5], "story": "story_dungeon"},
    5: {"name": "volcano", "type": "combat", "enemies": ["fire_elemental", "lord_of_abyss"], "connected": [4, 8], "story": "story_volcano"},
    6: {"name": "village", "type": "peaceful", "connected": [1, 7]},
    7: {"name": "city", "type": "peaceful", "connected": [3, 6, 8]},
    8: {"name": "citadel", "type": "peaceful", "connected": [5, 7]},
}

enemy_hp_map = {
    "goblin": 60, "wolf": 50, "troll": 80, "bear": 90,
    "ghost_knight": 110, "vampire": 100, "skeleton": 80,
    "necromancer": 120, "fire_elemental": 150, "lord_of_abyss": 400,
    "gargoyle": 130, "dark_mage": 140, "stone_guardian": 200,
}

npcs = {
    6: [
        {"name": "elder", "faction": "village", "intro_key": "npc_intro_elder", "smalltalk_key": "npc_smalltalk_elder"},
        {"name": "merchant", "faction": "village", "intro_key": "npc_intro_merchant", "smalltalk_key": "npc_smalltalk_merchant"},
    ],
    7: [
        {"name": "guard", "faction": "city", "intro_key": "npc_intro_guard", "smalltalk_key": "npc_smalltalk_guard"},
        {"name": "quest_giver", "faction": "city", "intro_key": "npc_intro_quest_giver", "smalltalk_key": "npc_smalltalk_quest_giver"},
    ],
    8: [
        {"name": "elder", "faction": "citadel", "intro_key": "npc_intro_elder", "smalltalk_key": "npc_smalltalk_elder"},
    ],
}

def is_peaceful(loc_id):
    return locations_data[loc_id]["type"] == "peaceful"

def get_loc_name(loc_id):
    return t(locations_data[loc_id]["name"])

def reset_enemy():
    global enemy_name, enemy_hp, boss_phase, boss_poison_turns, enemy_frozen_turns, arkim_cooldown
    enemy_frozen_turns = 0
    arkim_cooldown = 0
    if is_peaceful(location):
        enemy_name = ""; enemy_hp = 0; return
    enemies = locations_data[location]["enemies"]
    if location == 5:
        enemy_name = "fire_elemental" if boss_defeated else "lord_of_abyss"
    else:
        enemy_name = random.choice(enemies)
    enemy_hp = enemy_hp_map.get(enemy_name, 60)
    if enemy_name == "lord_of_abyss":
        boss_phase = 1
        boss_poison_turns = 0

def add_log(msg):
    log_text.config(state='normal')
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')

def add_item(item_id, count=1):
    global inventory
    for entry in inventory:
        if entry["id"] == item_id:
            entry["count"] += count
            update_passive_bonuses(); return
    inventory.append({"id": item_id, "count": count})
    update_passive_bonuses()

def remove_item(item_id, count=1):
    global inventory, player_max_hp, player_hp, mana_max, mana
    for entry in inventory:
        if entry["id"] == item_id:
            entry["count"] -= count
            if entry["count"] <= 0:
                inventory.remove(entry)
            update_passive_bonuses()
            if player_hp > player_max_hp: player_hp = player_max_hp
            if mana > mana_max: mana = mana_max
            return

def has_items(ingredients):
    for ing in ingredients:
        total = sum(e["count"] for e in inventory if e["id"] == ing["id"])
        if total < ing["count"]:
            return False
    return True

def migrate_inventory(old_inv):
    id_map = {"Большое зелье": "big_potion", "Big Potion": "big_potion",
              "Магический амулет": "magic_amulet", "Magic Amulet": "magic_amulet",
              "Меч +5": "sword", "Sword +5": "sword",
              "Кольцо защиты": "ring", "Ring of Protection": "ring",
              "Эликсир маны": "elixir_mana", "Mana Elixir": "elixir_mana",
              "Корона власти": "crown", "Crown of Power": "crown",
              "Мега-зелье": "mega_potion", "Mega Potion": "mega_potion",
              "Легендарный меч": "legendary_sword", "Legendary Sword": "legendary_sword",
              "Корона архимага": "archmage_crown", "Archmage Crown": "archmage_crown"}
    if old_inv and isinstance(old_inv[0], dict):
        return old_inv
    counts = {}
    for item in old_inv:
        iid = id_map.get(item)
        if iid:
            counts[iid] = counts.get(iid, 0) + 1
    return [{"id": k, "count": v} for k, v in counts.items()]

def update_passive_bonuses():
    global attack_bonus, defence_bonus, player_max_hp, mana_max
    attack_bonus = 0; defence_bonus = 0
    base_max_hp = 100 + (level - 1) * 20
    base_max_mana = 50 + (level - 1) * 5
    for entry in inventory:
        item = ITEMS.get(entry["id"])
        if item:
            attack_bonus += item.get("bonus_attack", 0)
            defence_bonus += item.get("bonus_defence", 0)
            base_max_hp += item.get("bonus_max_hp", 0)
            base_max_mana += item.get("bonus_max_mana", 0)
    player_max_hp = base_max_hp
    mana_max = base_max_mana

def drop_loot():
    global gold
    if random.random() < 0.5:
        loot_pool = ["sword", "ring", "big_potion", "magic_amulet", "elixir_mana"] * 3 + ["crown"]
        loot_id = random.choice(loot_pool)
        add_item(loot_id)
        add_log(t("loot_drop").format(t(loot_id)))
    else:
        g = random.randint(5, 20)
        gold += g
        add_log(t("found_gold").format(g))

def unlock_achievement(ach_id):
    global achievements_unlocked
    if ach_id in achievements_unlocked:
        return
    achievements_unlocked.append(ach_id)
    ach = ACHIEVEMENTS[ach_id]
    add_log(t("ach_unlocked").format(t(ach["name_key"])))
    play_sound("levelup")
    save_game()

def check_achievements():
    if enemy_kill_counts.get("goblin", 0) >= 10:
        unlock_achievement("goblin_slayer")
    if stats_best_damage >= 100:
        unlock_achievement("blade_master")
    if gold >= 500:
        unlock_achievement("rich")
    if len(completed_quests) >= 3:
        unlock_achievement("quest_master")
    if "lord_of_abyss" in enemy_kill_counts:
        unlock_achievement("legend")
    if stats_crafts >= 1:
        unlock_achievement("craftsman")
    if stats_crits >= 10:
        unlock_achievement("crit_master")
    if len(visited_locations) >= 9:
        unlock_achievement("explorer")
    unique_items = set(e["id"] for e in inventory)
    if len(unique_items) >= 5:
        unlock_achievement("collector")
    for fac in reputation:
        if reputation[fac] >= 20:
            unlock_achievement("rep_master")
            break

def save_game(show_log=False):
    data = {"player_hp": player_hp, "player_max_hp": player_max_hp,
            "potions": potions, "mana": mana, "mana_max": mana_max,
            "gold": gold, "level": level, "exp": exp, "exp_to_next": exp_to_next,
            "location": location, "enemy_name": enemy_name, "enemy_hp": enemy_hp,
            "game_over": game_over, "inventory": inventory,
            "attack_bonus": attack_bonus, "defence_bonus": defence_bonus,
            "stats_kills": stats_kills, "stats_potions_used": stats_potions_used,
            "stats_best_damage": stats_best_damage, "stats_crafts": stats_crafts,
            "stats_crits": stats_crits,
            "active_quest": active_quest, "quest_progress": quest_progress,
            "completed_quests": completed_quests, "location_history": location_history,
            "achievements_unlocked": achievements_unlocked,
            "enemy_kill_counts": enemy_kill_counts, "story_shown": story_shown,
            "boss_defeated": boss_defeated, "reputation": reputation,
            "visited_locations": list(visited_locations),
            "npc_memory": npc_memory,
            "custom_spells": custom_spells,
            "playtime": int(time.time() - GAME_START_TIME)}
    try:
        tmp = SAVE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, SAVE_FILE)
        if show_log:
            add_log("💾 " + t("save_msg"))
    except Exception:
        pass

def load_game_data():
    global player_hp, player_max_hp, potions, mana, mana_max, gold, level, exp, exp_to_next
    global location, enemy_name, enemy_hp, game_over, inventory, attack_bonus, defence_bonus
    global stats_kills, stats_potions_used, stats_best_damage, stats_crafts, stats_crits
    global active_quest, quest_progress, completed_quests, location_history
    global achievements_unlocked, enemy_kill_counts, story_shown, boss_defeated
    global reputation, visited_locations, npc_memory, custom_spells, GAME_START_TIME
    if not os.path.exists(SAVE_FILE):
        return False
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        player_hp = data.get("player_hp", 100)
        player_max_hp = data.get("player_max_hp", 100)
        potions = data.get("potions", 3)
        mana = data.get("mana", 50); mana_max = data.get("mana_max", 50)
        gold = data.get("gold", 50)
        level = data.get("level", 1); exp = data.get("exp", 0); exp_to_next = data.get("exp_to_next", 50)
        location = data.get("location", 6)
        enemy_name = data.get("enemy_name", "goblin"); enemy_hp = data.get("enemy_hp", 60)
        game_over = data.get("game_over", False)
        inventory = migrate_inventory(data.get("inventory", []))
        attack_bonus = data.get("attack_bonus", 0); defence_bonus = data.get("defence_bonus", 0)
        stats_kills = data.get("stats_kills", 0); stats_potions_used = data.get("stats_potions_used", 0)
        stats_best_damage = data.get("stats_best_damage", 0)
        stats_crafts = data.get("stats_crafts", 0)
        stats_crits = data.get("stats_crits", 0)
        active_quest = data.get("active_quest", None)
        quest_progress = data.get("quest_progress", {})
        completed_quests = data.get("completed_quests", [])
        location_history = data.get("location_history", [])
        achievements_unlocked = data.get("achievements_unlocked", [])
        enemy_kill_counts = data.get("enemy_kill_counts", {})
        story_shown = data.get("story_shown", [])
        boss_defeated = data.get("boss_defeated", False)
        reputation = data.get("reputation", {"village": 0, "city": 0, "citadel": 0})
        for k in ("village", "city", "citadel"):
            if k not in reputation: reputation[k] = 0
        visited_locations = set(data.get("visited_locations", []))
        npc_memory = data.get("npc_memory", {})
        custom_spells = data.get("custom_spells", [])
        saved_playtime = data.get("playtime", 0)
        GAME_START_TIME = time.time() - saved_playtime
        return True
    except Exception:
        return False

def update_status():
    loc_name = get_loc_name(location)
    loc_type = "⚔️" if not is_peaceful(location) else "🏠"
    status = f"{t('level')}: {level}   {t('exp')}: {exp}/{exp_to_next}\n"
    status += f"{t('hp')}: {player_hp}/{player_max_hp}   {t('mana')}: {mana}/{mana_max}   {t('potions')}: {potions}   {t('gold')}: {gold}\n"
    status += f"{loc_type} {t('location')}: {loc_name}\n"
    if not is_peaceful(location):
        if enemy_name == "lord_of_abyss":
            status += f"👑 {t('enemy')}: {t(enemy_name)}  HP: {enemy_hp}  [{t('phase')} {boss_phase}/3]"
        else:
            status += f"{t('enemy')}: {t(enemy_name)}  HP: {enemy_hp}"
    else:
        status += "🏙️ " + t("peaceful_location")
    if attack_bonus: status += f"\n⚔️ +{attack_bonus}"
    if defence_bonus: status += f"  🛡️ +{defence_bonus}"
    if arkim_cooldown > 0 and not is_peaceful(location):
        status += f"\n" + t("arkim_cooldown_status").format(arkim_cooldown)
    if active_quest:
        q = QUESTS[active_quest]
        prog = quest_progress.get(q["enemy"], 0)
        status += "\n" + t("quest_progress_fmt").format(q["name"][LANG], prog, q["target"])
    status_label.config(text=status)
    try:
        state = "disabled" if game_over else "normal"
        btn_attack.config(state=state); btn_heal.config(state=state)
        btn_fireball.config(state=state); btn_heal_spell.config(state=state)
    except Exception:
        pass

def check_quests():
    global active_quest, exp, gold
    if not active_quest:
        return
    q = QUESTS[active_quest]
    if quest_progress.get(q["enemy"], 0) >= q["target"]:
        exp += q["exp"]; gold += q["gold"]
        completed_quests.append(active_quest)
        add_log(t("quest_done").format(q["name"][LANG], q["exp"], q["gold"]))
        faction = q.get("faction")
        if faction:
            add_rep(faction, 5)
            add_log(t("rep_gain").format(5, t(REP_FACTIONS[faction]["name_key"])))
        play_sound("levelup")
        active_quest = None
        quest_progress[q["enemy"]] = 0
        check_achievements()

def show_story_if_new(loc_id):
    if is_peaceful(loc_id):
        return
    story_key = locations_data[loc_id].get("story")
    if story_key and story_key not in story_shown:
        story_shown.append(story_key)
        add_log(t(story_key))

def enemy_turn():
    global player_hp, game_over, boss_poison_turns, enemy_frozen_turns
    if enemy_frozen_turns > 0:
        enemy_frozen_turns -= 1
        add_log(f"❄️ {t(enemy_name)} пропускает ход!" if LANG=="ru" else f"❄️ {t(enemy_name)} skips a turn!")
        return

    if boss_poison_turns > 0:
        poison_dmg = random.randint(5, 15)
        player_hp -= poison_dmg
        boss_poison_turns -= 1
        add_log(t("boss_poison").format(poison_dmg))

    if enemy_name == "lord_of_abyss":
        if boss_phase == 3:
            enemy_dmg = random.randint(40, 70)
        elif boss_phase == 2:
            enemy_dmg = random.randint(25, 45)
            if random.random() < 0.3:
                boss_poison_turns = 3
        else:
            enemy_dmg = random.randint(25, 45)
    else:
        enemy_dmg = get_enemy_damage()

    enemy_dmg = max(1, enemy_dmg - defence_bonus)
    player_hp -= enemy_dmg
    if player_hp < 0: player_hp = 0
    add_log(t("enemy_attacks").format(t(enemy_name), enemy_dmg))
    play_sound("hit")
    if player_hp <= 0:
        add_log(t("death")); game_over = True; play_sound("death"); save_game()
    elif player_hp == 1:
        unlock_achievement("survivor")

def process_enemy_death():
    global stats_kills, exp, exp_to_next, level, gold, enemy_hp
    global boss_defeated, game_over, player_max_hp, player_hp, mana, mana_max
    global quest_progress, enemy_kill_counts, enemy_frozen_turns, arkim_cooldown
    enemy_frozen_turns = 0
    arkim_cooldown = 0

    stats_kills += 1
    enemy_kill_counts[enemy_name] = enemy_kill_counts.get(enemy_name, 0) + 1
    quest_progress[enemy_name] = quest_progress.get(enemy_name, 0) + 1
    faction = LOCATION_FACTION.get(location)
    if faction:
        add_rep(faction, 1)

    if enemy_name == "lord_of_abyss":
        boss_defeated = True
        add_log(t("victory")); add_log(t("epilogue"))
        game_over = True
        play_sound("victory")
        check_achievements()
        save_game(); update_status()
        show_victory_screen()
        return

    exp_gain = 20 + level * 2
    exp += exp_gain
    add_log(t("exp_gain").format(exp_gain))
    drop_loot()
    while exp >= exp_to_next:
        exp -= exp_to_next; level += 1
        update_passive_bonuses()
        player_hp = player_max_hp
        mana = min(mana + 10, mana_max)
        exp_to_next = int(exp_to_next * 1.5)
        add_log(t("level_up").format(level)); play_sound("levelup")
    mana = min(mana + 10, mana_max)
    check_quests(); check_achievements()
    save_game(); update_status()

def player_action(action):
    global player_hp, player_max_hp, potions, mana, level, exp, exp_to_next, enemy_hp, game_over
    global stats_kills, stats_potions_used, stats_best_damage, gold, boss_phase, boss_poison_turns
    global boss_defeated, stats_crits, arkim_cooldown
    if game_over:
        add_log(t("game_over")); return

    if action == "heal":
        if potions > 0:
            heal = random.randint(15, 35) if is_peaceful(location) else random.randint(20, 45)
            player_hp = min(player_hp + heal, player_max_hp)
            potions -= 1; stats_potions_used += 1
            if is_peaceful(location):
                add_log(t("heal_outside").format(heal, potions))
            else:
                add_log(t("you_healed").format(heal, potions))
                arkim_cooldown = max(0, arkim_cooldown - 1)
            play_sound("heal")
            save_game(); update_status()
        else:
            add_log(t("no_potions"))
        return

    if is_peaceful(location):
        add_log(t("no_enemies")); return
    if enemy_hp <= 0:
        add_log(t("enemy_dead")); return

    if action in ("attack", "fireball", "heal_spell"):
        arkim_cooldown = max(0, arkim_cooldown - 1)

    if action == "attack":
        base_dmg = 15 + level * 2 + attack_bonus
        dmg = random.randint(base_dmg, base_dmg + 15)
        is_crit = random.random() < CRIT_CHANCE
        if is_crit:
            dmg = int(dmg * CRIT_MULT)
            stats_crits += 1
            add_log(t("you_dealt_crit").format(dmg)); play_sound("crit")
        else:
            add_log(t("you_dealt").format(dmg)); play_sound("attack")
        enemy_hp -= dmg
        if dmg > stats_best_damage: stats_best_damage = dmg
    elif action == "fireball":
        if mana >= 20:
            mana -= 20
            dmg = random.randint(30, 60) + attack_bonus // 2
            is_crit = random.random() < CRIT_CHANCE
            if is_crit:
                dmg = int(dmg * CRIT_MULT)
                stats_crits += 1
                add_log(t("you_dealt_crit").format(dmg)); play_sound("crit")
            else:
                add_log(t("fireball_cast").format(dmg)); play_sound("fireball")
            enemy_hp -= dmg
            if dmg > stats_best_damage: stats_best_damage = dmg
        else:
            add_log(t("no_mana")); return
    elif action == "heal_spell":
        if mana >= 15:
            mana -= 15
            heal = random.randint(20, 40)
            player_hp = min(player_hp + heal, player_max_hp)
            add_log(t("heal_cast").format(heal)); play_sound("heal_spell")
        else:
            add_log(t("no_mana")); return

    if enemy_name == "lord_of_abyss" and enemy_hp > 0:
        max_hp = enemy_hp_map["lord_of_abyss"]
        ratio = enemy_hp / max_hp
        if boss_phase == 1 and ratio < 0.7:
            boss_phase = 2
            add_log(t("boss_phase2")); play_sound("levelup")
        elif boss_phase == 2 and ratio < 0.3:
            boss_phase = 3
            add_log(t("boss_phase3")); play_sound("levelup")

    if enemy_hp <= 0:
        process_enemy_death(); return

    enemy_turn()
    update_status()

def get_enemy_damage():
    if enemy_name == "stone_guardian": return random.randint(20, 35)
    elif enemy_name == "gargoyle": return random.randint(15, 28)
    elif enemy_name == "dark_mage": return random.randint(18, 30)
    elif enemy_name == "fire_elemental": return random.randint(18, 32)
    elif enemy_name == "necromancer": return random.randint(15, 28)
    elif enemy_name in ("ghost_knight", "vampire"): return random.randint(12, 24)
    elif enemy_name == "troll": return random.randint(10, 22)
    elif enemy_name == "skeleton": return random.randint(10, 18)
    elif enemy_name == "bear": return random.randint(8, 18)
    elif enemy_name == "wolf": return random.randint(6, 14)
    else: return random.randint(4, 12)

def show_location_dialog(connected, callback):
    win = tk.Toplevel(root)
    win.title(t("where_to")); win.configure(bg="#222")
    win.geometry("300x420")
    win.transient(root); win.grab_set()
    tk.Label(win, text=t("where_to"), font=("Arial", 14, "bold"),
             bg="#222", fg="white").pack(pady=15)
    for loc_id in connected:
        loc_name = get_loc_name(loc_id)
        icon = "🏠" if is_peaceful(loc_id) else "⚔️"
        def make_cmd(lid):
            return lambda: (win.destroy(), callback(lid))
        tk.Button(win, text=f"{icon} {loc_name}", font=("Arial", 12), width=20,
                  bg="#3a6ea5", fg="white", command=make_cmd(loc_id)).pack(pady=5)
    tk.Button(win, text=t("back"), font=("Arial", 11), width=20,
              bg="#6b6b6b", fg="white", command=win.destroy).pack(pady=15)

def do_move_to(new_loc):
    global location
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location) and enemy_hp > 0:
        add_log(t("kill_first")); return
    location_history.append(location)
    location = new_loc
    visited_locations.add(new_loc)
    if not is_peaceful(location):
        reset_enemy()
        add_log(t("move_forward").format(get_loc_name(location), t(enemy_name)))
        show_story_if_new(location)
        if enemy_name == "lord_of_abyss":
            add_log(t("boss_intro"))
    else:
        add_log(t("arrived").format(get_loc_name(location)))
    play_sound("move")
    check_achievements()
    save_game(); update_status()

def go_forward():
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location) and enemy_hp > 0:
        add_log(t("kill_first")); return
    connected = locations_data[location]["connected"]
    if not connected: add_log(t("path_closed")); return
    show_location_dialog(connected, do_move_to)

def go_back():
    global location
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location) and enemy_hp > 0:
        add_log(t("kill_first")); return
    if not location_history: add_log(t("nowhere_back")); return
    location = location_history.pop()
    visited_locations.add(location)
    if not is_peaceful(location):
        reset_enemy()
        add_log(t("move_back").format(get_loc_name(location)))
    else:
        add_log(t("arrived").format(get_loc_name(location)))
    play_sound("move"); save_game(); update_status()

def rest():
    global player_hp, mana
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location): add_log(t("cannot_rest")); return
    heal = random.randint(20, 50); mana_restore = random.randint(10, 30)
    player_hp = min(player_hp + heal, player_max_hp)
    mana = min(mana + mana_restore, mana_max)
    add_log(t("rest_heal").format(heal, mana_restore)); play_sound("rest")
    save_game(); update_status()

def npc_get_greeting(npc):
    name = npc["name"]
    faction = npc.get("faction", "village")
    talks = get_npc_talks(name)
    rep_lvl = get_rep_level(faction)
    lines = []
    if talks == 0:
        lines.append(t("npc_memory_first"))
    elif talks < 5:
        lines.append(t("npc_memory_back"))
    else:
        lines.append(t("npc_memory_frequent"))
    if rep_lvl == 0:
        lines.append(t("npc_rep_low"))
    elif rep_lvl >= 2:
        lines.append(t("npc_rep_high"))
    if enemy_kill_counts.get("goblin", 0) >= 10:
        lines.append(t("npc_react_goblin"))
    if gold >= 500:
        lines.append(t("npc_react_rich"))
    if "lord_of_abyss" in enemy_kill_counts:
        lines.append(t("npc_react_boss"))
    elif len(completed_quests) >= 3:
        lines.append(t("npc_react_hero"))
    return lines

def npc_get_available_quests(npc):
    return [qid for qid, q in QUESTS.items()
            if q["npc"] == npc["name"] and q["location"] == location
            and qid not in completed_quests]

def talk():
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location): add_log(t("no_talk")); return
    if location not in npcs: add_log(t("nobody_here")); return
    if len(npcs[location]) == 1:
        open_npc_dialog(npcs[location][0])
    else:
        win = tk.Toplevel(root)
        win.title(t("npc_dialog_title")); win.configure(bg="#222")
        win.geometry("320x320")
        win.transient(root); win.grab_set()
        tk.Label(win, text=t("npc_dialog_title"), font=("Arial", 14, "bold"),
                 bg="#222", fg="white").pack(pady=15)
        for npc in npcs[location]:
            def make_cmd(n):
                return lambda: (win.destroy(), open_npc_dialog(n))
            tk.Button(win, text=t(npc["name"]), font=("Arial", 12), width=20,
                      bg="#3a6ea5", fg="white", command=make_cmd(npc)).pack(pady=5)
        tk.Button(win, text=t("npc_choice_leave"), font=("Arial", 11), width=20,
                  bg="#6b6b6b", fg="white", command=win.destroy).pack(pady=15)

def open_npc_dialog(npc):
    global active_quest
    name = npc["name"]
    faction = npc.get("faction", "village")
    inc_npc_talks(name)

    win = tk.Toplevel(root)
    win.title(t("npc_dialog_title") + " — " + t(name))
    win.configure(bg="#222"); win.geometry("520x520")
    win.transient(root); win.grab_set()

    header = tk.Frame(win, bg="#222")
    header.pack(fill=tk.X, padx=15, pady=10)
    tk.Label(header, text="🧙 " + t(name), font=("Arial", 16, "bold"),
             bg="#222", fg="gold").pack(anchor="w")
    rep_text = f"{t(REP_FACTIONS[faction]['name_key'])}: {get_rep(faction)} ({get_rep_label(faction)})"
    tk.Label(header, text=rep_text, font=("Arial", 10),
             bg="#222", fg="#7CFC00").pack(anchor="w")
    tk.Frame(win, height=2, bg="#444").pack(fill=tk.X, padx=15)

    log_box = scrolledtext.ScrolledText(win, height=14, state='normal',
                                        font=("Arial", 11), bg="#111", fg="#dddddd",
                                        wrap=tk.WORD)
    log_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def write_line(text, color="#dddddd"):
        log_box.insert(tk.END, text + "\n\n")
        log_box.see(tk.END)

    write_line(t(npc.get("intro_key", "npc_intro_elder")), "#ffcc66")
    for line in npc_get_greeting(npc):
        write_line(line, "#aaaaaa")

    btn_frame = tk.Frame(win, bg="#222")
    btn_frame.pack(pady=10)

    def action_talk():
        write_line("— " + t("npc_choice_talk"), "#7CFC00")
        write_line(t(npc.get("smalltalk_key", "npc_smalltalk_elder")), "#dddddd")

    def action_quest():
        global active_quest
        available = npc_get_available_quests(npc)
        if active_quest:
            write_line("— " + t("npc_quest_active"), "#ff8080")
            q = QUESTS[active_quest]
            prog = quest_progress.get(q["enemy"], 0)
            write_line(f"{q['name'][LANG]}: {prog}/{q['target']}", "#ffcc66")
            return
        if not available:
            write_line("— " + t("npc_quest_already"), "#ff8080")
            return
        qid = available[0]
        active_quest = qid
        q = QUESTS[qid]
        write_line("— " + t("quest_new").format(q["name"][LANG]), "#7CFC00")
        write_line(q["desc"][LANG], "#dddddd")
        play_sound("click")
        save_game(); update_status()

    def action_leave():
        win.destroy()

    tk.Button(btn_frame, text="💬 " + t("npc_choice_talk"), font=("Arial", 11),
              bg="#3a6ea5", fg="white", width=16, command=action_talk).grid(row=0, column=0, padx=5, pady=3)
    tk.Button(btn_frame, text="📜 " + t("npc_choice_quest"), font=("Arial", 11),
              bg="#3a7a3a", fg="white", width=16, command=action_quest).grid(row=0, column=1, padx=5, pady=3)
    tk.Button(btn_frame, text="🚪 " + t("npc_choice_leave"), font=("Arial", 11),
              bg="#6b6b6b", fg="white", width=16, command=action_leave).grid(row=1, column=0, columnspan=2, padx=5, pady=3)

def arkim_workshop():
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location):
        add_log(t("arkim_only_peaceful")); return

    win = tk.Toplevel(root)
    win.title("✨ " + t("arkim_workshop"))
    win.configure(bg="#222"); win.geometry("560x600")
    win.transient(root); win.grab_set()

    tk.Label(win, text="✨ " + t("arkim_workshop"),
             font=("Arial", 18, "bold"), bg="#222", fg="gold").pack(pady=10)

    tk.Label(win, text=t("arkim_use") + ":", font=("Arial", 11, "bold"),
             bg="#222", fg="white").pack(anchor="w", padx=20)
    listbox = tk.Listbox(win, font=("Arial", 11), bg="#111", fg="lightgreen",
                         selectbackground="#3a6ea5", activestyle="none", height=6)
    listbox.pack(fill=tk.X, padx=20, pady=5)

    def refresh_list():
        listbox.delete(0, tk.END)
        if not custom_spells:
            listbox.insert(tk.END, "— " + t("arkim_no_spells"))
            return
        for sp in custom_spells:
            base = ARKIMS[sp["base"]]
            elem = ARKIMS[sp["element"]]
            cost = base["mana"] + elem["mana"]
            dmg = base["damage"] + elem["bonus_dmg"]
            listbox.insert(tk.END, f"✨ {sp['name']}  ({dmg} DMG, {cost} {t('mana')})")

    refresh_list()

    tk.Frame(win, height=2, bg="#444").pack(fill=tk.X, padx=20, pady=8)
    tk.Label(win, text="➕ " + t("arkim_create"), font=("Arial", 13, "bold"),
             bg="#222", fg="gold").pack(anchor="w", padx=20)

    base_row = tk.Frame(win, bg="#222"); base_row.pack(fill=tk.X, padx=20, pady=4)
    tk.Label(base_row, text=t("arkim_select_base") + ":",
             font=("Arial", 11), bg="#222", fg="white", width=10, anchor="w").pack(side=tk.LEFT)
    base_var = tk.StringVar(value=BASE_ARKIMS[0])
    tk.OptionMenu(base_row, base_var, *BASE_ARKIMS).pack(side=tk.LEFT)

    elem_row = tk.Frame(win, bg="#222"); elem_row.pack(fill=tk.X, padx=20, pady=4)
    tk.Label(elem_row, text=t("arkim_select_element") + ":",
             font=("Arial", 11), bg="#222", fg="white", width=10, anchor="w").pack(side=tk.LEFT)
    elem_var = tk.StringVar(value=ELEMENT_ARKIMS[0])
    tk.OptionMenu(elem_row, elem_var, *ELEMENT_ARKIMS).pack(side=tk.LEFT)

    preview = tk.Label(win, text="", font=("Arial", 10), bg="#222", fg="#7CFC00",
                       justify=tk.LEFT, wraplength=500)
    preview.pack(padx=20, pady=8)

    def update_preview(*args):
        b = ARKIMS[base_var.get()]
        e = ARKIMS[elem_var.get()]
        dmg = b["damage"] + e["bonus_dmg"]
        cost = b["mana"] + e["mana"]
        preview.config(text=f"{t('arkim_damage').format(dmg)}   |   {t('arkim_mana_cost').format(cost)}",
                       fg="#7CFC00")
    base_var.trace("w", update_preview)
    elem_var.trace("w", update_preview)
    update_preview()

    def create_arkim():
        name = simpledialog.askstring(t("arkim_create"), t("arkim_name_prompt"), parent=win)
        if not name: return
        custom_spells.append({"name": name.strip(), "base": base_var.get(), "element": elem_var.get()})
        add_log(t("arkim_created").format(name))
        play_sound("levelup"); save_game(); refresh_list()

    tk.Button(win, text="✨ " + t("arkim_create"), font=("Arial", 12), width=20,
              bg="#3a7a3a", fg="white", command=create_arkim).pack(pady=8)

    def delete_arkim():
        sel = listbox.curselection()
        if not sel or not custom_spells: return
        idx = sel[0]
        if idx < len(custom_spells):
            custom_spells.pop(idx)
            add_log(t("arkim_deleted")); save_game(); refresh_list()

    tk.Button(win, text="🗑 " + t("arkim_delete_btn"), font=("Arial", 11),
              bg="#a53a3a", fg="white", command=delete_arkim).pack(pady=4)
    tk.Button(win, text=t("back"), font=("Arial", 12), width=14,
              bg="#6b6b6b", fg="white", command=win.destroy).pack(pady=10)

def open_custom_spell_menu():
    if game_over: add_log(t("game_over")); return
    if is_peaceful(location): add_log(t("no_enemies")); return
    if enemy_hp <= 0: add_log(t("enemy_dead")); return
    if arkim_cooldown > 0:
        add_log(t("arkim_cooldown_msg")); return
    if not custom_spells:
        add_log(t("arkim_no_spells_in_combat")); return

    win = tk.Toplevel(root)
    win.title("✨ " + t("arkim_use"))
    win.configure(bg="#222"); win.geometry("480x420")
    win.transient(root); win.grab_set()

    tk.Label(win, text="✨ " + t("arkim_use"), font=("Arial", 16, "bold"),
             bg="#222", fg="gold").pack(pady=10)

    listbox = tk.Listbox(win, font=("Arial", 11), bg="#111", fg="lightgreen",
                         selectbackground="#3a6ea5", activestyle="none")
    listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    for sp in custom_spells:
        base = ARKIMS[sp["base"]]
        elem = ARKIMS[sp["element"]]
        cost = base["mana"] + elem["mana"]
        dmg = base["damage"] + elem["bonus_dmg"]
        listbox.insert(tk.END, f"✨ {sp['name']}  ({dmg} DMG, {cost} {t('mana')})")

    desc_label = tk.Label(win, text="", font=("Arial", 10), bg="#222", fg="#dddddd",
                          justify=tk.LEFT, wraplength=440)
    desc_label.pack(padx=20, pady=5)

    def on_select(evt=None):
        sel = listbox.curselection()
        if not sel: return
        sp = custom_spells[sel[0]]
        base = ARKIMS[sp["base"]]
        elem = ARKIMS[sp["element"]]
        cost = base["mana"] + elem["mana"]
        can = mana >= cost
        desc_label.config(text=f"{t('arkim_mana_cost').format(cost)}   |   {t('mana')}: {mana}",
                          fg="#7CFC00" if can else "#ff6060")
    listbox.bind("<<ListboxSelect>>", on_select)

    def cast_selected():
        sel = listbox.curselection()
        if not sel: return
        idx = sel[0]
        win.destroy()
        player_cast_custom(idx)

    btn_row = tk.Frame(win, bg="#222"); btn_row.pack(pady=10)
    tk.Button(btn_row, text="✨ " + t("arkim_use"), font=("Arial", 12), width=14,
              bg="#3a7a3a", fg="white", command=cast_selected).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_row, text=t("back"), font=("Arial", 12), width=14,
              bg="#6b6b6b", fg="white", command=win.destroy).pack(side=tk.LEFT, padx=5)

def player_cast_custom(idx):
    global mana, enemy_hp, player_hp, player_max_hp, stats_best_damage, stats_crits
    global enemy_frozen_turns, arkim_cooldown
    if arkim_cooldown > 0:
        add_log(t("arkim_cooldown_msg")); return
    if idx >= len(custom_spells): return
    sp = custom_spells[idx]
    base = ARKIMS[sp["base"]]
    elem = ARKIMS[sp["element"]]
    cost = base["mana"] + elem["mana"]
    if mana < cost:
        add_log(t("no_mana")); return
    mana -= cost
    dmg = base["damage"] + elem["bonus_dmg"] + attack_bonus // 2

    is_crit = random.random() < CRIT_CHANCE
    if is_crit:
        dmg = int(dmg * CRIT_MULT); stats_crits += 1
        add_log(t("arkim_cast_crit").format(sp["name"], dmg)); play_sound("crit")
    else:
        add_log(t("arkim_cast").format(sp["name"], dmg)); play_sound("fireball")

    enemy_hp -= dmg
    if dmg > stats_best_damage: stats_best_damage = dmg

    if base.get("heal"):
        heal = base["heal"]
        player_hp = min(player_hp + heal, player_max_hp)
        add_log(f"💚 +{heal} HP")

    if random.random() < elem["chance"]:
        eff = elem["effect"]
        if eff == "burn":
            enemy_hp -= 10
            add_log(t("arkim_effect_burn").format(10))
        elif eff == "freeze":
            enemy_frozen_turns = 1
            add_log(t("arkim_effect_freeze"))
        elif eff == "stun":
            enemy_frozen_turns = 1
            add_log(t("arkim_effect_stun"))
        elif eff == "steal":
            player_hp = min(player_hp + 10, player_max_hp)
            add_log(t("arkim_effect_steal").format(10))

    arkim_cooldown = 2

    if enemy_hp <= 0:
        process_enemy_death(); return

    enemy_turn()
    update_status(); save_game()

SHOP_ITEMS = {
    "big_potion":   30,
    "magic_amulet": 50,
    "elixir_mana":  40,
    "crown":        150,
}

def shop():
    global gold
    if game_over: add_log(t("game_over")); return
    if not is_peaceful(location): add_log(t("no_shop_here")); return
    if location != 7: add_log(t("shop_only_city")); return

    discount = get_discount("city")
    win = tk.Toplevel(root)
    win.title(t("shop")); win.configure(bg="#222")
    win.geometry("480x520")
    win.transient(root); win.grab_set()

    tk.Label(win, text="🛒 " + t("shop"), font=("Arial", 18, "bold"),
             bg="#222", fg="gold").pack(pady=10)

    info_frame = tk.Frame(win, bg="#222")
    info_frame.pack(fill=tk.X, padx=20)
    gold_label = tk.Label(info_frame, text=f"{t('shop_your_gold')}: {gold} 💰",
                          font=("Arial", 12), bg="#222", fg="white")
    gold_label.pack(anchor="w")
    if discount > 0:
        tk.Label(info_frame, text=f"{t('shop_discount')}: -{int(discount*100)}%",
                 font=("Arial", 11), bg="#222", fg="#7CFC00").pack(anchor="w")

    listbox = tk.Listbox(win, font=("Arial", 12), bg="#111", fg="lightgreen",
                         selectbackground="#3a6ea5", activestyle="none")
    listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    item_ids = list(SHOP_ITEMS.keys())

    def refresh_list():
        listbox.delete(0, tk.END)
        for item_id in item_ids:
            base_price = SHOP_ITEMS[item_id]
            final_price = int(base_price * (1 - discount))
            name = t(item_id)
            it = ITEMS.get(item_id, {})
            effect = ""
            if "heal" in it: effect = f" (+{it['heal']} HP)"
            elif "mana" in it: effect = f" (+{it['mana']} mana)"
            elif "bonus_attack" in it: effect = f" (+{it['bonus_attack']} ATK)"
            elif "bonus_defence" in it: effect = f" (+{it['bonus_defence']} DEF)"
            elif "bonus_max_hp" in it: effect = f" (+{it['bonus_max_hp']} HP)"
            listbox.insert(tk.END, f"{name}{effect}  —  {final_price} 💰")
    refresh_list()

    desc_label = tk.Label(win, text="", font=("Arial", 10), bg="#222", fg="#dddddd",
                          justify=tk.LEFT, wraplength=440)
    desc_label.pack(padx=20, pady=5)

    def on_select(evt=None):
        sel = listbox.curselection()
        if not sel: desc_label.config(text=""); return
        item_id = item_ids[sel[0]]
        final_price = int(SHOP_ITEMS[item_id] * (1 - discount))
        can = gold >= final_price
        desc_label.config(text=f"{t('shop_price')}: {final_price} 💰   |   {t('shop_your_gold')}: {gold} 💰",
                          fg="#7CFC00" if can else "#ff6060")
    listbox.bind("<<ListboxSelect>>", on_select)

    def buy():
        global gold
        sel = listbox.curselection()
        if not sel: return
        item_id = item_ids[sel[0]]
        final_price = int(SHOP_ITEMS[item_id] * (1 - discount))
        if gold < final_price:
            add_log(t("shop_cant_afford")); return
        gold -= final_price
        add_item(item_id)
        add_log(t("shop_buy").format(t(item_id), final_price))
        play_sound("shop"); check_achievements(); save_game()
        gold_label.config(text=f"{t('shop_your_gold')}: {gold} 💰")
        refresh_list(); on_select(); update_status()

    btn_row = tk.Frame(win, bg="#222"); btn_row.pack(pady=10)
    tk.Button(btn_row, text="💰 " + t("shop_buy_btn"), font=("Arial", 12), width=14,
              bg="#3a7a3a", fg="white", command=buy).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_row, text=t("back"), font=("Arial", 12), width=14,
              bg="#6b6b6b", fg="white", command=win.destroy).pack(side=tk.LEFT, padx=5)

def crafting():
    global stats_crafts
    if game_over: add_log(t("game_over")); return

    win = tk.Toplevel(root)
    win.title(t("craft_title")); win.configure(bg="#222")
    win.geometry("520x560")
    win.transient(root); win.grab_set()

    tk.Label(win, text="🔨 " + t("craft_title"), font=("Arial", 18, "bold"),
             bg="#222", fg="gold").pack(pady=10)

    listbox = tk.Listbox(win, font=("Arial", 11), bg="#111", fg="lightgreen",
                         selectbackground="#3a6ea5", activestyle="none")
    listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def recipe_available(rec):
        return has_items(rec["ingredients"])

    def refresh():
        listbox.delete(0, tk.END)
        for rec in RECIPES:
            result_name = t(rec["result"]["id"])
            mark = "✅" if recipe_available(rec) else "❌"
            listbox.insert(tk.END, f"{mark}  {result_name}")
    refresh()

    desc_label = tk.Label(win, text="", font=("Arial", 10), bg="#222", fg="#dddddd",
                          justify=tk.LEFT, wraplength=480)
    desc_label.pack(padx=20, pady=5)

    def show_desc(evt=None):
        sel = listbox.curselection()
        if not sel: desc_label.config(text=""); return
        rec = RECIPES[sel[0]]
        lines = [t("craft_ingredients")]
        for ing in rec["ingredients"]:
            have = sum(e["count"] for e in inventory if e["id"] == ing["id"])
            color = "✅" if have >= ing["count"] else "❌"
            lines.append(f"  {color} {t(ing['id'])} x{ing['count']}  ({have})")
        res = rec["result"]
        lines.append("")
        lines.append(f"{t('craft_result')} {t(res['id'])} x{res['count']}")
        desc_label.config(text="\n".join(lines))
    listbox.bind("<<ListboxSelect>>", show_desc)

    def do_craft():
        global stats_crafts
        sel = listbox.curselection()
        if not sel: return
        rec = RECIPES[sel[0]]
        if not recipe_available(rec):
            add_log(t("craft_fail")); return
        for ing in rec["ingredients"]:
            remove_item(ing["id"], ing["count"])
        add_item(rec["result"]["id"], rec["result"]["count"])
        stats_crafts += 1
        add_log(t("craft_success").format(t(rec["result"]["id"])))
        play_sound("levelup"); check_achievements(); save_game()
        refresh(); show_desc(); update_status()

    btn_row = tk.Frame(win, bg="#222"); btn_row.pack(pady=10)
    tk.Button(btn_row, text="🔨 " + t("craft_btn"), font=("Arial", 12), width=14,
              bg="#3a7a3a", fg="white", command=do_craft).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_row, text=t("back"), font=("Arial", 12), width=14,
              bg="#6b6b6b", fg="white", command=win.destroy).pack(side=tk.LEFT, padx=5)

def show_map():
    win = tk.Toplevel(root)
    win.title("🗺️ " + t("map_title")); win.configure(bg="#1a1a2e")
    win.geometry("580x520")
    win.transient(root); win.grab_set()

    tk.Label(win, text="🗺️ " + t("map_title"),
             font=("Arial", 16, "bold"), bg="#1a1a2e", fg="gold").pack(pady=10)
    canvas = tk.Canvas(win, width=540, height=380, bg="#0a0a15", highlightthickness=1,
                       highlightbackground="#444")
    canvas.pack(padx=15, pady=10)

    positions = {1: (80, 70), 2: (260, 70), 3: (440, 70),
                 6: (80, 180), 7: (260, 180), 9: (440, 180),
                 4: (440, 280), 5: (440, 360), 8: (260, 280)}
    connections = [(1, 2), (2, 3), (1, 6), (3, 9), (3, 7),
                   (6, 7), (7, 8), (9, 4), (4, 5), (8, 5)]

    for a, b in connections:
        x1, y1 = positions[a]; x2, y2 = positions[b]
        canvas.create_line(x1, y1, x2, y2, fill="#555", width=2)

    current_connected = locations_data[location]["connected"] if not game_over else []

    for loc_id, (x, y) in positions.items():
        is_current = (loc_id == location)
        is_visited = (loc_id in visited_locations)
        is_peace = is_peaceful(loc_id)
        can_travel = (loc_id in current_connected) and not (not is_peaceful(location) and enemy_hp > 0) and not game_over

        if is_current:
            color, outline, width = "#ffd700", "#ffffff", 4
        elif is_visited:
            color = "#3a7a3a" if is_peace else "#a53a3a"
            outline, width = "#888", 2
        else:
            color, outline, width = "#333", "#555", 1

        if can_travel and not is_current:
            outline = "#7CFC00"
            width = 3

        r = 28
        canvas.create_oval(x - r, y - r, x + r, y + r,
                           fill=color, outline=outline, width=width)
        canvas.create_text(x, y - 6, text="🏠" if is_peace else "⚔️", font=("Arial", 14), fill="white")
        canvas.create_text(x, y + 10, text=str(loc_id), font=("Arial", 10, "bold"), fill="white")
        canvas.create_text(x, y + r + 10, text=get_loc_name(loc_id), font=("Arial", 9), fill="#cccccc")

    # Подсказка
    tk.Label(win, text="🖱 " + t("map_click_hint"),
             font=("Arial", 10, "italic"), bg="#1a1a2e", fg="#7CFC00").pack(pady=5)

    legend = tk.Frame(win, bg="#1a1a2e")
    legend.pack(pady=5)
    tk.Label(legend, text="🟡 " + t("map_you_here"),
             font=("Arial", 10), bg="#1a1a2e", fg="#ffd700").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="🏠 " + ("Мирная" if LANG=="ru" else "Peaceful"),
             font=("Arial", 10), bg="#1a1a2e", fg="#7CFC00").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="⚔️ " + ("Боевая" if LANG=="ru" else "Combat"),
             font=("Arial", 10), bg="#1a1a2e", fg="#ff8080").pack(side=tk.LEFT, padx=10)

    def on_map_click(event):
        if game_over: return
        if not is_peaceful(location) and enemy_hp > 0:
            add_log(t("kill_first")); return
        click_x, click_y = event.x, event.y
        connected = locations_data[location]["connected"]
        for loc_id, (lx, ly) in positions.items():
            dist = ((click_x - lx) ** 2 + (click_y - ly) ** 2) ** 0.5
            if dist <= 30:
                if loc_id == location:
                    return  # уже здесь
                if loc_id in connected:
                    win.destroy()
                    do_move_to(loc_id)
                    return
                # Не соседняя — игнор
                return

    canvas.bind("<Button-1>", on_map_click)

    tk.Button(win, text=t("back"), font=("Arial", 12), width=14,
              bg="#6b6b6b", fg="white", command=win.destroy).pack(pady=8)

def show_inventory():
    if not inventory:
        messagebox.showinfo(t("inventory"), t("empty_inventory")); return
    inv_win = tk.Toplevel(root)
    inv_win.title(t("inventory")); inv_win.geometry("350x380")
    inv_win.configure(bg="#222"); inv_win.transient(root)
    tk.Label(inv_win, text=t("inventory"), bg="#222", fg="white",
             font=("Arial", 14, "bold")).pack(pady=8)
    listbox = tk.Listbox(inv_win, font=("Arial", 12), bg="#111", fg="lightgreen")
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    for entry in inventory:
        name = t(entry["id"])
        display = f"{name} x{entry['count']}" if entry["count"] > 1 else name
        listbox.insert(tk.END, display)

    def use_selected():
        sel = listbox.curselection()
        if not sel: return
        idx = sel[0]
        if idx < len(inventory):
            use_item(inventory[idx]["id"]); inv_win.destroy()
    tk.Button(inv_win, text=t("use"), command=use_selected).pack(pady=8)

def use_item(item_id):
    global player_hp, player_max_hp, mana
    item = ITEMS.get(item_id)
    if not item: return
    if item["type"] == "consumable":
        if "heal" in item:
            heal = item["heal"]
            player_hp = min(player_hp + heal, player_max_hp)
            add_log(f"+{heal} HP"); play_sound("heal")
        if "mana" in item:
            mana = min(mana + item["mana"], mana_max)
            add_log(f"+{item['mana']} mana"); play_sound("heal_spell")
        remove_item(item_id)
    else:
        add_log(t("passive_item"))
    update_status()

def show_stats():
    playtime = int(time.time() - GAME_START_TIME)
    h = playtime // 3600; m = (playtime % 3600) // 60; s = playtime % 60
    text = (f"{t('stats_title')}\n\n"
            f"{t('stats_playtime').format(f'{h:02d}:{m:02d}:{s:02d}')}\n"
            f"{t('stats_kills').format(stats_kills)}\n"
            f"{t('stats_potions_used').format(stats_potions_used)}\n"
            f"{t('stats_best_damage').format(stats_best_damage)}\n"
            f"{t('stats_crits').format(stats_crits)}\n"
            f"{t('stats_quests_done').format(len(completed_quests))}\n"
            f"{t('stats_achievements').format(len(achievements_unlocked), len(ACHIEVEMENTS))}\n\n")
    text += f"{t('stats_reputation')}\n"
    for fac, data in REP_FACTIONS.items():
        text += f"  • {t(data['name_key'])}: {get_rep(fac)} ({get_rep_label(fac)})\n"
    text += "\n"
    if achievements_unlocked:
        text += "🏆:\n"
        for a in achievements_unlocked:
            text += f"• {t(ACHIEVEMENTS[a]['name_key'])}\n"
    messagebox.showinfo(t("stats_title"), text)

def show_help():
    messagebox.showinfo(t("help"), t("help_text"))

def reset_save():
    if messagebox.askyesno(t("reset_save"), t("reset_confirm")):
        if os.path.exists(SAVE_FILE):
            try: os.remove(SAVE_FILE)
            except Exception: pass
        messagebox.showinfo(t("reset_save"), t("reset_done"))

def quit_game():
    if messagebox.askyesno(t("quit_title"), t("save_quit")):
        save_game()
    save_settings(); stop_music(); root.destroy()

def show_victory_screen():
    playtime = int(time.time() - GAME_START_TIME)
    h = playtime // 3600; m = (playtime % 3600) // 60; s = playtime % 60
    time_str = f"{h:02d}:{m:02d}:{s:02d}"
    win = tk.Toplevel(root)
    win.title(t("victory_title")); win.configure(bg="#1a1a2e")
    win.geometry("500x500")
    win.transient(root); win.grab_set()
    tk.Label(win, text="🏆 " + t("victory_title") + " 🏆",
             font=("Arial", 24, "bold"), bg="#1a1a2e", fg="gold").pack(pady=20)
    text = t("victory_text").format(level, stats_kills, len(completed_quests),
                                     len(achievements_unlocked), len(ACHIEVEMENTS),
                                     stats_best_damage, time_str)
    tk.Label(win, text=text, font=("Arial", 12), bg="#1a1a2e", fg="white",
             justify=tk.LEFT).pack(pady=10, padx=20)

    def start_ng_plus():
        win.destroy(); new_game_plus()

    def continue_game():
        win.destroy(); show_menu()

    tk.Button(win, text=t("new_game_plus"), font=("Arial", 13), width=18,
              bg="#3a7a3a", fg="white", command=start_ng_plus).pack(pady=8)
    tk.Button(win, text=t("continue"), font=("Arial", 12), width=18,
              bg="#6b6b6b", fg="white", command=continue_game).pack(pady=5)

def new_game_plus():
    global player_hp, player_max_hp, potions, mana, mana_max, exp, exp_to_next
    global location, enemy_name, enemy_hp, game_over, inventory, attack_bonus, defence_bonus
    global active_quest, quest_progress, completed_quests, location_history, story_shown
    global boss_defeated, custom_spells, arkim_cooldown
    player_hp = player_max_hp
    potions = 3
    mana = mana_max
    exp = 0; exp_to_next = 50 + (level - 1) * 25
    location = 6; enemy_name = "goblin"; enemy_hp = 60
    game_over = False; inventory = []
    attack_bonus = 0; defence_bonus = 0
    active_quest = None; quest_progress = {}
    location_history = []; story_shown = []
    boss_defeated = False
    custom_spells = []
    arkim_cooldown = 0
    log_text.config(state='normal'); log_text.delete(1.0, tk.END); log_text.config(state='disabled')
    add_log(t("ng_plus_start")); add_log(t("welcome"))
    add_log(("Ты в " if LANG == "ru" else "You are in ") + get_loc_name(location))
    reset_enemy()
    save_game(); show_game_screen()

TUTORIAL_STEPS = ["tut_1", "tut_2", "tut_3", "tut_4", "tut_5", "tut_6", "tut_7"]

def show_tutorial_step(win, step_index, on_finish):
    for w in win.winfo_children():
        w.destroy()
    win.title(t("tutorial_title")); win.configure(bg="#222")
    win.geometry("520x420")
    win.resizable(False, False)
    tk.Label(win, text=f"{t('tutorial_title')}  {step_index + 1}/{len(TUTORIAL_STEPS)}",
             font=("Arial", 14, "bold"), bg="#222", fg="white").pack(pady=10)
    tk.Frame(win, height=2, bg="#444").pack(fill=tk.X, padx=20)
    tk.Label(win, text=t(TUTORIAL_STEPS[step_index]), font=("Arial", 11), bg="#222",
             fg="#dddddd", justify=tk.LEFT, wraplength=480, anchor="nw",
             padx=20, pady=15).pack(fill=tk.BOTH, expand=True)
    btn_row = tk.Frame(win, bg="#222"); btn_row.pack(pady=12)

    def next_step():
        if step_index + 1 < len(TUTORIAL_STEPS):
            show_tutorial_step(win, step_index + 1, on_finish)
        else:
            win.destroy(); on_finish()

    def skip():
        win.destroy(); on_finish()

    if step_index + 1 < len(TUTORIAL_STEPS):
        tk.Button(btn_row, text=t("tut_next"), font=("Arial", 11), width=14,
                  bg="#3a6ea5", fg="white", command=next_step).pack(side=tk.LEFT, padx=5)
    else:
        tk.Button(btn_row, text=t("tut_start"), font=("Arial", 11), width=14,
                  bg="#3a7a3a", fg="white", command=next_step).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_row, text=t("tut_skip"), font=("Arial", 11), width=14,
              bg="#6b6b6b", fg="white", command=skip).pack(side=tk.LEFT, padx=5)

def start_tutorial(callback):
    win = tk.Toplevel(root)
    win.transient(root); win.grab_set()
    show_tutorial_step(win, 0, callback)

def start_game(new_game_flag=True):
    global player_hp, player_max_hp, potions, mana, mana_max, gold, level, exp, exp_to_next
    global location, enemy_name, enemy_hp, game_over, inventory, attack_bonus, defence_bonus
    global stats_kills, stats_potions_used, stats_best_damage, stats_crafts, stats_crits
    global active_quest, quest_progress, completed_quests, location_history
    global achievements_unlocked, enemy_kill_counts, story_shown, boss_phase, boss_poison_turns
    global boss_defeated, reputation, visited_locations, npc_memory, custom_spells, arkim_cooldown

    def actually_start():
        if new_game_flag:
            reset_enemy()
            log_text.config(state='normal'); log_text.delete(1.0, tk.END); log_text.config(state='disabled')
            add_log(t("welcome"))
            add_log(("Ты в " if LANG == "ru" else "You are in ") + get_loc_name(location))
            visited_locations.add(location)
            save_game(); play_current_game_music()
        else:
            if load_game_data():
                reset_enemy()
                add_log(t("load_save").format(get_loc_name(location)))
                visited_locations.add(location)
                play_current_game_music()
            else:
                messagebox.showerror("Error", "Load failed!" if LANG == "en" else "Ошибка загрузки!")
                return
        show_game_screen()

    if new_game_flag:
        player_hp = 100; player_max_hp = 100; potions = 3
        mana = 50; mana_max = 50; gold = 50
        level = 1; exp = 0; exp_to_next = 50
        location = 6; enemy_name = "goblin"; enemy_hp = 60
        game_over = False; inventory = []
        attack_bonus = 0; defence_bonus = 0
        stats_kills = 0; stats_potions_used = 0; stats_best_damage = 0
        stats_crafts = 0; stats_crits = 0
        active_quest = None; quest_progress = {}; completed_quests = []
        location_history = []; achievements_unlocked = []
        enemy_kill_counts = {}; story_shown = []
        boss_phase = 1; boss_poison_turns = 0
        boss_defeated = False
        reputation = {"village": 0, "city": 0, "citadel": 0}
        visited_locations = set()
        npc_memory = {}
        custom_spells = []
        arkim_cooldown = 0
        start_tutorial(actually_start)
    else:
        actually_start()

def show_menu():
    stop_music(); play_music("menu_music.ogg")
    menu_frame.pack(fill=tk.BOTH, expand=True)
    game_frame.pack_forget(); settings_frame.pack_forget()

def show_game_screen():
    menu_frame.pack_forget(); game_frame.pack(fill=tk.BOTH, expand=True)
    settings_frame.pack_forget(); update_status()

def build_settings():
    """Пересоздаёт все виджеты настроек по текущему языку."""
    for widget in settings_frame.winfo_children():
        widget.destroy()

    tk.Label(settings_frame, text=t("settings"), font=("Arial", 22, "bold"),
             bg="#222", fg="white").pack(pady=15)
    tk.Frame(settings_frame, height=2, bg="#444").pack(fill=tk.X, padx=60, pady=5)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("language"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    lang_var.set("Русский" if LANG == "ru" else "English")
    tk.OptionMenu(row, lang_var, "Русский", "English").pack(side=tk.LEFT)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("fullscreen"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    fs_var.set(t("on") if FULLSCREEN else t("off"))
    tk.OptionMenu(row, fs_var, t("on"), t("off")).pack(side=tk.LEFT)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("music"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    music_var.set(t("on") if MUSIC_ENABLED else t("off"))
    tk.OptionMenu(row, music_var, t("on"), t("off")).pack(side=tk.LEFT)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("music_volume"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    global music_vol_scale
    music_vol_scale = tk.Scale(row, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
                               bg="#222", fg="white", highlightthickness=0,
                               command=on_music_volume_change)
    music_vol_scale.set(int(MUSIC_VOLUME * 100))
    music_vol_scale.pack(side=tk.LEFT)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("music_choice"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    music_choice_var.set(music_choice_display(MUSIC_CHOICE))
    tk.OptionMenu(row, music_choice_var, t("music_random"),
                  "🎵 " + t("track_1"), "🎵 " + t("track_2")).pack(side=tk.LEFT)
    tk.Button(row, text="▶ " + t("listen"), font=("Arial", 10),
              bg="#3a7a3a", fg="white", command=listen_music).pack(side=tk.LEFT, padx=8)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("sounds"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    sounds_var.set(t("on") if SOUNDS_ENABLED else t("off"))
    tk.OptionMenu(row, sounds_var, t("on"), t("off")).pack(side=tk.LEFT)

    row = tk.Frame(settings_frame, bg="#222"); row.pack(pady=6, fill=tk.X, padx=60)
    tk.Label(row, text=t("sounds_volume"), font=("Arial", 12), bg="#222", fg="white",
             width=20, anchor="w").pack(side=tk.LEFT)
    global sounds_vol_scale
    sounds_vol_scale = tk.Scale(row, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
                                bg="#222", fg="white", highlightthickness=0,
                                command=on_sounds_volume_change)
    sounds_vol_scale.set(int(SOUNDS_VOLUME * 100))
    sounds_vol_scale.pack(side=tk.LEFT)

    tk.Frame(settings_frame, height=2, bg="#444").pack(fill=tk.X, padx=60, pady=15)
    btn_row = tk.Frame(settings_frame, bg="#222"); btn_row.pack(pady=10)
    tk.Button(btn_row, text=t("apply"), font=("Arial", 12), width=15,
              bg="#3a6ea5", fg="white", command=apply_settings).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_row, text=t("reset_save"), font=("Arial", 12), width=15,
              bg="#a53a3a", fg="white", command=reset_save).pack(side=tk.LEFT, padx=5)
    tk.Button(settings_frame, text=t("back"), font=("Arial", 12), width=15,
              bg="#6b6b6b", fg="white", command=show_menu).pack(pady=10)


def show_settings():
    menu_frame.pack_forget(); game_frame.pack_forget()
    build_settings()
    settings_frame.pack(fill=tk.BOTH, expand=True)

def apply_settings():
    global LANG, FULLSCREEN, MUSIC_ENABLED, SOUNDS_ENABLED, MUSIC_CHOICE
    LANG = "ru" if lang_var.get() == "Русский" else "en"
    FULLSCREEN = (fs_var.get() == t("on"))
    MUSIC_ENABLED = (music_var.get() == t("on"))
    SOUNDS_ENABLED = (sounds_var.get() == t("on"))
    MUSIC_CHOICE = music_choice_from_display(music_choice_var.get())
    root.attributes('-fullscreen', FULLSCREEN)
    if not MUSIC_ENABLED:
        stop_music()
    else:
        if game_frame.winfo_ismapped():
            play_current_game_music()
        else:
            play_music("menu_music.ogg")
    update_sounds_volume(); save_settings()
    update_all_buttons()
    build_settings()  
    root.title(f"{t('title')} — {VERSION}")
    update_status()

def listen_music():
    choice = music_choice_from_display(music_choice_var.get())
    fname = pick_random_game_music() if choice == "random" else choice
    if not SOUND_ENABLED:
        messagebox.showinfo(t("listen"), "Pygame not available." if LANG == "en" else "Pygame не установлен.")
        return
    path = resource_path(os.path.join("sounds", fname))
    if not os.path.exists(path):
        messagebox.showinfo(t("listen"), f"File not found: {fname}"); return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

def music_choice_display(key):
    if key == "random": return t("music_random")
    elif key == "game_music1.ogg": return "🎵 " + t("track_1")
    elif key == "game_music2.ogg": return "🎵 " + t("track_2")
    return t("music_random")

def music_choice_from_display(disp):
    if disp == t("music_random"): return "random"
    elif disp == "🎵 " + t("track_1"): return "game_music1.ogg"
    elif disp == "🎵 " + t("track_2"): return "game_music2.ogg"
    return "random"

def on_music_volume_change(val):
    global MUSIC_VOLUME
    MUSIC_VOLUME = int(val) / 100
    update_music_volume(); save_settings()

def on_sounds_volume_change(val):
    global SOUNDS_VOLUME
    SOUNDS_VOLUME = int(val) / 100
    update_sounds_volume(); save_settings()

def update_all_buttons():
    for btn in all_buttons:
        if btn in menu_buttons:
            idx = menu_buttons.index(btn)
            if idx == 0: btn.config(text=t("new_game"))
            elif idx == 1: btn.config(text=t("load_game"))
            elif idx == 2: btn.config(text=t("help"))
            elif idx == 3: btn.config(text=t("settings"))
            elif idx == 4: btn.config(text=t("quit"))
        elif btn in game_buttons:
            idx = game_buttons.index(btn)
            labels = [
                t("attack"), t("heal"), t("fireball"), t("heal_spell"), t("inventory"),
                t("rest"), t("talk"), t("shop"), t("craft"), "✨ " + t("arkims"),
                "🗺️ " + t("map"), t("forward"), t("back_btn"), t("save"),
                t("stats_short"), t("settings"), t("quit"), "🔮 " + t("arkim_use")
            ]
            if idx < len(labels):
                btn.config(text=labels[idx])

load_settings()
root = tk.Tk()
root.title(f"{t('title')} — {VERSION}")
root.geometry("740x720")
root.resizable(False, False)
root.configure(bg="#222")

load_sounds()

menu_buttons = []; game_buttons = []; settings_buttons = []; all_buttons = []
lang_var = tk.StringVar(value="Русский")
fs_var = tk.StringVar(value="Выкл")
music_var = tk.StringVar(value="Вкл")
sounds_var = tk.StringVar(value="Вкл")
music_choice_var = tk.StringVar(value="Случайно")

menu_frame = tk.Frame(root, bg="#222")
menu_frame.pack(fill=tk.BOTH, expand=True)
tk.Label(menu_frame, text=t("title"), font=("Arial", 28, "bold"), bg="#222", fg="white").pack(pady=20)
tk.Label(menu_frame, text=VERSION, font=("Arial", 11), bg="#222", fg="gray").pack()
tk.Frame(menu_frame, height=2, bg="#444").pack(fill=tk.X, padx=100, pady=20)

btn_new = tk.Button(menu_frame, text=t("new_game"), font=("Arial", 14), width=22,
                    bg="#3a6ea5", fg="white", command=lambda: start_game(True))
btn_new.pack(pady=5); menu_buttons.append(btn_new); all_buttons.append(btn_new)

btn_load = tk.Button(menu_frame, text=t("load_game"), font=("Arial", 14), width=22,
                     bg="#3a6ea5", fg="white", command=lambda: start_game(False))
btn_load.pack(pady=5); menu_buttons.append(btn_load); all_buttons.append(btn_load)

btn_help = tk.Button(menu_frame, text=t("help"), font=("Arial", 14), width=22,
                     bg="#6b6b6b", fg="white", command=show_help)
btn_help.pack(pady=5); menu_buttons.append(btn_help); all_buttons.append(btn_help)

btn_settings = tk.Button(menu_frame, text=t("settings"), font=("Arial", 14), width=22,
                         bg="#6b6b6b", fg="white", command=show_settings)
btn_settings.pack(pady=5); menu_buttons.append(btn_settings); all_buttons.append(btn_settings)

btn_quit = tk.Button(menu_frame, text=t("quit"), font=("Arial", 14), width=22,
                     bg="#a53a3a", fg="white", command=quit_game)
btn_quit.pack(pady=5); menu_buttons.append(btn_quit); all_buttons.append(btn_quit)

game_frame = tk.Frame(root, bg="#222")
status_label = tk.Label(game_frame, text="", justify=tk.LEFT, font=("Courier", 11),
                        bg="#111", fg="white", padx=10, pady=10)
status_label.pack(fill=tk.X, padx=10, pady=5)
log_text = scrolledtext.ScrolledText(game_frame, height=13, state='disabled',
                                     font=("Consolas", 10), bg="#0a0a0a", fg="#7CFC00",
                                     insertbackground="white")
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
btn_frame = tk.Frame(game_frame, bg="#222"); btn_frame.pack(pady=10)

btn_style = {"width": 10, "font": ("Arial", 9, "bold"), "bg": "#3a6ea5", "fg": "white"}
action_style = {"width": 10, "font": ("Arial", 9, "bold"), "bg": "#a53a3a", "fg": "white"}
peaceful_style = {"width": 10, "font": ("Arial", 9, "bold"), "bg": "#3a7a3a", "fg": "white"}
craft_style = {"width": 10, "font": ("Arial", 9, "bold"), "bg": "#8a6e2a", "fg": "white"}
map_style = {"width": 10, "font": ("Arial", 9, "bold"), "bg": "#2a5a8a", "fg": "white"}
arkim_style = {"width": 10, "font": ("Arial", 9, "bold"), "bg": "#6a3a8a", "fg": "white"}

def make_btn(parent, text, cmd, style, r, c):
    b = tk.Button(parent, text=text, command=cmd, **style)
    b.grid(row=r, column=c, padx=3, pady=3)
    return b

btn_attack = make_btn(btn_frame, t("attack"), lambda: player_action("attack"), action_style, 0, 0)
game_buttons.append(btn_attack); all_buttons.append(btn_attack)
btn_heal = make_btn(btn_frame, t("heal"), lambda: player_action("heal"), peaceful_style, 0, 1)
game_buttons.append(btn_heal); all_buttons.append(btn_heal)
btn_fireball = make_btn(btn_frame, t("fireball"), lambda: player_action("fireball"), action_style, 0, 2)
game_buttons.append(btn_fireball); all_buttons.append(btn_fireball)
btn_heal_spell = make_btn(btn_frame, t("heal_spell"), lambda: player_action("heal_spell"), peaceful_style, 0, 3)
game_buttons.append(btn_heal_spell); all_buttons.append(btn_heal_spell)
btn_inventory = make_btn(btn_frame, t("inventory"), show_inventory, btn_style, 0, 4)
game_buttons.append(btn_inventory); all_buttons.append(btn_inventory)

btn_rest = make_btn(btn_frame, t("rest"), rest, peaceful_style, 1, 0)
game_buttons.append(btn_rest); all_buttons.append(btn_rest)
btn_talk = make_btn(btn_frame, t("talk"), talk, peaceful_style, 1, 1)
game_buttons.append(btn_talk); all_buttons.append(btn_talk)
btn_shop = make_btn(btn_frame, t("shop"), shop, peaceful_style, 1, 2)
game_buttons.append(btn_shop); all_buttons.append(btn_shop)
btn_craft = make_btn(btn_frame, t("craft"), crafting, craft_style, 1, 3)
game_buttons.append(btn_craft); all_buttons.append(btn_craft)
btn_arkim = make_btn(btn_frame, "✨ " + t("arkims"), arkim_workshop, arkim_style, 1, 4)
game_buttons.append(btn_arkim); all_buttons.append(btn_arkim)

btn_map = make_btn(btn_frame, "🗺️ " + t("map"), show_map, map_style, 2, 0)
game_buttons.append(btn_map); all_buttons.append(btn_map)
btn_forward = make_btn(btn_frame, t("forward"), go_forward, btn_style, 2, 1)
game_buttons.append(btn_forward); all_buttons.append(btn_forward)
btn_back = make_btn(btn_frame, t("back_btn"), go_back, btn_style, 2, 2)
game_buttons.append(btn_back); all_buttons.append(btn_back)
btn_save = make_btn(btn_frame, t("save"), lambda: save_game(True), btn_style, 2, 3)
game_buttons.append(btn_save); all_buttons.append(btn_save)
btn_stats = make_btn(btn_frame, t("stats_short"), show_stats, btn_style, 2, 4)
game_buttons.append(btn_stats); all_buttons.append(btn_stats)

btn_game_settings = make_btn(btn_frame, t("settings"), show_settings, btn_style, 3, 0)
game_buttons.append(btn_game_settings); all_buttons.append(btn_game_settings)
btn_game_quit = make_btn(btn_frame, t("quit"), quit_game, action_style, 3, 1)
game_buttons.append(btn_game_quit); all_buttons.append(btn_game_quit)
btn_arkim_cast = make_btn(btn_frame, "🔮 " + t("arkim_use"), open_custom_spell_menu, arkim_style, 3, 2)
game_buttons.append(btn_arkim_cast); all_buttons.append(btn_arkim_cast)

settings_frame = tk.Frame(root, bg="#222")

show_menu()
root.mainloop()
