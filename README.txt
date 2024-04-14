--------------------------------------

     fw-port conflict prevention

--------------------------------------

- Locate your odoo folder
- `cd` to the parent folder
- Copy here the files `example.sh`, `example_2.sh`, `fwports.py`
- Run `./example.sh`
  This will:
      - checkout and reset origin/15.0
      - checkout a new 15.0-l10n-it-edi-fwhell-test
      - make a fake change on addons/l10n_it_edi/data/invoice_it_template.xml
      - git add-s the change and commits
      - runs `fwports.py 15.0-l10n-it-edi-fwhell-test`
          - get a patch 15.0..15.0-l10n-it-edi-fwhell-test
          - checkout 16.0
          - check if the patch is applicable (it is)
          - checkout saas-16.3
          - check if the patch is applicable (it isn't)
          - creates saas-16.3-l10n-it-edi-fwhell-test
          - outputs git log 15.0..15.0-l10n-it-edi-fwhell-test
            to retrieve the commit messages so that when you
            will commit the fix, you can copy that
- Run `./example_2.sh`
      - Fixes addons/l10n_it_edi/data/invoice_it_template.xml
      - git add-s the change and commits
      - runs `fwports.py saas-16.3-l10n-it-edi-fwhell-test`
          - get a patch saas-16.3..saas-16.3-l10n-it-edi-fwhell-test
          - checkout saas-16.3
          - check if the patch is applicable (it isn't)
          - creates saas-16.4-l10n-it-edi-fwhell-test
          - outputs git log saas-16.3..saas-16.3-l10n-it-edi-fwhell-test
            to retrieve the commit messages so that when you
            will commit the fix, you can copy that
