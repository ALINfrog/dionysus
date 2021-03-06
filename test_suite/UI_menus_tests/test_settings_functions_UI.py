"""Tests for settings_functions_UI.py"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from dionysus_app.UI_menus.settings_functions_UI import (get_user_choice_to_set_location,
                                                         user_decides_to_set_default_location,
                                                         user_set_chart_save_folder,
                                                         welcome_set_default_location_message,
                                                         )


class TestWelcomeSetDefaultLocationMessage(TestCase):
    def setUp(self):
        self.welcome_print_stmt = (
            'Welcome to dionysus.\n'
            'It looks like this is your first time running the program.\n\n'
            'Would you like to set a default location to save your charts?\n'
            'You can do this later or change your selection in Settings.\n'
            )

    @patch('dionysus_app.UI_menus.settings_functions_UI.print')
    def test_app_start_set_default_chart_save_location_user_set(
            self, mocked_print):
        assert welcome_set_default_location_message() is None

        mocked_print.assert_called_once_with(self.welcome_print_stmt)


class TestGetUserChoiceToSetLocation(TestCase):
    def setUp(self):
        self.input_prompt = "Type 'Y' for Yes or 'N' for No, and press enter: "
        self.affirmative_inputs = ['y',
                                   'Y',
                                   'yes',
                                   'Yes',
                                   'YES',
                                   'yEs',
                                   'YeS',
                                   ]
        self.negative_inputs = ['',  # Blank input/user hits return without input.
                                ' ',
                                '  ',
                                'n'
                                'N'
                                'No',
                                'NO',
                                'No thanks',
                                'Your mother was an hamster',
                                ]

    @patch('dionysus_app.UI_menus.settings_functions_UI.input')
    def test_get_user_choice_to_set_location_affirmative(self, mocked_input):
        for input_str in self.affirmative_inputs:
            with self.subTest(msg=f'input of {input_str} should return True'):
                mocked_input.return_value = input_str

                assert get_user_choice_to_set_location() is True
                mocked_input.assert_called_once_with(self.input_prompt)

                mocked_input.reset_mock(return_value=True)

    @patch('dionysus_app.UI_menus.settings_functions_UI.input')
    def test_get_user_choice_to_set_location_negative(self, mocked_input):
        for input_str in self.negative_inputs:
            with self.subTest(msg=f'input of {input_str} should return True'):
                mocked_input.return_value = input_str

                assert get_user_choice_to_set_location() is False
                mocked_input.assert_called_once_with(self.input_prompt)

                mocked_input.reset_mock(return_value=True)


class TestUserDecidesToSetDefaultLocation(TestCase):
    def setUp(self):
        self.user_choices = [True, False]

    @patch('dionysus_app.UI_menus.settings_functions_UI.clear_screen')
    @patch('dionysus_app.UI_menus.settings_functions_UI.get_user_choice_to_set_location')
    @patch('dionysus_app.UI_menus.settings_functions_UI.welcome_set_default_location_message')
    def test_user_decides_to_set_default_location(self,
                                                  mocked_welcome_set_default_location_message,
                                                  mocked_get_user_choice_to_set_location,
                                                  mocked_clear_screen,
                                                  ):
        for choice in self.user_choices:
            with self.subTest(msg=f'User choice = get_user_choice_to_set_location = {choice}'):
                mocked_get_user_choice_to_set_location.return_value = choice

                assert user_decides_to_set_default_location() == choice

                mocked_welcome_set_default_location_message.assert_called_once_with()
                mocked_get_user_choice_to_set_location.assert_called_once_with()
                mocked_clear_screen.assert_called_once_with()

                mocked_welcome_set_default_location_message.reset_mock(return_value=True)
                mocked_get_user_choice_to_set_location.reset_mock(return_value=True)
                mocked_clear_screen.reset_mock(return_value=True)


class TestUserSetChartSaveFolder(TestCase):
    mocked_APP_DEFAULT_CHART_SAVE_FOLDER = Path('app_default')

    def setUp(self):
        self.test_dialogue_message = 'Please select location for chart save folder, or press cancel to use default.'
        # Preset app default
        self.mocked_APP_DEFAULT_CHART_SAVE_FOLDER = Path('app_default')

        self.test_user_location = 'camelot'
        self.user_feedback = f'Default chart save folder set to {self.test_user_location}'

    @patch('dionysus_app.UI_menus.settings_functions_UI.APP_DEFAULT_CHART_SAVE_FOLDER',
           mocked_APP_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.UI_menus.settings_functions_UI.print')
    @patch('dionysus_app.UI_menus.settings_functions_UI.select_folder_dialogue')
    def test_user_set_set_chart_folder_blank_input(self, mocked_select_folder_dialogue, mocked_print):
        mocked_select_folder_dialogue.return_value = ''

        assert user_set_chart_save_folder() == self.mocked_APP_DEFAULT_CHART_SAVE_FOLDER

        mocked_select_folder_dialogue.assert_called_once_with(title_str=self.test_dialogue_message,
                                                              start_dir='..')
        mocked_print.assert_not_called()

    @patch('dionysus_app.UI_menus.settings_functions_UI.APP_DEFAULT_CHART_SAVE_FOLDER',
           mocked_APP_DEFAULT_CHART_SAVE_FOLDER)
    @patch('dionysus_app.UI_menus.settings_functions_UI.print')
    @patch('dionysus_app.UI_menus.settings_functions_UI.select_folder_dialogue')
    def test_user_set_set_chart_folder_user_selects_location(self, mocked_select_folder_dialogue, mocked_print):
        mocked_select_folder_dialogue.return_value = self.test_user_location

        assert user_set_chart_save_folder() == self.test_user_location

        mocked_select_folder_dialogue.assert_called_once_with(title_str=self.test_dialogue_message,
                                                              start_dir='..')
        mocked_print.assert_called_once_with(self.user_feedback)
