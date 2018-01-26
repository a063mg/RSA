from django.http import HttpResponse
from django.shortcuts import render
from requests import get, post

def home(req):
    return render(req, 'index.html', {})

def ifint(integer):
    integer = str(integer)
    lst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if integer == '':
         return False
    else:
        ifinteger = True
        for i in range(len(integer)):
            if integer[i] not in lst:
                ifinteger = False
        return(ifinteger)

def issimple(num):
    if num == 1:
        return False
    else:
        lst = list(range(0, num))
        i = 2
        while i < num:
            if lst[i] != 0:
                if num%lst[i] == 0:
                    return False
                for j in range(i, num, i):
                    lst[j] = 0
            i += 1
        return True

def nod(a, b):
        return(a%b == 0)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in list(range(3, int(num**0.5)+2, 2)):
        if num % n == 0:
            return False
    return True

def bpow(x, n, m):
  count=1;
  if not n:
    return 1
  while n:
    if n%2==0:
      n /= 2;
      x*=x;
      x %= m;
    else:
      n -= 1;
      count*=x;
      count %=m;
  return count % m

def find_special_number(n):
    num = 0 
    while num < n+1:
        if is_prime(num):
            if n%num != 0:
                e = num
                return e
        num += 1
                

def genkey(p, q):
    # generating keys

    n = p*q
    N = (p-1)*(q-1)

    e = 0 

    # finding special number
    e = find_special_number(N)
    d = mulinv(e, N)

    return(e, n, d, n)

def encode(e, n, text):
    # Converting texr 2 int
    splitext = []
    for char in text:
        splitext.append(str(ord(char)))

    # Encrypting text
    code = ''
    i = 0
    for char in splitext:
        m = int(char)
        code += str(bpow(m, e, n))
        code += ' '

    return code

def decode(e, n, code):
    # Decrypting text
    word = ''
    intext = []
    for char in code:
        m = int(char)
        intext.append(int(bpow(m, e, n)))

    # Converting int 2 text
    for char in intext:
        if not(char >= 65536):
            word += chr(char)
        else:
            return('False')
    return word

def contact_gen_key(request):
    error = ''
    frst = ''
    scnd = ''
    if request.POST:
        frst = request.POST.get('first')
        scnd = request.POST.get('second')
        if not(ifint(frst) and ifint(scnd)):
            error = 'Both numbers must be integer'
        else:
            frst = int(frst)
            scnd = int(scnd)
            if not(is_prime(frst) and is_prime(scnd)):
                error = 'Both numbers must be simple'
            if (frst < 100) or (scnd < 100):
                error = 'Both numbers must be more than 100'
        if scnd == '':
            error = 'Enter second number'
        if frst == '':
            error = 'Enter first number'
        if not error:
            keys = genkey(frst, scnd)
            openedkey = '{}, {}'.format(keys[0], keys[1])
            closedkey = '{}, {}'.format(keys[2], keys[3])
            return render(request, 'genkey.html', {'error': error, 'first': frst, 'second': scnd, 'open': openedkey, 'closed': closedkey})
        
    return render(request, 'genkey.html', {'error': error, 'first': frst, 'second': scnd})

def encode_contact(request):
    error = ''
    text = ''
    key = ''
    frst = ''
    scnd = ''
    sep = ''
    code = ''
    if request.POST:        
        key = request.POST.get('key')
        text = request.POST.get('text')
        key = key.replace(',', '')
        keys = key.split()
        if len(keys) != 2:
            error = 'Key must contain 2 numbers'
        else:
            sep = ', '
            frst = keys[0]
            scnd = keys[1]
            if not(ifint(frst) and ifint(scnd)):
                error = 'Key numbers must be integer'
        if text == '':
            error = 'Enter your text'
        if key == '':
            error = 'Enter your keys'
        if not error:
            code = encode(int(frst), int(scnd), text)
            return render(request, 'encoder.html', {'error': error, 'text': text, 'first': frst+sep, 'second': scnd, 'code': code})
        
    return render(request, 'encoder.html', {'error': error, 'text': text, 'first': frst+sep, 'second': scnd})


def decode_contact(request):
    error = ''
    text = ''
    key = ''
    frst = ''
    scnd = ''
    sep = ''
    code = ''
    if request.POST:        
        key = request.POST.get('key')
        code = request.POST.get('code')
        key = key.replace(',', '')
        keys = key.split()
        if not(ifint(code.replace(' ', ''))):
            error = 'Code must contain only numbers and spaces'
        if len(keys) != 2:
            error = 'Key must contain 2 numbers'
        else:
            sep = ', '
            frst = keys[0]
            scnd = keys[1]
            if not(ifint(frst) and ifint(scnd)):
                error = 'Key numbers must be integer'
        if code == '':
            error = 'Enter your code'
        if key == '':
            error = 'Enter your keys'
        if not error:
            text = decode(int(frst), int(scnd), code.split())
            if text == 'False':
                error = 'Error, wrong keys, or code'
                text = ''
            return render(request, 'decoder.html', {'error': error, 'first': frst+sep, 'second': scnd, 'code': code, 'text': text})
        
    return render(request, 'decoder.html', {'error': error, 'code': code, 'first': frst+sep, 'second': scnd})


def rsa_contact(request):
    error = ''
    text = ''
    key = ''
    frst = ''
    scnd = ''
    sep = ''
    user = ''
    code = ''
    if request.POST:
        key = request.POST.get('key')
        code = request.POST.get('code')
        text = request.POST.get('text')
        key = key.replace(',', '')
        keys = key.split()
        if not(ifint(code.replace(' ', ''))):
            error = 'Code must contain only numbers and spaces'
        if len(keys) != 2:
            error = 'Key must contain 2 numbers'
        else:
            sep = ', '
            frst = keys[0]
            scnd = keys[1]
            if not(ifint(frst) and ifint(scnd)):
                error = 'Key numbers must be integer'
        if code == '':
            error = 'Enter your code'
        if key == '':
            error = 'Enter your keys'
        if text == '':
            error = 'Enter your text'
        if not error:
            code = decode(int(frst), int(scnd), code.split())
            if text != 'False':
                if code == text:
                    user = 'True'
                else:
                    user = 'False'
            else:
                user = 'False'
            return render(request, 'user.html', {'user': user})
        
    return render(request, 'rsa.html', {'error': error, 'code': code, 'first': frst+sep, 'second': scnd, 'text': text})



