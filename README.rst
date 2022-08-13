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

For details, please see the README of the official ADVISER repository: https://github.com/DigitalPhonetics/adviser/


Run the conDUCKtor songfinder dialog system
===========================================

You can run the conDUCKtor system with the following command:

.. code-block:: bash

    python run_songfinder_chat.py songfinder
    
You can type text to chat with the system (confirm your utterance by pressing the ``Enter``-Key once) or type ``bye`` (followed by pressing the ``Enter``-Key once) to end the conversation. (If the number of dialogs is set to more than 1, the conversation will restart after typing ``bye``. In this case, you can terminate the system via ``Ctrl+C``.)


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
