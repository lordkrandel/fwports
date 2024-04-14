#!/bin/bash -v

pushd odoo
git checkout -f origin/15.0 -B 15.0
git checkout -B 15.0-l10n-it-edi-fwhell-test
sed "s/OO99999999999/OO99999999998/g" --in-place addons/l10n_it_edi/data/invoice_it_template.xml
git add addons/l10n_it_edi/data/invoice_it_template.xml
git commit -m "[FIX] l10n_it_edi: fwhell test change that will conflict" -m "Let's see how many conflicts I can get"
python ../fwports.py 15.0-l10n-it-edi-fwhell-test --force
popd
