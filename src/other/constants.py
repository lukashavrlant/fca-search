import os

LOCALHOST = True if 'lukashavrlant' in __file__ else False

# folders
ROOT_FOLDER = os.path.realpath(__file__).replace('src/other/constants.py', '')
FILES_FOLDER = ROOT_FOLDER + 'files/'
DATA_FOLDER = FILES_FOLDER + 'data/'
TEST_FOLDER = FILES_FOLDER + 'tests/'
DATABASES_FOLDER = FILES_FOLDER + 'databases/'
TEMP_FOLDER = FILES_FOLDER + 'temp/'
BIN_FOLDER = FILES_FOLDER + 'bin/'

INDEX_FOLDER_NAME = 'index/'
INFO_FOLDER_NAME = ''


# files
DOCUMENT_INFO_NAME = 'documents_info'
ALL_WORDS_NAME = 'allwords.txt'
STOPWORDS_NAME = 'stopwords.txt'
STEMSDICT_NAME = 'stemsdict'
KEYWORDSINDOCUMENTS_NAME = 'keywordsInDocuments'
SCORES_TABLE = 'scoresTable'
SETTINGS_FILE = 'settings.json'

# bins
PDFTOTEXT = BIN_FOLDER + 'pdftotext '
PYTHON3 = 'python3 ' if LOCALHOST else '/home/havrlanl/python-3.2.2/bin/python3 '

# other
CHMOD_INDEX = 0o766


def printConstants():
	print("ROOT_FOLDER: " + ROOT_FOLDER)
	print("FILES_FOLDER: " + FILES_FOLDER)
	print("DATABASES_FOLDER: " + DATABASES_FOLDER)
	print("DATA_FOLDER: " + DATA_FOLDER)
	