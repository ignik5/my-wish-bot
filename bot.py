import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time
from config import GROUP_TOKEN, YOUR_ID, WIFE_ID, ALLOWED_USERS
from dictionaries import desire_messages, mood_messages, place_messages, feedback_messages, roleplay_messages, booking_options
from keyboards import (
    get_main_keyboard, get_desires_keyboard, get_roleplay_keyboard,
    get_mood_keyboard, get_place_keyboard, get_feedback_keyboard,
    get_booking_time_keyboard, get_booking_category_keyboard
)
from utils import send_to_you, send_to_wife

def main():
    while True:  # Бесконечный цикл переподключения
        try:
            vk_session = vk_api.VkApi(token=GROUP_TOKEN)
            vk = vk_session.get_api()
            group_id = vk.groups.getById(group_id=None)[0]['id']
            longpoll = VkBotLongPoll(vk_session, group_id)

            print("Бот запущен")
            
            state = {}
            last = {}
            tmp = {}

            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                    uid = event.message.from_id
                    text = event.message.text.strip().replace('%20', ' ')
                    print(f"RAW text: {repr(text)}")
                    
                    # Игнорируем посторонних
                    if uid not in ALLOWED_USERS:
                        continue
                    
                    # === ОБЩАЯ ЛОГИКА ДЛЯ ВСЕХ ===
                    # Если нажата кнопка "🔙 Назад" — показываем главное меню
                    if text == '🔙 Назад':
                        state[uid] = 'main'
                        vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                         keyboard=get_main_keyboard().get_keyboard())
                        continue
                    
                    # Если нажата "🚨 ЭКСТРЕННО!" — отправляем партнёру
                    if text == '🚨 ЭКСТРЕННО!':
                        if uid == YOUR_ID:
                            send_to_wife(vk, '🚨 СРОЧНО! ОЧЕНЬ ХОЧУ ТЕБЯ! ПРЯМО СЕЙЧАС! 🔥🔥🔥')
                        else:
                            send_to_you(vk, '🚨 СРОЧНО! ОЧЕНЬ ХОЧУ ТЕБЯ! ПРЯМО СЕЙЧАС! 🔥🔥🔥')
                        vk.messages.send(user_id=uid, message='✅ Экстренный вызов отправлен!', random_id=random.randint(1,2**31))
                        continue
                    
                    
                    # === ПЕРЕСЫЛКА ОБЫЧНОГО ТЕКСТА ===
                    # Если написан обычный текст (не начинается с эмодзи кнопок) — пересылаем партнёру
                    if not text.startswith(('❤️', '🎭', '🛋️', '📅', '💬', '🚨', '🔙', '✅', '✏️', '🕯️', '⚡', '🤍', '🔥', '🙏', '🌟', '🌀', '👩‍⚕️', '👨‍🏫', '👮', '💼', '✨', '🍂', '☀️', '🌙')):
                        if uid == YOUR_ID:
                            send_to_wife(vk, f"📝 {text}")
                            vk.messages.send(user_id=uid, message='✅ Отправлено жене', random_id=random.randint(1,2**31))
                        else:
                            send_to_you(vk, f"📝 {text}")
                            vk.messages.send(user_id=uid, message='✅ Отправлено мужу', random_id=random.randint(1,2**31))
                        continue
                    
                    # === ОБРАБОТКА КНОПОК (ДЛЯ ОБОИХ) ===
                    # Инициализация состояния
                    if uid not in state:
                        state[uid] = 'main'
                        # При первом сообщении показываем меню
                        vk.messages.send(user_id=uid, message='Привет! Вот твой пульт желаний 👇', 
                                         random_id=random.randint(1,2**31), 
                                         keyboard=get_main_keyboard().get_keyboard())
                        continue
                    
                    # ---------- Запись ----------
                    if state[uid] == 'booking_cat':
                        if text == '❤️ Желания':
                            state[uid] = 'booking_item'
                            tmp[uid] = {'type': 'desire'}
                            vk.messages.send(user_id=uid, message='Выбери желание', random_id=random.randint(1,2**31), 
                                             keyboard=get_desires_keyboard().get_keyboard())
                        elif text == '🎭 Ролевые игры':
                            state[uid] = 'booking_item'
                            tmp[uid] = {'type': 'roleplay'}
                            vk.messages.send(user_id=uid, message='Выбери ролевую игру', random_id=random.randint(1,2**31), 
                                             keyboard=get_roleplay_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Выбери категорию', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_category_keyboard().get_keyboard())
                        continue

                    if state[uid] == 'booking_item':
                        if tmp.get(uid, {}).get('type') == 'desire' and text in desire_messages:
                            tmp[uid]['msg'] = desire_messages[text]
                            state[uid] = 'booking_time'
                            vk.messages.send(user_id=uid, message='Выбери время', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_time_keyboard().get_keyboard())
                        elif tmp.get(uid, {}).get('type') == 'roleplay' and text in roleplay_messages:
                            tmp[uid]['msg'] = f"Хочу {roleplay_messages[text]}"
                            state[uid] = 'booking_time'
                            vk.messages.send(user_id=uid, message='Выбери время', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_time_keyboard().get_keyboard())
                        elif tmp.get(uid, {}).get('type') == 'roleplay' and text == '✏️ Свой вариант':
                            state[uid] = 'waiting_custom_roleplay'
                            vk.messages.send(user_id=uid, message='Напиши свой сценарий', random_id=random.randint(1,2**31))
                        else:
                            kb = get_desires_keyboard() if tmp.get(uid,{}).get('type')=='desire' else get_roleplay_keyboard()
                            vk.messages.send(user_id=uid, message='Выбери из списка', random_id=random.randint(1,2**31), keyboard=kb)
                        continue

                    if state[uid] == 'waiting_custom_roleplay':
                        if text:
                            tmp[uid]['msg'] = f"Хочу ролевую игру: {text}"
                            state[uid] = 'booking_time'
                            vk.messages.send(user_id=uid, message='Выбери время', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_time_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Напиши текст', random_id=random.randint(1,2**31))
                        continue

                    if state[uid] == 'booking_time':
                        if text == '🔙 Назад':
                            state[uid] = 'booking_cat'
                            vk.messages.send(user_id=uid, message='Выбери категорию', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_category_keyboard().get_keyboard())
                        elif text in booking_options:
                            if booking_options[text] == 'custom':
                                state[uid] = 'waiting_custom_time'
                                vk.messages.send(user_id=uid, message='Напиши время текстом', random_id=random.randint(1,2**31))
                            else:
                                # Отправляем запись партнёру
                                msg = f"📅 Запись: {tmp[uid]['msg']} на {booking_options[text]}"
                                if uid == YOUR_ID:
                                    send_to_wife(vk, msg)
                                else:
                                    send_to_you(vk, msg)
                                vk.messages.send(user_id=uid, message=f'✅ Запись на {booking_options[text]}', 
                                                 random_id=random.randint(1,2**31))
                                state[uid] = 'main'
                                vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                                 keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Выбери вариант', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_time_keyboard().get_keyboard())
                        continue

                    if state[uid] == 'waiting_custom_time':
                        if text:
                            msg = f"📅 Запись: {tmp[uid]['msg']} на {text}"
                            if uid == YOUR_ID:
                                send_to_wife(vk, msg)
                            else:
                                send_to_you(vk, msg)
                            vk.messages.send(user_id=uid, message=f'✅ Запись на {text}', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Напиши время', random_id=random.randint(1,2**31))
                        continue

                    # ---------- Основное меню ----------
                    if state[uid] == 'main':
                        if text == '❤️ Желания':
                            state[uid] = 'desires'
                            vk.messages.send(user_id=uid, message='Выбери желание', random_id=random.randint(1,2**31), 
                                             keyboard=get_desires_keyboard().get_keyboard())
                        elif text == '🎭 Ролевые игры':
                            state[uid] = 'roleplay'
                            vk.messages.send(user_id=uid, message='Выбери сценарий', random_id=random.randint(1,2**31), 
                                             keyboard=get_roleplay_keyboard().get_keyboard())
                        elif text == '🎭 Настроение':
                            state[uid] = 'mood'
                            vk.messages.send(user_id=uid, message='Настроение', random_id=random.randint(1,2**31), 
                                             keyboard=get_mood_keyboard().get_keyboard())
                        elif text == '🛋️ Место':
                            state[uid] = 'place'
                            vk.messages.send(user_id=uid, message='Выбери место', random_id=random.randint(1,2**31), 
                                             keyboard=get_place_keyboard().get_keyboard())
                        elif text == '📅 Запись':
                            state[uid] = 'booking_cat'
                            vk.messages.send(user_id=uid, message='Что записать?', random_id=random.randint(1,2**31), 
                                             keyboard=get_booking_category_keyboard().get_keyboard())
                        elif text == '💬 Обратная связь':
                            state[uid] = 'feedback'
                            vk.messages.send(user_id=uid, message='Обратная связь', random_id=random.randint(1,2**31), 
                                             keyboard=get_feedback_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())

                    elif state[uid] == 'desires':
                        if text in desire_messages:
                            last[uid] = text
                            # Отправляем желание партнёру
                            if uid == YOUR_ID:
                                send_to_wife(vk, desire_messages[text])
                            else:
                                send_to_you(vk, desire_messages[text])
                            vk.messages.send(user_id=uid, message=f'✅ {text}', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Выбери из списка', random_id=random.randint(1,2**31), 
                                             keyboard=get_desires_keyboard().get_keyboard())

                    elif state[uid] == 'roleplay':
                        if text in roleplay_messages:
                            last[uid] = text
                            msg = f"Хочу {roleplay_messages[text]}"
                            if uid == YOUR_ID:
                                send_to_wife(vk, msg)
                            else:
                                send_to_you(vk, msg)
                            vk.messages.send(user_id=uid, message=f'✅ {text}', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        elif text == '✏️ Свой вариант':
                            state[uid] = 'roleplay_custom'
                            vk.messages.send(user_id=uid, message='Напиши свой сценарий', random_id=random.randint(1,2**31))
                        else:
                            vk.messages.send(user_id=uid, message='Выбери из списка', random_id=random.randint(1,2**31), 
                                             keyboard=get_roleplay_keyboard().get_keyboard())

                    elif state[uid] == 'roleplay_custom':
                        if text:
                            msg = f"Хочу ролевую игру: {text}"
                            if uid == YOUR_ID:
                                send_to_wife(vk, msg)
                            else:
                                send_to_you(vk, msg)
                            vk.messages.send(user_id=uid, message='✅ Отправлено', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Напиши текст', random_id=random.randint(1,2**31))

                    elif state[uid] == 'mood':
                        if text in mood_messages:
                            msg = mood_messages[text]
                            if uid == YOUR_ID:
                                send_to_wife(vk, msg)
                            else:
                                send_to_you(vk, msg)
                            vk.messages.send(user_id=uid, message=f'✅ {text}', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Выбери настроение', random_id=random.randint(1,2**31), 
                                             keyboard=get_mood_keyboard().get_keyboard())

                    elif state[uid] == 'place':
                        if text in place_messages:
                            if uid in last and last[uid] in desire_messages:
                                msg = f"{desire_messages[last[uid]]} {place_messages[text]}"
                            elif uid in last and last[uid] in roleplay_messages:
                                msg = f"Хочу {roleplay_messages[last[uid]]} {place_messages[text]}"
                            else:
                                msg = f"Хочу {place_messages[text]}"
                            
                            if uid == YOUR_ID:
                                send_to_wife(vk, msg)
                            else:
                                send_to_you(vk, msg)
                            
                            vk.messages.send(user_id=uid, message=f'✅ {text}', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Выбери место', random_id=random.randint(1,2**31), 
                                             keyboard=get_place_keyboard().get_keyboard())

                    elif state[uid] == 'feedback':
                        if text == '🔁 Повтори последнее':
                            if uid in last:
                                if last[uid] in desire_messages:
                                    msg = f"Повтор: {desire_messages[last[uid]]}"
                                elif last[uid] in roleplay_messages:
                                    msg = f"Повтор: Хочу {roleplay_messages[last[uid]]}"
                                else:
                                    msg = None
                                
                                if msg:
                                    if uid == YOUR_ID:
                                        send_to_wife(vk, msg)
                                    else:
                                        send_to_you(vk, msg)
                                    vk.messages.send(user_id=uid, message='✅ Повтор отправлен', random_id=random.randint(1,2**31))
                            else:
                                vk.messages.send(user_id=uid, message='Нет сохранённого желания', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        elif text in feedback_messages:
                            msg = feedback_messages[text]
                            if uid == YOUR_ID:
                                send_to_wife(vk, msg)
                            else:
                                send_to_you(vk, msg)
                            vk.messages.send(user_id=uid, message=f'✅ {text}', random_id=random.randint(1,2**31))
                            state[uid] = 'main'
                            vk.messages.send(user_id=uid, message='Главное меню', random_id=random.randint(1,2**31), 
                                             keyboard=get_main_keyboard().get_keyboard())
                        else:
                            vk.messages.send(user_id=uid, message='Выбери пункт', random_id=random.randint(1,2**31), 
                                             keyboard=get_feedback_keyboard().get_keyboard())
        
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Переподключаюсь через 5 секунд...")
            time.sleep(5)
            # continue — перезапускаем цикл while

if __name__ == '__main__':
    main()