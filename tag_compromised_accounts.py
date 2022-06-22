#!/usr/bin/env python
import sys
COUNTER = "chaine_de_caractères_unique_pour_le_comptage"

if len(sys.argv) != 3:
    print("Usage: {} <hashlist.ntds> <potfile>".format(sys.argv[0]))
    print("\nNote: potfile entries should be formatted as follows: <hash>:<cleartext password> (hashcat style potfile)")
    exit()
#vérifie si la ligne du fichier ntds contient un des hashs crackés, cad vérifie si le compte est compromis et retourne le nombre d'occurence d'un mot de passe cassé
def is_cracked_hash(line, cracked_hashes, duplicates):
    occurrence = 0
    ret = False
    
    for hash in cracked_hashes:
        splitted_hash = hash.split(':')[0] 
        if splitted_hash in line:
            ret = True
            full_hash = hash
            break
    
    if (ret is True and (full_hash in duplicates)):
        duplicates[full_hash] += 1
        duplicates[COUNTER] += 1
        
    elif (ret is True):
        duplicates[full_hash] = 1
        duplicates[COUNTER] += 1
        
    return ret

outfile = open("listes_des_utilisateurs_compromis.txt", "w")
duplicates = {}
duplicates[COUNTER] = 0

with open(sys.argv[2], 'r') as potfile:
    cracked_hashes = potfile.readlines()

with open(sys.argv[1], 'r') as hashlist:
    lines = hashlist.readlines()
    for line in lines:
        if is_cracked_hash(line, cracked_hashes, duplicates):
            outfile.write(line.rstrip('\n') + "\t\tMot de passe cassé !\n")
        else:
            outfile.write(line)

    print("\n{} comptes utilisateurs ont été compromis.\n".format(duplicates[COUNTER]))
    duplicates.pop(COUNTER)
    
    print("[Doublons]\n")
    #print("[Password duplicates]\n")
    for passwd, occurrence in duplicates.items() :
        if occurrence > 1:
            split = passwd.strip('\n').split(':')
            #print("The following password is used {} times: {} ({})".format(occurrence, split[1], split[0]))
            print("Le mot de passe suivant est utilisé par {} utilisateurs: {} ({})".format(occurrence, split[1], split[0]))
    outfile.close()
    potfile.close()
    hashlist.close()
