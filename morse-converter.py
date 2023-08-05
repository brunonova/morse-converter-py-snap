#!/usr/bin/env python3

# Copyright (C) 2016 Bruno Nova <brunomb.nova@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Convert between text and morse, and vice-versa.
"""

import re, sys, unicodedata
from argparse import ArgumentParser


# Conversion "table"
_conv = {
	" ": " ",
	"A": ".-",
	"B": "-...",
	"C": "-.-.",
	"D": "-..",
	"E": ".",
	"F": "..-.",
	"G": "--.",
	"H": "....",
	"I": "..",
	"J": ".---",
	"K": "-.-",
	"L": ".-..",
	"M": "--",
	"N": "-.",
	"O": "---",
	"P": ".--.",
	"Q": "--.-",
	"R": ".-.",
	"S": "...",
	"T": "-",
	"U": "..-",
	"V": "...-",
	"W": ".--",
	"X": "-..-",
	"Y": "-.--",
	"Z": "--..",
	"0": "-----",
	"1": ".----",
	"2": "..---",
	"3": "...--",
	"4": "....-",
	"5": ".....",
	"6": "-....",
	"7": "--...",
	"8": "---..",
	"9": "----.",
	".": ".-.-.-",
	",": "--..--",
	"?": "..--..",
	"!": "-.-.--",
	"'": ".----.",
	"/": "-..-.",
	"(": "-.--.",
	")": "-.--.-",
	"&": ".-...",
	":": "-.-.-.",
	"=": "-...-",
	"+": ".-.-.",
	"-": "-....-",
	"_": "..--.-",
	'"': ".-..-.",
	"$": "...-..-",
	"@": ".--.-.",
}
_iconv = {m: t for t, m in _conv.items()}  # inverse dict of _conv


def stripAccents(s):
	"""Strip all accents from the string (ex: "Café" -> "Cafe")."""
	chars = [c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)]
	return "".join(chars)

def morseToText(s):
	"""Converts the given string in morse to text."""
	words = re.split("  +", s)  # words are separated by 2 or more spaces
	chars = [w.split() for w in words]
	return " ".join(["".join([_iconv.get(c, "?") for c in w]) for w in chars])

def textToMorse(s):
	"""Converts the given string to morse."""
	s = stripAccents(s).upper()
	return " ".join([_conv.get(c, "?") for c in s])


def _printConvTable():
	for t, m in sorted(_conv.items()):
		if t != " ":
			print("{}: {}".format(t, m))

def _parseArgs():
	parser = ArgumentParser(description="Converts text to morse, and vice-versa.")
	actions = parser.add_argument_group("actions")
	group = actions.add_mutually_exclusive_group(required=True)
	group.add_argument("-m", "--to-morse", action="store_true",
	                   help="convert text to morse")
	group.add_argument("-t", "--to-text", action="store_true",
	                   help="convert morse to text")
	group.add_argument("-T", "--table", action="store_true",
	                    help="print the conversion table")
	return parser.parse_args()


if __name__ == "__main__":
	args = _parseArgs()
	if args.table:
		_printConvTable()
	else:
		convMethod = morseToText if args.to_text else textToMorse

		# Print help header
		if sys.stdin.isatty():
			if args.to_text:
				print("Write the morse codes to convert to text.")
			else:
				print("Write the text to convert to morse code.")
			print("End by pressing Control+D on an empty line.\n")

		# Read and convert
		lines = sys.stdin.readlines()
		print(*[convMethod(s.strip()) for s in lines], sep="\n")
