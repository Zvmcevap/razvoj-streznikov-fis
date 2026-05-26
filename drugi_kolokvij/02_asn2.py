from pyasn1.type import univ, namedtype, constraint
from pyasn1.codec.der.decoder import decode
from pyasn1.codec.der.encoder import encode


class House(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            "rooms",
            univ.Integer().subtype(
                subtypeSpec=constraint.ValueRangeConstraint(1, 4)
            )
        ),
        namedtype.NamedType(
            "windows",
            univ.Integer().subtype(
                subtypeSpec=constraint.ValueRangeConstraint(5, 8)
            )
        ),
        namedtype.NamedType(
            "doors",
            univ.Integer().subtype(
                subtypeSpec=constraint.ValueRangeConstraint(7, 11)
            )
        ),
        namedtype.NamedType(
            "sockets",
            univ.Integer().subtype(
                subtypeSpec=constraint.ValueRangeConstraint(9, 13)
            )
        )
    )


def read_der_hex(filename):
    with open(filename, "r") as f:
        data = f.read().strip().replace(" ", "").replace("\n", "")
    return bytes.fromhex(data)


def check_file(filename):
    print(f"\nChecking {filename}")

    der_data = read_der_hex(filename)

    try:
        obj, rest = decode(der_data, asn1Spec=House())

        if rest:
            print("Napaka: po DER objektu so še dodatni bajti:", rest.hex())
            return

        print("OK:")
        print(obj.prettyPrint())

    except Exception as e:
        print("Napaka v objektu:")
        print(e)


check_file("drugi_kolokvij/house1.txt")
check_file("drugi_kolokvij/house2.txt")
check_file('drugi_kolokvij/house_fixed.txt')
fixed = House()
fixed["rooms"] = 2
fixed["windows"] = 7
fixed["doors"] = 10
fixed["sockets"] = 9

fixed_der = encode(fixed)
print(fixed_der.hex())