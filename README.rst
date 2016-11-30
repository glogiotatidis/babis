===============================
babis
===============================


.. image:: https://img.shields.io/pypi/v/babis.svg
        :target: https://pypi.python.org/pypi/babis

.. image:: https://img.shields.io/travis/glogiotatidis/babis.svg
        :target: https://travis-ci.org/glogiotatidis/babis

.. image:: https://readthedocs.org/projects/babis/badge/?version=latest
        :target: https://babis.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/glogiotatidis/babis/shield.svg
     :target: https://pyup.io/repos/github/glogiotatidis/babis/
     :alt: Updates


Decorator that pings URLs before and after executing the wrapped obj.


* Free software: GNU General Public License v3
* Documentation: https://babis.readthedocs.io.

Features
--------

* Pre and After run pings
* Custom user agent
* Silent failures
* Rate limiting

Usage
-----

Ping after successful execution. Useful to monitor cron jobs with services like
`Dead Man's Snitch`_ or `HealthChecks.io`_::

   @babis.decorator(ping_after='http://healthchecks.io/XXX')
   def cron_job():
     pass

Some services support pre and after hooks to measure the running time::

   @babis.decorator(ping_before='http://healthchecks.io/XXX', ping_after='http://healthchecks.io/XXX')
   def measured_cron_job():
     pass

You can also send a POST instead of the default GET::

   @babis.decorator(ping_before='http://healthchecks.io/XXX', method='post')
   def cron_job_with_post():
     pass

And if you don't care if the ping fails, silence the errors::

   @babis.decorator(ping_before='http://healthchecks.io/XXX', silent_failures=True)
   def cron_job_silent_failure():
     pass

You can also rate limit the number of pings send to play nice with third party
services, let's say to at most 1 call in 5 minutes::

   @babis.decorator(ping_after='http://healthchecks.io/XXX', rate='1/5m')
   def cron_job_silent_failure():
     pass


or 24 calls per day::

   @babis.decorator(ping_after='http://healthchecks.io/XXX', rate='24/1d')
   def cron_job_silent_failure():
     pass


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Dead Man's Snitch`: https://deadmanssnitch.com/
.. _`HealthChecks.io`: https://healthchecks.io/
