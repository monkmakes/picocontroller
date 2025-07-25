from distutils.core import setup
setup(
  name = 'picocontroller',         # How you named your package folder (MyLib)
  packages = ['picocontroller'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A module for the MonkMakes Pico Controller',   # Give a short description about your library
  author = 'Simon Monk',                   # Type in your name
  author_email = 'support@monkmakes.com',      # Type in your E-Mail
  url = 'https://monkmakes.com/picocontroller',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/monkmakes/picocontroller/archive/refs/tags/0.4.tar.gz',    # I explain this later on
  keywords = ['Pico Controller','Raspberry Pi', 'Pico', 'Menu', 'OLED'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'ssd1306',
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
    'Programming Language :: Python :: Implementation :: MicroPython',
  ],
)