# Violent Python - TJ. O'Connor
## Chapter 1
Created 2 scripts to crack Unix passwords, both modern and older versions. I could also understand better about Zip encryption and how to crack password-protected Zip files using the [pyzipper](https://pypi.org/project/pyzipper/) library, which is not mentioned in the book, but its the modern replacement of the zipfile library. The last could not test passwords against AES-encrypted zip files. In this zip file password cracker I used argparse, a simple threading implementation, and pyzipper. 
### UNIX Password Cracker (using deprecated "crypt" module - requires Python version < 3.12.13)
for "older" Unix systems (/etc/passwd)
`./chapter1/unix_password_cracker.py`
  
for "modern" Unix systems (/etc/shadow)
`./chapter1/modern_unix_password_cracker.py`
### Zip File Password Cracker
Used pyzipper instead of zipfile library to be able to test AES-encrypted zip files.

---
## Chapter 2
pg.41



