from abc import ABC

class AppSettings(ABC):
            
    def register_app(self, app_folder):
        self.settings.insert_code('    # My apps', f"    '{app_folder}.{self.app_name}.app.{self.app_name.title()}Config',")


    def register_abstract_user(self):
        self.settings.add_in_end(f"\nAUTH_USER_MODEL = 'accounts.User'")
                    