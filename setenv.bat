set PYTHON3PATH=C:\Tools\DEV\Software\Python-3.7.2
set GRAPHVIZPATH=C:\Tools\DEV\Software\graphviz-2.38\bin
rem set PYTHONHOME=%PYTHON3PATH%
set PYTHONPATH=%PYTHON3PATH%;%PYTHON3PATH%\Lib;%PYTHON3PATH%\Scripts;%GRAPHVIZPATH%
set PATH=.;%PYTHONPATH%;%GRAPHVIZPATH%;%PATH%

set proxy=127.0.0.1:3128

set http_proxy=%proxy%
set HTTP_PROXY=%proxy%
set https_proxy=%proxy%
set HTTPS_PROXY=%proxy%

set REQUESTS_CA_BUNDLE=C:\Tools\DEV\cert\cacert.pem

