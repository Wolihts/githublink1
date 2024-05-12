from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from model import *

class View(QWidget):
    def __init__(self) -> None:
        """
        gui for our calculator, everything the window/app needs like geomtry to mode and even title.
        """
        super().__init__()
        self.setWindowTitle('Calculator1.0')
        self.setFixedSize(300, 500)
        self.is_standard_mode = True
        self.last_answer = "0"
        self.shape_inputs = {}
        self.last_focused_input = None
        self.layout = QVBoxLayout()
        self.ans_label = QLabel("Ans = 0")
        self.ans_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.ans_label)
        self.input_display = ClickOnlyLineEdit()
        self.input_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.input_display)
        self.setup_ModeShapes()
        self.buttons = QGridLayout()
        self.setup()
        self.layout.addLayout(self.buttons)
        self.setLayout(self.layout)
        self.update_mode()

    def setup_ModeShapes(self) -> None:
        """
        binds toggle actions and configures the selection controls
        for various shapes in shape mode
        """
        self.shape_selection = QVBoxLayout()
        self.radio_group = QButtonGroup(self)
        self.shapes = ["Circle", "Square", "Rectangle", "Triangle"]
        for shape in self.shapes:
            radio_button = QRadioButton(shape)
            toggle_lambda = lambda checked, shape=shape: self.toggle_shape(checked, shape)
            radio_button.toggled.connect(toggle_lambda)
            self.radio_group.addButton(radio_button)
            self.shape_selection.addWidget(radio_button)
            self.setup_ShapeInputs(shape)
        self.layout.addLayout(self.shape_selection)

    def setup_ShapeInputs(self, shape: str) -> None:
        """
        input fields for each shape so that to accept dimensions from user
        """
        if shape in ["Circle", "Square"]:
            input_field = ClickOnlyLineEdit()
            placeholder_text = "Enter radius" if shape == "Circle" else "Enter side length"
            input_field.setPlaceholderText(placeholder_text)
            input_field.hide()
            self.shape_inputs[shape] = (input_field,)
            self.shape_selection.addWidget(input_field)
        elif shape in ["Rectangle", "Triangle"]:
            input_fields = (ClickOnlyLineEdit(), ClickOnlyLineEdit())
            placeholders = ("Enter length", "Enter width") if shape == "Rectangle" else ("Enter base", "Enter height")
            for i, input_field in enumerate(input_fields):
                input_field.setPlaceholderText(placeholders[i])
                input_field.hide()
                self.shape_selection.addWidget(input_field)
            self.shape_inputs[shape] = input_fields

    def setup(self) -> None:
        """
        Our buttons which are basically formatted as a calculator
        mainly our buttons layout, using pyqt6
        """
        self.buttons = QGridLayout()
        self.buttons.addWidget(QPushButton('Clear'), 0, 0)
        self.buttons.addWidget(QPushButton('Mode'), 0, 1)
        self.buttons.addWidget(QPushButton('Del'), 0, 2)
        self.buttons.addWidget(QPushButton('/'), 0, 3)
        self.buttons.addWidget(QPushButton('7'), 1, 0)
        self.buttons.addWidget(QPushButton('8'), 1, 1)
        self.buttons.addWidget(QPushButton('9'), 1, 2)
        self.buttons.addWidget(QPushButton('*'), 1, 3)
        self.buttons.addWidget(QPushButton('4'), 2, 0)
        self.buttons.addWidget(QPushButton('5'), 2, 1)
        self.buttons.addWidget(QPushButton('6'), 2, 2)
        self.buttons.addWidget(QPushButton('-'), 2, 3)
        self.buttons.addWidget(QPushButton('1'), 3, 0)
        self.buttons.addWidget(QPushButton('2'), 3, 1)
        self.buttons.addWidget(QPushButton('3'), 3, 2)
        self.buttons.addWidget(QPushButton('+'), 3, 3)
        self.buttons.addWidget(QPushButton('+/-'), 4, 0)
        self.buttons.addWidget(QPushButton('0'), 4, 1)
        self.buttons.addWidget(QPushButton('.'), 4, 2)
        self.buttons.addWidget(QPushButton('='), 4, 3)
        ans_button = QPushButton('Ans')
        self.buttons.addWidget(ans_button, 5, 0, 1, 4)

        for i in range(self.buttons.count()):
            button = self.buttons.itemAt(i).widget()
            button.setFixedSize(50, 50)
            button.clicked.connect(self.handle_clicks)
        self.layout.addLayout(self.buttons)
    
    def handle_clicks(self) -> None:
        """
        Handles button clicks, performing operations based on the button's label
        Automatically clears any error message when any input is made
        Prevents operators from being added at the start of an input unless valid
        mainly exceptions
        """
        button = self.sender()
        label = button.text()
        
        if self.is_standard_mode:
            target_display = self.input_display
        else:
            selected_shape = self.radio_group.checkedButton().text() if self.radio_group.checkedButton() else None
            if selected_shape:
                inputs = self.shape_inputs[selected_shape]
                if isinstance(inputs, tuple):
                    target_display = self.last_focused_input if self.last_focused_input and self.last_focused_input.isVisible() else inputs[0]
                else:
                    target_display = inputs
            else:
                self.input_display.setText("Select a shape")
                return

        current_input = target_display.text()

        if "Error" in current_input:
            target_display.clear()

        if label == 'Clear':
            target_display.clear()
        elif label == 'Del':
            target_display.setText(target_display.text()[:-1])
        elif label == 'Mode':
            self.is_standard_mode = not self.is_standard_mode
            self.update_mode()
        elif label == '=':
            if self.is_standard_mode:
                self.calculate_result()
            else:
                self.calculate_shape()
        elif label in '0123456789':
            target_display.insert(label)
        elif label == '.':
            if current_input == '' or not current_input.endswith('.'):
                target_display.insert('.')
            elif current_input == '' or not current_input[-1].isdigit():
                target_display.insert('0.')
            else:
                target_display.insert('.')
        elif label in '+-*/':
            if current_input and (current_input[-1].isdigit() or current_input[-1] in ')'):
                target_display.insert(label)
        elif label == '+/-':
            self.toggle_sign(target_display)
        elif label == 'Ans':
            if self.last_focused_input:
                current_input = self.last_focused_input.text()
                if current_input and current_input[-1].isdigit():
                    self.last_focused_input.insert('+' + self.last_answer)
                else:
                    self.last_focused_input.insert(self.last_answer)
            else:
                self.input_display.insert(self.last_answer)

    def toggle_sign(self, target_display) -> None:
        """
        Toggles a sign of the current input if it's numeric
            
        """
        current_text = target_display.text()
        try:
            value = float(current_text)
            if value != 0:
                negated_value = str(-value)
                target_display.setText(negated_value) 
        except ValueError:
            pass

    def toggle_shape(self, checked, shape) -> None:
        """
        Toggle input fields for all the shapes
            Done so that it focuses on the field of the mode selected
        """
        if checked:
            for input_field in self.shape_inputs[shape]:
                input_field.show()
                input_field.setFocus()
            self.last_focused_input = self.shape_inputs[shape][0]
        else:
            for input_field in self.shape_inputs[shape]:
                input_field.hide()

    def update_mode(self) -> None:
        """
        Updates UI parts based on the mode, shape mode and normal mode, and refreshes mode visibility
            Example: Shape mode disables standard mode fields, Standard mode disables Shape fields
        """
        for button in self.radio_group.buttons():
            button.setVisible(not self.is_standard_mode)
        
        for shape, inputs in self.shape_inputs.items():
            if isinstance(inputs, tuple):
                for input_field in inputs:
                    is_visible = not self.is_standard_mode and button.isChecked()
                    input_field.setVisible(is_visible)
            else:
                inputs.setVisible(not self.is_standard_mode and button.isChecked())

        always_enabled_buttons = {'.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'Clear', 'Mode', 'Del', 'Ans'}
        for i in range(self.buttons.count()):
            button = self.buttons.itemAt(i).widget()
            button.setEnabled(self.is_standard_mode or button.text() in always_enabled_buttons)
        
        self.input_display.setEnabled(self.is_standard_mode)
        
    def delete_last_character(self) -> None:
        """
        Removes last character from the input display
        """
        current_text = self.input_display.text()
        modified_text = current_text[:-1]
        self.input_display.setText(modified_text)

    def calculate_result(self) -> None:
        """
        Calculate expression entered and update that answer
        """
        try:
            result = str(eval(self.input_display.text()))
            self.last_answer = result
            self.ans_label.setText(f"Ans = {result}")
            self.input_display.clear()
        except Exception as e:
            self.input_display.setText("Error")

    def calculate_shape(self) -> None:
        """
        Calculate area of selected shape
        """
        shape_function = {'Circle': circle, 'Square': square, 'Rectangle': rectangle, 'Triangle': triangle}
        selected_shape = self.radio_group.checkedButton().text() if self.radio_group.checkedButton() else None
        if selected_shape:
            inputs = self.shape_inputs[selected_shape]
            if isinstance(inputs, tuple):
                input_values = [field.text() for field in inputs]
            else:
                input_values = [inputs.text()]

            try:
                if any(float(val) <= 0 for val in input_values):
                    raise ValueError("Value must be positive")

                if selected_shape in ["Circle", "Square"]:
                    result = shape_function[selected_shape](*input_values)
                elif selected_shape in ["Rectangle", "Triangle"]:
                    result = shape_function[selected_shape](*input_values)
                self.ans_label.setText(f"Ans = {result}")
                self.last_answer = str(result)
                self.enable_answer_button(True)
                for input_field in inputs:
                    input_field.clear()
            except Exception as e:
                self.ans_label.setText("Error: " + str(e))
                self.last_answer = ""
                self.enable_answer_button(False)
                for input_field in inputs:
                    input_field.setText("Error")
        else:
            self.input_display.setText("Select a shape")
            self.enable_answer_button(False)

    def enable_answer_button(self, enable: bool) -> None:
        """
        Enable or disable the Answer button based on if there is error or not
        """
        for i in range(self.buttons.count()):
            button = self.buttons.itemAt(i).widget()
            if button.text() == 'Ans':
                button.setEnabled(enable)

class ClickOnlyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(ClickOnlyLineEdit, self).__init__(parent)
        self.setReadOnly(True)

    def keyPressEvent(self, event):
        """
        prevent keyboard input
        """
        pass

    def contextMenuEvent(self, event):
        """
        preventing right-click copy-paste operations
        """
        pass
    
    def mousePressEvent(self, event):
        """
        mainly to set focus and update last focused input in the parent
        """
        super().mousePressEvent(event)
        self.setFocus()
        if hasattr(self.parent(), 'last_focused_input'):
            self.parent().last_focused_input = self
    
   
