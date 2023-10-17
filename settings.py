import configparser
from pathlib import Path


class Settings:
    def __init__(self, defaults=None, filename='settings.ini'):
        self.version_number = 1
        self.version = '1.0 alpha'
        self.config = configparser.ConfigParser(defaults=defaults)
        self.home = Path.home()
        self.home_pictures = self.home / "Pictures"
        self.ini_file = Path(filename)
        if not self.ini_file.exists():
            self.create()
        self.config.read(self.ini_file, encoding="utf8")

    def get(self, section, option, fallback=None):
        """获取配置项"""
        result = self.config.get(section, option, fallback=fallback)
        if result == 'True':
            return True
        if result == 'False':
            return False
        return result

    def set(self, section, option, value):
        """设置配置项"""
        self.config.set(section, option, str(value))

    def create(self):
        """创建默认配置文件并设置默认值"""
        self.config['SoftwareConfig'] = {
            'title': '自动跑',
            'icon': './src/desktop.ico',
        }
        self.config['SearchConfig'] = {
            'search-mode': 'single',
            'search-key': '',
        }
        self.config['FilterClassify'] = {
            'filter-mode': '最新',
            'category-mode': '先图文后视频',
        }
        self.config['TaskConfig'] = {
            'task-count': '200',
            'cyclic-mode': 'True',
            'interval-minute': '30',
            'is-like': 'False',
            'is-collect': 'True',
            'is-follow': 'False',
            'is-comment': 'True',
            'is-skip-collect': 'True',
            'is-again-comment-collect': 'False',
            'is-random-rare-word': 'False',
            'rare-word-count': '3',
            'is-check-shield': 'True',
            'is-shield-retry': 'False',
            'retry-count': '3',
        }
        self.config['TimeConfig'] = {
            'task-interval-time': '8',
            'is-random-interval-time': 'True',
            'comment-text': '',
        }
        with open(self.ini_file, 'w', encoding='utf8') as configfile:
            self.config.write(configfile)

    def save(self):
        """将路径信息保存到配置文件"""
        with open(self.ini_file, 'w', encoding='utf8') as configfile:
            self.config.write(configfile)

    def print_set(self):
        for section, section_v in self.config.items():
            for k, v in section_v.items():
                print(f"self.settings.set(\"{section}\", \"{k}\", f\"\")")

    def print_get(self):
        for section, section_v in self.config.items():
            for k, v in section_v.items():
                print(f"self.settings.get(\"{section}\", \"{k}\")")


if __name__ == '__main__':
    s = Settings()
    s.print_set()
    print()
    s.print_get()
