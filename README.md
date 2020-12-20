# Covid Cough Challenge (bitsxlamarato's Hackaton Late Dec 2020)
## Covid detection by sending audio in Telegram.
This work can was splitted in two sub-projects:
  * **Machine Learning**:
    *  Model has been created to classify coughs types from the frequency domain representation of speech recordings, obtained via Fast Fourier Transform (FFT). 
  * **Telegram Bot**:
    * Telegram receives audio via user, and then it is classified to the different types of cough. 
### Perequisites
**Python 3.8.0** with [this packages](requirements.txt)

## Built With
* [NeoVim](https://neovim.io/) - Vim-based text editor
* [Python 3.8](https://www.python.org/downloads/release/python-380) - Programming language

### Some improvements that can be done
- [ ] Probably a better model to predict the data.
- [ ] A better user interface in telegram, using inline-keyboards p.e.

## Authors
* **Diego Delgado** - [@dieg666](https://github.com/dieg666)
* **Daniel Gómez** - [@daniel-og](https://github.com/daniel-og)



