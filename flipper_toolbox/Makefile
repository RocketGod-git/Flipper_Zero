
# E303 : too many blank lines
# E302 : expected 2 blank lines, found 1
# E201 whitespace after '['
# E202 whitespace before ']'
# E501 line too long

# E203,E201,E202,E501
# PEP8=pep8
PYCODESTYLE=pycodestyle
PEP8ARG=--ignore=E501,E221,E241
# PEP8ARG=--ignore=E303,E302,E201,E202,E501 

PYLINT=pylint


FILES=ir_gen_all_codes.py ir_plot.py \
	nfc_gen_url.py nfc_hexdump.py nfc_prox2flip.py \
	subghz_create_dat.py subghz_decode_presets.py subghz_gen_cmd.py \
	subghz_histogram.py

all: pylint

lint: pylint

pylint:
	for targ in ${FILES} ; do \
		echo $$targ ; \
		pylint $$targ  ; \
	done

# pylint --load-plugins perflint $$targ  ; \
# python -m py_compile $$targ ; \
#


pep8: pycodestyle

pycodestyle:
	for targ in ${FILES} ; do \
		echo $$targ ; \
		${PYCODESTYLE} ${PEP8ARG} $$targ ; \
	done


clean:
	@/bin/rm -fr *sub *.ir *.nfc touch_tunes-??? __pycache__
