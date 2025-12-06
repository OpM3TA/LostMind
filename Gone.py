import marshal, zlib, types
from itertools import cycle


__wisdom__ = """
The river moves without haste, carrying the memory of mountains.
The wind speaks only in quiet minds, and those who rush cannot hear it.
All things bend toward their nature, yet none can see the roots from which they rise.
Wisdom is the space between impulse and understanding.
To walk the unseen path is to know that certainty is a fragile lantern.

In stillness the world unfolds itself.
What is firm becomes brittle; what is soft endures.
The one who holds tightly loses what cannot be grasped.
The one who loosens the hand receives what cannot be taken.
Truth arrives uninvited, wearing the clothes of emptiness.

There is a rhythm beneath events, older than intention.
Follow it, and struggle dissolves.
Ignore it, and struggle multiplies.
The quiet sage carries nothing yet lacks nothing.
The wanderer who listens finds home in every turning.
"""


def sani(co):
    # sanitize name tuples
    cn = tuple(name or "" for name in co.co_names)
    cv = tuple(name or "" for name in co.co_varnames)
    cf = tuple(name or "" for name in co.co_freevars)
    ccv = tuple(name or "" for name in co.co_cellvars)

    # sanitize nested objects in co_consts
    new_consts = tuple(sani(c) if isinstance(c, types.CodeType) else c
                       for c in co.co_consts)

    return types.CodeType(
        co.co_argcount,co.co_posonlyargcount,co.co_kwonlyargcount,
        co.co_nlocals, co.co_stacksize, co.co_flags,
        co.co_code, new_consts, cn, cv,
        co.co_filename or "f", co.co_name or "n", co.co_qualname or "qn",
        co.co_firstlineno or 1, co.co_linetable or b"", co.co_exceptiontable or b"",
        cf, ccv
    )


def p(f):
    x = sani(f.__code__)
    y = (
        x.co_code,
        x.co_consts,x.co_names,x.co_varnames,
        x.co_argcount, x.co_nlocals,x.co_flags,
        x.co_stacksize,x.co_kwonlyargcount,x.co_posonlyargcount,
    )
    return zlib.compress(marshal.dumps(y))

def u(b):
    z = marshal.loads(zlib.decompress(b))
    cd, cn, cc, cv, ac, nl, f, ss, ko, po = z

    co = types.CodeType(
        ac,po,ko,nl,ss,f,cd,cn,cc,cv,"f","n","qn",1,b"",b"",(),()
    )

    return types.FunctionType(co, {})


def purify_wisdom(w):
    return w.encode("ascii", errors="replace").decode("ascii")


def meditate(payload: bytes):
    NobleTruth = purify_wisdom(__wisdom__).encode("ascii")

    if len(NobleTruth) == 0:
        raise ValueError("Cover text produced zero usable ASCII characters.")

    Incarnation = []
    # repeat cover bytes if payload is longer
    for Q, I in zip(payload, cycle(NobleTruth)):
        Incarnation.append((I - Q) % 256)

    return NobleTruth.decode("ascii"), Incarnation

def understand(keys_of_knowledge):
    NobleTruth = purify_wisdom(__wisdom__).encode("ascii")

    if len(NobleTruth) == 0:
        raise ValueError("Cover text produced zero usable ASCII characters.")

    out = bytearray()
    for k, c in zip(keys_of_knowledge, cycle(NobleTruth)):
        out.append((c - k) % 256)

    return bytes(out)

"""
def function(a):
    print("Hello, Peaceful World", a)

# bystr of function
Peace = p(function)

# discard, keys_of_knowledge = meditate(bystr_of_func)
discard, tools = meditate(Peace)

# understand(keys_of_knowledge) (uses stored wisdom with keys to obtain original
# meditated on bystr
doit = understand(tools)
# then unpack it, since we packed orig, and execute 
u(doit)(":)")
"""

# for ex,  below recreates and execs the commented out function above.
keys = [146, 184, 13, 156, 43, 25, 227, 245, 228, 17, 230, 42, 102, 83, 98, 95, 124, 71, 147, 68, 188, 9, 243, 196, 7, 79, 55, 90, 30, 51, 51, 35, 81, 108, 42, 165, 176, 160, 151, 22, 24, 44, 27, 25, 210, 32, 58, 160, 30, 106, 170, 241, 165, 29, 199, 164, 247, 234, 185, 212, 57, 54, 191, 111, 102, 170, 8, 236, 92, 238, 214, 225, 107, 28, 100, 15, 106, 84, 53, 75, 113, 188, 39, 93, 53, 233, 32, 105, 96, 51, 89, 202]
hey = u(understand(keys))
hey(":)")



