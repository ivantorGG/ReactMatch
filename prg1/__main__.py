# -*- coding: utf-8 -*-


import functools
import random
import sqlite3
import sys
import time
import csv
import os
from inst_vinds import GoInstructions

from PyQt6 import uic
from PyQt6 import QtGui, QtCore, QtMultimedia
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont, QPixmap, QTransform
from PyQt5.QtWidgets import QApplication as Q5Application


def update_wind(things_to_hide=None, things_to_show=None):
    """Скрываем часть окна, показываем другую часть окна.
    Вводим список того, что хотим скрыть, и того, что хотим показать"""

    if things_to_show is None:
        things_to_show = []
    if things_to_hide is None:
        things_to_hide = []
    for el in things_to_hide:
        try:
            el.hide()
        except AttributeError:
            for el2 in el:
                el2.hide()
    for el in things_to_show:
        try:
            el.show()
        except AttributeError:
            for el2 in el:
                el2.show()


class ReactMatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.go_intro = True
        self.go_instructions = False
        self.inst_animation_i = 0
        self.initUI()

    def initUI(self):
        """initUI"""
        uic.loadUi('prg.ui', self)  # Загружаем дизайн
        self.go_inst_animation = False
        if self.go_intro:
            self.go_intro = False
            app2 = Q5Application([])
            ex2 = GoInstructions('first_vid.avi', 8, False)
            ex2.show()
            app2.exec_()
        with open('first_load.txt', 'r', encoding='utf8') as f_read:
            first_start = f_read.readlines()

        with open('first_load.txt', 'w', encoding='utf8') as f_write:
            f_write.write('False')
        if first_start[0] == 'True':
            for btn in [self.lang_change_btn, self.start_btn, self.name_label, self.login_btn,
                        self.caption_label, self.lang_change_btn, self.frofil_lbl, self.top_players_btn]:
                btn.hide()
            for el in [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6,
                       self.label_7, self.label_8, self.label_9, self.label_10, self.label_11, self.label_12,
                       self.label_13, self.label_14, self.label_15, self.label_16]:
                el.show()
            self.instructions_btn.move(190, 250)
            self.label.setPixmap(
                QPixmap('images/click_here_v1.png').scaled(210, 210).transformed(QTransform().rotate(230)))
            self.label.resize(self.label.sizeHint())
            self.label_11.setPixmap(
                QPixmap('images/click_here_v6.png').scaled(160, 160).transformed(QTransform().rotate(240)))
            self.label_11.resize(self.label_11.sizeHint())
            self.label_2.setPixmap(
                QPixmap('images/click_here_v1.png').scaled(200, 200).transformed(QTransform().rotate(330)))
            self.label_2.resize(self.label_2.sizeHint())
            self.label_3.setPixmap(QPixmap('images/click_here_v3.png').scaled(160, 160))
            self.label_3.resize(self.label_3.sizeHint())
            self.label_4.setPixmap(QPixmap('images/click_here_v2.png').scaled(200, 200))
            self.label_4.resize(self.label_4.sizeHint())
            self.label_5.setPixmap(QPixmap('images/click_here_v4.png').scaled(160, 160))
            self.label_5.resize(self.label_5.sizeHint())
            self.label_6.setPixmap(
                QPixmap('images/click_here_v2.png').scaled(200, 200).transformed(QTransform().rotate(180)))
            self.label_6.resize(self.label_6.sizeHint())
            self.label_7.setPixmap(
                QPixmap('images/click_here_v3.png').scaled(160, 160).transformed(QTransform().rotate(270)))
            self.label_7.resize(self.label_7.sizeHint())
            self.label_7.raise_()
            self.label_8.setPixmap(
                QPixmap('images/click_here_v4.png').scaled(160, 160).transformed(QTransform().rotate(90)))
            self.label_8.resize(self.label_8.sizeHint())
            self.label_9.setPixmap(
                QPixmap('images/click_here_v5.png').scaled(160, 160).transformed(QTransform().rotate(180)))
            self.label_9.resize(self.label_9.sizeHint())
            self.label_10.setPixmap(
                QPixmap('images/click_here_v5.png').scaled(160, 160).transformed(QTransform().rotate(270)))
            self.label_10.resize(self.label_10.sizeHint())
            self.label_12.setPixmap(
                QPixmap('images/click_here_v6.png').scaled(160, 160).transformed(QTransform().rotate(310)))
            self.label_12.resize(self.label_12.sizeHint())
            self.label_13.setPixmap(
                QPixmap('images/click_here_v7.png').scaled(160, 160).transformed(QTransform().rotate(30)))
            self.label_13.resize(self.label_13.sizeHint())
            self.label_14.setPixmap(
                QPixmap('images/click_here_v7.png').scaled(160, 160).transformed(QTransform().rotate(90)))
            self.label_14.resize(self.label_14.sizeHint())
            self.label_15.setPixmap(
                QPixmap('images/click_here_v7.png').scaled(160, 160).transformed(QTransform().rotate(120)))
            self.label_15.resize(self.label_15.sizeHint())
            self.label_16.setPixmap(
                QPixmap('images/click_here_v3.png').scaled(160, 160).transformed(QTransform().rotate(290)))
            self.label_16.resize(self.label_16.sizeHint())
            self.go_inst_animation = True

        # настройки окна
        self.setFixedSize(800, 600)  # я не хочу чтобы размер игры меняли
        self.move(360, 100)  # перемещаю для удобства
        self.setWindowIcon(QtGui.QIcon('images/icon.png'))  # устанавливаем иконку
        self.setWindowTitle('ReactMatch')  # устанавливаем название

        # тут все переменные
        with open('lang.txt', 'r', encoding='utf8') as f:
            self.lang = f.readlines()[0]  # ставим изначальный язык

        self.level = 0  # изначально нулевой уровень
        self.times_lvl1 = []  # время реакции 1 уровня
        self.level1_btn_clicks_count = 0  # счётчик нажатий на кнопку 1 уровня
        self.move_lvl1_label = False  # перемещать надпись времени в 1 уровне
        self.lvl1_show_all_time_list = []  # внутри - qlabelы с временем 1-го уровня
        self.lvl2_time_list = []  # внутри - данные с временем 2-го уровня
        self.next_timeshow_lbl_pos_y = 20  # координаты надписи о времени
        self.trans_move = False  # переход не происходит
        self.stop_hustle = False  # экрану не надо переставать дрожать
        self.rotate_logo = False  # поворачивать прицел пока не надо
        self.logo_rotated_again = False  # прицел пока не повёрнут второй раз
        self.angle = 0  # градус, на который надо поворачивать прицел
        self.trans_block1_is_cut = False  # блок 1 пока не обрезан
        self.logo_rotated = False  # прицел пока не повёрнут
        self.countdown_done = False  # отсчёт пока не состоялся
        self.is_lvl2_btn1_clicked = False  # на 1-ю кнопку на уровне 2 ещё не кликнули
        self.is_lvl2_btn2_clicked = False  # на 2-ю кнопку на уровне 2 ещё не кликнули
        self.is_lvl2_btn3_clicked = False  # на 3-ю кнопку на уровне 2 ещё не кликнули
        self.is_lvl2_btn4_clicked = False  # на 4-ю кнопку на уровне 2 ещё не кликнули
        self.showercolor_goes_right = True  # изначально штука, которая движется и показывает цвет на
        # 3 уровне движется вправо
        # на 3 уровне 5 под-уровней и вот позиции y, которые может принимать эта штука для каждого под-уровня
        self.showercolor_poses_y = {1: 125,
                                    2: 235,
                                    3: 345,
                                    4: 455,
                                    5: 1000}

        self.lvl3_btn_clicks = 0
        self.tmp_showercolors = []
        self.lvl3_to_lvl4_trans_time = 0
        # вот все сундуки в 4 уровне
        self.lvl4_chest_btns = [self.lvl4_chest1_btn, self.lvl4_chest2_btn, self.lvl4_chest3_btn,
                                self.lvl4_chest4_btn, self.lvl4_chest5_btn, self.lvl4_chest6_btn,
                                self.lvl4_chest7_btn, self.lvl4_chest8_btn]
        # пусть пока правильная анимация сундуков не начинается
        self.go_corr_chest_animation = False
        # пусть пока неправильная анимация сундуков не начинается
        self.go_false_chest_animation = False
        # для анимации сундука, сейчас картинка сундука по номеру - 1
        self.chest_animation_i = 0
        # картинки сундука по номеру для анимации
        self.chest_animation_fases = ['chest_images/chest1.png',
                                      'chest_images/chest2.png',
                                      'chest_images/chest3.png',
                                      'chest_images/chest4.png',
                                      'chest_images/chest5.png',
                                      'chest_images/chest6.png',
                                      ]
        # изначально фаза анимации движения всех 8 сундуков - 1
        self.animation_faza = 1
        # изначально для некоторых фаз у нас проигрывается первая половина фазы
        self.first_harf_animation = True
        self.showing_corr_chest_count = 0
        # пока ни один сундук не может быть открыт
        self.chest_can_be_opened = False
        # пока ни один сундук не открыт
        self.chest_is_opened = False
        # пока не появляется блок для оценки качества игры
        self.go_estimation_block = False
        # пока игрок не дал оценку
        self.estimation = None
        # блок оценки пока не высунулся
        self.estimation_block_is_moved = False
        # блок оценки пока не засунулся обратно
        self.estimation_block_is_moved_again = False
        self.lvl5_animation_faza = 0

        self.results_all_players = QTableWidget(self)
        self.results_all_players.setColumnCount(4)
        self.results_all_players.setColumnWidth(0, 115)
        self.results_all_players.setColumnWidth(1, 115)
        self.results_all_players.setColumnWidth(2, 115)
        self.results_all_players.setColumnWidth(3, 115)
        self.results_all_players.setHorizontalHeaderLabels(['ЛОГИН', 'РЕЗУЛЬТАТ', 'ОЦЕНКА', 'ПРОФЕССИЯ'])
        self.results_all_players.resize(474, 450)
        self.results_all_players.move(155, 40)

        # ставим картинки для перехода
        # блок1 - левый
        self.trans_block2 = QLabel(self)
        self.trans_block2.setPixmap(QPixmap('images/trans_block2.png'))
        self.trans_block2.move(745, -210)
        self.trans_block2.resize(1000, 1055)
        # блок2 - правый
        self.trans_block1 = QLabel(self)
        self.trans_block1.setPixmap(QPixmap('images/trans_block1.png'))
        self.trans_block1.move(-780, -238)
        self.trans_block1.resize(1000, 1055)
        # блок3 - прицел
        self.trans_block3 = QLabel(self)
        self.trans_block3.setPixmap(QPixmap('images/logo.png'))
        self.trans_block3.move(300, 200)
        self.trans_block3.resize(181, 181)
        # label для обратного отсчёта на прицеле
        self.time_ending_logo_label = QLabel('6', self.trans_block3)
        self.time_ending_logo_label.move(80, 72)
        self.time_ending_logo_label.setStyleSheet("""color: rgb(255, 255, 255);
                                                    font: 63 20pt "Segoe UI Semibold";""")

        # ставим Qtimerы
        # для верхней надписи на 1-м уровне
        self.tmr_level1_label = QTimer()
        self.tmr_level1_label.timeout.connect(
            self.move_showlabel_timer)  # за каждую секунду происходит self.move_showlabel_timer
        self.tmr_level1_label.start(20)  # задержка между выполнением self.move_showlabel_timer 50 миллисекунд

        # для всех кнопок 2-го уровня
        self.tmr_level2 = QTimer()
        self.tmr_level2.timeout.connect(self.show_text_level2_btn_timer)
        self.tmr_level2.start(50)

        # для движения 1-го и 2-го блоков перехода
        self.tmr_trans_blocks_1_2 = QTimer()
        self.tmr_trans_blocks_1_2.timeout.connect(self.move_trans_blocks_timer)
        self.tmr_trans_blocks_1_2.start(20)

        # для поворота прицела
        self.tmr_trans_blocks_3 = QTimer()
        self.tmr_trans_blocks_3.timeout.connect(self.rotate_logo_timer)
        self.tmr_trans_blocks_3.start(5)

        # для обратного отсчёта на прицеле
        self.tmr_trans_countdown = QTimer()
        self.tmr_trans_countdown.timeout.connect(self.countdown_timer)
        self.tmr_trans_countdown.start(10)

        # для движения показателя цвета на 3-м уровне
        self.tmr_move_showcolor = QTimer()
        self.tmr_move_showcolor.timeout.connect(self.move_showercolor_timer)
        self.tmr_move_showcolor.start(20)

        # для анимации открывания сундука
        self.tmr_lvl4_chest_clicked_animation = QTimer()
        self.tmr_lvl4_chest_clicked_animation.timeout.connect(self.lvl4_chest_clicked_animation_timer)
        self.tmr_lvl4_chest_clicked_animation.start(30)

        # для анимации 8 сундуков
        self.tmr_lvl4_chests_animation = QTimer()
        self.tmr_lvl4_chests_animation.timeout.connect(self.lvl4_animation_timer)
        self.tmr_lvl4_chests_animation.start(30)

        # для движения блока оценки качества игры
        self.tmr_lvl5_estimation_block = QTimer()
        self.tmr_lvl5_estimation_block.timeout.connect(self.lvl5_estimation_block)
        self.tmr_lvl5_estimation_block.start(15)

        # для движения блока оценки качества игры
        self.tmr_lvl5_animation_block = QTimer()
        self.tmr_lvl5_animation_block.timeout.connect(self.lvl5_animation_block)
        self.tmr_lvl5_animation_block.start(20)

        self.tmr_inst_animations = QTimer()
        self.tmr_inst_animations.timeout.connect(self.inst_animations)
        self.tmr_inst_animations.start(400)

        # создаём звуки
        # для нормального момента (коричневый цвет)
        sound_file = 'sounds/normal_sound.wav'  # имя файла
        self.normal_sound = QtMultimedia.QSoundEffect()  # чёто присваиваем
        self.normal_sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))  # вообще без понятия, что тут
        self.normal_sound.setVolume(50)  # ставим громкость

        # для крутого момента (зелёный цвет)
        sound_file = 'sounds/cool_sound.wav'
        self.cool_sound = QtMultimedia.QSoundEffect()
        self.cool_sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))

        # для мегакрутого момента (красный цвет)
        sound_file = 'sounds/megacool_sound.wav'
        self.megacool_sound = QtMultimedia.QSoundEffect()
        self.megacool_sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))

        # для открытия правильного сундука
        self.opening_corr_chest_sound = QtMultimedia.QSoundEffect()
        self.opening_corr_chest_sound.setSource(QtCore.QUrl.fromLocalFile('sounds/chest_opening.wav'))

        # для открытия неправильного сундука
        self.opening_false_corr_chest_sound = QtMultimedia.QSoundEffect()
        self.opening_false_corr_chest_sound.setSource(QtCore.QUrl.fromLocalFile('sounds/false_chest_opening.wav'))

        # музыка анимации сундуков
        self.chests_animation_sound = QtMultimedia.QSoundEffect()
        self.chests_animation_sound.setSource(QtCore.QUrl.fromLocalFile('sounds/limbo_chests_snd.wav'))

        # для обратного отсчёта
        sound_one = QtMultimedia.QSoundEffect()
        sound_one.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/one_sound.wav"))

        sound_two = QtMultimedia.QSoundEffect()
        sound_two.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/two_sound.wav"))

        sound_three = QtMultimedia.QSoundEffect()
        sound_three.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/three_sound.wav"))

        sound_four = QtMultimedia.QSoundEffect()
        sound_four.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/four_sound.wav"))

        sound_five = QtMultimedia.QSoundEffect()
        sound_five.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/five_sound.wav"))

        # словарь для цифр и звуков обратного отсчёта
        self.nums_and_sounds = {
            1: sound_one,
            2: sound_two,
            3: sound_three,
            4: sound_four,
            5: sound_five
        }

        self.normal_marking = QtMultimedia.QSoundEffect()
        self.normal_marking.setSource(QtCore.QUrl.fromLocalFile("sounds/normal_marking.wav"))

        self.marking_for = QtMultimedia.QSoundEffect()
        self.marking_for.setSource(QtCore.QUrl.fromLocalFile("sounds/marking_for.wav"))

        self.final_marking = QtMultimedia.QSoundEffect()
        self.final_marking.setSource(QtCore.QUrl.fromLocalFile("sounds/final_marking.wav"))

        # упаковываем виджеты в фазы окна
        # главное окно
        self.main_wind = ([self.lang_change_btn, self.start_btn, self.instructions_btn, self.name_label, self.login_btn,
                           self.caption_label, self.lang_change_btn, self.frofil_lbl, self.top_players_btn] + [
                              self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6,
                              self.label_7, self.label_8, self.label_9, self.label_10, self.label_11, self.label_12,
                              self.label_13, self.label_14, self.label_15, self.label_16])
        # окно логина
        self.login_wind = [self.who_is_label, self.name_edit, self.passw_edit, self.login_done_btn, self.reg_btn,
                           self.login_error_label, self.back_to_mainwind_btn, self.create_avatar]
        # окно регистрации
        self.reg_wind = [self.who_is_label_2, self.reg_name_edit, self.reg_passw_edit, self.reg_done_btn,
                         self.reg_error_label, self.back_to_loginwind_btn, self.create_avatar]
        # окно первого уровня
        self.level1_wind = [self.level1_random_btn, self.level1_timeshow_label, self.lvl1_show_all_time_list]
        # окно второго уровня
        self.level2_wind = [self.level2_btn_1]
        # скрываю некоторые кнопки второго уровня т. к. они появляются позже
        self.level2_btn_2.hide()
        self.level2_btn_3.hide()
        self.level2_btn_4.hide()
        # окно третьего уровня
        self.level3_wind = [self.lvl3_brown_label1, self.lvl3_green_label1, self.lvl3_red_label1,
                            self.lvl3_brown_label2, self.lvl3_green_label2, self.lvl3_red_label2,
                            self.lvl3_brown_label3, self.lvl3_green_label3, self.lvl3_red_label3,
                            self.lvl3_brown_label4, self.lvl3_green_label4, self.lvl3_red_label4,
                            self.lvl3_brown_label5, self.lvl3_green_label5, self.lvl3_red_label5,
                            self.lvl3_pause_showercolor_btn, self.lvl3_show_color1_label, self.tmp_showercolors]
        # окно четвёртого уровня
        self.level4_wind = [self.lvl4_chest1_btn, self.lvl4_chest2_btn, self.lvl4_chest3_btn,
                            self.lvl4_chest4_btn, self.lvl4_chest5_btn, self.lvl4_chest6_btn,
                            self.lvl4_chest7_btn, self.lvl4_chest8_btn]
        # окно перехода
        self.trans_wind = [self.trans_block1, self.trans_block2, self.time_ending_logo_label, self.trans_block3]
        # окно пятого уровня
        self.level5_wind = [self.lvl5_bg_lbl1, self.lvl5_bg_lbl2, self.lvl5_levels_lbl, self.lvl5_raitings_lbl,
                            self.lvl5_lvl1_lbl, self.lvl5_lvl2_lbl, self.lvl5_lvl3_lbl, self.lvl5_lvl4_lbl,
                            self.lvl5_lvl1_mark_lbl, self.lvl5_lvl2_mark_lbl, self.lvl5_lvl3_mark_lbl,
                            self.lvl5_lvl4_mark_lbl,
                            self.lvl5_finar_rait_lbl, self.lvl5_finar_mark_lbl, self.lvl5_message_lbl]
        self.level6_wind = [self.results_all_players, self.back_to_mainwind_btn]

        # скрываем ненужные части окна
        for el in (self.login_wind + self.reg_wind + self.level1_wind + self.level2_wind + self.trans_wind +
                   self.level3_wind + self.level4_wind + self.level5_wind + self.level6_wind):
            try:
                el.hide()
            except AttributeError:
                for el2 in el:
                    el2.hide()

        # функционал кнопок главного окна
        self.start_btn.clicked.connect(self.start)  # кнопка старт
        self.instructions_btn.clicked.connect(self.instructions)  # кнопка инструкции
        self.lang_change_btn.setIcon(QtGui.QIcon('images/russia.png'))  # кнопка смены языка
        self.lang_change_btn.setIconSize(QtCore.QSize(100, 100))  # ставим размер кнопки смены языка
        self.lang_change_btn.clicked.connect(self.lang_changed)  # кнопка смены языка

        # открываем файл с сохранённым игроком и изменяем надпись текущего игрока
        with open('curr_user.txt', 'r', encoding='utf8') as f:
            self.name_label.setText(f.readlines()[0])

        # открываем файл со всеми зарегистрированными игроками
        with open('users.csv', 'r', encoding='utf8') as f:
            # чё там внутри
            lines = csv.reader(f, delimiter=';', quotechar='"')
            lines = list(lines)
            for el in lines:
                if el:  # если строка не пустая
                    if el[0] == self.name_label.text():  # если это текущий игрок
                        try:  # если игрок добавил аватарку
                            pix = QPixmap(el[2])  # считываем путь к файлу
                            self.frofil_lbl.setPixmap(pix.scaled(100, 100))  # ставим аватарку
                            break
                        except IndexError:  # иначе, ставим дефолтную аватарку
                            pix = QPixmap('images/default_avatar.png')
                            self.frofil_lbl.setPixmap(pix.scaled(100, 100))
            self.frofil_lbl.resize(self.frofil_lbl.sizeHint())

        # функционал кнопок логин окна
        self.login_btn.clicked.connect(self.login)  # начало логина
        self.login_done_btn.clicked.connect(self.login_is_done)  # конец логина
        self.back_to_mainwind_btn.clicked.connect(self.back_to_mainwind)  # вернуться в начальное меню

        # функционал кнопок регистрации окна
        self.reg_btn.clicked.connect(self.register)  # начало регистрации
        self.reg_done_btn.clicked.connect(self.reg_is_done)  # конец регистрации
        self.back_to_loginwind_btn.clicked.connect(self.back_to_loginwind)  # вернуться в логин меню
        self.create_avatar.clicked.connect(self.create_avatar_func)  # кнопка создания аватарки

        # кнопка 1 уровня окна
        self.level1_random_btn.setIcon(QtGui.QIcon('images/icon.png'))  # иконка
        self.level1_random_btn.setIconSize(QtCore.QSize(100, 100))  # размер иконки
        self.level1_random_btn.clicked.connect(self.lvl1_btn_clicked)  # функционал

        # кнопки 2 уровня окна
        self.level2_btn_1.clicked.connect(self.lvl2_btn1_clicked)  # функционал 1-й кнопки
        self.level2_btn_2.clicked.connect(self.lvl2_btn2_clicked)  # функционал 2-й кнопки
        self.level2_btn_3.clicked.connect(self.lvl2_btn3_clicked)  # функционал 3-й кнопки
        self.level2_btn_4.clicked.connect(self.lvl2_btn4_clicked)  # функционал 4-й кнопки

        # кнопки 3 уровня окна
        self.lvl3_pause_showercolor_btn.setIcon(QtGui.QIcon('images/pause.ico'))  # кнопка остановить показатель цвета
        self.lvl3_pause_showercolor_btn.setIconSize(QtCore.QSize(500, 500))  # изменяем размер картинки
        self.lvl3_pause_showercolor_btn.clicked.connect(self.lvl3_btn_clicked)
        # ставим картинку на показатель цвета и изменяем её размер
        self.lvl3_show_color1_label.setPixmap(QPixmap('images/show_color_lvl3.png').scaled(200, 100))
        # перемещаем показатель цвета на начальные координаты
        self.lvl3_show_color1_label.move(-40, 15)
        # изменяем размер label, чтобы картинка не урезалась
        self.lvl3_show_color1_label.resize(self.lvl3_show_color1_label.sizeHint())

        # кнопки 4 уровня окна
        for chest_btn in self.lvl4_chest_btns:  # для каждого сундука в 4 уровне
            chest_btn.setIcon(QtGui.QIcon('chest_images/chest1.png'))  # ставим картинку сундука
            chest_btn.setIconSize(QtCore.QSize(85, 85))
            chest_btn.clicked.connect(self.lvl4_chest_clicked_animation)  # если на него кликнули, вызываем ф-ю анимации

        # группа кнопок оценивания качества игры
        self.react_btn_group.buttonClicked.connect(self.estimation_btn_clicked)
        self.top_players_btn.clicked.connect(self.top_players)

        self.lang_changed()
        self.lang_changed()

    def inst_animations(self):
        if self.go_inst_animation:
            self.inst_animation_i += 1
            self.inst_animation_i %= 4
            img = ['images/click_here_v1.png', 'images/v1_v0.png', 'images/v1_v1.png', 'images/v1_v2.png'][self.inst_animation_i]
            self.label.setPixmap(QPixmap(img).scaled(210, 210).transformed(QTransform().rotate(230)))
            self.label_2.setPixmap(QPixmap(img).scaled(210, 210).transformed(QTransform().rotate(330)))

    def lvl5_animation_block(self):
        if self.lvl5_animation_faza == 1:
            if self.lvl5_bg_lbl1.x() < 50:
                self.lvl5_bg_lbl1.move(self.lvl5_bg_lbl1.x() + 10, self.lvl5_bg_lbl1.y())
                self.lvl5_bg_lbl2.move(self.lvl5_bg_lbl2.x() - 10, self.lvl5_bg_lbl2.y())
            else:
                self.lvl5_animation_faza = 2
                self.tmr_lvl5_animation_block.start(3080)
                for el in self.level5_wind:
                    el.raise_()

        if self.lvl5_animation_faza == 2:
            if self.lvl5_levels_lbl.isHidden():
                self.lvl5_levels_lbl.show()
                self.marking_for.play()
                self.tmr_lvl5_animation_block.start(780)

            elif self.lvl5_lvl1_lbl.isHidden():
                self.lvl5_lvl1_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_lvl2_lbl.isHidden():
                self.lvl5_lvl2_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_lvl3_lbl.isHidden():
                self.lvl5_lvl3_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_lvl4_lbl.isHidden():
                self.normal_marking.play()
                self.lvl5_lvl4_lbl.show()
                self.tmr_lvl5_animation_block.start(1580)

            elif self.lvl5_raitings_lbl.isHidden():
                self.marking_for.play()
                self.lvl5_raitings_lbl.show()
                self.tmr_lvl5_animation_block.start(780)

            elif self.lvl5_lvl1_mark_lbl.isHidden():
                self.lvl5_lvl1_mark_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_lvl2_mark_lbl.isHidden():
                self.lvl5_lvl2_mark_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_lvl3_mark_lbl.isHidden():
                self.lvl5_lvl3_mark_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_lvl4_mark_lbl.isHidden():
                self.lvl5_lvl4_mark_lbl.show()
                self.normal_marking.play()

            elif self.lvl5_finar_rait_lbl.isHidden():
                self.lvl5_finar_rait_lbl.show()
                self.final_marking.play()
                self.tmr_lvl5_animation_block.start(2680)

            elif self.lvl5_finar_mark_lbl.isHidden():
                self.normal_marking.play()
                self.lvl5_finar_mark_lbl.show()

                con = sqlite3.connect("records.sqlite")
                cur = con.cursor()
                # Выполнение запроса и получение всех результатов
                result = cur.execute(f"""SELECT message FROM results
                                        WHERE result == '{self.lvl5_finar_mark_en}'""").fetchone()
                self.lvl5_message_lbl.setText(result[0])
                self.lvl5_message_lbl.resize(self.lvl5_message_lbl.sizeHint())

                self.lvl5_message_lbl.show()

                logins = cur.execute("""SELECT login FROM players""").fetchall()

                if (self.name_label.text(),) not in logins:
                    # запись
                    cur.execute(f"""INSERT INTO players (login, result, estimation)
                        VALUES ('{self.name_label.text()}', '{self.lvl5_finar_mark_en}', {self.estimation})""")
                    con.commit()
                    cur.close()
                else:
                    prev_result = cur.execute(f"""SELECT result_num FROM results_num
                                                WHERE result_word =(
                                                SELECT result FROM players
                                                WHERE login = '{self.name_label.text()}')""").fetchone()
                    new_result = cur.execute(f"""SELECT result_num FROM results_num
                                            WHERE result_word = '{self.lvl5_finar_mark_en}'""").fetchone()
                    if int(prev_result[0]) < int(new_result[0]):
                        cur.execute(f"""UPDATE players
                                SET result = '{self.lvl5_finar_mark_en}', estimation = {self.estimation}
                                WHERE login == '{self.name_label.text()}'""")
                        con.commit()
                        cur.close()
                    else:
                        cur.execute(f"""UPDATE players
                                    SET estimation = {self.estimation}
                                    WHERE login == '{self.name_label.text()}'""")
                        con.commit()
                        cur.close()

                # Подключение к БД
                con = sqlite3.connect("records.sqlite")
                # Создание курсора
                cur = con.cursor()
                # Выполнение запроса и получение всех результатов
                result = cur.execute("""SELECT * FROM players
                                        ORDER BY (
                                        SELECT result_num FROM results_num
                                        WHERE result_word = result ) DESC""").fetchall()
                for i, el in enumerate(result):
                    job = cur.execute(f"""SELECT message FROM results
                                        WHERE result = '{result[i][1]}'""").fetchone()[0]
                    el = (list(el))
                    el.append(job)
                    result[i] = el
                self.results_all_players.setRowCount(len(result))
                # Вывод результатов
                for row, item in enumerate(result):
                    for col in range(4):
                        self.results_all_players.setItem(row, col, QTableWidgetItem(str(item[col])))
                con.close()

            else:
                self.lvl5_animation_faza = 3

                self.start(6)

    def create_avatar_func(self):
        """Создать аватарку"""
        fname = QFileDialog.getOpenFileName(self, 'Выбрать аватарку', '')[0]  # выбор картинки для аватарки
        pix = QPixmap(fname)
        self.frofil_lbl.setPixmap(pix.scaled(100, 100))  # изменяем размер картинки
        self.frofil_lbl.resize(self.frofil_lbl.sizeHint())

        with open('users.csv', 'r', encoding='utf8') as f_read:  # открываем файл со всеми игроками
            lines = csv.reader(f_read, delimiter=';', quotechar='"')
            lines = list(lines)
            for el in lines:
                if el:
                    if el[0] == self.name_label.text():
                        try:  # если установлена аватарка для этого игрока
                            lines[lines.index(el)][2] = fname  # изменяем путь к файлу
                        except IndexError:
                            lines[lines.index(el)].append(fname)  # добавляем путь к файлу
                        break

        with open('users.csv', 'w', encoding='utf8', newline='') as f_write:  # переписываем содержание файла с игроками
            writer = csv.writer(f_write, delimiter=';', quotechar='"')
            for el in lines:
                writer.writerow(el)

    def estimation_btn_clicked(self, obj):
        """Нажата одна из пяти кнопок оценки качества игры"""
        self.estimation = int(obj.text())  # сохраняем оценку
        self.go_estimation_block = False  # всё, больше не двигаем блок оценивания

    def lvl5_estimation_block(self):
        """Передвигаем блок оценивания качества игры"""
        if self.go_estimation_block:  # если можно двигать вниз
            if self.rect_btn1.y() < 200:  # если ещё не додвинулся до конца
                # двигаем всё вот это
                self.rect_btn1.move(self.rect_btn1.x(), self.rect_btn1.y() + 15)
                self.rect_btn2.move(self.rect_btn2.x(), self.rect_btn2.y() + 15)
                self.rect_btn3.move(self.rect_btn3.x(), self.rect_btn3.y() + 15)
                self.rect_btn4.move(self.rect_btn4.x(), self.rect_btn4.y() + 15)
                self.rect_btn5.move(self.rect_btn5.x(), self.rect_btn5.y() + 15)
                self.react_label.move(self.react_label.x(), self.react_label.y() + 15)
                self.rate_label.move(self.rate_label.x(), self.rate_label.y() + 15)
            else:  # если додвинулся до конца
                # переносим всё на передний план
                self.react_label.raise_()
                self.rate_label.raise_()
                self.rect_btn5.raise_()
                self.rect_btn4.raise_()
                self.rect_btn3.raise_()
                self.rect_btn2.raise_()
                self.rect_btn1.raise_()
                self.estimation_block_is_moved = True  # блок додвинулся
        elif self.estimation_block_is_moved:  # иначе, если блок додвинулся до конца
            if self.rect_btn1.y() > -80:  # если он ещё не скрылся
                # двигаем наверх
                self.rect_btn1.move(self.rect_btn1.x(), self.rect_btn1.y() - 15)
                self.rect_btn2.move(self.rect_btn2.x(), self.rect_btn2.y() - 15)
                self.rect_btn3.move(self.rect_btn3.x(), self.rect_btn3.y() - 15)
                self.rect_btn4.move(self.rect_btn4.x(), self.rect_btn4.y() - 15)
                self.rect_btn5.move(self.rect_btn5.x(), self.rect_btn5.y() - 15)
                self.react_label.move(self.react_label.x(), self.react_label.y() - 15)
                self.rate_label.move(self.rate_label.x(), self.rate_label.y() - 15)
            else:  # если он скрылся
                self.estimation_block_is_moved = False  # он скрылся
                self.estimation_block_is_moved_again = True  # он передвинулся снова
        if self.estimation_block_is_moved_again:  # если он передвинулся снова
            self.estimation_block_is_moved_again = False  # теперь он не передвинулся снова
            self.start(5)  # ставим уровень 5

    def top_players(self):
        con = sqlite3.connect("records.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute("""SELECT * FROM players
                                ORDER BY (
                                SELECT result_num FROM results_num
                                WHERE result_word = result ) DESC""").fetchall()
        for i, el in enumerate(result):
            job = cur.execute(f"""SELECT message FROM results
                                WHERE result = '{result[i][1]}'""").fetchone()[0]
            el = (list(el))
            el.append(job)
            result[i] = el

        self.results_all_players.setRowCount(len(result))
        # Вывод результатов
        for row, item in enumerate(result):
            for col in range(4):
                self.results_all_players.setItem(row, col, QTableWidgetItem(str(item[col])))
        con.close()
        update_wind(self.main_wind, self.level6_wind)

    def lvl4_animation_timer(self):
        """Анимация сундуков на 4 уровне"""
        # если настал 4 уровень и немного подождали время завершения перехода
        if self.level == 4 and time.time() - self.lvl3_to_lvl4_trans_time > 6:
            if self.animation_faza == 1:  # если первая фаза
                if self.lvl4_chest1_btn.x() > 240:  # пока 1 сундук ещё не переместился куда надо
                    # двигаем всё вот это
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 5, self.lvl4_chest1_btn.y() - 10)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 5, self.lvl4_chest2_btn.y() - 10)

                elif self.lvl4_chest3_btn.x() > 240:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 5, self.lvl4_chest3_btn.y() - 3)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 5, self.lvl4_chest4_btn.y() - 3)

                elif self.lvl4_chest5_btn.x() > 240:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 5, self.lvl4_chest5_btn.y() + 4)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 5, self.lvl4_chest6_btn.y() + 4)

                elif self.lvl4_chest7_btn.x() > 240:
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 5, self.lvl4_chest7_btn.y() + 11)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 5, self.lvl4_chest8_btn.y() + 11)

                else:
                    self.angle = 0
                    self.animation_faza = 1.5  # ставим новую фазу
                    self.tmr_lvl4_chests_animation.start(200)
                    self.correct_chest = random.choice(  # выбираем правильный сундук
                        [self.lvl4_chest1_btn, self.lvl4_chest2_btn, self.lvl4_chest3_btn,
                         self.lvl4_chest4_btn, self.lvl4_chest5_btn, self.lvl4_chest6_btn,
                         self.lvl4_chest7_btn, self.lvl4_chest8_btn])

            if self.animation_faza == 1.5:
                if self.showing_corr_chest_count % 2 == 0:
                    self.correct_chest.setStyleSheet("""background-color: green;""")
                else:
                    self.correct_chest.setStyleSheet("""background-color: light gray;""")
                self.showing_corr_chest_count += 1
                if self.showing_corr_chest_count == 8:
                    self.animation_faza = 2
                    self.tmr_lvl4_chests_animation.start(16)

            if self.animation_faza == 2:
                if self.lvl4_chest6_btn.y() < 450:
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() + 10)
                if self.lvl4_chest8_btn.x() > 250:
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 11, self.lvl4_chest8_btn.y())

                if self.lvl4_chest3_btn.x() < 290 and self.first_harf_animation:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() - 7)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y() + 7)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y() - 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() + 7)

                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 2)
                else:
                    self.first_harf_animation = False

                if self.lvl4_chest3_btn.x() > 240 and not self.first_harf_animation:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y() - 7)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y() + 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() - 7)

                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 2)

                if self.lvl4_chest7_btn.x() < 440:
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() - 7)
                else:
                    self.lvl4_chest8_btn.move(240, self.lvl4_chest8_btn.y())
                    self.animation_faza = 3
                    self.first_harf_animation = True

            if self.animation_faza == 3:
                if self.lvl4_chest6_btn.y() > 310:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() - 10)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)

                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() - 10)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 10)

                if self.lvl4_chest8_btn.x() < 440:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y())
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y())

                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y())
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y())
                else:
                    self.animation_faza = 4

            if self.animation_faza == 4:
                if self.lvl4_chest4_btn.y() > 30:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 10)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() - 10)

                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 10)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 10)

                if self.lvl4_chest6_btn.x() > 240:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y())
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y())

                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y())
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y())
                else:
                    self.animation_faza = 5

            if self.animation_faza == 5:
                if self.lvl4_chest4_btn.y() < 170:
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 10)
                if self.lvl4_chest3_btn.x() > 240:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y())
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y() - 7)
                else:
                    self.animation_faza = 6
                    self.first_harf_animation = True

                if self.lvl4_chest1_btn.x() > 390 and self.first_harf_animation:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y() + 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 10, self.lvl4_chest8_btn.y() + 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() - 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() - 7)

                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() - 2)
                else:
                    self.first_harf_animation = False

                if self.lvl4_chest1_btn.x() < 440 and not self.first_harf_animation:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y() - 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y() - 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() + 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y() + 7)

                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 2)

            if self.animation_faza == 6:
                if self.lvl4_chest2_btn.y() < 170:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() - 10)
                if self.lvl4_chest3_btn.x() < 440:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y())
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y())
                if self.lvl4_chest1_btn.x() > 240:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y() - 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 10, self.lvl4_chest8_btn.y() - 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() + 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() + 7)

                else:
                    self.animation_faza = 7
                    self.lvl4_chest1_btn.move(240, 30)
                    self.lvl4_chest4_btn.move(440, 310)
                    self.lvl4_chest5_btn.move(240, 450)
                    self.lvl4_chest6_btn.move(440, 450)
                    self.lvl4_chest7_btn.move(240, 310)
                    self.lvl4_chest8_btn.move(240, 170)

            if self.animation_faza == 7:
                if self.lvl4_chest5_btn.y() > 170:
                    if self.lvl4_chest5_btn.y() > 310:
                        if self.lvl4_chest5_btn.y() > 380 or self.lvl4_chest5_btn.y() < 240:
                            self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 24, self.lvl4_chest5_btn.y() - 11)
                            self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 24, self.lvl4_chest6_btn.y() - 11)
                            self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 24, self.lvl4_chest4_btn.y() - 11)
                            self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 24, self.lvl4_chest7_btn.y() - 11)
                        else:
                            self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 18, self.lvl4_chest5_btn.y() - 11)
                            self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 18, self.lvl4_chest6_btn.y() - 11)
                            self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 18, self.lvl4_chest4_btn.y() - 11)
                            self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 18, self.lvl4_chest7_btn.y() - 11)
                    else:
                        if self.lvl4_chest5_btn.y() > 380 or self.lvl4_chest5_btn.y() < 240:
                            self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 24, self.lvl4_chest5_btn.y() - 11)
                            self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 24, self.lvl4_chest6_btn.y() - 11)
                            self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 24, self.lvl4_chest4_btn.y() - 11)
                            self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 24, self.lvl4_chest7_btn.y() - 11)
                        else:
                            self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 18, self.lvl4_chest5_btn.y() - 11)
                            self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 18, self.lvl4_chest6_btn.y() - 11)
                            self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 18, self.lvl4_chest4_btn.y() - 11)
                            self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 18, self.lvl4_chest7_btn.y() - 11)

                if self.lvl4_chest1_btn.y() < 310:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 10)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() + 10)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 10)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)

                else:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 6, self.lvl4_chest5_btn.y())
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 6, self.lvl4_chest6_btn.y())
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 6, self.lvl4_chest4_btn.y())
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 6, self.lvl4_chest7_btn.y())
                    self.animation_faza = 8

            if self.animation_faza == 8:
                if self.lvl4_chest7_btn.y() < 450:
                    if self.lvl4_chest7_btn.y() < 120:
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() + 20)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() + 20)
                    elif self.lvl4_chest7_btn.y() > 360:
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y() + 20)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() + 20)
                    else:
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 20)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 20)
                if self.lvl4_chest5_btn.y() > 30:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() - 5)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 5)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() - 5)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() - 5)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 5)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() - 5)
                else:
                    self.animation_faza = 9

            if self.animation_faza == 9:
                if self.lvl4_chest5_btn.x() < 440:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y())
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y())
                if self.lvl4_chest1_btn.y() > 30:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 10)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)
                if self.lvl4_chest6_btn.x() > 240:
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() + 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() - 7)

                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y() - 7)

                else:
                    self.lvl4_chest6_btn.move(240, 170)
                    self.lvl4_chest5_btn.move(440, 30)
                    self.lvl4_chest3_btn.move(440, 170)
                    self.lvl4_chest1_btn.move(240, 30)
                    self.lvl4_chest3_btn.move(240, 310)
                    self.lvl4_chest8_btn.move(440, 170)
                    self.lvl4_chest7_btn.move(440, 310)
                    self.lvl4_chest2_btn.move(440, 450)
                    self.lvl4_chest4_btn.move(240, 450)
                    self.animation_faza = 10

            if self.animation_faza == 10:
                if self.lvl4_chest7_btn.y() < 450:
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 10)
                if self.lvl4_chest2_btn.x() > 240:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y())
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() - 7)
                else:
                    self.animation_faza = 11

                if self.lvl4_chest8_btn.x() > 390 and self.first_harf_animation:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y() + 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 10, self.lvl4_chest8_btn.y() + 7)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() - 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() - 7)

                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 2)
                else:
                    self.first_harf_animation = False

                if self.lvl4_chest8_btn.x() < 440 and not self.first_harf_animation:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y() - 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y() - 7)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() + 7)

                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 2)

            if self.animation_faza == 11:
                if self.angle < 180:
                    self.angle += 6
                    t = QTransform().rotate(self.angle)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest1_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest2_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest3_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest4_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest5_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest6_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest7_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest8_btn.setIcon(QtGui.QIcon(image_rotated))
                if self.lvl4_chest1_btn.y() < 170:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 5, self.lvl4_chest1_btn.y() + 12)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 5, self.lvl4_chest5_btn.y() + 12)
                elif self.lvl4_chest1_btn.y() > 310:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 5, self.lvl4_chest1_btn.y() + 12)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 5, self.lvl4_chest5_btn.y() + 12)
                else:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 12)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 12)

                if self.lvl4_chest3_btn.y() > 240:
                    if self.lvl4_chest3_btn.y() > 275:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 6, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 6, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 6, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 6, self.lvl4_chest8_btn.y() + 5)
                    if self.lvl4_chest3_btn.y() > 240:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 4, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 4, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 4, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 4, self.lvl4_chest8_btn.y() + 5)
                elif self.lvl4_chest3_btn.y() > 170:
                    if self.lvl4_chest3_btn.y() > 205:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 6, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 6, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 6, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 6, self.lvl4_chest8_btn.y() + 5)
                    if self.lvl4_chest3_btn.y() > 170:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 4, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 4, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 4, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 4, self.lvl4_chest8_btn.y() + 5)

                if self.lvl4_chest2_btn.y() > 240:
                    if self.lvl4_chest2_btn.y() > 310:
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 6, self.lvl4_chest2_btn.y() - 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 6, self.lvl4_chest7_btn.y() - 15)
                    if 240 < self.lvl4_chest2_btn.y() <= 310:
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 4, self.lvl4_chest2_btn.y() - 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 4, self.lvl4_chest7_btn.y() - 15)
                elif self.lvl4_chest2_btn.y() > 30:
                    if self.lvl4_chest2_btn.y() > 105:
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 4, self.lvl4_chest2_btn.y() - 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 4, self.lvl4_chest7_btn.y() - 15)
                    if 30 < self.lvl4_chest2_btn.y() <= 105:
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 6, self.lvl4_chest2_btn.y() - 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 6, self.lvl4_chest7_btn.y() - 15)

                if self.lvl4_chest1_btn.y() == 450:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 5, self.lvl4_chest1_btn.y())
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 5, self.lvl4_chest5_btn.y())
                    self.lvl4_chest2_btn.move(240, 30)
                    self.lvl4_chest7_btn.move(440, 30)
                    self.animation_faza = 12

            if self.animation_faza == 12:
                if self.lvl4_chest2_btn.x() < 440:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y() + 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() + 7)

                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y() + 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 10, self.lvl4_chest8_btn.y() + 7)

                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() - 7)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y() - 7)

                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y() - 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() - 7)
                else:
                    self.animation_faza = 13
                    self.first_harf_animation = True

            if self.animation_faza == 13:
                if self.lvl4_chest5_btn.y() < 450:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 10)
                if self.lvl4_chest6_btn.x() > 240:
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() - 7)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y())
                else:
                    self.animation_faza = 14

                if self.lvl4_chest2_btn.x() > 380 and self.first_harf_animation:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y() - 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() + 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() + 7)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y() - 7)

                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() + 2)
                else:
                    self.first_harf_animation = False

                if self.lvl4_chest2_btn.x() < 440 and not self.first_harf_animation:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y() + 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() - 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y() - 7)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y() + 7)

                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() - 2)

            if self.animation_faza == 14:
                if self.lvl4_chest4_btn.y() < 450:
                    if self.lvl4_chest4_btn.y() < 135 and self.lvl4_chest4_btn.x() < 300:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() + 20)
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() + 20)
                    elif self.lvl4_chest4_btn.y() > 345 and self.lvl4_chest4_btn.x() > 240:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() + 20)
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() + 20)
                    else:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 20)
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() + 20)
                if self.lvl4_chest2_btn.y() > 30:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() - 5)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 5)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() - 5)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() - 5)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 5)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() - 5)
                else:
                    self.lvl4_chest6_btn.move(240, self.lvl4_chest6_btn.y())
                    self.lvl4_chest7_btn.move(240, self.lvl4_chest7_btn.y())
                    self.lvl4_chest5_btn.move(240, self.lvl4_chest5_btn.y())
                    self.lvl4_chest4_btn.move(240, self.lvl4_chest4_btn.y())

                    self.lvl4_chest2_btn.move(440, self.lvl4_chest2_btn.y())
                    self.lvl4_chest8_btn.move(440, self.lvl4_chest8_btn.y())
                    self.lvl4_chest1_btn.move(440, self.lvl4_chest1_btn.y())
                    self.lvl4_chest3_btn.move(440, self.lvl4_chest3_btn.y())
                    self.animation_faza = 15

            if self.animation_faza == 15:
                if self.lvl4_chest4_btn.y() > 30:
                    if self.lvl4_chest4_btn.y() > 345 and self.lvl4_chest4_btn.x() < 300:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() - 20)
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() - 20)
                    if self.lvl4_chest4_btn.y() < 135 and self.lvl4_chest4_btn.x() > 240:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() - 20)
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() - 20)
                    else:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() - 20)
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() - 20)
                if self.lvl4_chest2_btn.y() < 170:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 5)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 5)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() + 5)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 5)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 5)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 5)
                else:
                    self.lvl4_chest4_btn.move(240, 30)
                    self.lvl4_chest3_btn.move(440, 30)
                    self.animation_faza = 16

            if self.animation_faza == 16:
                if self.lvl4_chest4_btn.x() < 440:
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() + 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() + 7)

                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y() + 7)

                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() - 7)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y() - 7)

                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 10, self.lvl4_chest8_btn.y() - 7)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y() - 7)
                else:
                    self.animation_faza = 17

            if self.animation_faza == 17:
                if self.lvl4_chest1_btn.y() > 30:
                    if self.lvl4_chest1_btn.y() > 345 and self.lvl4_chest1_btn.x() < 300:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y() - 20)
                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() - 20)
                    if self.lvl4_chest1_btn.y() < 135 and self.lvl4_chest1_btn.x() > 240:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y() - 20)
                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() - 20)
                    else:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 20)
                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() - 20)
                if self.lvl4_chest2_btn.y() < 170:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 5)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() + 5)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 5)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 5)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 5)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 5)
                else:
                    self.animation_faza = 18
                    self.first_harf_animation = True

            if self.animation_faza == 18:
                if self.lvl4_chest6_btn.y() < 170:
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() + 10)
                if self.lvl4_chest2_btn.x() < 290 and self.first_harf_animation:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y() + 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() - 7)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y() - 7)

                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 2)
                else:
                    self.first_harf_animation = False

                if self.lvl4_chest2_btn.x() > 240 and not self.first_harf_animation:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y() - 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() + 7)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() - 7)
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y() + 7)

                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 2)

                if self.lvl4_chest1_btn.x() < 440:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y())
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y() - 7)

                else:
                    self.first_harf_animation = True
                    self.animation_faza = 19

            if self.animation_faza == 19:
                if self.lvl4_chest7_btn.x() < 440:
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y())
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y())
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y())
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y())

                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y())
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y())
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y())
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y())
                else:
                    self.animation_faza = 20

            if self.animation_faza == 20:
                if self.angle < 360:
                    self.angle += 6
                    t = QTransform().rotate(self.angle)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest1_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest2_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest3_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest4_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest5_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest6_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest7_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest8_btn.setIcon(QtGui.QIcon(image_rotated))

                if self.lvl4_chest5_btn.y() > 310:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 5, self.lvl4_chest5_btn.y() - 12)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 5, self.lvl4_chest8_btn.y() - 12)
                elif self.lvl4_chest5_btn.y() < 170:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 5, self.lvl4_chest5_btn.y() - 12)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 5, self.lvl4_chest8_btn.y() - 12)
                else:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() - 12)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 12)

                if self.lvl4_chest3_btn.y() > 240:
                    if self.lvl4_chest3_btn.y() > 275:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 6, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 6, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 6, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 6, self.lvl4_chest2_btn.y() + 5)
                    if self.lvl4_chest3_btn.y() > 240:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 4, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 4, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 4, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 4, self.lvl4_chest2_btn.y() + 5)
                elif self.lvl4_chest3_btn.y() > 170:
                    if self.lvl4_chest3_btn.y() > 205:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 6, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 6, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 6, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 6, self.lvl4_chest2_btn.y() + 5)
                    if self.lvl4_chest3_btn.y() > 170:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 4, self.lvl4_chest3_btn.y() - 5)
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 4, self.lvl4_chest4_btn.y() - 5)

                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 4, self.lvl4_chest6_btn.y() + 5)
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 4, self.lvl4_chest2_btn.y() + 5)

                if self.lvl4_chest1_btn.y() < 240:
                    if self.lvl4_chest1_btn.y() < 100:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 6, self.lvl4_chest1_btn.y() + 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 6, self.lvl4_chest7_btn.y() + 15)
                    if 100 < self.lvl4_chest1_btn.y() <= 240:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 4, self.lvl4_chest1_btn.y() + 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 4, self.lvl4_chest7_btn.y() + 15)
                elif self.lvl4_chest1_btn.y() < 450:
                    if self.lvl4_chest1_btn.y() < 380:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 4, self.lvl4_chest1_btn.y() + 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 4, self.lvl4_chest7_btn.y() + 15)
                    if 380 < self.lvl4_chest1_btn.y() <= 450:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 6, self.lvl4_chest1_btn.y() + 15)
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 6, self.lvl4_chest7_btn.y() + 15)

                if self.lvl4_chest5_btn.y() == 30:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 5, self.lvl4_chest5_btn.y())
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 5, self.lvl4_chest8_btn.y())
                    self.lvl4_chest7_btn.move(240, 450)
                    self.lvl4_chest1_btn.move(440, 450)
                    self.animation_faza = 21
                    self.angle = 0

            if self.animation_faza == 21:
                if self.lvl4_chest4_btn.y() > 30:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() - 10)

                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 10)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() - 10)

                if self.lvl4_chest6_btn.x() < 440:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() + 10, self.lvl4_chest5_btn.y())
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y())

                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y())
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y())
                else:
                    self.animation_faza = 22

            if self.animation_faza == 22:
                if self.lvl4_chest6_btn.y() < 450:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 10)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 10)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() + 10)

                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 10)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() - 10)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() - 10)

                if self.lvl4_chest4_btn.x() < 440:
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y())
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() - 10, self.lvl4_chest2_btn.y())
                else:
                    self.animation_faza = 23

            if self.animation_faza == 23:
                if self.lvl4_chest3_btn.x() < 440:
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y() + 7)

                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() - 10, self.lvl4_chest8_btn.y() + 7)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() + 7)

                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() - 7)
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 10, self.lvl4_chest2_btn.y() - 7)

                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 10, self.lvl4_chest5_btn.y() - 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() - 7)
                else:
                    self.animation_faza = 24

            if self.animation_faza == 24:
                if self.lvl4_chest2_btn.y() < 450:
                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)
                if self.lvl4_chest4_btn.x() < 290 and self.first_harf_animation:
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() + 10, self.lvl4_chest4_btn.y() - 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y() + 7)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y() + 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y() - 7)

                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 2)
                else:
                    self.first_harf_animation = False

                if self.lvl4_chest4_btn.x() > 240 and not self.first_harf_animation:
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 10, self.lvl4_chest4_btn.y() + 7)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() + 10, self.lvl4_chest7_btn.y() - 7)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y() - 7)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y() + 7)

                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() - 2)

                if self.lvl4_chest1_btn.x() > 240:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() - 10, self.lvl4_chest1_btn.y())
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 10, self.lvl4_chest8_btn.y() - 7)

                else:
                    self.first_harf_animation = True
                    self.animation_faza = 25

            if self.animation_faza == 25:
                if self.lvl4_chest6_btn.y() < 450:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 10)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 10)
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() + 10)

                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() - 10)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 10)
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() - 10)

                if self.lvl4_chest7_btn.x() > 240:
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 10, self.lvl4_chest1_btn.y())
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 10, self.lvl4_chest7_btn.y())
                else:
                    self.animation_faza = 26

            if self.animation_faza == 26:
                if self.lvl4_chest4_btn.y() < 450:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 10)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 10)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 10)

                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() - 10)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 10)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 10)

                if self.lvl4_chest3_btn.x() > 240:
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 10, self.lvl4_chest6_btn.y())
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 10, self.lvl4_chest3_btn.y())
                else:
                    self.animation_faza = 27

            if self.animation_faza == 27:
                if self.lvl4_chest4_btn.y() > 310:
                    self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() - 10)
                    self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() - 10)
                    self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() - 10)

                    self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() + 10)
                    self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() + 10)
                    self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() + 10)

                if self.lvl4_chest3_btn.x() < 440:
                    self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() - 10, self.lvl4_chest6_btn.y())
                    self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() + 10, self.lvl4_chest3_btn.y())
                else:
                    self.animation_faza = 28
                    self.tmr_lvl4_chests_animation.start(1)

            if self.animation_faza == 28:
                self.angle += 4
                if self.angle <= 360:
                    t = QTransform().rotate(self.angle)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest3_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest3_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                else:
                    self.lvl4_chest3_btn.setStyleSheet("background-color: #e62565")
                if self.angle > 320 and self.angle - 320 <= 360:
                    t = QTransform().rotate(self.angle - 320)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest8_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest8_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 320:
                    self.lvl4_chest8_btn.setStyleSheet("background-color: #cc0605")
                if self.angle > 680 and self.angle - 680 <= 360:
                    t = QTransform().rotate(self.angle - 680)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest7_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest7_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 680:
                    self.lvl4_chest7_btn.setStyleSheet("background-color: #3333ff")
                if self.angle > 1060 and self.angle - 1060 <= 360:
                    t = QTransform().rotate(self.angle - 1060)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest2_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest2_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 1060:
                    self.lvl4_chest2_btn.setStyleSheet("background-color: #32cd32")
                if self.angle > 1380 and self.angle - 1380 <= 360:
                    t = QTransform().rotate(self.angle - 1380)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest5_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest5_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 1380:
                    self.lvl4_chest5_btn.setStyleSheet("background-color: #013220")
                if self.angle > 1760 and self.angle - 1760 <= 360:
                    t = QTransform().rotate(self.angle - 1760)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest1_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest1_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 1760:
                    self.lvl4_chest1_btn.setStyleSheet("background-color: #52cbe3")
                if self.angle > 2100 and self.angle - 2100 <= 360:
                    t = QTransform().rotate(self.angle - 2100)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest4_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest4_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 2100:
                    self.lvl4_chest4_btn.setStyleSheet("background-color: #b8860b")
                if self.angle > 2420 and self.angle - 2420 <= 360:
                    t = QTransform().rotate(self.angle - 2420)
                    pix = QPixmap('chest_images/chest1.png').transformed(t)
                    image_rotated = '%s_rotated.png' % (os.path.splitext('chest_images/chest1.png')[0])
                    pix.save(image_rotated)
                    self.lvl4_chest6_btn.setIcon(QtGui.QIcon(image_rotated))
                    self.lvl4_chest6_btn.setStyleSheet(
                        f"background-color: {random.choice(['#e62565', '#cc0605', '#3333ff', '#32cd32', '#013220', '#52cbe3', '#b8860b', '#991199'])}")
                elif self.angle > 2420:
                    self.lvl4_chest6_btn.setStyleSheet("background-color: #991199")

                if self.angle - 2420 > 360 and not self.chest_is_opened:
                    self.tmr_lvl4_chests_animation.start(600)
                    self.chest_can_be_opened = True

                if self.first_harf_animation and random.choice([0, 1]):
                    if self.lvl4_chest5_btn.x() > 60:
                        self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x() - 2, self.lvl4_chest5_btn.y())
                    else:
                        self.first_harf_animation = False
                    if self.lvl4_chest5_btn.y() < 210:
                        self.lvl4_chest5_btn.move(self.lvl4_chest5_btn.x(), self.lvl4_chest5_btn.y() + 1)

                    if self.lvl4_chest7_btn.x() > 210:
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x() - 1, self.lvl4_chest7_btn.y())
                    if self.lvl4_chest7_btn.y() < 90:
                        self.lvl4_chest7_btn.move(self.lvl4_chest7_btn.x(), self.lvl4_chest7_btn.y() + 3)

                    if self.lvl4_chest3_btn.x() > 400:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x() - 1, self.lvl4_chest3_btn.y())
                    if self.lvl4_chest3_btn.y() < 70:
                        self.lvl4_chest3_btn.move(self.lvl4_chest3_btn.x(), self.lvl4_chest3_btn.y() + 2)

                    if self.lvl4_chest8_btn.x() < 560:
                        self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x() + 4, self.lvl4_chest8_btn.y())
                    if self.lvl4_chest8_btn.y() > 140:
                        self.lvl4_chest8_btn.move(self.lvl4_chest8_btn.x(), self.lvl4_chest8_btn.y() - 2)

                    if self.lvl4_chest2_btn.x() < 640:
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x() + 6, self.lvl4_chest2_btn.y())
                    if self.lvl4_chest2_btn.y() > 280:
                        self.lvl4_chest2_btn.move(self.lvl4_chest2_btn.x(), self.lvl4_chest2_btn.y() - 1)

                    if self.lvl4_chest1_btn.x() < 490:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x() + 1, self.lvl4_chest1_btn.y())
                    if self.lvl4_chest1_btn.y() > 380:
                        self.lvl4_chest1_btn.move(self.lvl4_chest1_btn.x(), self.lvl4_chest1_btn.y() - 2)

                    if self.lvl4_chest6_btn.x() < 310:
                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x() + 2, self.lvl4_chest6_btn.y())
                    if self.lvl4_chest6_btn.y() > 430:
                        self.lvl4_chest6_btn.move(self.lvl4_chest6_btn.x(), self.lvl4_chest6_btn.y() - 1)

                    if self.lvl4_chest4_btn.x() > 175:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x() - 1, self.lvl4_chest4_btn.y())
                    if self.lvl4_chest4_btn.y() < 330:
                        self.lvl4_chest4_btn.move(self.lvl4_chest4_btn.x(), self.lvl4_chest4_btn.y() + 2)

            if self.animation_faza == 29:
                if self.lvl4_chest5_btn.x() != 340 and self.lvl4_chest5_btn != self.correct_chest:
                    self.lvl4_chest5_btn.move(340, 230)
                elif self.lvl4_chest7_btn.x() != 340 and self.lvl4_chest7_btn != self.correct_chest:
                    self.lvl4_chest7_btn.move(340, 230)
                    self.lvl4_chest7_btn.raise_()
                elif self.lvl4_chest3_btn.x() != 340 and self.lvl4_chest3_btn != self.correct_chest:
                    self.lvl4_chest3_btn.move(340, 230)
                    self.lvl4_chest3_btn.raise_()
                elif self.lvl4_chest8_btn.x() != 340 and self.lvl4_chest8_btn != self.correct_chest:
                    self.lvl4_chest8_btn.move(340, 230)
                    self.lvl4_chest8_btn.raise_()
                elif self.lvl4_chest2_btn.x() != 340 and self.lvl4_chest2_btn != self.correct_chest:
                    self.lvl4_chest2_btn.move(340, 230)
                    self.lvl4_chest2_btn.raise_()
                elif self.lvl4_chest1_btn.x() != 340 and self.lvl4_chest1_btn != self.correct_chest:
                    self.lvl4_chest1_btn.move(340, 230)
                    self.lvl4_chest1_btn.raise_()
                elif self.lvl4_chest6_btn.x() != 340 and self.lvl4_chest6_btn != self.correct_chest:
                    self.lvl4_chest6_btn.move(340, 230)
                    self.lvl4_chest6_btn.raise_()
                elif self.lvl4_chest4_btn.x() != 340 and self.lvl4_chest4_btn != self.correct_chest:
                    self.lvl4_chest4_btn.move(340, 230)
                    self.lvl4_chest4_btn.raise_()
                else:
                    self.correct_chest.move(340, 230)
                    self.correct_chest.raise_()
                if (self.correct_chest.x(), self.correct_chest.y()) == (340, 230):
                    self.animation_faza = -1
                    self.go_estimation_block = True

    def lvl4_chest_clicked_animation_timer(self):
        """Кликнули на какой-то сундук"""
        if self.chest_can_be_opened:  # если сундук может быть открыт
            if self.go_false_chest_animation:  # если открыт неправильный сундук
                self.chest_animation_i += 1  # увеличиваем фазу анимации сундука
                try:
                    self.what_ches_opened.setIcon(QtGui.QIcon(self.chest_animation_fases[self.chest_animation_i]))
                except IndexError:  # если фазы анимации закончились
                    self.chest_animation_i = 0  # ставим первую фазу анимации
                    self.go_false_chest_animation = False  # закончили возню с анимацией неправильного сундука
                    self.animation_faza = 29  # ставим финальную фазу анимации 8 сундуков
                    self.chest_can_be_opened = False  # больше сундуки нельзя открывать

            elif self.go_corr_chest_animation:  # если открыт правильный сундук
                self.chest_animation_i += 1
                try:
                    self.correct_chest.setIcon(QtGui.QIcon(self.chest_animation_fases[self.chest_animation_i]))
                except IndexError:
                    self.chest_animation_i = 0
                    self.go_corr_chest_animation = False
                    self.animation_faza = 29
                    self.chest_can_be_opened = False

    def move_showlabel_timer(self):
        """Отвечает за перемещение надписи на 1 уровне"""
        if self.move_lvl1_label and self.level1_timeshow_label.y() < 50:  # если можно двигать, кнопка была нажата
            # двигаем по y до 50
            self.level1_timeshow_label.move(self.level1_timeshow_label.x(), self.level1_timeshow_label.y() + 10)

    def show_text_level2_btn_timer(self):
        """Отвечает за текст времени на кнопке 2-го уровня"""
        if self.level == 2:  # если второй уровень
            if not self.is_lvl2_btn1_clicked:  # и ещё на кнопку 1 не кликнули
                # изначально на кнопке сколько-то очков, с каждой миллисекундой они уменьшаются
                # если очки заканчиваются, на кнопке появляются добавочные очки.
                if not self.level2_btn_1.text().startswith('+'):  # если очки не добавочные
                    if int(self.level2_btn_1.text()) - 1 > 0:  # если при вычете очков оставшиеся не добавочные
                        self.level2_btn_1.setText(str(int(self.level2_btn_1.text()) - 1))  # изменяем кол-во очков на -1
                    else:  # если следующие очки добавочные
                        self.level2_btn_1.setText('+1')  # изменяем на +1
                else:  # если очки добавочные
                    self.level2_btn_1.setText(
                        f"+{str(int(self.level2_btn_1.text()[1:]) + 1)}")  # добавляем +1 добавочные очки

            if self.is_lvl2_btn1_clicked and not self.is_lvl2_btn2_clicked:  # если на кнопку 1 кликнули
                # и на кнопку 2 ещё не кликнули
                if not self.level2_btn_2.text().startswith('+'):
                    if int(self.level2_btn_2.text()) - 1 > 0:
                        self.level2_btn_2.setText(str(int(self.level2_btn_2.text()) - 1))
                    else:
                        self.level2_btn_2.setText('+1')
                else:
                    self.level2_btn_2.setText(
                        f"+{str(int(self.level2_btn_2.text()[1:]) + 1)}")

            if self.is_lvl2_btn2_clicked and not self.is_lvl2_btn3_clicked:
                if not self.level2_btn_3.text().startswith('+'):
                    if int(self.level2_btn_3.text()) - 1 > 0:
                        self.level2_btn_3.setText(str(int(self.level2_btn_3.text()) - 1))
                    else:
                        self.level2_btn_3.setText('+1')
                else:
                    self.level2_btn_3.setText(
                        f"+{str(int(self.level2_btn_3.text()[1:]) + 1)}")

            if self.is_lvl2_btn3_clicked and not self.is_lvl2_btn4_clicked:
                if not self.level2_btn_4.text().startswith('+'):
                    if int(self.level2_btn_4.text()) - 1 > 0:
                        self.level2_btn_4.setText(str(int(self.level2_btn_4.text()) - 1))
                    else:
                        self.level2_btn_4.setText('+1')
                else:
                    self.level2_btn_4.setText(
                        f"+{str(int(self.level2_btn_4.text()[1:]) + 1)}")

    def move_trans_blocks_timer(self):
        """Двигаем блоки перехода"""
        #  если блоки можно двигать и они ещё не додвинулись до середины
        if self.trans_move and self.trans_block1.x() < -300 and not self.logo_rotated_again:
            # двигаем блок1 по x вправо
            self.trans_block1.move(self.trans_block1.x() + 30, self.trans_block1.y())
            # двигаем блок2 по x влево
            self.trans_block2.move(self.trans_block2.x() - 30, self.trans_block2.y())

        # иначе если блок почти дошёл до середины и экрану не надо переставать дрожать и
        # прицел пока не был повёрнут второй раз
        elif self.trans_block1.x() > -360 and not self.stop_hustle and not self.logo_rotated_again:
            # в блоке for показываем, как экран дрожит
            for i in range(300):
                # двигаем экран рандомно по y и x
                self.move(self.x() + random.randint(-7, 7), self.y() + random.randint(-7, 7))
                self.move(360, 100)  # затем возвращаем его в начальное положение

                self.stop_hustle = True  # экрану надо перестать дрожать

        # если блоки можно двигать и они на середине и первый блок пока не обрезан и прицел пока не повернулся снова
        if (self.trans_move and self.trans_block1.x() >= -300 and not self.trans_block1_is_cut and
                not self.logo_rotated_again):
            self.trans_block3.show()  # показываем прицел
            self.trans_block1.resize(690, 1055)  # изменяем размер блока 1
            self.rotate_logo = True  # прицел можно поворачивать
            self.trans_block1_is_cut = True  # блок 1 обрезан

        # если прицел снова повернулся
        if self.logo_rotated_again:
            if self.trans_block1.x() == -300:  # если блоки на середине
                update_wind(self.what_to_hide, self.what_to_show)  # обновляем экран
                self.tmr_trans_blocks_1_2.start(30)  # изменяем скорость уплывания блоков
                self.trans_block1.resize(1000, 1055)  # показываем обрезанную часть блока 1
            if self.trans_block1.x() > -800:  # если блоки пока не убрались до конца
                self.trans_block1.move(self.trans_block1.x() - 11, self.trans_block1.y())  # передвигаем блок 1
                self.trans_block2.move(self.trans_block2.x() + 11, self.trans_block2.y())  # передвигаем блок 2
            else:  # если блоки убрались до конца
                self.logo_rotated_again = False
                update_wind(self.trans_wind)  # скрываем переходные штуки

    def rotate_logo_timer(self):
        """Поворот прицела"""
        if self.rotate_logo:  # если можно поворачивать прицел
            self.angle += 5  # увеличиваем градус, на который надо его поворачивать
            if self.angle >= 720:  # если уже много повернули
                self.rotate_logo = False  # хватит поворачивать
                self.logo_rotated = True  # прицел повёрнут
            # ставим картинку с повёрнутым logo.png на self.angle градусов
            self.trans_block3.setPixmap(QPixmap('images/logo.png').transformed(QTransform().rotate(self.angle)))

            if self.angle % 90 == 5:  # 1
                self.trans_block3.move(292, 193)
            elif self.angle % 90 == 10:  # 2
                self.trans_block3.move(285, 186)
            elif self.angle % 90 == 15:  # 3
                self.trans_block3.move(278, 180)
            elif self.angle % 90 == 20:  # 4
                self.trans_block3.move(274, 175)
            elif self.angle % 90 == 25:  # 5
                self.trans_block3.move(269, 171)
            elif self.angle % 90 == 30:  # 6
                self.trans_block3.move(265, 167)
            elif self.angle % 90 == 35:  # 7
                self.trans_block3.move(262, 164)
            elif self.angle % 90 == 40:  # 8
                self.trans_block3.move(261, 163)
            elif self.angle % 90 == 45:  # 9
                self.trans_block3.move(263, 163)
            elif self.angle % 90 == 50:  # 10
                self.trans_block3.move(263, 163)
            elif self.angle % 90 == 55:  # 11
                self.trans_block3.move(264, 165)
            elif self.angle % 90 == 60:  # 12
                self.trans_block3.move(266, 167)
            elif self.angle % 90 == 65:  # 13
                self.trans_block3.move(269, 171)
            elif self.angle % 90 == 70:  # 14
                self.trans_block3.move(274, 175)
            elif self.angle % 90 == 75:  # 15
                self.trans_block3.move(280, 180)
            elif self.angle % 90 == 80:  # 16
                self.trans_block3.move(284, 187)
            elif self.angle % 90 == 85:  # 17
                self.trans_block3.move(290, 193)
            elif (self.angle == 90 or self.angle == 180 or self.angle == 270 or self.angle == 360 or
                  self.angle == 450 or self.angle == 540 or self.angle == 630 or self.angle == 720):  # 18
                self.trans_block3.move(297, 199)

            self.trans_block3.resize(self.trans_block3.sizeHint())  # изменяем размер, чтобы прицел не урезался

        elif self.countdown_done:
            self.angle -= 5  # увеличиваем градус, на который надо его поворачивать
            if self.angle <= -540:  # если уже много повернули
                self.countdown_done = False  # хватит отсчитывать
                self.logo_rotated_again = True  # прицел повёрнут снова
                self.trans_block3.hide()  # скрываем прицел
            # ставим картинку с повёрнутым logo.png на self.angle градусов
            self.trans_block3.setPixmap(QPixmap('images/logo.png').transformed(QTransform().rotate(self.angle)))
            abs(self.angle)
            if self.angle % 90 == 5:  # 1
                self.trans_block3.move(292, 193)
            elif self.angle % 90 == 10:  # 2
                self.trans_block3.move(285, 186)
            elif self.angle % 90 == 15:  # 3
                self.trans_block3.move(278, 180)
            elif self.angle % 90 == 20:  # 4
                self.trans_block3.move(274, 175)
            elif self.angle % 90 == 25:  # 5
                self.trans_block3.move(269, 171)
            elif self.angle % 90 == 30:  # 6
                self.trans_block3.move(265, 167)
            elif self.angle % 90 == 35:  # 7
                self.trans_block3.move(262, 164)
            elif self.angle % 90 == 40:  # 8
                self.trans_block3.move(261, 163)
            elif self.angle % 90 == 45:  # 9
                self.trans_block3.move(263, 163)
            elif self.angle % 90 == 50:  # 10
                self.trans_block3.move(263, 163)
            elif self.angle % 90 == 55:  # 11
                self.trans_block3.move(264, 165)
            elif self.angle % 90 == 60:  # 12
                self.trans_block3.move(266, 167)
            elif self.angle % 90 == 65:  # 13
                self.trans_block3.move(269, 171)
            elif self.angle % 90 == 70:  # 14
                self.trans_block3.move(274, 175)
            elif self.angle % 90 == 75:  # 15
                self.trans_block3.move(280, 180)
            elif self.angle % 90 == 80:  # 16
                self.trans_block3.move(284, 187)
            elif self.angle % 90 == 85:  # 17
                self.trans_block3.move(290, 193)
            elif (self.angle == 90 or self.angle == 180 or self.angle == 270 or self.angle == 360 or
                  self.angle == 450 or self.angle == 540 or self.angle == 630 or self.angle == 720):  # 18
                self.trans_block3.move(297, 199)

            self.trans_block3.resize(self.trans_block3.sizeHint())  # изменяем размер, чтобы прицел не урезался

    def countdown_timer(self):
        """Обратный отсчёт в переходе"""
        if self.logo_rotated:  # если прицел был повёрнут по часовой
            self.tmr_trans_countdown.start(1000)
            self.time_ending_logo_label.show()  # показываем label для обратного отсчёта
            if int(self.time_ending_logo_label.text()) - 1 == 0:  # если обратный отсчёт скоро закончится
                self.logo_rotated = False  # хватит отсчитывать
                self.countdown_done = True  # отсчёт состоялся
                self.time_ending_logo_label.hide()
                self.angle = 0  # обнуляем градус
            # уменьшаем текст на -1
            self.time_ending_logo_label.setText(str(int(self.time_ending_logo_label.text()) - 1))
            self.time_ending_logo_label.resize(self.time_ending_logo_label.sizeHint())
            # проигрываем звук
            try:
                self.nums_and_sounds[int(self.time_ending_logo_label.text())].play()
            except KeyError:
                pass

    def move_showercolor_timer(self):
        """Двигаем показатель цвета на уровне 3"""
        if self.level == 3:  # если 3 уровень
            if self.showercolor_goes_right:  # если движется вправо
                if self.lvl3_show_color1_label.x() >= 328:  # если додвинулся до конца вправо
                    self.showercolor_goes_right = False
                self.lvl3_show_color1_label.move(self.lvl3_show_color1_label.x() + 10, self.lvl3_show_color1_label.y())
            else:  # если движется влево
                if self.lvl3_show_color1_label.x() <= -40:
                    self.showercolor_goes_right = True
                self.lvl3_show_color1_label.move(self.lvl3_show_color1_label.x() - 10, self.lvl3_show_color1_label.y())

    def start(self, level=0):
        """Начало игры"""
        # проверка какой уровень нужен
        # 1 уровень
        if level == 0:
            self.initUI()
            self.level = 1  # ставим 1 уровень
            if self.go_instructions:
                self.transition(18, self.main_wind, self.level1_wind)
                app2 = Q5Application([])
                ex2 = GoInstructions('inst_vid_lvl1.avi', 14, True)
                ex2.show()
                app2.exec_()
            else:
                self.transition(5, self.main_wind, self.level1_wind)
            self.timer_lvl1_start = time.time()  # запускаем таймер

        # 2 уровень
        elif level == 2:
            self.level = 2  # ставим 2 уровень

            if self.go_instructions:
                self.transition(13, self.level1_wind, self.level2_wind)
                app2 = Q5Application([])
                ex2 = GoInstructions('inst_vid_lvl2.avi', 10, True)
                ex2.show()
                app2.exec_()
            else:
                self.level2_btn_1.setText('140')
                self.transition(3, self.level1_wind, self.level2_wind)

        elif level == 3:
            self.level = 3  # ставим 3 уровень

            if self.go_instructions:
                self.transition(11, self.level2_wind + [self.level2_btn_2, self.level2_btn_3, self.level2_btn_4],
                                self.level3_wind)
                app2 = Q5Application([])
                ex2 = GoInstructions('inst_vid_lvl3.avi', 7, True)
                ex2.show()
                app2.exec_()
            else:
                self.transition(3, self.level2_wind + [self.level2_btn_2, self.level2_btn_3, self.level2_btn_4],
                                self.level3_wind)

        elif level == 4:

            if self.go_instructions:
                self.transition(22, self.level3_wind, self.level4_wind)
                app2 = Q5Application([])
                ex2 = GoInstructions('inst_vid_lvl4.avi', 18, True)
                ex2.show()
                app2.exec_()
            else:
                self.transition(3, self.level3_wind, self.level4_wind)

            self.level = 4
            self.lvl3_to_lvl4_trans_time = time.time()
            self.chests_animation_sound.play()

        elif level == 5:
            self.level = 5

            if sum(self.times_lvl1) / len(self.times_lvl1) <= 0.3:
                lvl1_mark = 'A+'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 0.4:
                lvl1_mark = 'A'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 0.5:
                lvl1_mark = 'B+'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 0.62:
                lvl1_mark = 'B'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 0.74:
                lvl1_mark = 'C+'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 0.86:
                lvl1_mark = 'C'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 1:
                lvl1_mark = 'D+'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 1.15:
                lvl1_mark = 'D'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 1.3:
                lvl1_mark = 'E+'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 1.48:
                lvl1_mark = 'E'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 3:
                lvl1_mark = 'F+'
            elif sum(self.times_lvl1) / len(self.times_lvl1) <= 8:
                lvl1_mark = 'F'
            else:
                lvl1_mark = 'F-'

            if sum(self.lvl2_time_list) == 0:
                lvl2_mark = 'A+'
            elif sum(self.lvl2_time_list) <= 2:
                lvl2_mark = 'A'
            elif sum(self.lvl2_time_list) <= 4:
                lvl2_mark = 'B+'
            elif sum(self.lvl2_time_list) <= 6:
                lvl2_mark = 'B'
            elif sum(self.lvl2_time_list) <= 8:
                lvl2_mark = 'C+'
            elif sum(self.lvl2_time_list) <= 10:
                lvl2_mark = 'C'
            elif sum(self.lvl2_time_list) <= 13:
                lvl2_mark = 'D+'
            elif sum(self.lvl2_time_list) <= 16:
                lvl2_mark = 'D'
            elif sum(self.lvl2_time_list) <= 20:
                lvl2_mark = 'E+'
            elif sum(self.lvl2_time_list) <= 25:
                lvl2_mark = 'E'
            elif sum(self.lvl2_time_list) <= 32:
                lvl2_mark = 'F+'
            elif sum(self.lvl2_time_list) <= 45:
                lvl2_mark = 'F'
            else:
                lvl2_mark = 'F-'

            lvl3_pre_mark_num = 0
            for el in self.tmp_showercolors:
                if el.x() in range(73, 112) or el.x() in range(128, 171):
                    lvl3_pre_mark_num += 1
                elif el.x() in range(113, 127):
                    lvl3_pre_mark_num += 0
                else:
                    lvl3_pre_mark_num += 2

            lvl3_num_and_mark = {0: 'A+',
                                 1: 'A',
                                 2: 'B+',
                                 3: 'B',
                                 4: 'C+',
                                 5: 'C',
                                 6: 'D+',
                                 7: 'E+',
                                 8: 'E',
                                 9: 'F+',
                                 10: 'F-',
                                 }
            lvl3_mark = lvl3_num_and_mark[lvl3_pre_mark_num]

            lvl4_mark = 'A+' if self.what_ches_opened == self.correct_chest else 'F-'

            self.lvl5_lvl1_mark_lbl.setText(lvl1_mark)
            self.lvl5_lvl2_mark_lbl.setText(lvl2_mark)
            self.lvl5_lvl3_mark_lbl.setText(lvl3_mark)
            self.lvl5_lvl4_mark_lbl.setText(lvl4_mark)

            final_mark_and_nums = {'A+': 0,
                                   'A': 1,
                                   'B+': 2,
                                   'B': 3,
                                   'C+': 4,
                                   'C': 5,
                                   'D+': 6,
                                   'D': 7,
                                   'E+': 8,
                                   'E': 9,
                                   'F+': 10,
                                   'F': 11,
                                   'F-': 12,
                                   }
            final_nums_and_mark = {0: 'A+',
                                   1: 'A',
                                   2: 'B+',
                                   3: 'B',
                                   4: 'C+',
                                   5: 'C',
                                   6: 'D+',
                                   7: 'D',
                                   8: 'E+',
                                   9: 'E',
                                   10: 'F+',
                                   11: 'F',
                                   12: 'F-',
                                   }

            num_marks = [final_mark_and_nums[mark] for mark in [lvl1_mark, lvl2_mark, lvl3_mark, lvl4_mark]]

            self.lvl5_finar_mark_lbl.setText(final_nums_and_mark[sum(num_marks) // 4])
            self.lvl5_finar_mark_en = final_nums_and_mark[sum(num_marks) // 4]

            self.lvl5_animation_faza = 1
            self.lvl5_bg_lbl1.show()
            self.lvl5_bg_lbl2.show()

            if self.lang == 'RU':
                ru_and_en_raitings = {
                    'A+': '5+',
                    'A': '5',
                    'B+': '4+',
                    'B': '4',
                    'C+': '3+',
                    'C': '3',
                    'D+': '2+',
                    'D': '2',
                    'E+': '1+',
                    'E': '1',
                    'F+': '0+',
                    'F': '0',
                    'F-': '0-',
                }
                self.lvl5_lvl1_mark_lbl.setText(ru_and_en_raitings[self.lvl5_lvl1_mark_lbl.text()])
                self.lvl5_lvl2_mark_lbl.setText(ru_and_en_raitings[self.lvl5_lvl2_mark_lbl.text()])
                self.lvl5_lvl3_mark_lbl.setText(ru_and_en_raitings[self.lvl5_lvl3_mark_lbl.text()])
                self.lvl5_lvl4_mark_lbl.setText(ru_and_en_raitings[self.lvl5_lvl4_mark_lbl.text()])
                self.lvl5_finar_mark_lbl.setText(ru_and_en_raitings[self.lvl5_finar_mark_lbl.text()])

        elif level == 6:
            self.level = 6
            self.transition(0, self.level5_wind + self.level4_wind, self.level6_wind)
            self.go_instructions = False

    def instructions(self):
        """Кнопка инструкций"""
        self.go_instructions = True
        for btn in [self.lang_change_btn, self.start_btn, self.name_label, self.login_btn,
                    self.caption_label, self.lang_change_btn, self.frofil_lbl, self.top_players_btn]:
            btn.show()
        for el in [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6,
                   self.label_7, self.label_8, self.label_9, self.label_10, self.label_11, self.label_12,
                   self.label_13, self.label_14, self.label_15, self.label_16]:
            el.hide()
        self.instructions_btn.move(190, 330)
        app2 = Q5Application([])
        ex2 = GoInstructions('inst_vid.avi', 17, True)
        ex2.show()
        app2.exec_()

    def lvl1_btn_clicked(self):
        """Нажата кнопка на уровне 1"""
        if self.level1_btn_clicks_count != 0:  # если нажатий не 0, не первое нажатие
            self.timer_lvl1_end = time.time()  # завершаем отсчёт времени

            time_delta = round(self.timer_lvl1_end - self.timer_lvl1_start, 2)  # интервал времени между нажатиями

            self.times_lvl1.append(time_delta)  # записываем интервал
            if time_delta <= 0.2:  # если мегабыстрое нажатие
                # изменяем цвет на красный
                self.level1_timeshow_label.setStyleSheet('color: rgb(255, 0, 0); font: 30px')
                self.megacool_sound.play()  # проигрываем мегакрутой звук
            elif time_delta <= 0.6:  # если быстрое нажатие
                # изменяем цвет на темновато-зелёный
                self.level1_timeshow_label.setStyleSheet('color: rgb(0, 170, 0); font: 30px')
                self.cool_sound.play()  # проигрываем крутой звук
            else:  # если долгое
                # изменяем цвет на коричневый
                self.level1_timeshow_label.setStyleSheet('color: rgb(68, 13, 18); font: 30px')
                self.normal_sound.play()  # проигрываем звук

            # телепортируем надпись с временем так, чтобы игрок её не видел
            self.level1_timeshow_label.move(self.width() // 2 - 20, -30)

            # изменяем текст на надписи
            self.level1_timeshow_label.setText(f"+{str(time_delta)}")

            self.move_lvl1_label = True  # надпись можно перемещать

            # добавляем текст к надписям о всех временах
            label = QLabel(f"+{str(time_delta)}", self)  # создаём метку с временем
            label.setFont(QFont('Segoe UI', 24))  # устанавливаем шрифт

            if time_delta <= 0.2:  # если мегабыстрое нажатие
                # изменяем цвет на красный
                label.setStyleSheet('color: rgb(255, 0, 0)')
            elif time_delta <= 0.6:  # если быстрое нажатие:
                # изменяем цвет на темновато-зелёный
                label.setStyleSheet('color: rgb(0, 170, 0)')
            else:  # если долгое
                # изменяем цвет на коричневый
                label.setStyleSheet('color: rgb(68, 13, 18)')

            label.move(20, self.next_timeshow_lbl_pos_y)  # перемещаем
            self.next_timeshow_lbl_pos_y += 30  # изменяем координаты следующей надписи
            label.show()  # показываем надпись
            self.lvl1_show_all_time_list.append(label)  # добавляем к остальным временам

            if self.level1_btn_clicks_count >= 19:  # если нажатий 19
                self.level1_random_btn.hide()
                self.start(2)  # то запускаем уровень 2

        # перемещаем кнопку в рандомное место на экране
        self.level1_random_btn.move(random.randint(150, 700), random.randint(150, 440))

        self.timer_lvl1_start = time.time()  # начинаем новый отсчёт

        self.level1_btn_clicks_count += 1  # счетчик нажатий увеличился

    def lvl2_btn1_clicked(self):
        """Нажата кнопка 1 на уровне 2"""
        if not self.is_lvl2_btn1_clicked:  # если пока не застопорилась кнопка
            btn_time = self.sender().text()  # замеряем время на кнопке
            if btn_time[0] == '+':  # если добавочное
                btn_time = btn_time[1:]
            btn_time = int(btn_time)
            if btn_time == 0:
                self.megacool_sound.play()
                self.level2_btn_1.setStyleSheet("""background-color: rgb(255, 0, 0);""")

            elif btn_time <= 5:
                self.cool_sound.play()
                self.level2_btn_1.setStyleSheet("""background-color: rgb(0, 170, 0);""")

            else:
                self.normal_sound.play()
                self.level2_btn_1.setStyleSheet("""background-color: rgb(68, 13, 18);""")

            self.lvl2_time_list.append(btn_time)  # сохраняем время
            self.is_lvl2_btn1_clicked = True  # застопорили
            self.tmr_level2.start(40)
            self.level2_btn_2.show()  # показываем следующую

    def lvl2_btn2_clicked(self):
        """Нажата кнопка 2 на уровне 2"""
        if self.is_lvl2_btn1_clicked and not self.is_lvl2_btn2_clicked:
            btn_time = self.sender().text()
            if btn_time[0] == '+':
                btn_time = btn_time[1:]
            btn_time = int(btn_time)
            if btn_time == 0:
                self.megacool_sound.play()
                self.level2_btn_2.setStyleSheet("""background-color: rgb(255, 0, 0);""")

            elif btn_time <= 10:
                self.cool_sound.play()
                self.level2_btn_2.setStyleSheet("""background-color: rgb(0, 170, 0);""")

            else:
                self.normal_sound.play()
                self.level2_btn_2.setStyleSheet("""background-color: rgb(68, 13, 18);""")

            self.lvl2_time_list.append(btn_time)
            self.is_lvl2_btn2_clicked = True
            self.tmr_level2.start(30)
            self.level2_btn_3.show()

    def lvl2_btn3_clicked(self):
        """Нажата кнопка 3 на уровне 2"""
        if self.is_lvl2_btn2_clicked and not self.is_lvl2_btn3_clicked:
            btn_time = self.sender().text()
            if btn_time[0] == '+':
                btn_time = btn_time[1:]
            btn_time = int(btn_time)
            if btn_time == 0:
                self.megacool_sound.play()
                self.level2_btn_3.setStyleSheet("""background-color: rgb(255, 0, 0);""")

            elif btn_time <= 10:
                self.cool_sound.play()
                self.level2_btn_3.setStyleSheet("""background-color: rgb(0, 170, 0);""")

            else:
                self.normal_sound.play()
                self.level2_btn_3.setStyleSheet("""background-color: rgb(68, 13, 18);""")

            self.lvl2_time_list.append(btn_time)
            self.is_lvl2_btn3_clicked = True
            self.tmr_level2.start(20)
            self.level2_btn_4.show()

    def lvl2_btn4_clicked(self):
        """Нажата кнопка 4 на уровне 2"""
        if self.is_lvl2_btn3_clicked and not self.is_lvl2_btn4_clicked:
            btn_time = self.sender().text()
            if btn_time[0] == '+':
                btn_time = btn_time[1:]
            btn_time = int(btn_time)
            if btn_time == 0:
                self.megacool_sound.play()
                self.level2_btn_4.setStyleSheet("""background-color: rgb(255, 0, 0);""")

            elif btn_time <= 10:
                self.cool_sound.play()
                self.level2_btn_4.setStyleSheet("""background-color: rgb(0, 170, 0);""")

            else:
                self.normal_sound.play()
                self.level2_btn_4.setStyleSheet("""background-color: rgb(68, 13, 18);""")

            self.lvl2_time_list.append(btn_time)
            self.is_lvl2_btn4_clicked = True
            self.level = 3
            self.start(3)

    def lvl3_btn_clicked(self):
        tmp_shower = QLabel(self)
        tmp_shower.setPixmap(QPixmap('images/show_color_lvl3.png').scaled(200, 100))
        tmp_shower.move(self.lvl3_show_color1_label.x(), self.lvl3_show_color1_label.y())
        tmp_shower.resize(tmp_shower.sizeHint())
        self.tmp_showercolors.append(tmp_shower)
        tmp_shower.show()

        if tmp_shower.x() in range(73, 112) or tmp_shower.x() in range(128, 171):
            self.cool_sound.play()
        elif tmp_shower.x() in range(113, 127):
            self.megacool_sound.play()
        else:
            self.normal_sound.play()

        self.lvl3_btn_clicks += 1
        self.tmr_move_showcolor.start(25 - 5 * self.lvl3_btn_clicks)

        if self.lvl3_btn_clicks < 5:
            self.lvl3_show_color1_label.move(-40, self.showercolor_poses_y[self.lvl3_btn_clicks])
        else:
            self.start(4)

    def lvl4_chest_clicked_animation(self):
        """Кликнули на сундук"""
        if self.chest_can_be_opened:  # если можно открыть
            if self.sender() == self.correct_chest:  # если открыли правильный
                self.go_corr_chest_animation = True  # проигрываем правильную анимацию
                self.opening_corr_chest_sound.play()
                self.chest_animation_fases[5] = 'chest_images/chest6_corr.png'  # изменяем последнюю фазу сундука

            else:
                self.go_false_chest_animation = True
                self.opening_false_corr_chest_sound.play()
            self.what_ches_opened = self.sender()
            self.chest_is_opened = True  # сундук открыт

    def login(self):
        """Функция логина, кнопка залогиниться нажата"""
        self.login_error_label.setText('')  # текста надписи ошибки быть не должно

        update_wind(self.main_wind, self.login_wind)  # обновляем экран

    def login_is_done(self):
        """Логин закончен, кнопка окончания логина нажата"""
        self.login_error_label.setText('')  # текста ошибки быть не должно
        with open('users.csv', 'r', encoding='utf8') as f:  # открываем файл с юзерами
            # читаем файл
            lines = csv.reader(f, delimiter=';', quotechar='"')
            lines = list(lines)
            logins = []
            for el in lines:  # получаем логины
                if el:
                    logins.append(el[0])

            all_log_passw = functools.reduce(lambda a1, b: a1 + b, lines)  # получаем всё

            if (self.name_edit.text()) in logins:  # проверка, что такой юзер зарегистрирован
                password = all_log_passw[all_log_passw.index(self.name_edit.text()) + 1]  # тут все пароли

                if (self.passw_edit.text()) == password:  # если пароли совпадают
                    # изменяем надписи юзера
                    self.name_label.setText(self.name_edit.text())
                    self.name_label.resize(self.name_label.sizeHint())

                    # обновляем экран
                    update_wind(self.login_wind, self.main_wind)

                else:  # пароль не совпадает
                    # приколюха :)
                    if self.lang == 'RU':  # если русский язык
                        errors = ['Блин! ', 'Ну вот! ', 'Нет! ', 'Погоди! ', 'Не получится! ']

                        # пишем что пароли не совпадают
                        self.login_error_label.setText(random.choice(errors) + 'Пароли не совпадают.')
                        self.login_error_label.resize(self.login_error_label.sizeHint())
                    else:
                        errors = ['Duck! ', 'Oh! ', 'No! ', 'Nice try. ', 'Waitwaitwaitwait! ']

                        # пишем что пароли не совпадают
                        self.login_error_label.setText(random.choice(errors) + 'Incorrect password.')
                        self.login_error_label.resize(self.login_error_label.sizeHint())

            else:  # такого юзера нет
                # приколюха :)
                if self.lang == 'RU':  # если русский язык
                    errors = ['Блин! ', 'Ну вот! ', 'Нет! ', 'Погоди! ', 'Не получится! ']

                    # пишем что такого юзера нет в базе данных
                    self.login_error_label.setText(random.choice(errors) + 'Такого игрока нет.')
                    self.login_error_label.resize(self.login_error_label.sizeHint())
                else:
                    errors = ['Duck! ', 'Oh! ', 'No! ', 'Nice try. ', 'Waitwaitwaitwait! ']

                    # пишем что пароли не совпадают
                    self.login_error_label.setText(random.choice(errors) + 'No player with this name.')
                    self.login_error_label.resize(self.login_error_label.sizeHint())

        with open('curr_user.txt', 'w', encoding='utf8', newline='') as f:
            f.write(self.name_label.text())

        with open('users.csv', 'r', encoding='utf8') as f_read:  # открываем файл со всеми игроками
            lines = csv.reader(f_read, delimiter=';', quotechar='"')
            lines = list(lines)
            for el in lines:
                if el:
                    if el[0] == self.name_label.text():
                        try:  # если установлена аватарка для этого игрока
                            self.frofil_lbl.setPixmap(QPixmap(el[2]).scaled(100, 100))
                        except IndexError:
                            self.frofil_lbl.setPixmap(QPixmap('images/default_avatar.png').scaled(100, 100))
                        break

    def back_to_mainwind(self):
        """Назад, на главный экран"""
        update_wind(self.login_wind + self.level6_wind, self.main_wind)

    def register(self):
        """Функция регистрации, кнопка регистрации нажата"""
        self.login_error_label.setText('')  # текста надписи ошибки быть не должно
        update_wind(self.login_wind, self.reg_wind)  # обновляем экран

    def reg_is_done(self):
        """Регистрация окончена, кнопка окончания регистрации нажата"""
        self.reg_error_label.setText('')
        with open('users.csv', 'a', encoding='utf8', newline='') as f_add, open('users.csv', 'r',
                                                                                encoding='utf8') as f_read:
            # проверка что юзер новый, что его ещё не было
            lines = csv.reader(f_read, delimiter=';', quotechar='"')
            lines = list(lines)
            logins = []
            for el in lines:  # получаем логины
                if el:
                    logins.append(el[0])
            if (self.reg_name_edit.text()) not in logins:
                # записываем нового юзера
                writer = csv.writer(f_add, delimiter=';', quotechar='"')
                writer.writerow([self.reg_name_edit.text(), self.reg_passw_edit.text()])

                # ставим имя юзера в главный экран
                self.name_label.setText(self.reg_name_edit.text())
                self.name_label.resize(self.name_label.sizeHint())

                # обновление экрана
                update_wind(self.reg_wind, self.main_wind)

            else:  # юзер старый, он есть в списке
                if self.lang == 'RU':  # если русский язык
                    # приколюха :)
                    errors = ['Блин! ', 'Ну вот! ', 'Нет! ', 'Погоди,', 'Не получится! ']

                    # пишем что такой юзер уже есть
                    self.reg_error_label.setText(random.choice(errors) + 'Такой игрок уже есть.')
                    self.reg_error_label.resize(self.reg_error_label.sizeHint())
                else:
                    # приколюха :)
                    errors = ['Duck! ', 'Oh! ', 'No! ', 'Nice try. ', 'Waitwaitwaitwait! ']

                    # пишем что такой юзер уже есть
                    self.reg_error_label.setText(random.choice(errors) + 'We already have player like this.')
                    self.reg_error_label.resize(self.reg_error_label.sizeHint())

        with open('curr_user.txt', 'w', encoding='utf8', newline='') as f:
            f.write(self.name_label.text())

        self.frofil_lbl.setPixmap(QPixmap('images/default_avatar.png').scaled(100, 100))

    def back_to_loginwind(self):
        update_wind(self.reg_wind, self.login_wind)

    def lang_changed(self):
        """Язык изменяется"""
        if self.lang == 'RU':  # если английский
            # создаём звуки для обратного отсчёта
            sound_one = QtMultimedia.QSoundEffect()
            sound_one.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/EN/one_sound.wav"))

            sound_two = QtMultimedia.QSoundEffect()
            sound_two.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/EN/two_sound.wav"))

            sound_three = QtMultimedia.QSoundEffect()
            sound_three.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/EN/three_sound.wav"))

            sound_four = QtMultimedia.QSoundEffect()
            sound_four.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/EN/four_sound.wav"))

            sound_five = QtMultimedia.QSoundEffect()
            sound_five.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/EN/five_sound.wav"))

            # словарь для цифр и звуков
            self.nums_and_sounds = {
                1: sound_one,
                2: sound_two,
                3: sound_three,
                4: sound_four,
                5: sound_five
            }
            self.lang_change_btn.setIcon(QtGui.QIcon('images/united-kingdom.png'))  # кнопка смены языка
            self.lang_change_btn.setIconSize(QtCore.QSize(95, 80))  # ставим размер кнопки смены языка
            with open('lang.txt', 'w', encoding='utf8') as f_write:
                f_write.write('EN')
            self.lang = 'EN'  # изменяем язык
            self.instructions_btn.setText('INSTRUCTIONS')
            self.start_btn.setText('START')
            self.login_btn.setText('Log In')
            self.login_done_btn.setText('READY')
            self.reg_done_btn.setText('READY')
            self.reg_btn.setText('REGISTER')
            self.who_is_label.setText(
                '                                                                       Who are you?')
            self.who_is_label_2.setText(
                '                                                                     So, who are you?')
            self.back_to_mainwind_btn.setText('BACK')
            self.back_to_loginwind_btn.setText('BACK')
            self.reg_name_edit.setText('Name here')
            self.reg_passw_edit.setText('Password here')
            self.name_edit.setText('Here name')
            self.passw_edit.setText('Here password')
            self.create_avatar.setText('Set avatar')
            self.top_players_btn.setText('TOPERS')
            self.lvl5_levels_lbl.setText('LEVELS')
            self.lvl5_raitings_lbl.setText('MARKS')
            self.lvl5_lvl1_lbl.setText('Level 1')
            self.lvl5_lvl2_lbl.setText('Level 2')
            self.lvl5_lvl3_lbl.setText('Level 3')
            self.lvl5_lvl4_lbl.setText('Level 4')
            self.lvl5_finar_rait_lbl.setText('    FINAL MARK')
            self.results_all_players.setHorizontalHeaderLabels(['LOGIN', 'RESULT', 'ESTIMATION', 'JOB'])

        else:  # если русский
            # создаём звуки для обратного отсчёта
            sound_one = QtMultimedia.QSoundEffect()
            sound_one.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/one_sound.wav"))

            sound_two = QtMultimedia.QSoundEffect()
            sound_two.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/two_sound.wav"))

            sound_three = QtMultimedia.QSoundEffect()
            sound_three.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/three_sound.wav"))

            sound_four = QtMultimedia.QSoundEffect()
            sound_four.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/four_sound.wav"))

            sound_five = QtMultimedia.QSoundEffect()
            sound_five.setSource(QtCore.QUrl.fromLocalFile("countdown_sounds/RU/five_sound.wav"))

            # словарь для цифр и звуков
            self.nums_and_sounds = {
                1: sound_one,
                2: sound_two,
                3: sound_three,
                4: sound_four,
                5: sound_five
            }
            self.lang_change_btn.setIcon(QtGui.QIcon('images/russia.png'))  # кнопка смены языка
            self.lang_change_btn.setIconSize(QtCore.QSize(100, 100))  # ставим размер кнопки смены языка
            with open('lang.txt', 'w', encoding='utf8') as f_write:
                f_write.write('RU')
            self.lang = 'RU'  # изменяем язык
            self.instructions_btn.setText('ИНСТРУКЦИЯ')
            self.start_btn.setText('СТАРТ')
            self.login_btn.setText('Войти')
            self.login_done_btn.setText('Готово!')
            self.reg_done_btn.setText('Готово!')
            self.reg_btn.setText('Зарегистрироваться')
            self.who_is_label.setText(
                '                                                                           Кто ты?')
            self.who_is_label_2.setText(
                '                                                                      Так кто же ты?')
            self.back_to_mainwind_btn.setText('НАЗАД')
            self.back_to_loginwind_btn.setText('НАЗАД')
            self.reg_name_edit.setText('Тут имя')
            self.reg_passw_edit.setText('Сюда пароль')
            self.name_edit.setText('Тут имя')
            self.passw_edit.setText('Сюда пароль')
            self.create_avatar.setText('Установить аватарку')
            self.top_players_btn.setText('ЛИДЕРЫ')
            self.lvl5_levels_lbl.setText('УРОВНИ')
            self.lvl5_raitings_lbl.setText('ОЦЕНКИ')
            self.lvl5_lvl1_lbl.setText('Уровень 1')
            self.lvl5_lvl2_lbl.setText('Уровень 2')
            self.lvl5_lvl3_lbl.setText('Уровень 3')
            self.lvl5_lvl4_lbl.setText('Уровень 4')
            self.lvl5_finar_rait_lbl.setText('ФИНАЛЬНАЯ ОЦЕНКА')
            self.results_all_players.setHorizontalHeaderLabels(['ЛОГИН', 'РЕЗУЛЬТАТ', 'ОЦЕНКА', 'ПРОФЕССИЯ'])

    def transition(self, secs: int, what_to_hide, what_to_show):
        """Переход между уровнями, указываем секунды"""
        # устанавливаем, сколько секунд будет длиться обратный отсчёт
        self.time_ending_logo_label.setText(str(secs + 1))

        self.trans_block1.show()  # показываем блок 1
        self.trans_block2.show()  # показываем блок 2
        self.trans_block2.raise_()  # перемещаем блок2 на передний план
        self.trans_block1.raise_()  # перемещаем блок1 на передний план
        self.trans_block3.raise_()  # перемещаем блок3 на передний план
        self.trans_block1.move(-780, -238)  # передвигаем блок1, чтобы игрок пока его не видел
        self.trans_block2.move(745, -210)  # передвигаем блок2, чтобы игрок пока его не видел

        self.stop_hustle = False  # экрану не надо переставать дрожать
        self.rotate_logo = False  # поворачивать прицел пока не надо
        self.logo_rotated_again = False  # прицел пока не повёрнут второй раз
        self.angle = 0  # градус, на который надо поворачивать прицел
        self.trans_block1_is_cut = False  # блок 1 пока не обрезан
        self.logo_rotated = False  # прицел пока не повёрнут
        self.countdown_done = False  # отсчёт пока не состоялся
        self.trans_move = True  # разрешаем двигать блоки

        self.what_to_hide = what_to_hide  # показываем, что надо спрятать
        self.what_to_show = what_to_show  # показываем, что надо показать


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReactMatch()
    ex.show()
    sys.exit(app.exec())
