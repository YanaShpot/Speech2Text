# Speech2Text
This is Speech to Text project for ML course at UCU
## Intoduction
Working with audio files is not as simple as it might look from the first sight. Note that wav audio recording is just a vector with amplitudes in each time interval. Thus firtstly we have to decide how our data should be represented in order to extract valuable information and have the ability to train a model on those extracted features. Moreover you have to overcome almost limitless challenges: bad quality microphones, background noise, reverb and echo, accent variations, and on and on. All of these issues need to be present in your training data to make sure the neural network can deal with them. 
## Related work
### Feature extraction
There are different aproaches of how the audio data can be used. In some approaches even raw audio data is used but it is commonly assumed that such data contains too much redundant information. Two popular ways to extract features are Mel-frequency cepstral coefficients and spectograms.
#### Spectrograms:
A spectrogram is the frequency domain representation of the audio signal through time. It's created by splitting the audio signal into component frequencies and plotting them with respect to time. The intensity of color in the spectrogram at any given point indicates the amplitude of the signal.
#### Mel-frequency cepstral coefficients (MFCCs):
In sound processing, the mel-frequency cepstrum (MFC) is a representation of the short-term power spectrum of a sound, based on a linear cosine transform of a log power spectrum on a nonlinear mel scale of frequency.
MFCCs are commonly derived as follows:

* Take the Fourier transform of (a windowed excerpt of) a signal.
* Map the powers of the spectrum obtained above onto the mel scale, using triangular overlapping windows.
* Take the logs of the powers at each of the mel frequencies.
* Take the discrete cosine transform of the list of mel log powers, as if it were a signal.
* The MFCCs are the amplitudes of the resulting spectrum.

### Acustic Model:
The input data in speech recognition is a sequence of observations in the form of frame vectors from regular time intervals. The desired output is a series of symbols: phonemes, graphemes, or words. The basic problem is that the number of frames does not have a predictible correspondence to the number of the output symbols. For example, if we assume 20ms per frame, the following audio signals of the word "speech" spoken at two different speeds have about 300 frames in the first example and something like 850 frames in the second example, yet they should both be decoded as the six-letter word, "speech".
## Data
## Algorithm
## Demo
## Installation
## Conclusions & Further Work
## References
