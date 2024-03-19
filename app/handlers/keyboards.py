from app.keyboards.reply import get_reply_keyboard
from app.messages import messages

HOME_KEYBOARD = get_reply_keyboard(messages['travel_button'])

TRAVEL_KEYBOARD = get_reply_keyboard(messages['travel_edit_button'], messages['travel_members_button'], messages['travel_locations_button'], messages['travel_notes_button'])