#!/bin/bash

rm -rf MD2QTI
# this unset line is a horrible hack. cert finding seems to be broken with pyz
unset REQUESTS_CA_BUNDLE
python3 -m pip install -r requirements.txt --target MD2QTI
rm -rf MD2QTI/*.dist-info
rm -rf MD2QTI/*.egg-info
cp *.py *.sh MD2QTI
python3 -m zipapp MD2QTI
