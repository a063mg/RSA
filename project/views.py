from django.http import HttpResponse
from django.shortcuts import render
from requests import get, post

def home(req, text):
    return HttpResponse('Hell0 {}!'.format(text))

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
        lst = range(0, num)
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

def genkey(p, q):

    n = p*q
    N = (p-1)*(q-1)

    e = 0 

    a = list(range(n+1))
    a[1] = 0
    lst = [1]

    i = 2
    while i <= N:
        if a[i] != 0:
            if nod(N, a[i]) == False:
                e = a[i]
                break;
        for j in list(range(i, n+1, i)):
            a[j] = 0
        i += 1

    d = mulinv(e, N)

    return(e, n, d, n)


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
            if not(issimple(frst) and issimple(scnd)):
                error = 'Both numbers must be simple'
            if frst < 100 or scnd < 100:
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
