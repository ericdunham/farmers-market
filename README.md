# Welcome to Farmer's Market!
[![Build Status](https://travis-ci.org/ericdunham/farmers-market.svg?branch=master)](https://travis-ci.org/ericdunham/farmers-market)
[![Code Climate](https://codeclimate.com/github/ericdunham/farmers-market/badges/gpa.svg)](https://codeclimate.com/github/codeclimate/codeclimate)
[![Coverage Status](https://coveralls.io/repos/github/ericdunham/farmers-market/badge.svg?branch=master)](https://coveralls.io/github/ericdunham/farmers-market?branch=master)

## Summary

This is a basic implementation of a checkout system for the farmer's market. Currently, baskets can be submitted, registers can be created and totaled up, and all appropriate discounts can be applied.

## Documentation

The full documentation for the project can be [viewed online](https://ericdunham.github.io/farmers-market/). It can also be generated with `make && make docs`. After generating the documentation successfully, a message will be shown like:
> Build finished. The HTML pages are in \_build/html.

By default, all documentation is generated in HTML and is available at `docs/_build/html/index.html` after generation.

## Testing

Testing for this project is done via [tox](https://tox.readthedocs.io/en/latest/) and can be run with `make test`. The previous command is simply a convenient alias for `tox`, which must be installed prior to running this command, or it will explode. Alternately, if [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) are installed, the tests can be run with `docker-compose up --build test` (the `--build` flag can be left off subsequent test runs, unless the base image changes).
