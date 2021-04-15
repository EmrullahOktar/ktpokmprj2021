from googletrans import Translator


trans = Translator()
cevirilmesi_gereken = "nice"# ocrden gelen yazi bu kısma eşitlenir

t = trans.translate(
    cevirilmesi_gereken, src="en", dest="tr"
)

print(f'Source: {t.src}')
print(f'Destination: {t.dest}')
print(f'{t.origin} -> {t.text}')

#lazım kısım t.text
print(t.text)





#ing = "mistakes"
#print(trans.translate(ing, src="en", dest="tr"))
#print(f'{t.origin} -> {t.text}')

