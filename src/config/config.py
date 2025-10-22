
"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""

SCR_VERSION = "0.0.0"

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class SCR_Config(object):


    def __init__(self):

        self.theme  = "light"
        self.themes = {
                        "light"  : {
                                    "background"          : "#FFFFFF",
                                    "foreground"          : "#000000",
                                    "selection_background": "#272932",
                                    "selection_foreground": "#FFFFFF",
                                   },
                                  
                        "dark" : {
                                    "background"          : "#272932",
                                    "foreground"          : "#FFFFFF",
                                    "selection_background": "#FFFFFF",
                                    "selection_foreground": "#000000",
                                 },
                      }

    def get_theme_background(self):

        return self.themes[self.theme]["background"]

    def get_theme_foreground(self):

        return self.themes[self.theme]["foreground"]

    def get_theme_sel_background(self):

        return self.themes[self.theme]["selection_background"]

    def get_theme_sel_foreground(self):

        return self.themes[self.theme]["selection_foreground"]

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""

