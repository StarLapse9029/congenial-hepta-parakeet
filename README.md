# Pseudo Random Number Generation

### Linear Congruential Generator (LCG)
Widely used method for generating pseudo-random sequences of numbers, simple and reasonbly efficient.  
In python, the recurrence is:
```python
seed = (multiplier * seed + increment) % modulus

```
Very sensitive to the choice parameters. A full cycle (generating every possible integer from 0 to the modulus - 1) is achieaveable
with a good choice of parameters, as stated by the Hull-Dobell Theorem.   
The three conditions to be satisfied are as follows:
1. The increment and the modulus must be relatively prime (their greatest common divisior must be 1).
2. The multiplier - 1 must be divisible by every prime factor of the modulus.
3. If the modulus is divisible by 4, the multiplier - 1 must also be multiple of 4.

These conditions guarantee a full period, but doesn't mean that the resulting numbers are cryptographically secure or truly random.

Basically:
Given multiplier = a, increment = c and modulus = m
- c and m → coprime
- prime factors of m → divide a−1
- if m has a factor of 4 → 4 divides a−1
<!-- 

LCG was a nice read
Reminder to do a deeper read on the Hull-Dobell Theorem

-->
## TODO
- Hexbin/Subsampling: For better graphs at higher sample sizes
- Add Scipy
- Add Pandas

### Algorithms
Listing PRNG algorithms that haven't been implemented and may or may not be implemented (Source: Google AI Mode)
- Middle-Square Method
- Linear Feedback Shift Register (LFSR)
- Xorshift
- Xoshiro/Xorshiro
- Permuted Congruential Generator (PCG)
- Mersenne Twister (MT19937)
- ChaCha20
- Blum Blum Shub (BBS)
