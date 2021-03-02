# -*- coding: utf-8 -*-
# 01.02.2021, created by Egor Eremenko
import unittest
import ext_data

class test_ext_data(unittest.TestCase):
    def test_find_sound_collection_tags(self):
        result = ext_data.find_sound_collection_tags([])
        self.assertIsInstance(result, type([]))

    def test_get_new_audio(self):
        result = ext_data.get_new_audio()
        self.assertIsInstance(result, type({}))

if __name__ == '__main__':
    unittest.main()