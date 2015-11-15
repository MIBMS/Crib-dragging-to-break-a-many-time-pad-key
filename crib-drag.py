#!/usr/bin/env python2.7

'''
Alice uses the same one time pad key 11 times. We use crib dragging to
break the cipher. We guess a word (crib) that appears in the first message, 
encode it hex. 
Then we separately xor the first two ciphertexts together, since the key is
xored with itself, we get a xor of the first two plaintexts. Then we xor the 
encoded word we had earlier at each position of the xored ciphertexts. If the
word matches the word at the right position, the word in the other plaintext 
appears since the two words xor each other out.
'''

ciptexts = []

f = open("Ciphertexts.txt", "r")
for line in f.read().splitlines():
    ciptexts.append(line)

f.close()

target_ciphertext = "32510ba9babebbbefd001547a810e67149caee11d945cd"\
"7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e7"\
"7472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"

ciptext = [x.decode("hex") for x in ciptexts]
target_ciptext = target_ciphertext.decode("hex")
keylist = ["_"]*len(target_ciptext)



#strxor function code from assignment instructions
# ord to ASCII code, xor, then back to ASCII (chr)

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])
        
def charxor(a,b):
    return chr(ord(a) ^ ord(b))
    
def process_response(question, accept_range, escape):
    processed_response = ""
    passed = False
    while not passed:
        response = raw_input(question)
        try:
            processed_response = int(response)
            if processed_response in accept_range:
                passed = True
            else:
                print "Number is outside acceptable range. Please try again or type 'esc' to quit." 
        except ValueError:
            for i in range(len(escape)):
                if response == escape[i]:
                    processed_response = escape[i]
                    passed = True
                    break
            else:
                if response in accept_range:
                    processed_response = response
                    passed = True
                else:
                    print "Invalid response. Please try again or type 'esc' to quit."
                               
    return processed_response
    
def position_response(xor,ciptext_response):
    crib = raw_input("Enter text that you think is in plaintext \
%s or the target plaintext:\n" % ciptext_response)

    for i in range(len(xor)):
        print "Position ", i, ": ", strxor(xor[i:],crib)
    
    position = process_response("At which position does the output \
make the most sense? Enter the position (from 0 to %s), 'none' for no match, \
or 'esc' to quit: \n" %(len(xor)-1), range(len(xor)), ("esc","none"))

    if position == "none":
        position, crib = position_response(xor, ciptext_response)

    return position, crib

    
def print_ciptext():
    display_key = ""
    dis_ciptextlst = []
    dis_target_ciptextlst = ["_"]*len(target_ciptext)
    dis_ciptext = []

    
    for i in range(len(keylist)):
        display_key = display_key + keylist[i]
    for j in range(len(ciptext)):
        dis_ciptext.append(strxor(ciptext[j],display_key))
        dis_ciptextlst.append(["_"]*len(ciptext[j]))
    for i in range(len(keylist)):                    
        if keylist[i] != "_":
            for j in range(len(dis_ciptextlst)):
                dis_ciptextlst[j][i] = dis_ciptext[j][i]
            dis_target_ciptextlst[i] = charxor(target_ciptext[i], keylist[i])
            
    for j in range(len(dis_ciptextlst)):
        dis_ciptext[j] = "".join(dis_ciptextlst[j])
    dis_target_ciptext = "".join(dis_target_ciptextlst)
    
    print "Your ciphertexts now look like these: "
    for i in range(len(dis_ciptext)):
        print "Ciphertext ", i, ":\n", dis_ciptext[i], "\n"
    print "Your key is now:\n", display_key, "\n"
    print "Your target ciphertext looks like this:\n", dis_target_ciptext, "\n"



while True:   
    
    print_ciptext()
    
    ciptext_response = process_response("Which ciphertext do you want to xor with the \
target ciphertext? Enter the ciphertext no. (0-9) or 'esc' to quit:\n", range(10), ("esc",))

    if ciptext_response == "esc":
        break
    
    xor = strxor(ciptext[ciptext_response], target_ciptext)
        
    (position, crib) = position_response(xor, ciptext_response)
    
    if position == "esc":
        break
    
    choose = process_response("Do you think the understandable output above \
comes from plaintext %s or the target plaintext? Enter 'p' for plaintext %s, 't' for \
target plaintext and 'esc' to quit:\n" % (ciptext_response, ciptext_response), ['p','t'], ("esc",))

    if choose == "esc":
        break
    elif choose == 'p':
        for i in range(len(crib)):
            if position+i <= min(len(target_ciptext), len(keylist))-1:
                keylist[position+i] = charxor(crib[i], target_ciptext[position+i])
    else:
        for i in range(len(crib)):
            if position+i <= min(len(ciptext[ciptext_response]), len(keylist))-1:
                keylist[position+i] = charxor(crib[i], ciptext[ciptext_response][position+i])
    
    print_ciptext()
        
    choose2 = process_response("Check the other ciphertexts. Do they all make sense? If they don't, \
then you should switch your answer. Press 'S' to switch your previous answer, 'N' to \
leave it be, 'esc' to quit:\n", ['s','n'], ("esc",)) 
    
        
    if choose2 == "esc":
        break
    elif choose2 == 's':
        if choose == 't':
            for i in range(len(crib)):
                if position+i <= min(len(target_ciptext), len(keylist))-1:
                    keylist[position+i] = charxor(crib[i], target_ciptext[position+i])
        else:
            for i in range(len(crib)):
                if position+i <= min(len(ciptext[ciptext_response]), len(keylist))-1:
                    keylist[position+i] = charxor(crib[i], ciptext[ciptext_response][position+i])



    






