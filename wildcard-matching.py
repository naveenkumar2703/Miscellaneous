# This code is for Leetcode challenge: https://leetcode.com/problems/wildcard-matching/
# 
#
#

# Below solutioin is based on dynamic programming approach
class Solution:

    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """

        multi_char_wild_card = '*'
        single_char_wild_card = '?'

        # Initialize variables to None
        result = [[None for pattern_ix in range(len(p) + 1)] for char_ix in range(len(s) + 1)]

        result[0][0] = True # Initialize first variable to True

        for pattern_ix in range(1, len(s) + 1):
            result[pattern_ix][0] = False # Initialize string matches as False

        for pattern_ix in range(1, len(p) + 1):
            if p[pattern_ix - 1] == multi_char_wild_card:
                result[0][pattern_ix] = result[0][pattern_ix - 1]
            else:
                result[0][pattern_ix] = False

        for pattern_ix in range(1, len(s) + 1):
            for char_ix in range(1, len(p) + 1):
                if p[char_ix - 1] == s[pattern_ix - 1]: #  one char match
                    result[pattern_ix][char_ix] = result[pattern_ix - 1][char_ix - 1] # assign the result
                elif p[char_ix - 1] == single_char_wild_card: # if ? single wild match
                    result[pattern_ix][char_ix] = result[pattern_ix - 1][char_ix - 1] # assign the result
                elif p[char_ix - 1] == multi_char_wild_card: # If multi char wild card
                    if result[pattern_ix - 1][char_ix] or result[pattern_ix][char_ix - 1]:
                        result[pattern_ix][char_ix] = True # set true when patterns are match
                    else:
                        result[pattern_ix][char_ix] = False
                else:
                    result[pattern_ix][char_ix] = False

        return result[len(s)][len(p)]

a = Solution()
# print(a.isMatch('fimde','?i*de'))
# print(a.isMatch('mississippi','m??*ss*?i*pi'))
# print(a.isMatch('abefcdgiescdfimde','ab*cd?i*de'))
assert a.isMatch('mississippi','m*issi*iss*') == False
assert a.isMatch('d','*d*d') == False
assert a.isMatch('missingtest','mi*ing?s*t') == False
assert a.isMatch('abcdefghijk','abc*defghijk')
assert a.isMatch('abce','abc*??') == False
assert a.isMatch('abcd','abc*d')
assert a.isMatch('aaaa','***a')
assert a.isMatch('ho','**ho')
assert a.isMatch('b','*a*') == False
assert a.isMatch('ab','*a*')
assert a.isMatch('fimde','?i*de')
assert a.isMatch('mississippi','m??*ss*?i*pi') == False
assert a.isMatch('abefcdgiescdfimde','ab*cd?i*de')
assert a.isMatch('some','so*e?') == False
assert a.isMatch('aa','a') == False
assert a.isMatch('aa','*?') # True
assert a.isMatch('a','*?*')
assert a.isMatch('cab','c*b')
assert a.isMatch('adceb','*a*b')  # True
assert False == a.isMatch('acdcb','a*c?b')
assert a.isMatch('ab','*ab')
assert a.isMatch('cabab','*ab') # True

#assert a.isMatch('cab','c*b')
assert a.isMatch('adceb','*a*b')  # True

assert False == a.isMatch('acdcb','a*c?b')


# Alternate solution using recursion and manual rules.

class AlternateSolution(object):

    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """


        pattern_index = 0
        str_index = 0

        single_char_card = '?'
        multi_char_card = '*'

        count_single_char = len([i for i in p if i == single_char_card])
        count_multi_char = len([i for i in p if i == multi_char_card])
        if s==p or (count_multi_char > 0 and len(p) == count_multi_char) or (count_single_char > 0 and len(s) == count_single_char):
            return True

        if count_single_char > len(s) or len(s) == 0 or len(p) == 0:
            return False

        while '**' in p:
            p = p.replace('**','*')

        str_length = len(s)
        pattern_length = len(p)
        
        while pattern_index < pattern_length or str_index < str_length:

            if pattern_index >= pattern_length:
                return False
            if str_index >= str_length and p[pattern_index] != multi_char_card:
                return False

            if p[pattern_index] != single_char_card and multi_char_card != p[pattern_index]:                

                if p[pattern_index] != s[str_index]:

                    return False
                else:
                    pattern_index += 1
                    str_index += 1
                    continue

            if p[pattern_index] == single_char_card:


                if str_index + 1 > str_length:
                    return False

                pattern_index += 1
                str_index += 1
                continue

            if p[pattern_index] == multi_char_card:

                if str_index > 0 and str_index + 1 < len(s) - 1 and pattern_index != str_index:
                    str_index += 1
                elif len(s) == 1:
                    str_index += 1
                pattern_index += 1
                chars_after_multi_card = ''

                while pattern_index < pattern_length:

                    if p[pattern_index] == '*' or p[pattern_index] == '?':

                        if chars_after_multi_card == '':

                            if p[pattern_index] == '*':

                                if str_index > 0:
                                    str_index += 1
                                    pattern_index += 1
                                continue
                            else:
                                pattern_index += 1
                                str_index += 1
                                chars_after_multi_card = '?'
                        break

                    chars_after_multi_card += p[pattern_index]

                    pattern_index += 1
                if chars_after_multi_card != '':

                    if chars_after_multi_card == '?':
                        if len(s) > 1 and str_index >= str_length + 1:
                            return False
                        elif str_index == str_length and str_length >= pattern_length:

                            return True

                        char_after_multi_card = None
                        while not char_after_multi_card and pattern_index < pattern_length:

                            char_after_multi_card = p[pattern_index] if pattern_index < pattern_length and p[pattern_index] != '*' else None
                            break
                        if char_after_multi_card is None:

                            return True



                    else:
                        next_strings = s[str_index:]

                        try:
                            new_s = s[str_index:]

                            if len(chars_after_multi_card) >= 2:
                                str_indices = [i for i in range(len(new_s)) if  new_s[i:i+len(chars_after_multi_card)]==chars_after_multi_card]
                            else:
                                str_indices = [i for i in range(len(new_s)-2) if  new_s[i:i+len(chars_after_multi_card)]==chars_after_multi_card]


                            
                            if len(str_indices) > 0 and len(p[pattern_index:]) > 0:

                                for ix in str_indices:
                                    
                                    if self.isMatch(s[str_index+ix+len(chars_after_multi_card):], p[pattern_index:]):
                                        return True
                                    else:
                                        return False

                            else:

                                if len (chars_after_multi_card):
                                    for c in chars_after_multi_card:
                                        if c not in s:
                                            return False

                                if pattern_index <= len(p):
                                    if pattern_index <= len(p) and '*' in p[pattern_index:]:
                                        return self.isMatch(new_s,p[pattern_index:])

                                if next_strings == chars_after_multi_card or next_strings.endswith(chars_after_multi_card):
                                    if pattern_index <= len(p):
                                        if p[pattern_index:] == '?':
                                            return False

                                    return True

                                else:
                                    return False
                        except Exception as e:
                            raise e
                            return False

                else:
                    return True


        return True


