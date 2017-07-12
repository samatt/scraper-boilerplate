
## Scraper Boilerplate

Tired of having to modify old projects everytime I need a new scraper with all the things. Currently setup to use Selenium to scrape and firbase to store. Look at `config.yaml.smp` for things you can set.

Need to put it in a container so I don't need to deal with 👇🏽. 

## VPS config 
Go [here](https://github.com/SeleniumHQ/selenium/blob/master/py/docs/source/index.rst#drivers) to fix `No such file or directory: 'geckodriver`

```
Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it's in your PATH, e. g., place it in /usr/bin or /usr/local/bin.
```

  - Geckodriver min requirement: v0.16
