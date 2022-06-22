from setuptools import setup
import pathlib
readme_path=(pathlib.Path(__file__).parent / "README.md").read_text()
setup(
name = 'insightsearch',         # How you named your package folder (MyLib)
 packages = ['insightsearch'],   # Chose the same as "name"
 version = '1.7',      # Start with a small number and increase it with every change you make
 license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
 
 description = 'Insightsearch will show sentiments, aspects and their opinions from your text/review data.',   # Give a short description about your library
 author = 'Vivek alex',                   # Type in your name
 author_email = 'vivekalexktr@gmail.com',      # Type in your E-Mail
 url = 'https://github.com/vivekalex61/insightsearch',   # Provide either the link to your github or to your website
 download_url = 'https://github.com/vivekalex61/insightsearch/archive/refs/tags/v1.5.tar.gz',  
 keywords = ['NLP', 'INSIGHT', 'REVIEW ANALYZER','REVIEW'],   # Keywords that define your package best
 project_urls={'Source Code': 'https://github.com/vivekalex61/insightsearch',},
 install_requires=[
          'transformers',
          'spacy',
          'pandas',
      'nltk','plotly','textblob','vaderSentiment'
      ],
long_description=readme_path,
long_description_content_type = 'text/markdown',
 classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
