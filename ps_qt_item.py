import os
import sys
import time
import uuid
import re
from functools import partial
from cryptography.fernet import Fernet
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QComboBox, QLabel,
                             QFileDialog, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QMessageBox, QCheckBox, QInputDialog)
from ps_code import operate_ps

"""
作者：hilqiqi0
QQ:2310775309
"""

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        UiModeAndFileHorizontal = QHBoxLayout() 

        self.mode_ps_group() 
        UiModeAndFileHorizontal.addWidget(self.GroupboxMode)  

        self.input_output_file_path_group() 
        UiModeAndFileHorizontal.addWidget(self.GroupboxFile) 

        self.application_ps_group()
        UiModeAndFileHorizontal.addWidget(self.GroupboxApplication) 

        self.image_time()  
        self.iamge_manage()  

        self.app_set_system()  

        authorLabel = QLabel("如有问题请及时与相关人员联系，QQ：2310775309", self)

        UiAllVertical = QVBoxLayout()  
        UiAllVertical.addLayout(UiModeAndFileHorizontal)  
        UiAllVertical.addWidget(self.ImageManage)  
        UiAllVertical.addWidget(self.GroupboxSystem)  
        UiAllVertical.addWidget(authorLabel)  

        self.setLayout(UiAllVertical)  

        self.resize(1000, 800)  
        self.center() 

        self.setWindowTitle('换图/切图') 
        self.setWindowIcon(QIcon('image/tree.png'))  

        self.show()  

        self.encryption_time()  

    def get_mac_address(self):
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        return mac

    def app_encryption(self):
        self.encryption_timer.stop()
        try:
            cipher_key = b"awhPia_uJT97kMQbkv95rWsOKkHRpSoXf6azl27qoGI="
            cipher = Fernet(cipher_key)

            encryption_path = os.getcwd() + "/encryption"
            if not os.path.exists(encryption_path):  
                string_info, ok = QInputDialog.getText(self, '软件注册', '你的电脑信息：' + self.get_mac_address() + "，请与相关人员联系获取秘钥，并输入秘钥……")

                if ok:
                    if len(string_info) == 140:
                        decrypted_string_info = cipher.decrypt(string_info.encode())
                        time_string = datetime.datetime.now().strftime('%Y-%m-%d')
                        encryption_string = self.get_mac_address() + time_string + "2310775309"
                        if bytes.decode(decrypted_string_info) == encryption_string:
                            QMessageBox.about(self, '信息', "验证通过！！！")
                            self.encryption_flg = True
                            with open(encryption_path, "w") as f:
                                encryption_file = self.get_mac_address() + "2310775309"
                                encrypted_text = cipher.encrypt(encryption_file.encode())
                                f.writelines(bytes.decode(encrypted_text))
                        else:
                            QMessageBox.critical(self, '错误', "验证失效！！！", QMessageBox.Yes)
                            self.encryption_timer.start()
                    else:
                        QMessageBox.critical(self, '错误', "请输入有效秘钥！！！", QMessageBox.Yes)
                        self.encryption_timer.start()
            else:
                with open(encryption_path, "r") as f:
                    get_encrypted_text = f.readline()
                    decrypted_get_encrypted_text = cipher.decrypt(get_encrypted_text.encode())

                encryption_file = self.get_mac_address() + "2310775309"
                if bytes.decode(decrypted_get_encrypted_text) == encryption_file:
                    QMessageBox.about(self, '信息', "信息校验完成！！！")
                    self.encryption_flg = True
                    with open(encryption_path, "w") as f:
                        encrypted_text = cipher.encrypt(encryption_file.encode())
                        f.writelines(bytes.decode(encrypted_text))
                else:
                    QMessageBox.critical(self, '错误', "信息校验失败！！！", QMessageBox.Yes)
                    self.encryption_timer.start()
        except:
            QMessageBox.critical(self, '错误', "请输入有效秘钥！！！", QMessageBox.Yes)
            self.encryption_timer.start()

    def iamge_manage(self):
        self.ImageManage = QGroupBox("图片", self)  

        ImageOperateHorizontal = QHBoxLayout()  
        ImageOperate = QLabel("图片操作：共{}张".format(0), self)  
        self.ImageOperate = ImageOperate

        LeftIcon = QtGui.QIcon()
        RightIcon = QtGui.QIcon()
        CopyIcon = QtGui.QIcon()
        DeleteIcon = QtGui.QIcon()
        StartIcon = QtGui.QIcon()

        LeftIcon.addPixmap(QtGui.QPixmap("image/left_maize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        RightIcon.addPixmap(QtGui.QPixmap("image/right_maize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CopyIcon.addPixmap(QtGui.QPixmap("image/copy_mushroom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DeleteIcon.addPixmap(QtGui.QPixmap("image/delete_onion.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartIcon.addPixmap(QtGui.QPixmap("image/start_flower.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        LeftButton = QPushButton("向左移动", self)
        RightButton = QPushButton("向右移动", self)
        CopyButton = QPushButton("复制图片", self)
        DeleteButton = QPushButton("删除图片", self)
        StartButton = QPushButton("开始制作", self)

        LeftButton.setFixedHeight(50)
        RightButton.setFixedHeight(50)
        CopyButton.setFixedHeight(50)
        DeleteButton.setFixedHeight(50)
        StartButton.setFixedHeight(50)

        LeftButton.setIcon(LeftIcon)
        RightButton.setIcon(RightIcon)
        CopyButton.setIcon(CopyIcon)
        DeleteButton.setIcon(DeleteIcon)
        StartButton.setIcon(StartIcon)

        LeftButton.setIconSize(QtCore.QSize(40, 40))
        RightButton.setIconSize(QtCore.QSize(40, 40))
        CopyButton.setIconSize(QtCore.QSize(40, 40))
        DeleteButton.setIconSize(QtCore.QSize(40, 40))
        StartButton.setIconSize(QtCore.QSize(40, 40))

        LeftButton.clicked.connect(self.left_button)
        RightButton.clicked.connect(self.right_button)
        CopyButton.clicked.connect(self.copy_button)
        DeleteButton.clicked.connect(self.delete_button)
        StartButton.clicked.connect(self.start_button)

        ImageOperateHorizontal.addWidget(ImageOperate)
        ImageOperateHorizontal.addWidget(LeftButton)
        ImageOperateHorizontal.addWidget(RightButton)
        ImageOperateHorizontal.addWidget(CopyButton)
        ImageOperateHorizontal.addWidget(DeleteButton)
        ImageOperateHorizontal.addWidget(StartButton)

        self.scrollArea = QtWidgets.QScrollArea(widgetResizable=True)  
        content_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(content_widget)  
        self._lay = QtWidgets.QHBoxLayout(content_widget)  

        ImageVertical = QVBoxLayout()  
        ImageVertical.addLayout(ImageOperateHorizontal)  
        ImageVertical.addWidget(self.scrollArea)  

        self.ImageManage.setLayout(ImageVertical)  

    def call_ps(self):

        parameter_dict = {"mode_dir_path": self.ModeInputPathLineEdit.text(),
                          "images_path": self.files_it,
                          "output_dir_path": self.OutputPathLineEdit.text(),
                          "mode_tpye": self.ModeLabelCombo.currentText(),
                          "image_name": self.ImageNameCombo.currentText(),
                          "image_type": self.ImageType,
                          "replace_number": self.ReplaceImageNumber.text(),
                          "disvisible_ps": self.VisiblePhotoshop.currentText(),
                          "close_ps": self.ClosePhotoshop.currentText()}
        print("输出参数")
        print(parameter_dict)

        # ps = operate_ps(**parameter_dict)
        QMessageBox.about(self, '信息', "完成！！！")

    def start_button(self):
        message_error = ""
        message_info = ""
        if int(time.time()) > 2698211200:
            message_error = "时间到期，请联系开发者！！！"
            print(message_error)
        elif self.ModeInputPathLineEdit.text() is None or self.ModeInputPathLineEdit.text() == "":
            message_error = "模型输入文件夹不为空！！！"
            print(message_error)
        elif not os.path.exists(self.ModeInputPathLineEdit.text()):
            message_error = "模型输入文件夹不存在！！！"
            print(message_error)
        elif self.ImageInputPathLineEdit.text() is None or self.ImageInputPathLineEdit.text() == "":
            message_error = "图片输入文件夹不为空！！！"
            print(message_error)
        elif not os.path.exists(self.ImageInputPathLineEdit.text()):
            message_error = "图片输入文件夹不存在！！！"
            print(message_error)
        elif self.OutputPathLineEdit.text() is None or self.OutputPathLineEdit.text() == "":
            message_error = "输出文件夹不为空！！！"
            print(message_error)
        elif not os.path.exists(self.OutputPathLineEdit.text()):
            message_error = "输出文件夹不存在！！！"
            print(message_error)
        elif self.ModeLabelCombo.currentText() == "切图":
            message_info = "开始切图……"
            print(message_info)
        elif self.ModeLabelCombo.currentText() == "换图":
            print(self.ImageType)
            if True not in [self.ImageType[ImageTypeName] for ImageTypeName in self.ImageType]:
                message_error = "请选择输出的格式！！！"
                print(message_error)
            elif len(self.files_it) % int(self.ReplaceImageNumber.text()) == 0:
                message_info = "开始换图……"
                print(message_info)
            else:
                message_error = "替换的图片数量不是{}的倍数！！！".format(self.ReplaceImageNumber.text())
                print(message_error)

        if message_error != "":
            QMessageBox.critical(self, '错误', message_error, QMessageBox.Yes)
        elif message_info != "":
            QMessageBox.about(self, '信息', message_info)

            if self.encryption_flg:
                self.call_ps()
            else:
                QMessageBox.critical(self, '错误', "软件未校验", QMessageBox.Yes)
                self.encryption_timer.start()

    def delete_button(self):
        if len(self.image_index_dict) > 0:
            del_image_path = []
            for index in self.image_index_dict:
                del_image_path.append(self.files_it[index])

            for image_path in del_image_path:
                self.files_it.remove(image_path)

            self.image_index_dict.clear()

            self.file_flag = True 
            self._timer.start()
            self.image_index = -1 

    def copy_button(self):
        if len(self.image_index_dict) > 1:
            QMessageBox.critical(self, '错误', "请仅选择一张!!!", QMessageBox.Yes)
        if self.image_index > -1:
            self.files_it.insert(self.image_index, self.files_it[self.image_index])
            self.file_flag = True  
            self._timer.start()

    def right_button(self):
        if len(self.image_index_dict) > 1:
            QMessageBox.critical(self, '错误', "请仅选择一张!!!", QMessageBox.Yes)
        if self.image_index < len(self.files_it) - 1 and self.image_index > -1:
            self.files_it[self.image_index], self.files_it[self.image_index + 1] = self.files_it[self.image_index + 1], \
                                                                                   self.files_it[self.image_index]
            self.file_flag = True  
            self._timer.start()

            self.image_index_dict.remove(self.image_index)
            self.image_index = self.image_index + 1
            self.image_index_dict.append(self.image_index)

    def left_button(self):
        if len(self.image_index_dict) > 1:
            QMessageBox.critical(self, '错误', "请仅选择一张!!!", QMessageBox.Yes)
        if self.image_index > 0:
            self.files_it[self.image_index], self.files_it[self.image_index - 1] = self.files_it[self.image_index - 1], \
                                                                                   self.files_it[self.image_index]
            self.file_flag = True  
            self._timer.start()

            self.image_index_dict.remove(self.image_index)
            self.image_index = self.image_index - 1
            self.image_index_dict.append(self.image_index)

    def load_directory_iamge(self, file_dir):
        print(file_dir)

        # self.files_it = [os.path.join(file_dir, file).replace('\\', r'/') for file in os.listdir(file_dir)]
        alphanum_key = lambda key: int(re.sub("\D", "", key))
        try:
            self.files_it = [os.path.join(file_dir, file).replace('\\', r'/') for file in sorted(os.listdir(file_dir), key=alphanum_key)]
        except:
            self.files_it = [os.path.join(file_dir, file).replace('\\', r'/') for file in os.listdir(file_dir)]
        self.file_flag = True  
        self.image_index = -1  
        self.image_index_dict = []  
        self._timer.start()

    def image_time(self):
        self._timer = QtCore.QTimer(self, interval=1)
        self._timer.timeout.connect(self.load_image)

    def encryption_time(self):
        self.encryption_timer = QtCore.QTimer(self, interval=1)
        self.encryption_timer.timeout.connect(self.app_encryption)

        self.encryption_flg = False  
        self.encryption_timer.start()

    def load_image(self):
        if self.file_flag:
            self.file_flag = False  

            while self._lay.count():
                self._lay.layout().takeAt(0).widget().deleteLater()

            self.image_button = []  

            for index, file_path in enumerate(self.files_it):
                self.add_icon(index, file_path)

            if self.image_index > -1:
                self.image_button_select(self.image_index)

            self.ImageOperate.setText("图片操作：共{}张".format(len(self.image_button)))

        else:
            self._timer.stop()

    def add_icon(self, index, file_path):
        file = file_path

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(file), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        image_button = QPushButton(self)
        image_button.setStyleSheet("background-color:white")
        image_button.setIcon(icon)
        image_button.setIconSize(QtCore.QSize(60, 120))
        image_button.clicked.connect(partial(self.image_button_change, index))

        self.image_button.append(image_button)

        self._lay.addWidget(image_button)

    def image_button_select(self, index):
        self.image_button[index].setStyleSheet("background-color:green")

    def image_button_change(self, index):
        color = self.image_button[index].palette().button().color()
        print(color.name())

        if color.name() == "#ffffff":  # white
            self.image_button[index].setStyleSheet("background-color:green")
            self.image_index_dict.append(index)
        elif color.name() == "#008000":     # green
            self.image_button[index].setStyleSheet("background-color:white")
            self.image_index_dict.remove(index)

        print(self.image_index_dict)
        if len(self.image_index_dict) == 1:
            self.image_index = self.image_index_dict[0]
        else:
            self.image_index = -1

    def mode_ps_group(self):
        self.GroupboxMode = QGroupBox('模式选择', self)  
  
        self.ModeLabel = QLabel("功能模式", self)  
        self.ModeLabelCombo = QComboBox(self)  
        self.ModeLabelCombo.addItem("换图")  
        self.ModeLabelCombo.addItem("切图")  

        ModeLabelHorizontal = QHBoxLayout()  
        ModeLabelHorizontal.addWidget(self.ModeLabel)  
        ModeLabelHorizontal.addWidget(self.ModeLabelCombo)  

        self.ImageTypeLabe = QLabel("图片类型（换图）", self)  
        ImageTypeLabeNull1 = QLabel(" ", self)  
        ImageTypeLabeNull2 = QLabel(" ", self)  
        ImageTypeLabeNull3 = QLabel(" ", self)  

        ImageTypeVerticalNull = QVBoxLayout()
        ImageTypeVertical = QVBoxLayout()
        CheckBoxPng = QCheckBox('png', self)
        CheckBoxBmp = QCheckBox('bmp', self)
        CheckBoxJpg = QCheckBox('jpg', self)
        CheckBoxTiff = QCheckBox('tiff', self)
        self.ImageType = {}

        CheckBoxPng.stateChanged.connect(self.check_image_type)
        CheckBoxBmp.stateChanged.connect(self.check_image_type)
        CheckBoxJpg.stateChanged.connect(self.check_image_type)
        CheckBoxTiff.stateChanged.connect(self.check_image_type)

        ImageTypeVerticalNull.addWidget(self.ImageTypeLabe)
        ImageTypeVerticalNull.addWidget(ImageTypeLabeNull1)
        ImageTypeVerticalNull.addWidget(ImageTypeLabeNull2)
        ImageTypeVerticalNull.addWidget(ImageTypeLabeNull3)
        ImageTypeVertical.addWidget(CheckBoxPng)
        ImageTypeVertical.addWidget(CheckBoxBmp)
        ImageTypeVertical.addWidget(CheckBoxJpg)
        ImageTypeVertical.addWidget(CheckBoxTiff)

        ImageTypeHorizontal = QHBoxLayout()  
        ImageTypeHorizontal.addLayout(ImageTypeVerticalNull)  
        ImageTypeHorizontal.addLayout(ImageTypeVertical)  

        self.ReplaceImage = QLabel("换图数量（换图）", self)  
        onlyInt = QIntValidator()
        self.ReplaceImageNumber = QLineEdit() 
        self.ReplaceImageNumber.setValidator(onlyInt)
        self.ReplaceImageNumber.setText("1")
        self.ReplaceImageNumber.setFixedWidth(137)

        ReplaceImageHorizontal = QHBoxLayout()  
        ReplaceImageHorizontal.addWidget(self.ReplaceImage)  
        ReplaceImageHorizontal.addWidget(self.ReplaceImageNumber)  

        self.ImageNameLabel = QLabel("图片命名（换图）", self)  
        self.ImageNameCombo = QComboBox(self)  
        self.ImageNameCombo.addItem("原图片名字")  
        self.ImageNameCombo.addItem("模板+序号")  
        self.ImageNameCombo.addItem("模板+壁纸")  

        ImageNameHorizontal = QHBoxLayout()  
        ImageNameHorizontal.addWidget(self.ImageNameLabel)  
        ImageNameHorizontal.addWidget(self.ImageNameCombo)  

        ModeVertical = QVBoxLayout()  
        ModeVertical.addLayout(ModeLabelHorizontal)  
        ModeVertical.addLayout(ImageNameHorizontal) 
        ModeVertical.addLayout(ReplaceImageHorizontal)  
        ModeVertical.addLayout(ImageTypeHorizontal)  

        self.GroupboxMode.setLayout(ModeVertical)  
        self.GroupboxMode.setFixedWidth(300)

    def application_ps_group(self):

        self.ClosePhotoshopLabel = QLabel("完成后是否关闭photoshop应用", self)  
        self.ClosePhotoshop = QComboBox(self)  
        self.ClosePhotoshop.addItem("YES")  
        self.ClosePhotoshop.addItem("NO") 

        ClosePhotoshopHorizontal = QHBoxLayout()  
        ClosePhotoshopHorizontal.addWidget(self.ClosePhotoshopLabel)  
        ClosePhotoshopHorizontal.addWidget(self.ClosePhotoshop)  

        self.VisiblePhotoshopLabel = QLabel("打开photoshop应用后是否隐藏", self)  
        self.VisiblePhotoshop = QComboBox(self)  
        self.VisiblePhotoshop.addItem("YES") 
        self.VisiblePhotoshop.addItem("NO")  

        VisiblePhotoshopHorizontal = QHBoxLayout() 
        VisiblePhotoshopHorizontal.addWidget(self.VisiblePhotoshopLabel)  
        VisiblePhotoshopHorizontal.addWidget(self.VisiblePhotoshop)  

        ApplicationVertical = QVBoxLayout() 
        ApplicationVertical.addLayout(VisiblePhotoshopHorizontal) 
        ApplicationVertical.addLayout(ClosePhotoshopHorizontal)  

        self.GroupboxApplication = QGroupBox('photoshop应用选项', self)  
        self.GroupboxApplication.setLayout(ApplicationVertical) 

    def check_image_type(self, state):
        checkBox = self.sender()
        if state == QtCore.Qt.Unchecked:
            self.ImageType[checkBox.text()] = False
        elif state == QtCore.Qt.Checked:
            self.ImageType[checkBox.text()] = True

    def input_output_file_path_group(self):
        self.GroupboxFile = QGroupBox('文件', self)  

        # 模型输入
        self.ModeInputLabel = QLabel("模型输入文件夹位置", self)  
        self.ModeInputPathLineEdit = QLineEdit(self)  
        self.ModeInputButton = QPushButton("浏览", self) 
        self.ModeInputButton.clicked.connect(partial(self.file_path_msg, self.ModeInputPathLineEdit)) 

        ModeInputHorizontal = QHBoxLayout()  
        ModeInputHorizontal.addWidget(self.ModeInputLabel)  
        ModeInputHorizontal.addWidget(self.ModeInputPathLineEdit)  
        ModeInputHorizontal.addWidget(self.ModeInputButton) 

        self.ImageInputLabel = QLabel("图片输入文件夹位置", self)  
        self.ImageInputPathLineEdit = QLineEdit(self)  
        self.ImageInputButton = QPushButton("浏览", self)  
        self.ImageInputButton.clicked.connect(partial(self.file_path_image_msg, self.ImageInputPathLineEdit))  

        ImageInputHorizontal = QHBoxLayout()  
        ImageInputHorizontal.addWidget(self.ImageInputLabel)  
        ImageInputHorizontal.addWidget(self.ImageInputPathLineEdit)  
        ImageInputHorizontal.addWidget(self.ImageInputButton)  

        self.OutputLabel = QLabel("输出文件夹位置", self)  
        self.OutputPathLineEdit = QLineEdit(self)  
        self.OutputButton = QPushButton("浏览", self)  
        self.OutputButton.clicked.connect(partial(self.file_path_msg, self.OutputPathLineEdit))  

        OutputHorizontal = QHBoxLayout()  
        OutputHorizontal.addWidget(self.OutputLabel)  
        OutputHorizontal.addWidget(self.OutputPathLineEdit) 
        OutputHorizontal.addWidget(self.OutputButton)  

        FileVertical = QVBoxLayout()  
        FileVertical.addLayout(ModeInputHorizontal)  
        FileVertical.addLayout(ImageInputHorizontal)  
        FileVertical.addLayout(OutputHorizontal)  

        self.GroupboxFile.setLayout(FileVertical)  

    def file_path_msg(self, PathLabel):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  
        PathLabel.setText(directory)

    def file_path_image_msg(self, PathLabel):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  
        PathLabel.setText(directory)
        if PathLabel.text():
            self.load_directory_iamge(directory)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def app_set_system_font(self, fun):
        current_font = int(self.SystemFontnumber.text())
        if 5 < current_font < 30:
            if fun == "+":
                current_font = current_font + 1
            else:
                current_font = current_font - 1

            self.SystemFontnumber.setText(str(current_font))
            font = QFont()
            font.setPointSize(current_font)
            self.setFont(font)

    def app_set_system_font_family(self):
        print("状态：", self.SystemFontFamily.currentText())
        font = QFont()
        if self.SystemFontFamily.currentText() == "宋体":
            font.setFamily("SimSun")
        elif self.SystemFontFamily.currentText() == "黑体":
            font.setFamily("SimHei")
        elif self.SystemFontFamily.currentText() == "微软雅黑":
            font.setFamily("Microsoft Yahei")
        elif self.SystemFontFamily.currentText() == "微软正黑体":
            font.setFamily("Microsoft JhengHei")
        elif self.SystemFontFamily.currentText() == "楷体":
            font.setFamily("KaiTi")
        elif self.SystemFontFamily.currentText() == "新宋体":
            font.setFamily("NSimSun")
        elif self.SystemFontFamily.currentText() == "仿宋":
            font.setFamily("FangSong")

        self.setFont(font)

    def app_set_system_font_bold(self, state):
        font = QFont()
        if state == QtCore.Qt.Unchecked:
            font.setBold(False)
        elif state == QtCore.Qt.Checked:
            font.setBold(True)
        self.setFont(font)

    def app_set_system(self):
        self.GroupboxSystem = QGroupBox('软件设置', self)  

        SystemFontLabel = QLabel("系统字体大小：", self)  
        SystemFontButtonAdd = QPushButton("+", self)  
        self.SystemFontnumber = QLabel("10", self) 
        SystemFontButtonDec = QPushButton("-", self)  
        SystemFontButtonAdd.clicked.connect(partial(self.app_set_system_font, "+"))  
        SystemFontButtonDec.clicked.connect(partial(self.app_set_system_font, "-"))  
        SystemFontButtonAdd.setFixedWidth(30)
        SystemFontButtonDec.setFixedWidth(30)

        SystemFontHorizontal = QHBoxLayout()  
        SystemFontHorizontal.addWidget(SystemFontLabel)  
        SystemFontHorizontal.addWidget(SystemFontButtonAdd)  
        SystemFontHorizontal.addWidget(self.SystemFontnumber)  
        SystemFontHorizontal.addWidget(SystemFontButtonDec) 

        SystemFontFamilyLabel = QLabel("系统字体样式：", self)  
        self.SystemFontFamily = QComboBox(self)  
        self.SystemFontFamily.addItem("宋体")  
        self.SystemFontFamily.addItem("黑体")  
        self.SystemFontFamily.addItem("微软雅黑")  
        self.SystemFontFamily.addItem("微软正黑体") 
        self.SystemFontFamily.addItem("新宋体")  
        self.SystemFontFamily.addItem("仿宋")  
        self.SystemFontFamily.currentIndexChanged.connect(self.app_set_system_font_family)

        SystemFontFamilyHorizontal = QHBoxLayout()  
        SystemFontFamilyHorizontal.addWidget(SystemFontFamilyLabel)  
        SystemFontFamilyHorizontal.addWidget(self.SystemFontFamily)  

        SystemFontBold = QCheckBox('加粗', self)
        SystemFontBold.stateChanged.connect(self.app_set_system_font_bold)

        HideLineEdit = QLineEdit(self)  
        HideLineEdit.setStyleSheet("background:transparent;border-width:0;border-style:outset")

        SystemHorizontal = QHBoxLayout()
        SystemHorizontal.addLayout(SystemFontHorizontal)  
        SystemHorizontal.addLayout(SystemFontFamilyHorizontal)  
        SystemHorizontal.addWidget(SystemFontBold)  
        SystemHorizontal.addWidget(HideLineEdit)

        self.GroupboxSystem.setLayout(SystemHorizontal)  


if __name__ == '__main__':
    # try:
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    # except Exception as e:
    #     print(e)
    #     input()
