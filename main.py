
import sys
import argparse
import unittest
from test import TestAll  

from PyQt5.QtWidgets import QApplication
from gui import MyWindow

import model
import t2_mandani_inference
import t2_plot


# Do testing of data.cvs
def run_test_suite():
    t2_mandani_inference.preprocessing(model.input_lvs, model.output_lv)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAll)
    runner = unittest.TextTestRunner()
    _ = runner.run(suite)


# GUI mode 
def run_gui():
    t2_mandani_inference.preprocessing(model.input_lvs, model.output_lv)
    
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Health Level evaluation")
    window.show()
    sys.exit(app.exec_())

# Console mode
def run_console():
    crisp = [
        1, # 1 Body Mass Index
        180, # 2 Blood Pressure
        2, # 3 Cholesterol Level
        1, # 4 Visual Acuity
        8, # 5 Sleep Duration
        100, # 6 Cooper Test
        1, # 7 IQ Test
    ]

    t2_mandani_inference.preprocessing(model.input_lvs, model.output_lv)
    result, result_fuzzy_set = t2_mandani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisp)

    print(result)

    # Draw input lvs
    #for lv in model.input_lvs: t2_plot.draw_lv(lv)
    # Draw output lvs
    #t2_plot.draw_lv(model.output_lv)
    # Draw final MF
    #t2_plot.draw_t2_fuzzy_set(model.output_lv['U'], result_fuzzy_set[0], result_fuzzy_set[1])


def main():
    parser = argparse.ArgumentParser(description='Evaluation of Health Level script')
    
    parser.add_argument('-t', '--test', action='store_true', help='Perform testing')
    parser.add_argument('-c', '--console', action='store_true', help='Console processing')

    args = parser.parse_args()

    if args.test:
        run_test_suite()
    elif args.console:
        run_console()
    else:
        run_gui()


if __name__ == '__main__':
    main()
    
