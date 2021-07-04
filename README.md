# ledstrip

I made this to control my aoguerbe led strip lights from internet.
I only used this with a Raspberry Pi, but bluepy should run on x86 Debian Linux.

## Usage

Create a file called `config.py` and put something like this:

```python
CONFIG = {
    'MAC': 'lights mac address'
}
```

Put the bluetooth mac address of your lights, then run `server.py` and all should work