import unittest
from pprint import pprint
from bottles import *

class BottleTest(unittest.TestCase):
    def test_validate_bottles_right(self):
        bottles = list(map(string_to_bottle, [
            "bb  ",
            "bb  ",
        ]))
        validate_bottles(bottles)

    def test_validate_bottles_wrong(self):
        bottles = list(map(string_to_bottle, [
            "bb  ",
            "rr  ",
        ]))
        with self.assertRaises(ValueError):
            validate_bottles(bottles)

    def test_bottle_pour_1(self):
        bottles = list(map(string_to_bottle, [
            "bb  ",
            "bb  ",
        ]))
        bottle_pour(bottles[0], bottles[1])
        self.assertEqual(bottles[0], string_to_bottle('    '))
        self.assertEqual(bottles[1], string_to_bottle('bbbb'))

    def test_bottle_pour_2(self):
        bottles = list(map(string_to_bottle, [
            "b   ",
            "bb  ",
        ]))
        bottle_pour(bottles[0], bottles[1])
        self.assertEqual(bottles[0], string_to_bottle('    '))
        self.assertEqual(bottles[1], string_to_bottle('bbb '))

    def test_bottle_pour_3(self):
        bottles = list(map(string_to_bottle, [
            "rrbb",
            "bb  ",
        ]))
        bottle_pour(bottles[0], bottles[1])
        self.assertEqual(bottles[0], string_to_bottle('rr  '))
        self.assertEqual(bottles[1], string_to_bottle('bbbb'))

    def test_bottle_pour_4(self):
        bottles = list(map(string_to_bottle, [
            "rrbb",
            "rbb ",
        ]))
        bottle_pour(bottles[0], bottles[1])
        self.assertEqual(bottles[0], string_to_bottle('rrb '))
        self.assertEqual(bottles[1], string_to_bottle('rbbb'))

    def test_bottle_pour_5(self):
        bottles = list(map(string_to_bottle, [
            "rrbb",
            "rbb ",
            "yyyy",
        ]))
        bottle_pour(bottles[0], bottles[1])
        self.assertEqual(bottles[0], string_to_bottle('rrb '))
        self.assertEqual(bottles[1], string_to_bottle('rbbb'))
        self.assertEqual(bottles[2], string_to_bottle('yyyy'))

    def test_bottles_solved_right(self):
        bottles = list(map(string_to_bottle, [
            "rrrr",
            "bbbb",
            "yyyy",
        ]))
        self.assertTrue(is_solved(bottles))

    def test_bottles_solved_wrong(self):
        bottles = list(map(string_to_bottle, [
            "rrrr",
            "bbby",
            "yyyb",
        ]))
        self.assertFalse(is_solved(bottles))

    def test_turn_list_1(self):
        bottles = list(map(string_to_bottle, [
            "bb  ",
            "bb  ",
            "yyyy",
        ]))

        validate_bottles(bottles)
        candidates = list(list_available_turns(bottles))
        for candidate in candidates:
            validate_bottles(candidate)

        self.assertCountEqual(candidates, [
            [
                string_to_bottle('bbbb'),
                string_to_bottle('    '),
                string_to_bottle('yyyy'),
            ],
            [
                string_to_bottle('    '),
                string_to_bottle('bbbb'),
                string_to_bottle('yyyy'),
            ],
        ])

    def test_turn_list_2(self):
        bottles = list(map(string_to_bottle, [
            "bbr ",
            "bbrr",
            "r   ",
        ]))

        validate_bottles(bottles)
        candidates = list(list_available_turns(bottles))
        for candidate in candidates:
            validate_bottles(candidate)

        self.assertCountEqual(candidates, [
            [
                string_to_bottle('bb  '),
                string_to_bottle('bbrr'),
                string_to_bottle('rr  '),
            ],
            [
                string_to_bottle('bbrr'),
                string_to_bottle('bbr '),
                string_to_bottle('r   '),
            ],
            [
                string_to_bottle('bbr '),
                string_to_bottle('bb  '),
                string_to_bottle('rrr '),
            ],
            [
                string_to_bottle('bbrr'),
                string_to_bottle('bbrr'),
                string_to_bottle('    '),
            ],
        ])

    def test_turn_list_3(self):
        bottles = list(map(string_to_bottle, [
            "ybyb",
            "byb ",
            "y   ",
        ]))

        validate_bottles(bottles)
        candidates = list(list_available_turns(bottles))
        for candidate in candidates:
            validate_bottles(candidate)

        self.assertCountEqual(candidates, [
            [
                string_to_bottle('yby '),
                string_to_bottle('bybb'),
                string_to_bottle('y   '),
            ],
        ])

    def test_solve_no_solution(self):
        bottles = list(map(string_to_bottle, [
            "bbrr",
            "rrbb",
        ]))

        self.assertEqual(solve(bottles), None)

    def test_solve_complex(self):
        bottles = list(map(string_to_bottle, [
            "1234",
            "4526",
            "3781",
            "2979",
            "6784",
            "1237",
            "8869",
            "6493",
            "1555",
            "    ",
            "    ",
        ]))

        solution = solve(bottles)
        self.assertNotEqual(solution, None)
        self.assertEqual(solution[0], bottles)
        self.assertTrue(is_solved(solution[-1]))

        for idx in range(len(solution) - 1):
            possible_steps = list_available_turns(solution[idx])
            self.assertTrue(solution[idx+1] in possible_steps)


if __name__ == '__main__':
    unittest.main()
