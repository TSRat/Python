# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Doc_Center'
copyright = '2026, TSRat'
author = 'TSRat'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = [
#     'rst2pdf.pdfbuilder'
# ]

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 顺便在文件末尾加上基础的 PDF 配置，防止中文乱码
# 'index' 代表主入口文件名，'Enterprise_Doc' 是生成的 PDF 文件名。
pdf_documents = [('index', 'Enterprise_Doc', '企业文档中心', '作者名')]

# 在 conf.py 中修改或添加这一行，把零部件文件隔离掉
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'common_footer.rst']

# 强行指定使用对中文支持最完美的 XeLaTeX 编译器
latex_engine = 'xelatex'

# 工业级 Mac 专用 LaTeX 完美渲染骨架
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'fncychap': '',  
    'fontpkg': r'''
    \setmainfont{Times New Roman}
    \setsansfont{Arial}
    \setmonofont{Menlo}
    ''',
    
    # 【核心修复】彻底擦除引发误会的 # 注释字眼，保持纯净的 LaTeX 语法
    'preamble': r'''
    \usepackage{xeCJK}
    \setCJKmainfont{PingFang SC}
    \setCJKsansfont{PingFang SC}
    \setCJKmonofont{Menlo}
    ''',
}