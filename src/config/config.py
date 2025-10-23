
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
                                    "selection_background": "#A7AABA",
                                    "selection_foreground": "#FFFFFF",
                                    "icon_new"            : "cce0eae9f8616e09065e8ca2f7f2e768fa70c5b2",
                                    "icon_folder"         : "15446caa0c97fc7e6f21c74e2f2eb6c05823297e",
                                    "icon_save"           : "76898ed4d16e54864c213e6a1ad878d1c3abf031",
                                    "icon_exit"           : "0433ee4ecf4c7f50782945b30a901532829e0141",
                                    "icon_theme"          : "54c3350cfddd32130bf01bac112530f80978f932",
                                    "icon_bug"            : "757f73a4d1b466d211241a627d89577487b286d6",
                                    "icon_info"           : "17dd27941655cc1c44deac3239592316f5db31b1",
                                    "icon_doc"            : "7d975f5635c444a059c9a14387eea043cbd5b657",
                                   },
                                  
                        "dark" : {
                                    "background"          : "#272932",
                                    "foreground"          : "#FFFFFF", 
                                    "selection_background": "#34363E",
                                    "selection_foreground": "#FFFFFF",
                                    "icon_new"            : "e91a19ef57b475414003d55e49180b1f26d95397",
                                    "icon_folder"         : "9137835f5ba5460ba8f1413bde7c592895c08018",
                                    "icon_save"           : "23fb7d17e04d0a5a799f082a44938632abbdc3dc",
                                    "icon_exit"           : "c5b5e8d3b1903c528117c8b40c1679bede698c87",
                                    "icon_theme"          : "eb94fe9671a090b21cfd62f87b9ee6ac951a6d9e",
                                    "icon_bug"            : "0641914e82986e52d832bd90660f69c04ccb83c3",
                                    "icon_info"           : "52c32b317976a59fcb8a01e53348b0ec55f5e3bb",
                                    "icon_doc"            : "2c84fd09659e45aac28f6b995cd71b7fbc2e6ae4",
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

    def get_theme_icon_new(self):

        return self.themes[self.theme]["icon_new"]

    def get_theme_icon_folder(self):

        return self.themes[self.theme]["icon_folder"]

    def get_theme_icon_save(self):

        return self.themes[self.theme]["icon_save"]

    def get_theme_icon_exit(self):

        return self.themes[self.theme]["icon_exit"]

    def get_theme_icon_theme(self):

        return self.themes[self.theme]["icon_theme"]

    def get_theme_icon_bug(self):

        return self.themes[self.theme]["icon_bug"]

    def get_theme_icon_info(self):

        return self.themes[self.theme]["icon_info"]

    def get_theme_icon_doc(self):

        return self.themes[self.theme]["icon_doc"]

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""

