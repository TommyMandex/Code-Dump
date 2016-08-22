import sys
import chilkat

crypt = chilkat.CkCrypt2()

success = crypt.UnlockComponent("Anything for 30-day trial")
if (success != True):
    print(crypt.lastErrorText())
    sys.exit()

#  Set the encryption algorithm to "AES"
crypt.put_CryptAlgorithm("aes")

#  Indicate that the Galois/Counter Mode (GCM) should be used:
crypt.put_CipherMode("gcm")

#  KeyLength may be 128, 192, 256
crypt.put_KeyLength(128)

#  This is the 128-bit AES secret key (in hex format)
K = "feffe9928665731c6d6a8f9467308308"

#  This is the 16-byte initialization vector:
IV = "cafebabefacedbaddecaf888"

#  This is the additional data to be used as input to the GCM AEAD algorithm,
#  but is not included in the output.  It plays a role in the computation of the
#  resulting authenticated tag.
AAD = "feedfacedeadbeeffeedfacedeadbeefabaddad2"

#  The plain-text bytes (in hex format) to be encrypted.
PT = "d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39"

#  The expected cipher text (in hex format)
CT = "42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091"

#  The expected authenticated tag given the above inputs.
T = "5bc94fbc3221a5db94fae95ae7121a47"

#  Note: The above data are the values for test vector #4 from
#  the PDF document at: http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/gcm/gcm-spec.pdf

#  EncodingMode specifies the encoding of the output for
#  encryption, and the input for decryption.
#  It may be "hex", "url", "base64", or "quoted-printable".
crypt.put_EncodingMode("hex")

#  Set the secret key and IV
crypt.SetEncodedIV(IV,"hex")
crypt.SetEncodedKey(K,"hex")

#  Set the additional authenticated data (AAD)
success = crypt.SetEncodedAad(AAD,"hex")

#  For the purpose of duplicating the test vectors, we are using the EncryptEncoded method.
#  This method decodes the input string according to the encoding specified by the EncodingMode
#  property, which in this case is "hex".  The decoded bytes are encrypted using the mode specified
#  by the CipherMode property.  The resulting
#  encrypted bytes are encoded (again using the encoding mode specified by EncodingMode),
#  and the result is returned.
#  <b>Note:</b> The CipherMode property sets the block mode of operation (gcm, cfb, cbc, ofb, ecb, etc.)
#  for any of the Chilkat encryption/decryption methods (such as EncryptBytes, EncryptString,
#  CkEncryptFile, etc.)   Just because GCM mode is demonstrated with EncryptEncoded/DecryptEncoded,
#  does not imply that GCM mode is specific to only these methods.
ctResult = crypt.encryptEncoded(PT)
if (crypt.get_LastMethodSuccess() != True):
    print(crypt.lastErrorText())
    sys.exit()

#  Examine the result.  It should be the same (case insensitive) as our expected result:
print("computed result: " + ctResult)
print("expected result: " + CT)

#  Examine the authenticated tag. It should be the same (case insensitive) as our expected authenticated tag:
tResult = crypt.getEncodedAuthTag("hex")
print("computed authTag: " + tResult)
print("expected authTag: " + T)

#  -------------------------------------------------------------------------------------
#  Now let's GCM decrypt...
#  -------------------------------------------------------------------------------------

#  Before GCM decrypting, we must set the authenticated tag to the value that is expected.
#  The decryption will fail if the resulting authenticated tag is not equal (case insensitive) to
#  the expected result.
#  Note: The return value of SetEncodedAuthTag indicates whether the string passed was a valid
#  representation of the encoding specified in the 2nd arg.
success = crypt.SetEncodedAuthTag(T,"hex")

#  All of our properties (IV, secret key, cipher mode, and AAD) are already set from the code above...

#  So let's decrypt CT to and check to see if we get PT.
ptResult = crypt.decryptEncoded(CT)
if (crypt.get_LastMethodSuccess() != True):
    #  Failed.  The resultant authenticated tag did not equal the expected authentication tag.
    print(crypt.lastErrorText())
    sys.exit()

#  Examine the decrypted result.  It should be the same as our expected plaintext (case insensitive)
print("plaintext decrypted: " + ptResult)
print("plaintext expected:  " + PT)

#  Let's intentionally set the expected authenticated tag to an incorrect value.
#  The decrypt operation should fail:
tInvalid = "ffaabbbc3221a5db94fae95ae7121a47"

success = crypt.SetEncodedAuthTag(tInvalid,"hex")

ptResult = crypt.decryptEncoded(CT)
if (crypt.get_LastMethodSuccess() != True):
    #  Failed.  The resultant authenticated tag did not equal the expected authentication tag.
    print(crypt.lastErrorText())
