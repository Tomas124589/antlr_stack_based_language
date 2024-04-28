import unittest
from pathlib import Path

from main import main


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).parent.parent

    def example_test(self, source_code_path: str, ground_truth_path: str):
        main(self.base_dir / source_code_path)

        with open(self.base_dir / ground_truth_path, 'r') as file:
            example_lines = [line.strip() for line in file]

        with open(self.base_dir / 'bytecode.txt', 'r') as file:
            byte_code_lines = [line.strip() for line in file]

        for i, example_line in enumerate(example_lines):
            try:
                self.assertEqual(example_line, byte_code_lines[i], 'Line {}'.format(i))
            except IndexError:
                self.assertEqual(True, False, 'Line {}'.format(i))

    def test_example01(self):
        self.example_test('examples/example01.txt', 'examples/example01_result.txt')

    def test_example02(self):
        self.example_test('examples/example02.txt', 'examples/example02_result.txt')

    def test_example03(self):
        self.example_test('examples/example03.txt', 'examples/example03_result.txt')


if __name__ == '__main__':
    unittest.main()
