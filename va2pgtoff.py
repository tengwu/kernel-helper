'''
Only support 48-bit address space
'''
import os
from tabulate import tabulate

va_hex = input('VA: ')
va_dec = int(va_hex, 16)

print(f'Your VA: {va_hex}, ', end=' ')
print(f'{va_dec} in decimal')

va_nooff = va_dec >> 12

# [[pgd_off, pud_off, pmd_off, pte_off]]
data = [[0, 0, 0, 0]]
data[0][3] = va_nooff & 0x1ff
data[0][2] = (va_nooff >> 9) & 0x1ff
data[0][1] = (va_nooff >> 2 * 9) & 0x1ff
data[0][0] = (va_nooff >> 3 * 9) & 0x1ff

print()
print(tabulate(data, headers=['pgd', 'pud', 'pmd', 'pte']))

