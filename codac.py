import sys
import argparse
import os

import codecs
import collections
import nltk
import pprint
	
def check_files_existence(fileslist):
	
	nonexistentfiles = []
	
	for f in fileslist:
		if not os.path.isfile(f):
			nonexistentfiles.append(f)
	
	if len(nonexistentfiles)>0:
		sys.exit("I file:\n\t- "+"\n\t- ".join(nonexistentfiles)+"\nnon esistono")
	
	
def check_formato (f, col):
	
	with codecs.open(f, "r", "utf-8") as fobj:
		i=0
		for line in fobj:
			i+=1
			if not line == "\n":
				splitline = line.split()
				
				#~ print "here", splitline, len(splitline)
				
				if not len(splitline) >= col:
					sys.exit("Formato del file "+f+" non corretto. Errore alla riga "+str(i))

	if i == 0:
		sys.exit("Formato del file "+f+" non corretto. File vuoto")
		

def print_kappa (est, label = "Agreement"):
	
	print label
	print "Kappa di Cohen:", est.kappa()
	
def print_stats (est, label = "Altre misure"):
	
	print label
	print "Alpha:", est.alpha()
	print "Pi:", est.pi()
	print "S:", est.S()
	
def print_matrice (mat, label = "Matrice di confusione"):
	
	print label
	
	labels = set()
	
	for el, v in mat.items():
		labels.add(el)
		for k in v:
			labels.add(k)
	
	lens = [len(el) for el in sorted(labels)]
	maxlen = max(lens)
	
	
	#~ strs = " ".join("{"+"{0}:^{1}".format(i, maxlen)+"}" for i in range(len(labels)+1))
	strs = "{"+"{0}:^{1}".format(0, maxlen)+"} "+" ".join("{"+"{0}:^{1}".format(i+1, lens[i])+"}" for i in range(len(labels)))
	
	#~ print strs	
		
	print strs.format(" ", *sorted(labels))


	for x in sorted(labels):
		print strs.format(x, *(mat[x].get(y, '-') for y in sorted(labels)))
			

def agreement_sintassi (f1, f2, columns_list, tags_to_exclude, to_print, m=None):
	
	
	las_agreement = []
	uas_agreement = []
	la_agreement = []
	
	dict_label=collections.defaultdict(lambda: collections.defaultdict(str))
	dict_head=collections.defaultdict(lambda: collections.defaultdict(str))
	
	for doc in [f1, f2]:
							
		with codecs.open(doc, "r", "utf-8") as f:
			
			line_no = 1
			tok_id = 1
			fr_id = 1
			
			for line in f:
				
				if not line == "\n":
					
					cols = line.split()
					
					testa = cols[columns_list[0]-1]
					etichetta = cols[columns_list[1]-1]
					
					tid = str(line_no) 						
					
					
					if not etichetta in tags_to_exclude:
						tripla_la = (doc, tid, etichetta) 
						tripla_las = (doc, str(fr_id)+"_"+str(tok_id), testa+"_"+etichetta) 
						tripla_uas = (doc, tid, testa) 
						
						uas_agreement.append (tripla_uas)				
						las_agreement.append (tripla_las)
						la_agreement.append (tripla_la)	
					
					dict_label[tid][doc] = etichetta
					dict_head[tid][doc] = testa		
					
					tok_id+=1
				else:
					fr_id +=1
					tok_id = 1
					
				line_no+=1
				
	est_las = nltk.agreement.AnnotationTask(las_agreement)
	est_uas = nltk.agreement.AnnotationTask(uas_agreement)
	est_la = nltk.agreement.AnnotationTask(la_agreement)


	matrice_labels = collections.defaultdict(lambda: collections.defaultdict(int))
	
	for tid in dict_label:
		matrice_labels[dict_label[tid][f1]][dict_label[tid][f2]]+=1
	
	
	print f1, "-", f2
	
	print 
	
	print_kappa(est_las, "Labeled Attachment Score")
	print
	print_kappa(est_uas, "Unlabeled Attachment Score")
	print 
	print_kappa(est_la, "Label Accuracy")
	print 

	
	if "M" in to_print:
		print_matrice(matrice_labels)
		print
		
		if m:
			new_matrice = collections.defaultdict(lambda: collections.defaultdict(int))
			
			for k1, d in matrice_labels.items():
				for k2, v in d.items():
					new_matrice[m[k1]][m[k2]] += v
			
			print_matrice(new_matrice, "Matrice mappata")
			print
	
	if "S" in to_print:
		print_stats(est_las, "Labeled Attachment Score")
		print 
		print_stats(est_uas, "Unlabeled Attachment Score")
		print
		print_stats(est_la, "Label Accuracy")
		print
	

def agreement_morfosintassi (f1, f2, column, tags_to_exclude, to_print, m=None):
	
	triples_list_coarse = []
	
	dict_coarse = collections.defaultdict(lambda: collections.defaultdict(str))

	for doc in [f1, f2]:
			
		with codecs.open(doc, "r", "utf-8") as f:
			line_no = 1
			tok_id = 1
			fr_id = 1
				
			for line in f:
				
				if not line == "\n":	
					cols = line.split()
					
					coarse_tag = cols[column[0]-1]
									
					#~ tid = str(fr_id)+"_"+str(tok_id) 	
					tid = str(line_no) 	

					tripla_c = (doc, tid, coarse_tag) 
					
					if not coarse_tag in tags_to_exclude:				
						triples_list_coarse.append(tripla_c)
			
			
					#~ corpus[tid][doc] = 
					
					dict_coarse[tid][doc] = coarse_tag
						
					tok_id+=1
				else:
					fr_id +=1
					tok_id = 1
					
				line_no+=1
		
	est_coarse = nltk.agreement.AnnotationTask(triples_list_coarse)
	
	matrice_coarse = collections.defaultdict(lambda: collections.defaultdict(int))
	
	for tid in dict_coarse:
		matrice_coarse[dict_coarse[tid][f1]][dict_coarse[tid][f2]]+=1
	
	
	print f1, "-", f2
	
	print
	
	print_kappa(est_coarse)

	print
	
	if "M" in to_print:
		print_matrice(matrice_coarse)
		print
		
		if m:
			new_matrice = collections.defaultdict(lambda: collections.defaultdict(int))
			
			for k1, d in matrice_coarse.items():
				for k2, v in d.items():
					new_matrice[m[k1]][m[k2]] += v
			
			print_matrice(new_matrice, "Matrice mappata")
			print


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Pairwise agreement')

	parser.add_argument("-e", "--exclude", metavar = "TAG", nargs = "+", action = "store", type = str, default = [],
						help = "specifica tag da escludere")

	parser.add_argument("-m", "--mappa", metavar = "file", action = "store", type = str,
						help = "specifica mappa per i tag")

	parser.add_argument("-p", "--print", dest = "to_print", metavar = "OPTION", action = "store", type = str, default = "M",
						help = "specifica quali informazioni aggiuntive stampare. Le opzioni sono 'M' -> matrice di confusione, \
						 'S' -> statistiche aggiuntive, 'E' -> riepilogo discordanze (su file serparato)")

	parser.add_argument('files', metavar='file', type=str, nargs='+',	help='lista di file')
							
	subparser = parser.add_subparsers (dest="tipo", help="tipo di analisi")
		
	parser_s = subparser.add_parser ("rel",  help="calcolo agreement relazionale (las, uas, la)")
	
	parser_s.add_argument('-c', '--columns', metavar = "COL", nargs = 2, action = "store", type = int, default=[7, 8],
						help='specifica le colonne su cui analizzare')

	parser_m = subparser.add_parser ("cat", help="calcolo agreement categoriale")
		
	parser_m.add_argument('-c', '--columns', metavar = "COL", nargs = 1, action = "store", type = int, default=[4],
						help='specifica le colonne su cui analizzare')
	


	args = parser.parse_args()	

	if args.mappa:
		mappa = collections.defaultdict(list)
		
		with codecs.open(args.mappa, "r", "utf-8") as fobj:
			for line in fobj:
				splitline = line.split(":")
				supertag = splitline[0]
				tags = splitline[1].split()
				
				mappa[supertag] = tags
				
		mappa_inversa = {v:k for k, el in mappa.items() for v in el}

		print mappa_inversa
		
	#controllo numero files >=2
	if len(args.files)<2:
		sys.exit("Specifica almeno due file")

	#controllo file esistano
	check_files_existence(args.files)
	
	#controllo formato dei file
	max_col = max(args.columns)
	#~ print max_col
	i = 0
	while i<len(args.files):
		f = args.files[i]
		check_formato(f, max_col)
		i+=1
	

		
		

	coppie = [(args.files[i], args.files[j]) for i in range(len(args.files)-1) for j in range(i+1, len(args.files))]
	
	get_agreement = agreement_morfosintassi if args.tipo == "categoriale" else agreement_sintassi
	
	for f1, f2 in coppie:
		if mappa_inversa:
			get_agreement(f1, f2, args.columns, args.exclude, args.to_print, m = mappa_inversa)
		else:
			get_agreement(f1, f2, args.columns, args.exclude, args.to_print)
