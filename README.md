# hashcat_potfile_correlator
Given a list of  extracted hashes (dumped with Impacket) and a hashcat potfile, this script generates:
* a list of users whose  account was cracked
* as well as a list containing duplicate passwords and their number.

Usage:
```
./tag_compromised_accounts.py <hashlist.ntds> <potfile>
```
