import argparse

from enum import Flag, auto
from pathlib import Path


class IntegrityError(Exception): pass


class Classes(Flag):
    ASSASSIN = auto()
    ASTROMANCER = auto()
    BLADE_DANCER = auto()
    BLADE_MASTER = auto()
    DESTROYER = auto()
    FORCE_MASTER = auto()
    GUNSLINGER = auto()
    KUNG_FU_MASTER = auto()
    SOUL_FIGHTER = auto()
    SUMMONER = auto()
    WARDEN = auto()
    WARLOCK = auto()
    ZEN_ARCHER = auto()

    ALL = (
        ASSASSIN | ASTROMANCER | BLADE_DANCER | BLADE_MASTER | DESTROYER | FORCE_MASTER | 
        GUNSLINGER | KUNG_FU_MASTER | SOUL_FIGHTER | SUMMONER | WARDEN | WARLOCK | ZEN_ARCHER
    )


class Stages(Flag):
    BEFORE_AWAKENING = auto()
    AFTER_AWAKENING = auto()
    THIRD_SPECIALIZATION = auto()

    ALL = BEFORE_AWAKENING | AFTER_AWAKENING | THIRD_SPECIALIZATION


class UpkFiles:
    COMMON = {
        '00003814', '00006660', '00007242', '00007307', '00008841', '00008904', '00009393', '00009801', '00009812', 
        '00010354', '00010504', '00010771', '00010772', '00010869', '00011949', '00012009', '00013263', '00023411', 
        '00023412', '00024690', '00026129', '00031769', '00034433', '00056127', '00059534', '00060548', '00060549', 
        '00060550', '00060551', '00060552', '00060553', '00060554', '00060555', '00060556', '00060557', '00060558', 
        '00060729', '00068166', '00064738'
    }

    SPECIAL = {
        (Classes.ASSASSIN,       Stages.BEFORE_AWAKENING    ): {'00007916'},
        (Classes.BLADE_DANCER,   Stages.BEFORE_AWAKENING    ): {'00018601'},
        (Classes.BLADE_MASTER,   Stages.BEFORE_AWAKENING    ): {'00007911'},
        (Classes.DESTROYER,      Stages.BEFORE_AWAKENING    ): {'00007914'},
        (Classes.FORCE_MASTER,   Stages.BEFORE_AWAKENING    ): {'00007913'},
        (Classes.GUNSLINGER,     Stages.BEFORE_AWAKENING    ): {'00007915'},
        (Classes.KUNG_FU_MASTER, Stages.BEFORE_AWAKENING    ): {'00007912'},
        (Classes.SOUL_FIGHTER,   Stages.BEFORE_AWAKENING    ): {'00034408'},
        (Classes.SUMMONER,       Stages.BEFORE_AWAKENING    ): {'00007917'},
        (Classes.WARDEN,         Stages.BEFORE_AWAKENING    ): {'00056126', '00056566'},
        (Classes.WARLOCK,        Stages.BEFORE_AWAKENING    ): {'00023439'},
        (Classes.ASSASSIN,       Stages.AFTER_AWAKENING     ): {'00056572'},
        (Classes.BLADE_DANCER,   Stages.AFTER_AWAKENING     ): {'00056574'},
        (Classes.BLADE_MASTER,   Stages.AFTER_AWAKENING     ): {'00056567'},
        (Classes.DESTROYER,      Stages.AFTER_AWAKENING     ): {'00056570'},
        (Classes.FORCE_MASTER,   Stages.AFTER_AWAKENING     ): {'00056569'},
        (Classes.GUNSLINGER,     Stages.AFTER_AWAKENING     ): {'00056571'},
        (Classes.KUNG_FU_MASTER, Stages.AFTER_AWAKENING     ): {'00056568'},
        (Classes.SOUL_FIGHTER,   Stages.AFTER_AWAKENING     ): {'00056576'},
        (Classes.SUMMONER,       Stages.AFTER_AWAKENING     ): {'00056573'},
        (Classes.WARDEN,         Stages.AFTER_AWAKENING     ): {'00056577'},
        (Classes.WARLOCK,        Stages.AFTER_AWAKENING     ): {'00056575'},
        (Classes.ZEN_ARCHER,     Stages.AFTER_AWAKENING     ): {'00068166', '00064738'},
        (Classes.ASSASSIN,       Stages.THIRD_SPECIALIZATION): {'00068516', '00069254'},
        (Classes.BLADE_MASTER,   Stages.THIRD_SPECIALIZATION): {'00060548', '00013263'},
        (Classes.DESTROYER,      Stages.THIRD_SPECIALIZATION): {'00067307'},
        (Classes.FORCE_MASTER,   Stages.THIRD_SPECIALIZATION): {'00068626', '00072638'},
        (Classes.KUNG_FU_MASTER, Stages.THIRD_SPECIALIZATION): {'00064821', '00064820', '00060459'},
    }


class AnimationProcessor:
    COMMANDS = ['remove', 'restore']

    def __init__(self, config):
        self.config = config

    def prepare_queue(self):
        names = set()

        if self.config.REMOVE_COMMON:
            names |= UpkFiles.COMMON

        for conf_classes, conf_stages in self.config.REMOVE_SPECIALS:
            for def_classes, def_stages in UpkFiles.SPECIAL.keys():
                classes = conf_classes & def_classes
                stages = conf_stages & def_stages

                names |= UpkFiles.SPECIAL.get((classes, stages), [])

        return [Path(f'{name}.upk') for name in names]

    def get_path(self, name):
        return self.config.BNS_ROOT / Path(r'contents\bns\CookedPC') / name

    def get_backup_path(self, name):
        return self.config.BACKUP_DIR / name

    def remove(self):   
        files = self.prepare_queue()

        if not all([self.get_path(file).is_file() for file in files]):
            raise IntegrityError
        
        self.config.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        for file in self.config.BACKUP_DIR.iterdir():
            file.unlink()

        for file in files:
            path = self.get_path(file)
            path.replace(self.get_backup_path(file))

    def restore(self):
        if not self.config.BACKUP_DIR.is_dir():
            raise IntegrityError

        for path in self.config.BACKUP_DIR.iterdir():
            path.replace(self.get_path(path.name))


class Settings:
    BNS_ROOT = Path(r'C:\Games\Blade and Soul')

    BACKUP_DIR = BNS_ROOT / Path('animation_backup')
    
    REMOVE_COMMON = True
    REMOVE_SPECIALS = [
        (Classes.ALL, Stages.ALL)
    ]


parser = argparse.ArgumentParser(description='Blade and Soul animations')
parser.add_argument('command', type=str, choices=AnimationProcessor.COMMANDS)


if __name__ == '__main__':
    args = parser.parse_args()

    config = Settings()
    processor = AnimationProcessor(config)
    command = getattr(processor, args.command)

    try:
        command()
    except IntegrityError:
        print('[IntegrityError] Some files don\'t exist.\n'
              '                 Restore animations first. If it won\'t help, check your client.')
