
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
                                    "background"            : "#FFFFFF",
                                    "foreground"            : "#000000",
                                    "sel_background"        : "#A7AABA",
                                    "sel_foreground"        : "#FFFFFF",
                                    "icon_new"              : "cce0eae9f8616e09065e8ca2f7f2e768fa70c5b2",
                                    "icon_folder"           : "15446caa0c97fc7e6f21c74e2f2eb6c05823297e",
                                    "icon_save"             : "76898ed4d16e54864c213e6a1ad878d1c3abf031",
                                    "icon_exit"             : "0433ee4ecf4c7f50782945b30a901532829e0141",
                                    "icon_theme"            : "54c3350cfddd32130bf01bac112530f80978f932",
                                    "icon_bug"              : "757f73a4d1b466d211241a627d89577487b286d6",
                                    "icon_info"             : "17dd27941655cc1c44deac3239592316f5db31b1",
                                    "icon_doc"              : "7d975f5635c444a059c9a14387eea043cbd5b657",
                                    "icon_var_scalar"       : "a24045c9967f9095e80c6d1b3fadff1a267eaabd",
                                    "icon_var_list"         : "76d45e8d460c5f0fbd871c857e6272680340d337",
                                    "icon_var_dict"         : "99adc38e033640253a72b0f269dfb84912853058",
                                    "icon_keyword"          : "14b802564477e8b8f64dc869c92a4b983edc1001",
                                    "icon_python"           : "4a3e9e2a263bc7213465bd391d7a2243ca588456",
                                    "icon_resource"         : "829bc598d570a4c322ec5b51d698ee40a0cdb072",
                                    "icon_testcase"         : "ca211c47afa3b991350a6c183d8aaf3f33db15a0",
                                    "icon_testsuite"        : "8e205a227046baee2a67b75fb12c95813784c484",
                                    "icon_folder_variables" : "949033dd2b69acfd3791881e24078e0c1a1d3d2f",
                                    "icon_folder_keywords"  : "f072f0504b91bc3ac90d7ea0f0f4cb0f0ba2bab1",
                                    "icon_close"            : "c4c80912bacc504d1b0259c9f2fe36c548b5aca0",
                                    "icon_next"             : "6b86610e1a71d541a418c3aeb3bc9561cc75ef46",
                                    "icon_previous"         : "0aed51b9ddeed91efe378a353a15cefcd16d3acc"            
                                   },
                                  
                        "dark" : {
                                    "background"            : "#272932",
                                    "foreground"            : "#FFFFFF", 
                                    "sel_background"        : "#34363E",
                                    "sel_foreground"        : "#FFFFFF",
                                    "icon_new"              : "e91a19ef57b475414003d55e49180b1f26d95397",
                                    "icon_folder"           : "9137835f5ba5460ba8f1413bde7c592895c08018",
                                    "icon_save"             : "23fb7d17e04d0a5a799f082a44938632abbdc3dc",
                                    "icon_exit"             : "c5b5e8d3b1903c528117c8b40c1679bede698c87",
                                    "icon_theme"            : "eb94fe9671a090b21cfd62f87b9ee6ac951a6d9e",
                                    "icon_bug"              : "0641914e82986e52d832bd90660f69c04ccb83c3",
                                    "icon_info"             : "52c32b317976a59fcb8a01e53348b0ec55f5e3bb",
                                    "icon_doc"              : "2c84fd09659e45aac28f6b995cd71b7fbc2e6ae4",
                                    "icon_var_scalar"       : "0b44b3ff6dae3eda5a91dbd5635605109bdac536",
                                    "icon_var_list"         : "62031073a4ccf845f01d1f007cb3a1b54c8d393d",
                                    "icon_var_dict"         : "e7353d32bfa5253059298d6175fd4a964b7c69b6",
                                    "icon_keyword"          : "48d80beb13e6d212765b5dd860106e1d83de2adf",
                                    "icon_python"           : "89ab47ab2f4da1ad6301713ee444fbdfcd0d273c",
                                    "icon_resource"         : "37876acb653f83c747af4b85fbf9877144251555",
                                    "icon_testcase"         : "ca211c47afa3b991350a6c183d8aaf3f33db15a0",
                                    "icon_testsuite"        : "8e205a227046baee2a67b75fb12c95813784c484",
                                    "icon_folder_variables" : "9d5fffb1c55c6ec2ae1d191b4a8da81bb52f3988",
                                    "icon_folder_keywords"  : "a192dd0bd33d992c21fb05a4b32e1d55084334ab",
                                    "icon_close"            : "4d7ceae0b6dd5d6f513fe835c953da883f6679b8",
                                    "icon_next"             : "1544b76bb3a7d83cc0f5c7757a48e6bcd1c19ba1",
                                    "icon_previous"         : "ad904921c967fef713cce3f04558c33c40581de8"  
                                 },

                        "normal"  : {
                                    "background"            : "#FFFFFF",
                                    "foreground"            : "#000000",
                                    "sel_background"        : "#A7AABA",
                                    "sel_foreground"        : "#FFFFFF",
                                    "icon_new"              : "cce0eae9f8616e09065e8ca2f7f2e768fa70c5b2",
                                    "icon_folder"           : "15446caa0c97fc7e6f21c74e2f2eb6c05823297e",
                                    "icon_save"             : "76898ed4d16e54864c213e6a1ad878d1c3abf031",
                                    "icon_exit"             : "0433ee4ecf4c7f50782945b30a901532829e0141",
                                    "icon_theme"            : "54c3350cfddd32130bf01bac112530f80978f932",
                                    "icon_bug"              : "757f73a4d1b466d211241a627d89577487b286d6",
                                    "icon_info"             : "17dd27941655cc1c44deac3239592316f5db31b1",
                                    "icon_doc"              : "7d975f5635c444a059c9a14387eea043cbd5b657",
                                    "icon_var_scalar"       : "a24045c9967f9095e80c6d1b3fadff1a267eaabd",
                                    "icon_var_list"         : "76d45e8d460c5f0fbd871c857e6272680340d337",
                                    "icon_var_dict"         : "99adc38e033640253a72b0f269dfb84912853058",
                                    "icon_keyword"          : "14b802564477e8b8f64dc869c92a4b983edc1001",
                                    "icon_python"           : "4a3e9e2a263bc7213465bd391d7a2243ca588456",
                                    "icon_resource"         : "829bc598d570a4c322ec5b51d698ee40a0cdb072",
                                    "icon_testcase"         : "ca211c47afa3b991350a6c183d8aaf3f33db15a0",
                                    "icon_testsuite"        : "8e205a227046baee2a67b75fb12c95813784c484",
                                    "icon_folder_variables" : "949033dd2b69acfd3791881e24078e0c1a1d3d2f",
                                    "icon_folder_keywords"  : "f072f0504b91bc3ac90d7ea0f0f4cb0f0ba2bab1",
                                    "icon_close"            : "c4c80912bacc504d1b0259c9f2fe36c548b5aca0",
                                    "icon_next"             : "6b86610e1a71d541a418c3aeb3bc9561cc75ef46",
                                    "icon_previous"         : "0aed51b9ddeed91efe378a353a15cefcd16d3acc"            
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

    def get_theme_icon_var_scalar(self):

        return self.themes[self.theme]["icon_var_scalar"]

    def get_theme_icon_var_list(self):

        return self.themes[self.theme]["icon_var_list"]

    def get_theme_icon_var_dict(self):

        return self.themes[self.theme]["icon_var_dict"]

    def get_theme_icon_keyword(self):

        return self.themes[self.theme]["icon_keyword"]

    def get_theme_icon_python(self):

        return self.themes[self.theme]["icon_python"]

    def get_theme_icon_resource(self):

        return self.themes[self.theme]["icon_resource"]

    def get_theme_icon_testcase(self):

        return self.themes[self.theme]["icon_testcase"]

    def get_theme_icon_testsuite(self):

        return self.themes[self.theme]["icon_testsuite"]

    def get_theme_icon_folder_variables(self):

        return self.themes[self.theme]["icon_folder_variables"]

    def get_theme_icon_folder_keywords(self):

        return self.themes[self.theme]["icon_folder_keywords"]

    def get_theme_icon_close(self):

        return self.themes[self.theme]["icon_close"]

    def get_theme_icon_next(self):

        return self.themes[self.theme]["icon_next"]

    def get_theme_icon_previous(self):

        return self.themes[self.theme]["icon_previous"]

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""

