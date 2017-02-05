# CodAC
CodAC - a coder agreement calculator
---
Lo script produce un'analisi sull'agreement tra annotatori, utilizzando la libreria nltk.

L'agreement può essere calcolato su due tipi di annotazioni:
- categoriale
- relazionale

Nel primo caso, è possibile specificare la colonna del file contenente l'informazione da testare (default: colonna 4, in cui è solitamente presente l'annotazione morfosintattica).

Nel secondo caso, è possibile specificare le colonne del file che contengono le informazioni da testare, nel caso in cui vengano specificate devono essere due, la prima contenente l'id dell'elemento con cui si instaura la relazione (es. testa sintattica), la seconda contenente la categoria della relazione (default: colonne 7 e 8).

I file di input devono essere in un formato tipo conll (un token per riga, campi separati da tab)
