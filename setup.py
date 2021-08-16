from distutils.core import setup
setup(
  name = 'insightsearch',         # How you named your package folder (MyLib)
  packages = ['insightsearch'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Insightsearch will show hidden sentiments, aspects and their opinions from your text data. It will show what people are talking about your product/service',   # Give a short description about your library
  author = 'Vivek alex',                   # Type in your name
  author_email = 'vivekalexktr@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vivekalex61/insightsearch/archive/refs/tags/v0.2.tar.gz',  
  keywords = ['NLP', 'INSIGHT', 'REVIEW ANALYZER','REVIEW'],   # Keywords that define your package best
  project_urls={
         
          'Source Code': 'https://github.com/vivekalex61/insightsearch',
        
      },
  install_requires=[
          'transformers',
          'spacy',
          'pandas',
      'nltk','plotly','textblob','os','pathlib','tensorflow'
      ],
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