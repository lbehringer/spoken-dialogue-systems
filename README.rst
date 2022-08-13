|release| |nbsp| |license|

.. |release| image:: https://img.shields.io/github/v/release/digitalphonetics/adviser?sort=semver
   :target: https://github.com/DigitalPhonetics/adviser/releases
.. |license| image:: https://img.shields.io/github/license/digitalphonetics/adviser
   :target: #license
.. |nbsp| unicode:: 0xA0
   :trim:

Documentation
=============

    Please see the `documentation <https://digitalphonetics.github.io/adviser/>`_ for more details.

Installation
============

For installation details, please see the README of the official ADVISER repository: https://github.com/DigitalPhonetics/adviser/

Cloning the repository (recommended)
------------------------------------

If ``Git`` is installed on your machine, you may instead clone the repository by entering in a terminal window:

.. code-block:: bash

    git clone https://github.com/lbehringer/spoken-dialogue-systems

System Library Requirements
---------------------------

For details, please see the README of the official ADVISER repository: https://github.com/DigitalPhonetics/adviser/


Install python requirements with pip
------------------------------------

ADvISER needs to be executed in a Python3 environment.

Once you obtained the code, navigate to its top level directory where you will find the file
``requirements_base.txt``, which lists all modules you need to run a basic text-to-text version of ADvISER. We suggest to create a
virtual environment from the top level directory, as shown below, followed by installing the necessary packages.


1. (Requires pip or pip3) Make sure you have virtualenv installed by executing

.. code-block:: bash

    python3 -m pip install --user virtualenv

2. Create the virtual environment (replace envname with a name of your choice)

.. code-block:: bash

    python3 -m venv <path-to-env>

3. Source the environment (this has to be repeated every time you want to use ADVISER inside a
new terminal session)

.. code-block:: bash

    source <path-to-env>/bin/activate

4. Install the required packages

.. code-block:: bash

    pip install -r requirements_base.txt 
 
(NOTE: or requirements_multimodal.txt if you want to use ASR / TTS)


5. Navigate to the adviser folder

.. code-block:: bash

    cd adviser

and, to make sure your installation is working, execute


.. code-block:: bash

    python run_songfinder_chat.py songfinder
    
You can type text to chat with the system (confirm your utterance by pressing the ``Enter``-Key once) or type ``bye`` (followed by pressing the ``Enter``-Key once) to end the conversation.


How to cite
===========
If you use or reimplement any of this source code, please cite the following paper:

.. code-block:: bibtex

   @InProceedings{
    title =     {ADVISER: A Toolkit for Developing Multi-modal, Multi-domain and Socially-engaged Conversational Agents},
    author =    {Chia-Yu Li and Daniel Ortega and Dirk V{\"{a}}th and Florian Lux and Lindsey Vanderlyn and Maximilian Schmidt and Michael Neumann and Moritz V{\"{o}}lkel and Pavel Denisov and Sabrina Jenne and Zorica Karacevic and Ngoc Thang Vu},
    booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL 2020) - System Demonstrations},
    publisher = {Association for Computational Linguistics},
    location =  {Seattle, Washington, USA},
    year =      {2020}
    }

License
=======
Adviser is published under the GNU GPL 3 license.
