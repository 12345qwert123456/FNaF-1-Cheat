![screenshot](https://github.com/12345qwert123456/FNaF-1-Cheat/raw/main/images/screenshot.jpg)

# FNaF 1 Cheat
Cheat for game "Five Nights At Freddy's 1" based on frida.

Check for versions:
 - 1.131.0.0 (game version 1.132)

## Installation

1. Install frida for python
```
pip install frida
pip install frida-tools
```

[Official instruction](https://github.com/frida/frida#1-install-from-prebuilt-binaries)

## Usage

1. Start the game
2. Start the cheat
```
python cheat.py
```

### Options

| Option                 | Description                                                                                        |
|------------------------|----------------------------------------------------------------------------------------------------|
|1. Set energy           | Sets the energy to the specified value                                                             |
|2. Set time             | Sets the hour's value to the specified value                                                       |
|3. Freeze time          | Stops the clock from increasing                                                                    |
|4. Skip night           | Sets the hour value to 6 and ends the night                                                        |
|5. Show minutes         | Shows how much time is left until the hour changes                                                 |
|6. Hack door animation  | Just fun, breaks the animation of doors, the door may look closed but the game thinks it is closed |
|0. Exit                 | Exit                                                                                               |
