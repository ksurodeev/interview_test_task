import re
import binding   ### auto-generated by pybind module
import json

fairytale = binding.yc_Fairytale_repka__Fairytale()

Ded = fairytale.character.add('Dedka')
Ded.Age = 75

Dog = fairytale.character.add('Zhuchka')
Dog.Age = 4

Ovosh = fairytale.vegetable.add('Repa')
Ovosh.Mass = 10

print(json.dumps(fairytale.get()))

