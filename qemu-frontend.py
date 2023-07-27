import re
import asyncio
from qemu.qmp import QMPClient


async def get_xaddress(qmp, address, size):
    res = await qmp.execute('human-monitor-command', {'command-line': f'xp /{size}gx {address}'})

    ret = []
    lines = res.split('\r\n')
    for line in lines:
        if line == '':
            continue
        value = line.split(': ')[1]  # pass through the address
        values = value.split(' ')
        values = [int(x, 16) for x in values if x != '']
        for v in values:
            ret.append(v)

    return ret, address

async def get_page_table(qmp, address):
    res, _ = await get_xaddress(qmp, address, 512)
    for (i, v) in enumerate(res):
        attr = v & 0x0000000000000fff
        v = v & 0xfffffffffffff000
        if v != 0:
            print(f'{i+1} -> 0x{v:016x}, attr: 0x{attr:03x}')

async def main():
    qmp = QMPClient('kernel-5.10')
    await qmp.connect('qmp.sock')

    while True:
        cmd = input("> ")
        if cmd == 'q' or cmd == 'quit':
            break

        if cmd[0:3] == 'fun':
            '''
            fun xpgt PHY_ADDRESS_OF_TOP_LEVEL_PGT
            fun pgtvis PHY_ADDRESS_OF_TOP_LEVEL_PGT
            '''
            cmd = re.sub(' +', ' ', cmd)
            options = cmd.split(' ')
            if options[1] == 'xpgt':
                await get_page_table(qmp, int(options[2], 16))
            elif options[1] == 'pgtvis':
                res = await get_xaddress(qmp, int(options[2], 16), 512)
                print(res)
            continue

        res = await qmp.execute('human-monitor-command', {'command-line': cmd})
        print(res)

    await qmp.disconnect()

asyncio.run(main())
