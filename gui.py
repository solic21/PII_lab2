
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QDoubleSpinBox, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon

import model
import t2_mandani_inference

class MyWindow(QWidget):
    def __init__(self):
        def __add_slider_and_spin_box(layout, label_text, interval):
            v_min, v_max, v_step = interval

            label = QLabel(label_text)

            slider = QSlider()
            slider.setOrientation(1)  
            slider.setMinimum(0)
            slider.setMaximum((v_max-v_min)/v_step)

            spin_box = QDoubleSpinBox()  
            spin_box.setMinimum(v_min)
            spin_box.setMaximum(v_max)
            slider.setSingleStep(v_step)

            # Callbach function on value changed
            slider.valueChanged.connect(lambda value: spin_box.setValue(round(value*v_step+v_min,2)))
            spin_box.valueChanged.connect(lambda value: slider.setValue(round((value-v_min)/v_step)))

            layout.addWidget(label)
            layout.addWidget(slider)
            layout.addWidget(spin_box)

            return slider, spin_box
        
        super().__init__()

        # Set up the main layout
        layout = QVBoxLayout()

        # Add sliders and spin boxes
        self.slider1, self.spin_box1 = __add_slider_and_spin_box(layout, "Body Mass Index", (0, 50, 0.1))
        self.slider2, self.spin_box2 = __add_slider_and_spin_box(layout, "Blood Pressure", (0, 200, 1))
        self.slider3, self.spin_box3 = __add_slider_and_spin_box(layout, "Cholesterol Level", (0, 200, 1))
        self.slider4, self.spin_box4 = __add_slider_and_spin_box(layout, "Visual Acuity", (0, 2, 0.01))
        self.slider5, self.spin_box5 = __add_slider_and_spin_box(layout, "Sleep Duration", (0, 24, 0.5))
        self.slider6, self.spin_box6 = __add_slider_and_spin_box(layout, "Cooper Test", (0, 4000, 1))
        self.slider7, self.spin_box7 = __add_slider_and_spin_box(layout, "IQ Test", (0, 200, 1))

        # Add a button to trigger an action
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # Add an output text field
        self.output_label = QLabel("Health Level:")
        self.output_field = QLineEdit(self)
        self.output_field.setReadOnly(True)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_field)

        # Min width
        self.setMinimumWidth(300)

        # Icon
        icon_path = "icon.svg"
        self.setWindowIcon(QIcon(icon_path))

        self.setLayout(layout)


    def calculate(self):
        # Get data from input fields
        crisp = [
            self.spin_box1.value(),
            self.spin_box2.value(),
            self.spin_box3.value(),
            self.spin_box4.value(),
            self.spin_box5.value(),
            self.spin_box6.value(),
            self.spin_box7.value()
        ]

        # Processing
        result, _ = t2_mandani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisp)
        word_output = result[1]
        self.output_field.setText(word_output)

        # Change output fild background color
        if word_output== 'deficient':
            self.output_field.setStyleSheet("background-color: blue;")
        elif word_output== 'subaverage':
            self.output_field.setStyleSheet("background-color: green;")
        elif word_output== 'average':
            self.output_field.setStyleSheet("background-color: red;")
        else:
            self.output_field.setStyleSheet("background-color: orange;")
            
