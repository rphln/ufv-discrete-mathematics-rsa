from argparse import ArgumentParser
from math import sqrt
from random import randint
from typing import List, Tuple


def modular_power(a: int, b: int, n: int) -> int:
    """
    Calculates $a^b (mod n)$.
    """

    if b == 1:
        return a
    if b == 0:
        return 1

    x1 = modular_power(a, b // 2, n) % n
    x2 = (x1 * x1) % n

    if b % 2 == 0:
        return x2
    else:
        return (x2 * a) % n


def gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Calculates the greatest common divisor of two integers by using the extended Euclidean algorithm.

    Returns a 3-tuple containing the divisor and both Bézout coefficients.
    """

    r = [a, b]
    q = []

    s = [1, 0]
    t = [0, 1]

    while r[-1] != 0:
        if len(q) > 0:
            s.append(s[-2] - q[-1] * s[-1])
            t.append(t[-2] - q[-1] * t[-1])

        q.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])

    return (
        a * s[-1] + b * t[-1],
        s[-1],
        t[-1],
    )


def is_likely_prime(p: int, to_check: int = 20) -> bool:
    """
    Returns whether an integer is likely a prime.
    """

    for a in range(to_check):
        g, _, _ = gcd(a, p)

        if g == 1 and modular_power(a, p - 1, p) != 1:
            return False

    return True


def random_prime(lower: int, upper: int) -> int:
    """
    Returns an integer `p` such that `lower <= p <= upper` that is likely to be a prime.
    """

    while True:
        p = randint(lower, upper)

        if is_likely_prime(p):
            return p


# We must constrain $n$ to at most $\sqrt{2^{63}}$. Since $n$ is $p \times q$, we
# need to constrain each of $p$ and $q$ to $\sqrt{n}$. Then, because we need an
# integer, we just truncate it.
UPPER = int(sqrt(sqrt(2 ** 63)))
LOWER = 2 ** 15


def make_key():
    """
    Generates a 32-bit RSA key pair.
    """

    p = random_prime(LOWER, UPPER)
    q = random_prime(LOWER, UPPER)

    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = randint(2, 2 ** 16)
        g, _, _ = gcd(e, phi)

        if g == 1:
            break

    _, d, _ = gcd(e, phi)

    if d < 0:
        d += phi

    return (n, e), d


def guess_key(n: int, e: int) -> int:
    """
    Attempts to guess a private key given a public key.
    """

    for p in range(2 ** 1, 2 ** 32):
        q = n // p

        if (p * q) != n or not is_likely_prime(p):
            continue

        phi = (p - 1) * (q - 1)
        g, _, _ = gcd(e, phi)

        if g == 1:
            break

    _, d, _ = gcd(e, phi)

    if d < 0:
        d += phi

    return d


def maximum_block_size(n: int) -> int:
    size = 0

    while sum(25 * 100 ** n for n in range(size + 1)) <= n:
        size += 1

    return size


def encode(message: str, n: int, e: int) -> List[int]:
    blocks = []
    block_size = maximum_block_size(n)

    while len(message) % block_size != 0:
        message += "Z"

    for slice in range(0, len(message), block_size):
        block = 0

        for character in message[slice : slice + block_size]:
            block *= 100
            block += ord(character) - ord("A")

        blocks.append(modular_power(block, e, n))

    return blocks


def decode(encrypted_message: List[int], n: int, d: int) -> str:
    block_size = maximum_block_size(n)
    message = []

    for encrypted_block in encrypted_message[::-1]:
        decrypted_block = modular_power(encrypted_block, d, n)

        for _ in range(block_size):
            character = decrypted_block % 100
            decrypted_block //= 100

            message += [chr(ord("A") + character)]

    return message[::-1]


parser = ArgumentParser("RSA")
parser.add_argument("--n", type=int, required=False)
parser.add_argument("--x", type=int, required=False)

parser.add_argument("action", choices=["generate", "encode", "decode", "guess"])

parser.add_argument("message", nargs="*")


def main(args):
    if args.action == "generate":
        (n, e), d = make_key()
        print(f"Public: python rsa.py --n {n} --x {e}")
        print(f"Private: python rsa.py --n {n} --x {d}")

        return

    assert args.n, "The argument `--n` must be set."
    assert args.x, "The argument `--x` must be set."

    if args.action == "encode":
        message = "".join(args.message)
        print(*encode(message, args.n, args.x))

        return

    if args.action == "decode":
        message = [int(n) for n in args.message]
        message = "".join(decode(message, args.n, args.x))
        print(message)

        return

    if args.action == "guess":
        print(guess_key(args.n, args.x))

        return


if __name__ == "__main__":
    main(parser.parse_args())
