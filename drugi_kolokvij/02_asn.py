"""
EVL DEFINITIONS ::= BEGIN

Narocilo ::= SEQUENCE {
    rakete     Rakete,
    bombe      Bombe,
    cokolade   Cokolade,
    takoj      BOOLEAN
}

Rakete ::= ENUMERATED {
    r3001(0),
    r4001(1),
    r5003(2)
}

Bombe ::= ENUMERATED {
    b1019(0),
    b2003(1),
    b5009(2)
}

Cokolade ::= ENUMERATED {
    c1009(0),
    c1499(1),
    c2011(2)
}

END
"""

from pyasn1.type import univ, namedtype, namedval
from pyasn1.codec.der.encoder import encode
from pyasn1.codec.der.decoder import decode


class Rakete(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ("r3001", 0),
        ("r4001", 1),
        ("r5003", 2)
    )


class Bombe(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ("b1019", 0),
        ("b2003", 1),
        ("b5009", 2)
    )


class Cokolade(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ("c1009", 0),
        ("c1499", 1),
        ("c2011", 2)
    )


class Narocilo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType("rakete", Rakete()),
        namedtype.NamedType("bombe", Bombe()),
        namedtype.NamedType("cokolade", Cokolade()),
        namedtype.NamedType("takoj", univ.Boolean())
    )


# ustvarjanje objekta
narocilo = Narocilo()
narocilo["rakete"] = "r3001"
narocilo["bombe"] = "b2003"
narocilo["cokolade"] = "c2011"
narocilo["takoj"] = True


# kodiranje
encoded = encode(narocilo)
print(encoded.hex())


# dekodiranje
decoded, rest = decode(encoded, asn1Spec=Narocilo())
print(decoded.prettyPrint())
