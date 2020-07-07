#!/usr/bin/env python

# RS256 JWT Generator
# v0.1 - @x90x90

import jwt
import datetime
import sys
import uuid

###################
# Standard Claims
###################

aud = ""
iss = ""
sub = ""

# Could do with automating these two bits, just need to pull the fingerprint from cert
x5t = ""
kid = ""

###################

def read_key_file(keyfile):
    data = open(keyfile).read()
    return data

# Not sure why I wrote this, it's not used o_O

def set_keys(prv_file, pub_file):
    prv_file = str(sys.argv[1])
    pub_file = str(sys.argv[2])
    prv_key = read_key_file(prv_file)
    pub_key = read_key_file(pub_file)
    return prv_key

def time_values():
    current_time = datetime.datetime.now() 
    # Set nbf value
    nbf_time = int(current_time.timestamp() )
    # Set iat value
    iat_time = int(current_time.timestamp() )
    # Set the exp value
    exp_time_delta = current_time + datetime.timedelta(minutes=10)
    exp_time = int(exp_time_delta.timestamp() )  
    return nbf_time,iat_time,exp_time

def unique_jti():
    jti_val = str(uuid.uuid4())
    return jti_val
    

def enc_jwt(aud,iss,sub,jti,nbf_time,iat_time,exp_time,prv_key,x5t,kid):
    encoded = jwt.encode({ "aud": aud,  "exp": exp_time,  "iss": iss,  "jti": jti,  "nbf": nbf_time,  "sub": sub}, prv_key, algorithm='RS256', headers={'x5t': x5t,'kid': kid})
    return encoded

def dec_jwt(encoded,pub_key):
    #Disable verification of the audience for test decode
    options = {'verify_aud': False, 'require_sub': True}
    decoded = jwt.decode(encoded, pub_key, algorithms='RS256',options=options)
    return decoded

if __name__== "__main__":

    if (len(sys.argv) != 3):
        print ('Usage: ' + str(sys.argv[0]) + ' <private key> <public key>')
        sys.exit()

    prv_key = read_key_file(sys.argv[1])
    pub_key = read_key_file(sys.argv[2])
    jti = unique_jti()
    nbf_time,iat_time,exp_time = time_values()

    encoded = enc_jwt(aud,iss,sub,jti,nbf_time,iat_time,exp_time,prv_key,x5t,kid)
    print (encoded)


    decoded = dec_jwt(encoded,pub_key)
    print (decoded)

