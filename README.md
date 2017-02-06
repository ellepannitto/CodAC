# CodAC
CodAC - a coder agreement calculator
---
Lo script produce un'analisi sull'agreement tra annotatori, utilizzando la libreria nltk.

I file di input devono essere in un formato tipo conll (un token per riga, campi separati da tab)	

L'agreement può essere calcolato su due tipi di annotazioni:
- categoriale (comando cat)
- relazionale (comando rel)

Nel primo caso, è possibile specificare la colonna del file contenente l'informazione da testare (default: colonna 4, in cui è solitamente presente l'annotazione morfosintattica).

Per calcolare l'agreement sull'annotazione morfosintattica tra i file annotatore1.conllu e annotatore2.conllu nella cartella esempi:

	$ python codac.py esempi/annotatore1.conllu esempi/annotatore2.conllu cat

o, se si vuole specificare di utilizzare la colonna 3:

	$ python codac.py esempi/annotatore1.conllu esempi/annotatore2.conllu cat -c 3

Nel secondo caso, è possibile specificare le colonne (esattamente 2) del file che contengono le informazioni da testare, la prima contenente l'id dell'elemento con cui si instaura la relazione (es. testa sintattica), la seconda contenente la categoria della relazione (default: colonne 7 e 8).

	$ python codac.py esempi/annotatore1.conllu esempi/annotatore2.conllu rel

o, se si vuole specificare di utilizzare le colonne 3 e 4:

	$ python codac.py esempi/annotatore1.conllu esempi/annotatore2.conllu cat -c 3 4

È possibile escludere alcuni tag dal computo, tramite il flag -e. Per esempio se si vogliono escludere i tag "NOUN" e "PROPN", si può specificare
	
	$ python codac.py -e NOUN,PROPN esempi/annotatore1.conllu esempi/annotatore2.conllu cat
	
Si possono stampare informazioni aggiuntive mediante il flag -p, come:
	- matrice di confusione (option M)
	- indici statistici aggiuntivi (option S)
	
Per esempio se si vuole stampare solo la matrice si può eseguire:
	
	$ python codac.py -p M esempi/annotatore1.conllu esempi/annotatore2.conllu cat
	
Se si vogliono stampare la matrice e le metriche:

	$ python codac.py -p M,S esempi/annotatore1.conllu esempi/annotatore2.conllu cat

Di default viene stampato solo il valore del kappa di Cohen

Per ottenere un breve riepilogo delle opzioni si può usare -h.

#TODO:
comando per file di mappa
