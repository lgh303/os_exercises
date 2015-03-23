

def translate(addr):
    va = int(addr[0], 16)
    pa = int(addr[1], 16)
    pde_idx = va >> 22
    pde_ctx = (pde_idx - 0x300 + 1) << 12 | 0x3
    pte_idx = (va & 0x3ff000) >> 12
    pte_ctx = (pa & 0xfffff000) | 0x3
    names = ['va', 'pa', 'pde_idx', 'pde_ctx', 'pte_idx', 'pte_ctx']
    values = [va, pa, pde_idx, pde_ctx, pte_idx, pte_ctx]
    for name, value in zip(names, values):
        print name + ': 0x%08x ' % value,
    print
            

def main():
    fin = open('data.in', 'r')
    data_list = fin.read().split('\n')
    fin.close()
    for each in data_list:
        if each: translate(each.split())

    
if __name__ == '__main__':
    main()
