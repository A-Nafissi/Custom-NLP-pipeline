"""Exercise notebook definitions without data exports or translation calls."""
import ast
import json
from pathlib import Path
import re
import unittest
import emoji
from better_profanity import profanity
from textblob import TextBlob

NOTEBOOK = Path(__file__).resolve().parents[1] / 'Youtube_Tutorial_code.ipynb'

class NotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
        cls.scope = {'re': re, 'emoji': emoji, 'profanity': profanity, 'TextBlob': TextBlob}
        definitions = []
        for cell in cls.notebook['cells']:
            if cell['cell_type'] != 'code':
                continue
            code = ''.join(cell['source'])
            if code.lstrip().startswith('%pip'):
                continue
            tree = ast.parse(code)
            definitions.extend(node for node in tree.body if isinstance(node, ast.FunctionDef))
            definitions.extend(node for node in tree.body if isinstance(node, ast.Assign)
                               and any(isinstance(target, ast.Name) and target.id in
                                       {'my_dict', 'TRANSLATE_TO_ENGLISH', 'CENSOR_PROFANITY'}
                                       for target in node.targets))
        exec(compile(ast.Module(body=definitions, type_ignores=[]), str(NOTEBOOK), 'exec'), cls.scope)

    def test_urls_at_start_and_middle(self):
        strip = self.scope['url_parsing']
        self.assertEqual(strip('https://example.com/path hello'), 'hello')
        self.assertEqual(strip('hello www.example.com bye').split(), ['hello', 'bye'])
        self.assertEqual(strip('no links here'), 'no links here')

    def test_emoji_variants_and_adjacent_text(self):
        convert = self.scope['emoji_to_text']
        self.assertEqual(convert('❤️').strip(), 'love')
        self.assertEqual(convert('hi😊there').split(), ['hi', 'happy', 'there'])
        self.assertIn('rocket', convert('🚀'))

    def test_numbers_negation_and_programming_language(self):
        clean = self.scope['data_cleaning']
        self.assertIn('1000', clean('1000'))
        self.assertIn('c#', clean('I use C#'))
        self.assertIn('not good', clean('not good'))
        self.assertEqual(clean('goooooood'), 'good')
        self.assertEqual(clean('love love love'), 'love')
        self.assertEqual(clean('@name-foo DataScience'), 'user foo data science')
        self.assertEqual(clean(''), '')

    def test_sentiment_labels(self):
        sentiment = self.scope['sentiment_analysis']
        self.assertEqual(sentiment('wonderful'), 'Positive')
        self.assertEqual(sentiment('awful'), 'Negative')
        self.assertEqual(sentiment(''), 'Neutral')

    def test_offline_defaults_and_clean_outputs(self):
        self.assertIsNone(self.scope['TRANSLATE_TO_ENGLISH'])
        self.assertFalse(self.scope['CENSOR_PROFANITY'])
        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                self.assertIsNone(cell['execution_count'])

if __name__ == '__main__':
    unittest.main()
