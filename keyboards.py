from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dictionaries import desire_messages, mood_messages, place_messages, feedback_messages, roleplay_messages, booking_options
# ---------- Клавиатуры ----------
def get_main_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button('❤️ Желания', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🎭 Ролевые игры', color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button('🎭 Настроение', color=VkKeyboardColor.SECONDARY)
    kb.add_button('🛋️ Место', color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button('📅 Запись', color=VkKeyboardColor.POSITIVE)
    kb.add_button('💬 Обратная связь', color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button('🚨 ЭКСТРЕННО!', color=VkKeyboardColor.NEGATIVE)
    return kb

def get_desires_keyboard():
    kb = VkKeyboard(one_time=False)
    for btn in desire_messages.keys():
        kb.add_button(btn, color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb

def get_roleplay_keyboard():
    kb = VkKeyboard(one_time=False)
    for rp in roleplay_messages.keys():
        kb.add_button(rp, color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('✏️ Свой вариант', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb

def get_mood_keyboard():
    kb = VkKeyboard(one_time=False)
    for mood in mood_messages.keys():
        kb.add_button(mood, color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb

def get_place_keyboard():
    kb = VkKeyboard(one_time=False)
    for pl in place_messages.keys():
        kb.add_button(pl, color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb

def get_feedback_keyboard():
    kb = VkKeyboard(one_time=False)
    for fb in feedback_messages.keys():
        kb.add_button(fb, color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('🔁 Повтори последнее', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb

def get_booking_time_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button('⚡ Прямо сейчас', color=VkKeyboardColor.POSITIVE)
    for opt in ['🍂 Сегодня вечером', '☀️ Завтра днём', '🌙 Завтра вечером', '📅 В пятницу вечером']:
        kb.add_button(opt, color=VkKeyboardColor.SECONDARY)
        kb.add_line()
    kb.add_button('✏️ Своё время', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb

def get_booking_category_keyboard():
    kb = VkKeyboard(one_time=False)
    kb.add_button('❤️ Желания', color=VkKeyboardColor.PRIMARY)
    kb.add_button('🎭 Ролевые игры', color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.SECONDARY)
    return kb