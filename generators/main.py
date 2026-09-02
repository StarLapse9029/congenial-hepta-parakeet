from lcg import LCG
import time

SEED = int(time.time())
SAMPLE_SIZE = 10

def main():
    lcg_comparison()

def lcg_comparison():

    glib_c_lcg = LCG(SEED)
    print('GLIB C LCG:')
    print(f'-- {glib_c_lcg.generate(SAMPLE_SIZE)}')

    java_posix_lcg = LCG(SEED, 2**48, 25214903917, 11) 
    print('JAVA LCG:') #Java's java.util.Random, POSIX [ln]rand48, glibc [ln]rand48[_r]
    print(f'-- {java_posix_lcg.generate(SAMPLE_SIZE)}')

    maybe_lcg = LCG(SEED, 2**32, 1103515245, 12345)
    print('GLIB C, 2^32 modulus variation:')
    print(f'-- {maybe_lcg.generate(SAMPLE_SIZE)}')

    # Other bad choices based on Hull-Dobell Theorem
    # 1. Zero increment -> reduces to a pure multiplicative LCG.
    #    Fails Hull-Dobell condition 1 outright (gcd(0, m) = m != 1).
    #    If seed and m share a factor, the sequence can collapse to 0 and stick there.
    zero_increment_lcg = LCG(SEED, 2**16, 5, 0) 
    print('Zero increment:')
    print(f'-- {zero_increment_lcg.generate(SAMPLE_SIZE)}')

    # 2. c and m not coprime -> violates condition 1 directly.
    #    m=100, c=10: gcd(10,100)=10, so the generator can only ever reach
    #    multiples of 10 that close under gcd -- collapses onto a small subset
    #    of possible values instead of covering [0, m).
    non_coprime_lcg = LCG(SEED, 100, 3, 10)    
    print('Non coprime:')
    print(f'-- {non_coprime_lcg.generate(SAMPLE_SIZE)}')

    # 3. Short period by small modulus -> obeys Hull-Dobell (full period) but
    #    the period itself (m) is tiny, so it repeats fast regardless of quality.
    #    Good for demonstrating "passes the theorem, still useless" -- period
    #    length and statistical quality are separate axes.
    short_period_lcg = LCG(SEED, 64, 5, 1)  # a-1=4 divisible by all prime factors of 64 (2), and by 4 -> full period, but only 64 distinct values
    print('Short period')
    print(f'-- {short_period_lcg.generate(SAMPLE_SIZE)}')
    # 4. Low-order bit correlation -> m is a power of 2 (2**k). This is the
    #    textbook LCG flaw: the low n bits of the output have period 2**n,
    #    meaning the LAST BIT alternates 0,1,0,1,... and the low few bits
    #    are predictable/correlated no matter how "random" a and c look.
    #    This is why glibc's rand() with power-of-2 modulus is considered weak
    #    for anything beyond the top bits.
    power_of_two_modulus_lcg = LCG(SEED, 2**8, 1103515245, 12345)    
    print('Power of two modulus')
    print(f'-- {power_of_two_modulus_lcg.generate(SAMPLE_SIZE)}')

    # 5. a too close to 1 -> technically passes Hull-Dobell, but consecutive
    #    outputs barely diverge from a linear function of the seed. You'll see
    #    near-perfect diagonal lines in the (x_n, x_n+1) plot instead of a
    #    filled square -- classic LCG lattice structure, exaggerated.
    near_identity_multiplier_lcg = LCG(SEED, 2**16, 1, 1)
    print('Near identity multiplier')
    print(f'-- {near_identity_multiplier_lcg.generate(SAMPLE_SIZE)}')

    # 6. RANDU -- an infamous real-world LCG shipped by IBM in the 1960s-70s.
    #    Passes basic 1D/2D tests but collapses into just 15 parallel planes
    #    when you plot 3D triples (x_n, x_n+1, x_n+2). The canonical example
    #    of why higher-dimensional lattice testing matters.
    randu_lcg = LCG(SEED, 2**31, 65539, 0)
    print('Randu')
    print(f'-- {randu_lcg.generate(SAMPLE_SIZE)}')

if __name__ == "__main__":
    main()
