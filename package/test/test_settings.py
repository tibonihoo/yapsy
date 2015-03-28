# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-

import os
import sys

import logging
TEST_MESSAGE = logging.debug

TEMP_CONFIG_FILE_NAME=os.path.join(
	os.path.dirname(
		os.path.abspath(__file__)),
	"tempconfig")

# set correct loading path for yapsy's files
sys.path.insert(0,
	os.path.dirname(
		os.path.dirname(
			os.path.abspath(__file__))))

sys.path.insert(0,
	os.path.dirname(
		os.path.dirname(
			os.path.dirname(
				os.path.abspath(__file__)))))



