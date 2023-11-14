import pandas as pd
import numpy as np
class DCM_tags:
    def  __init__(self, ds):
        self.rows = ds.Rows
        self.cols = ds.Columns
        self.window_widths = []
        self.window_centers = []
        self.voilut_func = 0
        self.invert = (ds.PhotometricInterpretation == 'MONOCHROME1')
        self.flipHorz = False
        self.flipVert = False
        self.side = None
        self.view = None
        self.setWindows(ds)
        self.setViolut(ds)
        self.setFlip(ds)
        self.setSide(ds)
        assert len(self.window_centers) == len(self.window_widths)
    def setWindows(self, ds):
        if "WindowWidth" not in ds or "WindowCenter" not in ds:
            pass
        else:
            ww = ds['WindowWidth']
            wc = ds['WindowCenter']
            self.window_widths = [float(e) for e in ww
                                  ] if ww.VM > 1 else [float(ww.value)]

            self.window_centers = [float(e) for e in wc
                                   ] if wc.VM > 1 else [float(wc.value)]
    def setViolut(self, ds):
        if hasattr(ds, 'VOILUTFunction'):
            voilut_func = str(ds.VOILUTFunction).upper()
        else:
            voilut_func = 'LINEAR'
        self.voilut_func = 1 if voilut_func == 'SIGMOID' else 0
    def setSide(self, ds):
        try:
            self.side = ds.ImageLaterality
        except AttributeError:
            try:
                self.side = ds.Laterality
            except AttributeError:
                pass
        try:
            self.view = ds.ViewPosition
        except AttributeError:
            pass    
    def setFlip(self, ds):
        laterality = None
        view = None
        orientation = [None]
        flipHorz = False
        flipVert = False
        try:
            laterality = ds.ImageLaterality
        except AttributeError:
            try:
                laterality = ds.Laterality
            except AttributeError:
                pass
        try:
            view = ds.ViewPosition
        except AttributeError:
            view = np.nan
        try:
            orientation = ds.PatientOrientation
        except AttributeError:
            orientation = np.nan
        if ~pd.isnull(orientation):
            if view == 'CC':
                if orientation[0] == 'P':
                    flipHorz = True
                else:
                    flipHorz = False
    
                if (laterality == 'L') & (orientation[1] == 'L'):
                    flipVert = True
                elif (laterality == 'R') & (orientation[1] == 'R'):
                    flipVert = True
                else:
                    flipVert = False
            elif (view == 'MLO') | (view == 'ML'):
                if orientation[0] == 'P':
                    flipHorz = True
                else:
                    flipHorz = False

                if (laterality == 'L') & ((orientation[1] == 'H') | (orientation[1] == 'HL')):
                    flipVert = True
                elif (laterality == 'R') & ((orientation[1] == 'H') | (orientation[1] == 'HR')):
                    flipVert = True
                else:
                    flipVert = False
            else:
                print(f"No matching view for current MAMMO, current view:{view}, current orientation: {orientation}")
                flipHorz = False
                flipVert = False
        else:
            # Flip RCC, RML, and RMLO images
            if (self.laterality == 'R') & ((self.view == 'CC') | (self.view == 'ML') | (self.view == 'MLO')):
                flipHorz = True
                flipVert = False
            else:
                flipHorz = False
                flipVert = False
        self.flipHorz = flipHorz
        self.flipVert = flipVert
# #get DICOM image metadata with dicomsdl
# class DCMSDL_tags:
#     def __init__(self, ds):
#         self.rows = ds.Rows
#         self.cols = ds.Columns
#         self.window_widths = []
#         self.window_centers = []
#         self.violut_func = 0
#         self.invert = (ds.PhotometricInterpretation == 'MONOCHROME1')
#         self.flipHorz = False
#         self.flipVert = False
#         self.side = None
#         self.view = None
#         self.setWindows(ds)
#         self.setViolut(ds)
#         self.setFlip(ds)
#         self.setSide(ds)
#         assert len(self.window_centers) == len(self.window_widths)
#     def setWindows(self, ds):
#         self.window_widths = ds.WindowWidth
#         self.window_centers = ds.WindowCenter
#         if self.window_widths is None or self.window_centers is None:
#             self.window_widths = []
#             self.window_centers = []
#         else:
#             try:
#                 if not isinstance(self.window_widths, list):
#                     self.window_widths = [self.window_widths]
#                 self.window_widths = [float(e) for e in self.window_widths]
#                 if not isinstance(self.window_centers, list):
#                     self.window_centers = [self.window_centers]
#                 self.window_centers = [float(e) for e in self.window_centers]
#             except:
#                 self.window_widths = []
#                 self.window_centers = []
#     def setViolut(self, ds):
#         voilut_func = ds.VOILUTFunction
#         if voilut_func is None:
#             voilut_func = 'LINEAR'
#         else:
#             voilut_func = str(self.voilut_func).upper()
#         self.voilut_func = 1 if voilut_func == 'SIGMOID' else 0
#     def setSide(self, ds):
#         try:
#             self.side = ds.ImageLaterality
#         except AttributeError:
#                 pass
#         if self.side is None:
#             try:
#                 self.side = ds.Laterality
#         try:
#             self.view = ds.ViewPosition
#         except AttributeError:
#             pass    
#     def setFlip(self, ds):
#         laterality = None
#         view = None
#         orientation = [None]
#         flipHorz = False
#         flipVert = False
#         try:
#             orientation = ds.PatientOrientation
#         except AttributeError:
#             pass
#         try:
#             view = ds.ViewPosition
#         except AttributeError:
#             pass
#         try:
#             laterality = ds.ImageLateratlity
#         except AttributeError:
#             try:
#                 laterality = ds.Laterality
#             except AttributeError:
#                 pass
#         if not all(pd.isnull(orientation)):
#             if view == 'CC':
#                 if orientation[0] == 'P':
#                     flipHorz = True
#                 if (laterality == 'L' and orientation[1] =='L') or (laterality == 'R' and orientation[1] =='R'):
#                     flipVert = True
#             elif (view == 'MLO') or (view == 'ML'):
#                 if orientation[0] == 'P':
#                     flipHorz = True
#                 if (laterality == 'L' and orientation[1] =='L') or (orientation[1] == 'HL'):
#                     flipVert = True
#                 elif (laterality == 'R' and orientation[1] =='R')or (orientation[1] == 'HR'):
#                     flipVert = True
#         else:
#             if (laterality == 'R') and ((view =='CC')or(view == 'ML')or(view == 'MLO')):
#                 flipHorz = True                                                        
#         self.flipHorz = flipHorz
#         self.flipVert = flipVert