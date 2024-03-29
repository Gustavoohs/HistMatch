# -*- coding: utf-8 -*-
"""
/***************************************************************************
 histmatch
                                 A QGIS plugin
 Image histogram matching process
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-01-05
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Gustavo Ferreira
        email                : gustavoohs@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import *
import sys, os
from osgeo import ogr, gdal
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .hist_match_dialog import histmatchDialog
import os.path

import numpy as np


class histmatch:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'histmatch_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Histogram Matching')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('histmatch', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = 'C:/hist_match_plugin/hist_match/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Histogram Matching'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Histogram Matching'),
                action)
            self.iface.removeToolBarIcon(action)

    def load_input(self):
        self.dlg.comboBox.clear()
        list_layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        list_rasters = []
        for i in list_layers:
            if i.type() == QgsMapLayer.RasterLayer:
                list_rasters.append(i.name())
        self.dlg.comboBox.addItems(list_rasters)

    def load_input2(self):
        self.dlg.comboBox_2.clear()
        list_layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        list_rasters = []
        for i in list_layers:
            if i.type() == QgsMapLayer.RasterLayer:
                list_rasters.append(i.name())
        self.dlg.comboBox_2.addItems(list_rasters)

    def open_file(self):
        
        lyr = str(QFileDialog.getOpenFileName(caption="Image", filter="Images (*.tif)")[0])
        
        if (lyr != ""):
            self.iface.addRasterLayer(lyr, str.split(os.path.basename(lyr),".") [0],"gdal")
            self.load_input()
    
    def open_file2(self):
        
        lyr = str(QFileDialog.getOpenFileName(caption="Image", filter="Images (*.tif)")[0])
        
        if (lyr != ""):
            self.iface.addRasterLayer(lyr, str.split(os.path.basename(lyr),".") [0],"gdal")
            self.load_input2()


    def get_layer1(self):
        """Get layer in a ComboBox"""
        layer = None
        lyr_name = self.dlg.comboBox.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == lyr_name:
                layer = lyr
        return layer
        
    def get_layer2(self):
        """Get layer in a ComboBox"""
        layer = None
        lyr_name = self.dlg.comboBox_2.currentText()
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == lyr_name:
                layer = lyr
        return layer

    '''def layerAsArray(layer):
        """ read the data from a single-band layer into a numpy array"""

        gd = gdal.Open(str(layer.source()))
        array = gd.ReadAsArray()
        return array'''

    def save_result(self):
        """abre a janela de dialógo para definir o nome e o local da layer a ser gerada"""
        save = str(QFileDialog.getSaveFileName(caption="Save result.",filter="GTiff (*.tif)")[0])
        self.dlg.lineEdit.setText(save)

    def variables(self):
        """variables for run function"""
        self.layer1 = self.get_layer1()
        self.layer2 = self.get_layer2()
        self.out = self.dlg.lineEdit.text()
        

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = histmatchDialog()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        self.load_input()
        self.load_input2()
        self.dlg.toolButton.clicked.connect(self.open_file)
        self.dlg.toolButton_2.clicked.connect(self.open_file2)
        self.dlg.toolButton_3.clicked.connect(self.save_result)
        self.dlg.button_box.accepted.disconnect()
        self.dlg.button_box.accepted.connect(self.run)
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            self.variables()

            ds1 = gdal.Open(str(self.layer1.source()))
            src = ds1.ReadAsArray()

            


            ds2 = gdal.Open(str(self.layer2.source()))
            dst = ds2.ReadAsArray()
            
            src = src.swapaxes(0,2).swapaxes(0,1)
            dst = dst.swapaxes(0,2).swapaxes(0,1)

              # Get radiometric resolution
            bits = 2 ** (src.dtype.itemsize * 8)

            
            if src.dtype != dst.dtype:
                raise('The source file has a different radiometric resolution than the target!')

            if len(src.shape) == 3:
            # Create LUTs for each band of the matched image
                matched = np.zeros_like(src)
                for i in range(src.shape[-1]):
                    src_cdf = np.cumsum(np.histogram(src[...,i], bins=bits, range=(0, bits-1), density=True)[0])
                    dst_cdf = np.cumsum(np.histogram(dst[...,i], bins=bits, range=(0, bits-1), density=True)[0])
                    lut = np.interp(src_cdf, dst_cdf, np.arange(bits))

                    matched[...,i] = lut[src[...,i]]
                driver = gdal.GetDriverByName("GTiff")

                out = driver.Create(self.out, matched.shape[1], matched.shape[0], matched.shape[2], gdal.GDT_Float32)       
                for i in range(matched.shape[2]):
                    out.GetRasterBand(i + 1).WriteArray(matched[...,i])
                    out.SetGeoTransform(ds1.GetGeoTransform())
                    out.SetProjection(ds1.GetProjection())
                    out.FlushCache()           

                self.iface.addRasterLayer(self.out)
        
            # Create the LUT for the matched image
            else:
                src_cdf = np.cumsum(np.histogram(src, bins=bits, range=(0, bits-1), density=True)[0])
                dst_cdf = np.cumsum(np.histogram(dst, bins=bits, range=(0, bits-1), density=True)[0])
                lut = np.interp(src_cdf, dst_cdf, np.arange(bits))

                # Apply the LUT to the source image
                matched = lut[src]
                driver = gdal.GetDriverByName("GTiff")

                out = driver.Create(self.out, matched.shape[1], matched.shape[0], 1, gdal.GDT_Float32)

                out.SetGeoTransform(ds1.GetGeoTransform())
                out.SetProjection(ds1.GetProjection())
                out.GetRasterBand(1).WriteArray(matched)
                out.FlushCache()
                out = None

                self.iface.addRasterLayer(self.out)
            '''if len(img1.shape) == 3:
                res = np.zeros_like(img1)
                for i in range(img1.shape[2]):
                    res[:,:,i] = match_histograms(img1[:,:,i], img2[:,:,i])
            else:
                res = match_histograms(img1, img2)'''

            
            
