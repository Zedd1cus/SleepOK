from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientFMS(StatesGroup):
    # Base UI
    selection_state = State()

    # UI Settings
    ui_settings_state = State()
    ui_reset_state = State()

    rise_agree = State()
    rise_changed = State()
    rise_changed_agree = State()

    # # UI Help
    # ui_help_state = State()

    # UI Rise or down
    ui_rise_state = State()
    ui_down_state = State()

    # Start settings
    settings_rise = State()
    settings_set_up_rise = State()
    settings_confirmation_rise = State()

    settings_sleep = State()
    settings_set_up_sleep = State()
    settings_confirmation_sleep = State()

    settings_time_of_notification = State()
    settings_set_up_time_of_notification = State()
    settings_confirmation_time_of_notification = State()



