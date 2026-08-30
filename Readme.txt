pip install -r requirements.txt
python -m pytest tests -m smoke --headed --slowmo 1000 -v -rA  --alluredir allure-results

install allure
#setup Path allure bin
allure generate allure-results --single-file


python -m pytest -s tests -n 2  --headed --slowmo 1000 --html=report.html --self-contained-html

python -m pytest -s tests -n 2  --headed --slowmo 1000 --alluredir allure-results


setupAllure:
  - var(pwdir):
      - shell (name Get pwdir): |
          pwd
  - |
    (name Setup Allure)
    curl -LO https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz
    tar xvf ./allure-2.32.0.tgz
  - shell (name Allure Version): |
      ${pwdir}/allure-2.32.0/bin/allure --version