import random
import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class PhonologySystem:
    """音韻系統"""
    consonants: Set[str] = field(default_factory=lambda: {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'ng', 'sh', 'th', 'ch'})
    vowels: Set[str] = field(default_factory=lambda: {'a', 'e', 'i', 'o', 'u'})
    syllable_patterns: List[str] = field(default_factory=lambda: ['V', 'CV', 'VC', 'CCV', 'CVC', 'CCVC'])
    phonotactic_rules: List[str] = field(default_factory=list)

    def generate_syllable(self) -> str:
        """根據音韻規則生成音節"""
        pattern = random.choice(self.syllable_patterns)
        syllable = ""

        for char in pattern:
            if char == 'C':
                syllable += random.choice(list(self.consonants))
            elif char == 'V':
                syllable += random.choice(list(self.vowels))

        return syllable

    def generate_word(self, syllable_count: int = None) -> str:
        """生成詞語"""
        if syllable_count is None:
            syllable_count = random.randint(1, 3)

        word = ""
        for _ in range(syllable_count):
            word += self.generate_syllable()

        return word

@dataclass
class MorphologyRule:
    """構詞規則"""
    name: str
    rule_type: str  # prefix, suffix, infix, reduplication
    marker: str
    meaning: str
    position: str = ""

@dataclass
class MorphologySystem:
    """構詞系統"""
    rules: List[MorphologyRule] = field(default_factory=list)
    word_classes: Dict[str, List[str]] = field(default_factory=lambda: {
        'noun': [], 'verb': [], 'case': []
    })

    def add_rule(self, name: str, rule_type: str, marker: str, meaning: str):
        """添加構詞規則"""
        rule = MorphologyRule(name, rule_type, marker, meaning)
        self.rules.append(rule)

    def apply_morphology(self, base_word: str, rule_name: str) -> str:
        """應用構詞規則"""
        for rule in self.rules:
            if rule.name == rule_name:
                if rule.rule_type == 'prefix':
                    return rule.marker + base_word
                elif rule.rule_type == 'suffix':
                    return base_word + rule.marker
                elif rule.rule_type == 'reduplication':
                    return base_word + base_word
        return base_word

@dataclass
class SyntaxRule:
    """句法規則"""
    name: str
    pattern: str  # SVO, SOV, VSO etc.
    description: str

@dataclass
class SyntaxSystem:
    """句法系統"""
    default_order: str = "SVO"
    allowed_orders: List[str] = field(default_factory=list)
    rules: List[SyntaxRule] = field(default_factory=list)

    def add_rule(self, name: str, pattern: str, description: str):
        """添加句法規則"""
        rule = SyntaxRule(name, pattern, description)
        self.rules.append(rule)

    def generate_sentence(self, subject: str, verb: str, obj: str = "", order: str = None) -> str:
        """根據語序生成句子"""
        word_order = order or self.default_order

        if word_order == "SVO":
            return f"{subject} {verb} {obj}".strip()
        elif word_order == "SOV":
            return f"{subject} {obj} {verb}".strip()
        elif word_order == "VOS":
            return f"{verb} {obj} {subject}".strip()
        elif word_order == "VSO":
            return f"{verb} {subject} {obj}".strip()
        else:
            return f"{subject} {verb} {obj}".strip()

class LanguageCreatorGame:
    """語言創造者遊戲主類"""

    def __init__(self):
        self.phonology = PhonologySystem()
        self.morphology = MorphologySystem()
        self.syntax = SyntaxSystem()
        self.vocabulary = defaultdict(list)  # {詞性: [詞語列表]}
        self.current_level = 1


    def display_welcome(self):
        """顯示歡迎訊息"""
        print("=" * 60)
        print("🌍 歡迎來到語言創造者遊戲！ 🌍")
        print("=" * 60)
        print("你將通過三個層次來創造一個全新的語言：")
        print("第一層：音韻系統 (Phonology)")
        print("第二層：構詞系統 (Morphology)")
        print("第三層：句法系統 (Syntax)")
        print("=" * 60)

    def level_1_phonology(self):
        """第一關：設定音韻系統"""
        print("\n🔤 第一關：音韻系統設定")
        print("-" * 40)
        print("讓我們為你的語言設定基本的聲音系統！")

        # 設定子音
        #print(f"\n目前的子音：{', '.join(sorted(self.phonology.consonants))}")
        while True:
            print(f"\n目前的子音：{', '.join(sorted(self.phonology.consonants))}")
            choice = input("\n你想要 (a)添加子音 (b)移除子音 (c)繼續下一步？ ").lower()
            if choice == 'a':
                new_consonant = input("請輸入要添加的子音：")
                if new_consonant and len(new_consonant) <= 2:
                    self.phonology.consonants.add(new_consonant)
                    print(f"已添加子音：{new_consonant}")
            elif choice == 'b':
                remove_consonant = input("請輸入要移除的子音：")
                if remove_consonant in self.phonology.consonants:
                    self.phonology.consonants.remove(remove_consonant)
                    print(f"已移除子音：{remove_consonant}")
            elif choice == 'c':
                break

        # 設定母音
        #print(f"\n目前的母音：{', '.join(sorted(self.phonology.vowels))}")
        while True:
            print(f"\n目前的母音：{', '.join(sorted(self.phonology.vowels))}")
            choice = input("\n你想要 (a)添加母音 (b)移除母音 (c)繼續下一步？ ").lower()

            if choice == 'a':
                new_vowel = input("請輸入要添加的母音：")
                if new_vowel and len(new_vowel) <= 3:
                    self.phonology.vowels.add(new_vowel)
                    print(f"已添加母音：{new_vowel}")

            elif choice == 'b':
                remove_vowel = input("請輸入要移除的母音：")
                if remove_vowel in self.phonology.vowels:
                    self.phonology.vowels.remove(remove_vowel)
                    print(f"已移除母音：{remove_vowel}")
            elif choice == 'c':
                break

        # 設定音節結構
        print(f"\n目前的詞彙音節結構：{', '.join(self.phonology.syllable_patterns)}")
        print("(C=子音, V=母音)")

        # 生成範例詞語
        print("\n🎲 讓我們用你的音韻系統生成一些詞語：")
        for i in range(5):
            word = self.phonology.generate_word()
            print(f"{i+1}. {word}")
            self.vocabulary['unknown'].append(word)

        print(f"\n✅ 第一關完成！")
        self.current_level = 2

    def level_2_morphology(self):
        """第二關：設定構詞系統"""
        print("\n🔧 第二關：構詞系統設定")
        print("-" * 40)
        print("現在我們來為語言添加構詞規則！")

        # 將之前生成的詞語分類
        print("\n首先，讓我們為之前生成的詞語分類：")
        for word in self.vocabulary['unknown'][:]:
            print(f"\n詞語：{word}")
            word_class = input("這個詞是 (n)名詞 (v)動詞 (c)格位？ ").lower()

            if word_class == 'n':
                self.vocabulary['noun'].append(word)
            elif word_class == 'v':
                self.vocabulary['verb'].append(word)
            elif word_class == 'c':
                self.vocabulary['case'].append(word)
            else:
                self.vocabulary['noun'].append(word)  # 預設為名詞

            self.vocabulary['unknown'].remove(word)

        # 添加構詞規則
        print("\n現在我們來創建構詞規則（輸入 ENTER 使用預設值）：")

        # 過去式規則
        past_marker = input("請設定過去式標記（例如：ni-）：") or "ni-"
        self.morphology.add_rule("past", "prefix", past_marker, "過去式")
        print(f"已添加過去式規則：動詞 + {past_marker}")

        # 語態規則
        voice_marker = input("請設定語態標記（例如：-a）:") or "-a"
        self.morphology.add_rule("voice", "suffix", voice_marker, "語態")
        print(f"已添加語態規則：動詞 + {voice_marker}")

        # 動貌規則
        aspect_marker = input("請設定動貌標記（例如：-ato）：") or "-ato"
        self.morphology.add_rule("aspect", "suffix", aspect_marker, "動貌")
        print(f"已添加動貌規則：動詞 + {aspect_marker}")

        # 演示構詞規則
        print("\n🎯 構詞規則演示：")
        if self.vocabulary['verb']:
            verb = random.choice(self.vocabulary['verb'])

            verbRuleLIST = ["past", "voice", "aspect"]
            ruleINT = random.randint(1, 3)
            applyLIST = verbRuleLIST[:ruleINT]

            form = verb
            for r in applyLIST:
                form = self.morphology.apply_morphology(form, r)

        self.vocabulary['case'] = ["ta", "ki"]

        print(f"\n✅ 第二關完成！")
        self.current_level = 3

    def level_3_syntax(self):
        """第三關：設定句法系統"""
        print("\n📝 第三關：句法系統設定")
        print("-" * 40)
        print("最後，我們來設定語言的句子結構！")

        # 設定基本語序
        print("\n請選擇基本語序：")
        print("1. SVO (主語-動詞-賓語) - 如英文、中文")
        print("2. SOV (主語-賓語-動詞) - 如日文、韓文")
        print("3. VOS (動詞-主語-賓語) - 如南島語")

        orderDICT = {
            "1": "SVO",
            "2": "SOV",
            "3": "VOS"
        }

        order_choice = input("請選擇 (1-3)：") or "1"
        main_order = orderDICT.get(order_choice, "SVO")
        self.syntax.default_order = main_order
        self.syntax.allowed_orders = []

        if main_order == "VOS":
            allow_VOS = input("是否同時允許 VSO 語序? (y/n):").lower() or "n"
            if allow_VOS == "y":
                self.syntax.allowed_orders.append("VSO")

        print(f"已設定語序：{self.syntax.default_order}，允許其他語序：{self.syntax.allowed_orders}")

        # 添加句法規則
        self.syntax.add_rule("basic_sentence", self.syntax.default_order, "基本句型")

        ## 疑問句規則
        #question_marker = input("請設定疑問標記（例如：kawa）：") or "kawa"
        #self.syntax.add_rule("question", f"{self.syntax.default_order}+{question_marker}", "疑問句")

        # 生成範例句子
        print(f"\n🎨 讓我們用 {self.syntax.default_order} 語序生成一些句子：")

        # 確保各詞類都有詞語
        if not self.vocabulary['noun']:
            self.vocabulary['noun'].append(self.phonology.generate_word())
        if not self.vocabulary['verb']:
            self.vocabulary['verb'].append(self.phonology.generate_word())

        for i in range(3):
            NOM = self.vocabulary['case'][0]
            OBL = self.vocabulary['case'][1]
            noun = random.choice(self.vocabulary['noun'])

            subject = f"{NOM} {noun}"
            verb = random.choice(self.vocabulary['verb'])
            obj = f"{OBL} {noun}"

            sentence = self.syntax.generate_sentence(subject, verb, obj)
            print(f"{i+1}. {sentence}")

            ## 疑問句版本
            #question_sentence = sentence + " " + question_marker
            #print(f"   疑問句：{question_sentence}")

        print(f"\n✅ 第三關完成！")

    def final_showcase(self):
        """最終展示創造的語言"""
        print("\n" + "=" * 60)
        print("🎉 恭喜！你已經成功創造了一個新語言！ 🎉")
        print("=" * 60)


        print(f"\n🔤 音韻系統:")
        print(f"   子音：{', '.join(sorted(self.phonology.consonants))}")
        print(f"   母音：{', '.join(sorted(self.phonology.vowels))}")
        print(f"   音節模式：{', '.join(self.phonology.syllable_patterns)}")

        print(f"\n🔧 構詞系統:")
        for rule in self.morphology.rules:
            print(f"   {rule.name}: {rule.rule_type} '{rule.marker}' ({rule.meaning})")

        print(f"\n📝 句法系統:")
        print(f"   基本語序：{self.syntax.default_order}")
        print(f"   其他語序：{self.syntax.allowed_orders}")
        for rule in self.syntax.rules:
            print(f"   {rule.name}: {rule.pattern}")

        print(f"\n📚 詞彙統計:")
        for word_class, words in self.vocabulary.items():
            if words and word_class != 'unknown':
                print(f"   {word_class}: {len(words)} 個詞")

        # 最終語言展示
        print(f"\n🌟 你的語言作品展示:")
        for i in range(3):
            if self.vocabulary['noun'] and self.vocabulary['verb']:
                NOM = self.vocabulary['case'][0]
                OBL = self.vocabulary['case'][1]
                subjNoun = random.choice(self.vocabulary['noun'])
                nounLIST = [n for n in self.vocabulary['noun'] if n != subjNoun]
                objNoun = random.choice(nounLIST)

                subject = f"{NOM} {subjNoun}"
                verb = random.choice(self.vocabulary['verb'])
                obj = f"{OBL} {objNoun}"

                # 添加一些構詞變化在動詞上
                if self.morphology.rules:
                    # 動詞構詞變化
                    verbRuleLIST = ["past", "voice", "aspect"]
                    ruleINT = random.randint(1, 3)
                    applyLIST = verbRuleLIST[:ruleINT]

                    for r in applyLIST:
                        verb = self.morphology.apply_morphology(verb, r)

                    # 名詞格位標記
                    if rule.name == "case":
                        subject = self.morphology.apply_morphology(subject, rule.name)
                        obj = self.morphology.apply_morphology(obj, rule.name)

                # 基本語序
                sentence = self.syntax.generate_sentence(subject, verb, obj)
                print(f"   {sentence}")

                # 其他語序
                for order in self.syntax.allowed_orders:
                    alt_sentence = self.syntax.generate_sentence(subject, verb, obj, order=order)
                    print(f"   {alt_sentence}")


    def run_game(self):
        """運行遊戲主循環"""
        self.display_welcome()

        input("\n按 Enter 開始遊戲...")

        # 第一關：音韻
        if self.current_level == 1:
            self.level_1_phonology()

        # 第二關：構詞
        if self.current_level == 2:
            input("\n按 Enter 進入第二關...")
            self.level_2_morphology()

        # 第三關：句法
        if self.current_level == 3:
            input("\n按 Enter 進入第三關...")
            self.level_3_syntax()

        # 最終展示
        input("\n按 Enter 查看你創造的語言...")
        self.final_showcase()

def main():
    """主程式"""
    game = LanguageCreatorGame()
    game.run_game()

if __name__ == "__main__":
    main()