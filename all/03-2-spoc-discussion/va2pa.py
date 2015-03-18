#Virtual Addr ==> Pysical Addr

data = []
addrs = ['6c74', '6b22', '03df','69dc', '317a', '4546','2c03', '7fd7', '390e', '748b']
pdbr = int('11', 16)


def init():
    fin = open('data.txt', 'r')
    content = fin.read().split('\n')
    fin.close()
    for each in content:
        data.append(each.split())


def work(addr):
    print 'Virtual Address ' + str(hex(addr))
    pdt_list = data[pdbr]
    pde_content = int(pdt_list[addr / 1024], 16)
    pde_valid = pde_content / 128
    pde_pfn = pde_content - pde_valid * 128
    print '  --> pde index:' + str(hex(addr / 1024)) + \
        '   pde content:(valid ' + str(pde_valid) + '  pfn ' + hex(pde_pfn) + ')'
    if pde_valid == 0:
        print '    --> Fault (page directory entry not valid)'
        return

    pte_list = data[pde_pfn]
    pte_content = int(pte_list[(addr % 1024) / 32], 16)
    pte_valid = pte_content / 128
    pte_pfn = pte_content - pte_valid * 128
    print '    --> pte index:' + str(hex((addr % 1024) / 32)) + \
        '   pte content:(valid ' + str(pte_valid) + '  pfn ' + hex(pte_pfn) + ')'
    if pte_valid == 0:
        print '      --> Fault (page table entry not valid)'
        return
    
    pt_list = data[pte_pfn]
    pt_content = pt_list[addr % 32]
    pa = pte_pfn * 32 + addr % 32
    print '      --> Translates to Physical Address ' + str(hex(pa)) + '--> Value: ' + pt_content
    

def main():
    init()
    for addr in addrs:
        work(int(addr, 16))
    

if __name__ == '__main__':
    main()
