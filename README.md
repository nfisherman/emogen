# emogen
A python command-line utility to generate a random emo username.

## Dependencies

Python > 3.10

## Usage

```
>>> import emogen, pathlib
>>> gen = emogen.EmoGen(pathlib.Path('sources'))
>>> for i in range(5):
...     print(gen.generate(i, i, i))
... 
_th3_ang3l_fr0m_y0ur_nightm4re_
concreteemo
_myownworsten3my_
W0undedW4rriorPrinc3ss
xXstille4tinglunchal0neXx
```

Alternatively, run the script from your terminal emulator to generate a name:
```
python3 -m emogen
```

## References

[1] M. Burford, “100+ Catchy Emo Usernames,” Thought Catalog. Accessed: Apr. 03, 2024. [Online]. Available: https://web.archive.org/web/20240404030841/https://thoughtcatalog.com/molly-burford/2022/01/100-emo-usernames-for-social-media/
