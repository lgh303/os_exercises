# lec6 SPOC思考题


NOTICE
- 有"w3l2"标记的题是助教要提交到学堂在线上的。
- 有"w3l2"和"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的git repo上。
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。


## 个人思考题
---

（1） (w3l2) 请简要分析64bit CPU体系结构下的分页机制是如何实现的
```
  + 采分点：说明64bit CPU架构的分页机制的大致特点和页表执行过程
  - 答案没有涉及如下3点；（0分）
  - 正确描述了64bit CPU支持的物理内存大小限制（1分）
  - 正确描述了64bit CPU下的多级页表的级数和多级页表的结构或反置页表的结构（2分）
  - 除上述两点外，进一步描述了在多级页表或反置页表下的虚拟地址-->物理地址的映射过程（3分）
 ```
- [x]  

>  
```
	答：
		64位CPU架构可以支持2^64字节的逻辑地址寻址
		x86_64 使用四级页表
		整个地址空间（逻辑和物理均）分成固定大小的页结构
		页大小为固定的4KB，64位的逻辑地址分为两个部分，较低的13位为页内偏移，剩余的51位是页索引，用来检索页表，得到物理页号
		对于多级页表的索引结构，所有的索引位分为多级，前一级的页表内容为下一级页表的起始地址，最后一级页表存储真实到物理页号
		某一级的页表尺寸是表示这个页表的位宽的2次幂大小


## 小组思考题
---

（1）(spoc) 某系统使用请求分页存储管理，若页在内存中，满足一个内存请求需要150ns。若缺页率是10%，为使有效访问时间达到0.5ms,求不在内存的页面的平均访问时间。请给出计算步骤。 

- [x]  

> 500=0.9\*150+0.1\*x
```
	答：
		0.9 * 150 + 0.1 * x = 500
		得 x = 3650
		不在内存的页面的平均访问时间是3.65ms
```

（2）(spoc) 有一台假想的计算机，页大小（page size）为32 Bytes，支持32KB的虚拟地址空间（virtual address space）,有4KB的物理内存空间（physical memory），采用二级页表，一个页目录项（page directory entry ，PDE）大小为1 Byte,一个页表项（page-table entries
PTEs）大小为1 Byte，1个页目录表大小为32 Bytes，1个页表大小为32 Bytes。页目录基址寄存器（page directory base register，PDBR）保存了页目录表的物理地址（按页对齐）。

PTE格式（8 bit） :
```
  VALID | PFN6 ... PFN0
```
PDE格式（8 bit） :
```
  VALID | PT6 ... PT0
```
其
```
VALID==1表示，表示映射存在；VALID==0表示，表示映射不存在。
PFN6..0:页帧号
PT6..0:页表的物理基址>>5
```
在[物理内存模拟数据文件](./03-2-spoc-testdata.md)中，给出了4KB物理内存空间的值，请回答下列虚地址是否有合法对应的物理内存，请给出对应的pde index, pde contents, pte index, pte contents。
```
Virtual Address 6c74
Virtual Address 6b22
Virtual Address 03df
Virtual Address 69dc
Virtual Address 317a
Virtual Address 4546
Virtual Address 2c03
Virtual Address 7fd7
Virtual Address 390e
Virtual Address 748b
```

比如答案可以如下表示：
```
Virtual Address 7570:
  --> pde index:0x1d  pde contents:(valid 1, pfn 0x33)
    --> pte index:0xb  pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)
      
Virtual Address 21e1:
  --> pde index:0x8  pde contents:(valid 0, pfn 0x7f)
      --> Fault (page directory entry not valid)

Virtual Address 7268:
  --> pde index:0x1c  pde contents:(valid 1, pfn 0x5e)
    --> pte index:0x13  pte contents:(valid 1, pfn 0x65)
      --> Translates to Physical Address 0xca8 --> Value: 16
```

```
答：

程序输出：

Virtual Address 0x6c74
  --> pde index:0x1b   pde content:(valid 1  pfn 0x20)
    --> pte index:0x3   pte content:(valid 1  pfn 0x61)
      --> Translates to Physical Address 0xc34--> Value: 06
Virtual Address 0x6b22
  --> pde index:0x1a   pde content:(valid 1  pfn 0x52)
    --> pte index:0x19   pte content:(valid 1  pfn 0x47)
      --> Translates to Physical Address 0x8e2--> Value: 1a
Virtual Address 0x3df
  --> pde index:0x0   pde content:(valid 1  pfn 0x5a)
    --> pte index:0x1e   pte content:(valid 1  pfn 0x5)
      --> Translates to Physical Address 0xbf--> Value: 0f
Virtual Address 0x69dc
  --> pde index:0x1a   pde content:(valid 1  pfn 0x52)
    --> pte index:0xe   pte content:(valid 0  pfn 0x7f)
      --> Fault (page table entry not valid)
Virtual Address 0x317a
  --> pde index:0xc   pde content:(valid 1  pfn 0x18)
    --> pte index:0xb   pte content:(valid 1  pfn 0x35)
      --> Translates to Physical Address 0x6ba--> Value: 1e
Virtual Address 0x4546
  --> pde index:0x11   pde content:(valid 1  pfn 0x21)
    --> pte index:0xa   pte content:(valid 0  pfn 0x7f)
      --> Fault (page table entry not valid)
Virtual Address 0x2c03
  --> pde index:0xb   pde content:(valid 1  pfn 0x44)
    --> pte index:0x0   pte content:(valid 1  pfn 0x57)
      --> Translates to Physical Address 0xae3--> Value: 16
Virtual Address 0x7fd7
  --> pde index:0x1f   pde content:(valid 1  pfn 0x12)
    --> pte index:0x1e   pte content:(valid 0  pfn 0x7f)
      --> Fault (page table entry not valid)
Virtual Address 0x390e
  --> pde index:0xe   pde content:(valid 0  pfn 0x7f)
    --> Fault (page directory entry not valid)
Virtual Address 0x748b
  --> pde index:0x1d   pde content:(valid 1  pfn 0x0)
    --> pte index:0x4   pte content:(valid 0  pfn 0x7f)
      --> Fault (page table entry not valid)
```


（3）请基于你对原理课二级页表的理解，并参考Lab2建页表的过程，设计一个应用程序（可基于python, ruby, C, C++，LISP等）可模拟实现(2)题中描述的抽象OS，可正确完成二级页表转换。

```
答：
程序地址：
		03-2-spoc-discussion/va2pa.py

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
```

（4）假设你有一台支持[反置页表](http://en.wikipedia.org/wiki/Page_table#Inverted_page_table)的机器，请问你如何设计操作系统支持这种类型计算机？请给出设计方案。

 (5)[X86的页面结构](http://os.cs.tsinghua.edu.cn/oscourse/OS2015/lecture06#head-1f58ea81c046bd27b196ea2c366d0a2063b304ab)
--- 

## 扩展思考题

阅读64bit IBM Powerpc CPU架构是如何实现[反置页表](http://en.wikipedia.org/wiki/Page_table#Inverted_page_table)，给出分析报告。

--- 
