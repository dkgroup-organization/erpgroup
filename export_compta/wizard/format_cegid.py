# -*- coding: utf-8 -*-

CEGID_LINE_LENGTH = 232

CEGID_FORMAT_M = """type;1;1;M;Type
compte;2;8;;Numéro de compte
journal2;10;2;;Code journal sur 2 caractère
folio;12;3;000;folio
date;15;6;;Date écriture (JJMMAA)
code_libelle;21;1;;Code libellé 21 1
libelle_libre;22;20;;Libellé libre 22 20
sens;42;1;;Sens Débit/Crédit (D/C) 42 1
montant;43;13;;Montant en centimes signé (position 43=signe) 43 13
compte_contrepartie;56;8;;Compte de contrepartie 56 8
date_echeance;64;6;;Date échéance (JJMMAA) 64 6
lettrage;70;2;;Code lettrage 70 2
statistiques;72;3;;Code statistiques 72 3
piece5;75;5;;N° de pièce sur 5 caractères maximum 75 5
affaire;80;10;;Code affaire 80 10
quantite;90;10;;Quantité 1 90 10
piece8;100;8;;Numéro de pièce jusqu'à 8 caractères 100 8
devise;108;3;EUR;Code devise (FRF ou EUR, Espace = FRF, ou Devise) 108 3
journal3;111;3;;Code journal sur 3 caractères 111 3
code_tva_gestion;114;1;O;Flag Code TVA géré dans l'écriture = O (oui) 114 1
code_tva;115;1;;Code TVA 115 1
calcul_tva;116;1;D;Méthode de calcul TVA
Libelle;117;30;;Libellé écriture sur 30 caract. (blanc si renseigné en 22 sur 20
code_tva2;147;2;;Code TVA sur 2 caractères 147 2
piece10;149;10;;N° de pièce alphanumérique sur 10 caract. 149 10
Reserve;159;10;;Réservé
montant_devise;169;13;;seulement Montant dans la devise (en centimes signés position 169=signe) 
piece_jointe;182;12;;QC Windows Pièce jointe à l'écriture, nom du fichier sur 8 caractères + 169=signe) 
quantite2;194;10;;Quantité 2 194 10
numuniq;204;10;;NumUniq 204 10
operateur;214;4;;Code opérateur 214 4
date_sys;218;14;;Date système 218 14"""
