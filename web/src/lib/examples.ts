/**
 * Built-in example programs. These are loaded from the same source
 * files the CLI interpreter uses so what you see here matches what
 * `python interpreter.py examples/foo.py` would print.
 *
 * We use Vite's `?raw` suffix to import the .py files as strings.
 */
import hello from '../../../examples/hello.py?raw';
import factorial from '../../../examples/factorial.py?raw';
import fizzbuzz from '../../../examples/fizzbuzz.py?raw';
import sum from '../../../examples/sum.py?raw';
import primes from '../../../examples/primes.py?raw';
import lists from '../../../examples/lists.py?raw';
import membership from '../../../examples/membership.py?raw';
import breakContinue from '../../../examples/break_continue.py?raw';
import stringMethods from '../../../examples/string_methods.py?raw';
import dicts from '../../../examples/dicts.py?raw';
import tuples from '../../../examples/tuples.py?raw';
import twoSum from '../../../examples/two_sum.py?raw';
import anagram from '../../../examples/anagram.py?raw';
import containsDuplicate from '../../../examples/contains_duplicate.py?raw';
import bestTimeToSell from '../../../examples/best_time_to_sell.py?raw';
import maxSubarray from '../../../examples/max_subarray.py?raw';
import validParentheses from '../../../examples/valid_parentheses.py?raw';
import mergeSorted from '../../../examples/merge_sorted.py?raw';
import longestCommonPrefix from '../../../examples/longest_common_prefix.py?raw';
import moveZeroes from '../../../examples/move_zeroes.py?raw';
import majorityElement from '../../../examples/majority_element.py?raw';
import missingNumber from '../../../examples/missing_number.py?raw';
import reverseString from '../../../examples/reverse_string.py?raw';
import groupAnagrams from '../../../examples/group_anagrams.py?raw';
import plusOne from '../../../examples/plus_one.py?raw';
import climbingStairs from '../../../examples/climbing_stairs.py?raw';
import pascalsTriangle from '../../../examples/pascals_triangle.py?raw';
import concatenationOfArray from '../../../examples/concatenation_of_array.py?raw';
import firstUniqueChar from '../../../examples/first_unique_char.py?raw';
import romanToInt from '../../../examples/roman_to_int.py?raw';
import palindromeNumber from '../../../examples/palindrome_number.py?raw';
import reverseInteger from '../../../examples/reverse_integer.py?raw';
import buildArray from '../../../examples/build_array.py?raw';
import removeDuplicatesSorted from '../../../examples/remove_duplicates_sorted.py?raw';
import removeElement from '../../../examples/remove_element.py?raw';
import validPalindrome from '../../../examples/valid_palindrome.py?raw';
import strStr from '../../../examples/str_str.py?raw';
import searchInsert from '../../../examples/search_insert.py?raw';
import rotateArray from '../../../examples/rotate_array.py?raw';
import lengthOfLastWord from '../../../examples/length_of_last_word.py?raw';
import addBinary from '../../../examples/add_binary.py?raw';
import pascalsTriangle2 from '../../../examples/pascals_triangle_2.py?raw';
import bestTimeToSell2 from '../../../examples/best_time_to_sell_2.py?raw';
import happyNumber from '../../../examples/happy_number.py?raw';
import rangeSumQuery from '../../../examples/range_sum_query.py?raw';

export interface Example {
  id: string;
  name: string;
  description: string;
  source: string;
}

export const EXAMPLES: Example[] = [
  // ---- Getting started ----
  { id: 'hello', name: 'Hello, world', description: 'A trivial starting program.', source: hello },
  { id: 'factorial', name: 'Factorial', description: 'Functions + recursion + loops.', source: factorial },
  { id: 'fizzbuzz', name: 'FizzBuzz', description: 'Modulo, conditionals, and printing.', source: fizzbuzz },
  { id: 'primes', name: 'Primes', description: 'Nested loops, `if/else`, `not`.', source: primes },

  // ---- Data structures ----
  { id: 'lists', name: 'Lists', description: 'List literals, indexing, iteration.', source: lists },
  { id: 'dicts', name: 'Dictionaries', description: 'Dict literals, keys, values, nested dicts.', source: dicts },
  { id: 'tuples', name: 'Tuples', description: 'Tuple literals, indexing, concatenation.', source: tuples },
  { id: 'membership', name: 'Membership', description: '`in` and `not in` operators.', source: membership },

  // ---- Control flow ----
  { id: 'break_continue', name: 'break / continue', description: 'Early exit / skip in loops.', source: breakContinue },

  // ---- Functions & builtins ----
  { id: 'sum', name: 'Sum', description: 'Augmented assignment `+=`.', source: sum },
  { id: 'string_methods', name: 'String methods', description: '`.upper()`, `.split()`, chaining.', source: stringMethods },

  // ---- LeetCode: Easy ----
  { id: 'two_sum', name: 'Two Sum', description: 'LC 1 — hash-map lookup for O(n) pair sum.', source: twoSum },
  { id: 'valid_parentheses', name: 'Valid Parentheses', description: 'LC 20 — stack-based bracket matcher.', source: validParentheses },
  { id: 'merge_sorted', name: 'Merge Sorted Array', description: 'LC 88 — three-pointer merge in-place.', source: mergeSorted },
  { id: 'move_zeroes', name: 'Move Zeroes', description: 'LC 283 — partition array in-place.', source: moveZeroes },
  { id: 'plus_one', name: 'Plus One', description: 'LC 66 — big-integer addition on digit arrays.', source: plusOne },
  { id: 'climbing_stairs', name: 'Climbing Stairs', description: 'LC 70 — Fibonacci via iterative DP.', source: climbingStairs },
  { id: 'concatenation_of_array', name: 'Concatenation of Array', description: 'LC 1929 — double an array by appending a copy.', source: concatenationOfArray },
  { id: 'first_unique_char', name: 'First Unique Char', description: 'LC 387 — frequency map then linear scan.', source: firstUniqueChar },
  { id: 'majority_element', name: 'Majority Element', description: 'LC 169 — Boyer-Moore voting algorithm.', source: majorityElement },
  { id: 'contains_duplicate', name: 'Contains Duplicate', description: 'LC 217 — detect repeats with a set.', source: containsDuplicate },
  { id: 'missing_number', name: 'Missing Number', description: 'LC 268 — sum-of-range trick for 0..n.', source: missingNumber },
  { id: 'roman_to_int', name: 'Roman to Integer', description: 'LC 13 — subtractive Roman numeral parsing.', source: romanToInt },
  { id: 'palindrome_number', name: 'Palindrome Number', description: 'LC 9 — reverse the second half of digits.', source: palindromeNumber },
  { id: 'reverse_integer', name: 'Reverse Integer', description: 'LC 7 — reverse digits with overflow check.', source: reverseInteger },
  { id: 'build_array', name: 'Build Array from Permutation', description: 'LC 1920 — index indirection `ans[i] = nums[nums[i]]`.', source: buildArray },
  { id: 'reverse_string', name: 'Reverse String', description: 'LC 344 — two-pointer in-place swap.', source: reverseString },
  { id: 'remove_duplicates_sorted', name: 'Remove Duplicates from Sorted Array', description: 'LC 26 — two-pointer dedupe on sorted input.', source: removeDuplicatesSorted },
  { id: 'remove_element', name: 'Remove Element', description: 'LC 27 — two-pointer, remove all instances of a value.', source: removeElement },
  { id: 'valid_palindrome', name: 'Valid Palindrome', description: 'LC 125 — filter alphanumerics, two-pointer compare.', source: validPalindrome },
  { id: 'str_str', name: 'Find the Index of the First Occurrence', description: 'LC 28 — naive substring search (no slicing).', source: strStr },
  { id: 'search_insert', name: 'Search Insert Position', description: 'LC 35 — binary search for insert index.', source: searchInsert },
  { id: 'add_binary', name: 'Add Binary', description: 'LC 67 — grade-school binary string addition.', source: addBinary },
  { id: 'length_of_last_word', name: 'Length of Last Word', description: 'LC 58 — scan from the end, skip spaces.', source: lengthOfLastWord },
  { id: 'range_sum_query', name: 'Range Sum Query', description: 'LC 303 — prefix sums for O(1) range queries.', source: rangeSumQuery },
  { id: 'best_time_to_sell_2', name: 'Best Time to Buy & Sell Stock II', description: 'LC 122 — greedy capture every upward step.', source: bestTimeToSell2 },
  { id: 'happy_number', name: 'Happy Number', description: 'LC 202 — Floyd cycle detection on digit-square sum.', source: happyNumber },

  // ---- LeetCode: Medium ----
  { id: 'longest_common_prefix', name: 'Longest Common Prefix', description: 'LC 14 — character-by-character scan across strings.', source: longestCommonPrefix },
  { id: 'group_anagrams', name: 'Group Anagrams', description: 'LC 49 — canonical sorted-key grouping with a dict.', source: groupAnagrams },
  { id: 'anagram', name: 'Valid Anagram', description: 'LC 242 — frequency-counting histogram compare.', source: anagram },
  { id: 'best_time_to_sell', name: 'Best Time to Buy & Sell Stock', description: 'LC 121 — one-pass min-price tracker.', source: bestTimeToSell },
  { id: 'max_subarray', name: 'Maximum Subarray', description: 'LC 53 — Kadane\'s algorithm for max sub-sum.', source: maxSubarray },
  { id: 'pascals_triangle', name: 'Pascal\'s Triangle', description: 'LC 118 — generate rows with running sums.', source: pascalsTriangle },
  { id: 'pascals_triangle_2', name: 'Pascal\'s Triangle II', description: 'LC 119 — return a single row using O(row) space.', source: pascalsTriangle2 },
  { id: 'rotate_array', name: 'Rotate Array', description: 'LC 189 — in-place rotation via triple reversal.', source: rotateArray },
];
