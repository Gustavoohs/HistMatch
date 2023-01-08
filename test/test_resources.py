# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'gustavoohs@gmail.com'
__date__ = '2023-01-05'
__copyright__ = 'Copyright 2023, Gustavo Ferreira'

import unittest

from qgis.PyQt.QtGui import QIcon



class histmatchDialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/histmatch/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())

if __name__ == "__main__":
    suite = unittest.makeSuite(histmatchResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)



