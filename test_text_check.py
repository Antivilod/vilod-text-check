import unittest
from text_check import check


class TextCheckTests(unittest.TestCase):
    def test_clean_lf_and_crlf(self):
        self.assertTrue(check(b'alpha\nbeta\n')['ok'])
        self.assertTrue(check(b'alpha\r\nbeta\r\n')['ok'])

    def test_empty_file(self):
        self.assertEqual(check(b'')['lines'], 0)
        self.assertTrue(check(b'')['ok'])

    def test_mixed_newlines_and_trailing_space(self):
        types = {x['type'] for x in check(b'a \r\nb\n')['issues']}
        self.assertEqual(types, {'mixed_line_endings','trailing_whitespace'})

    def test_long_dash_location_and_allow(self):
        raw = 'a\u2014b\n'.encode()
        self.assertEqual(check(raw)['issues'], [{'type':'long_dash','line':1,'column':2}])
        self.assertTrue(check(raw, allow_long_dashes=True)['ok'])

    def test_bom_nul_and_missing_newline(self):
        types = {x['type'] for x in check(b'\xef\xbb\xbfa\x00')['issues']}
        self.assertEqual(types, {'utf8_bom','nul_character','missing_final_newline'})

    def test_length_limit_is_optional(self):
        self.assertTrue(check(b'abcdef\n')['ok'])
        self.assertEqual(check(b'abcdef\n', 5)['issues'][0]['type'], 'line_too_long')

    def test_invalid_utf8(self):
        with self.assertRaises(ValueError): check(b'\xff')

    def test_no_content_in_report(self):
        result = check(b'PRIVATE_SYNTHETIC_SAMPLE \n')
        self.assertNotIn('PRIVATE_SYNTHETIC_SAMPLE', str(result))

    def test_issue_cap_keeps_total(self):
        result = check(('x\u2014\n' * 1001).encode())
        self.assertEqual(result['issue_count'], 1001)
        self.assertEqual(len(result['issues']), 1000)
        self.assertTrue(result['truncated'])

    def test_bare_cr_and_invalid_limit(self):
        self.assertEqual(check(b'a\r')['issues'][0]['type'], 'bare_carriage_return')
        with self.assertRaises(ValueError): check(b'a\n', 0)
