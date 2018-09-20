# Asyncio Playground

This sample script shows how much quicker asyncio than working with standard synchronous code. The example performs a web scrape of fightmetric.com to return data on all UFC fighters and print them out nicely to the terminal. The code allows you to do the scrape both synchronously and asynchronously using asyncio so that you can see the different between the two in terms of speed.

Please note that this code is intended for educational uses only and should not be used in production. Please also use caution and consideration when scraping websites. This example throttles the number of requests made to the server to 5 a second using asyncio's semaphore.

## Requirements
* Python 3.7+
* GCC compiler (for make)

## Getting started

* Clone the repository ``git clone git@github.com:robcharlwood/asyncio-playground.git``
* Run ``make install``

Install will create a virtualenv in the same directory as the checked out code and then installs requirements.

Once everything has installed you can run the script in two ways:

* Asynchronously - with ``make run``
* Synchronously - with ``make run-sync``

Enjoy!

## Authors

* **Rob Charlwood**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

![Mwaaah!](https://media.giphy.com/media/l3q2LH45XElELRzRm/giphy.gif "Mwaaah!")
