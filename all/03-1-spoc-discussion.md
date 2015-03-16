# lec5 SPOC思考题


NOTICE
- 有"w3l1"标记的题是助教要提交到学堂在线上的。
- 有"w3l1"和"spoc"标记的题是要求拿清华学分的同学要在实体课上完成，并按时提交到学生对应的git repo上。
- 有"hard"标记的题有一定难度，鼓励实现。
- 有"easy"标记的题很容易实现，鼓励实现。
- 有"midd"标记的题是一般水平，鼓励实现。


## 个人思考题
---

请简要分析最优匹配，最差匹配，最先匹配，buddy systemm分配算法的优势和劣势，并尝试提出一种更有效的连续内存分配算法 (w3l1)
```
  + 采分点：说明四种算法的优点和缺点
  - 答案没有涉及如下3点；（0分）
  - 正确描述了二种分配算法的优势和劣势（1分）
  - 正确描述了四种分配算法的优势和劣势（2分）
  - 除上述两点外，进一步描述了一种更有效的分配算法（3分）
 ```
- [x]  

>  
```
   答：
		最优匹配
			优点：
				避免大的空闲分区被拆分
				减小外部碎片的大小
				相对简单
			缺点：
				产生外部碎片
				释放分区需查找，较慢
				易产生很多小的外部碎片，无法被利用
		最差匹配
			优点：
				可避免出现大量的小碎片
				当中等大小的空间分配较多时，效果较好
			缺点：
				产生外部碎片
				释放分区较慢
				后期难以分配较大的分区
		最先匹配
			优点：
				实现简单
				释放分区简单
				高地址处有大块的空闲分区
			缺点：
				产生外部碎片
				分配大块空间时较慢
		Buddy System:
			优点：
				搜索合并分区速度快
				外部碎片少
			缺点：
				可能有很多内部碎片
		一种可能更有效的连续内存分配算法：
			综合以上三种方法，对不同大小的块分配需求，使用不同的分配算法
			对于中等大小的块分配较多时，使用最差匹配
			对于小尺寸的块分配较多时，使用最优匹配
			对于大尺寸的块分配较多时，使用最先匹配
```

## 小组思考题

请参考ucore lab2代码，采用`struct pmm_manager` 根据你的`学号 mod 4`的结果值，选择四种（0:最优匹配，1:最差匹配，2:最先匹配，3:buddy systemm）分配算法中的一种或多种，在应用程序层面(可以 用python,ruby,C++，C，LISP等高语言)来实现，给出你的设思路，并给出测试用例。 (spoc)

--- 
```
	答：
		实现Buddy System
		程序地址  ./03-1-spoc-discussion/BuddySys.py
		设计关键思路：
			以一个三元列表表示一块存储空间，其中的三个元素分别为（标号、空间大小、前缀标记串）；
			1、标号用来在释放空间时作为标示；
			2、空间大小即空间大小；
			3、前缀标记串初始为'#';
				当一块空间分裂时，其中一块标记串后面补'0'，另一块的标记串后面补'1';
				仅当两个空闲空间的标记串的除最后一位外均相同时可以合并;
		测试：
			与视频演示中使用相同数据，结果正确
```
```
# Buddy System

mem_list = []
SIZE = 1024


def init():
    mem_list.append([-1, SIZE, '#'])


def buddy_alloc(tag, size):
    print 'Buddy Alloc : (' + str(tag) + ' , ' + str(size) + ')'
    block = None
    for item in mem_list:
        if item[0] == -1 and item[1] >= size:
            if not block or item[1] < block[1]:
                block = item
    if not block:
        print '    No space available'
        print
    else:
        while block[1] >= size * 2:
            mem_list.insert(mem_list.index(block) + 1,
                            [-1, block[1] / 2, block[2] + '1'])
            block[1] = block[1] / 2
            block[2] = block[2] + '0'
        block[0] = tag
        print '    ' + str(mem_list)
        print


def merge(block):
    index = mem_list.index(block)
    if index > 0 and mem_list[index - 1][2][:-1] == block[2][:-1] \
       and mem_list[index - 1][0] == -1:
        mem_list.remove(mem_list[index - 1])
        block[1] = block[1] * 2
        block[2] = block[2][:-1]
        merge(block)
    elif index + 1 < len(mem_list) and mem_list[index + 1][2][:-1] == block[2][:-1] \
       and mem_list[index + 1][0] == -1:
        mem_list.remove(mem_list[index + 1])
        block[1] = block[1] * 2
        block[2] = block[2][:-1]
        merge(block)

    
def buddy_release(tag):
    print 'Buddy Release : ' + str(tag)
    for block in mem_list:
        if block[0] == tag:
            block[0] = -1
            merge(block)
            print '    ' + str(mem_list)
            print
            return


def test():
    init()
    buddy_alloc(1, 100)
    buddy_alloc(2, 240)
    buddy_alloc(3, 64)
    buddy_alloc(4, 256)
    buddy_release(2)
    buddy_release(1)
    buddy_alloc(5, 75)
    buddy_release(3)
    buddy_release(5)
    buddy_release(4)


if __name__ == '__main__':
    test()
```
```
Output :
Buddy Alloc : (1 , 100)
    [[1, 128, '#000'], [-1, 128, '#001'], [-1, 256, '#01'], [-1, 512, '#1']]

Buddy Alloc : (2 , 240)
    [[1, 128, '#000'], [-1, 128, '#001'], [2, 256, '#01'], [-1, 512, '#1']]

Buddy Alloc : (3 , 64)
    [[1, 128, '#000'], [3, 64, '#0010'], [-1, 64, '#0011'], [2, 256, '#01'], [-1, 512, '#1']]

Buddy Alloc : (4 , 256)
    [[1, 128, '#000'], [3, 64, '#0010'], [-1, 64, '#0011'], [2, 256, '#01'], [4, 256, '#10'], [-1, 256, '#11']]

Buddy Release : 2
    [[1, 128, '#000'], [3, 64, '#0010'], [-1, 64, '#0011'], [-1, 256, '#01'], [4, 256, '#10'], [-1, 256, '#11']]

Buddy Release : 1
    [[-1, 128, '#000'], [3, 64, '#0010'], [-1, 64, '#0011'], [-1, 256, '#01'], [4, 256, '#10'], [-1, 256, '#11']]

Buddy Alloc : (5 , 75)
    [[5, 128, '#000'], [3, 64, '#0010'], [-1, 64, '#0011'], [-1, 256, '#01'], [4, 256, '#10'], [-1, 256, '#11']]

Buddy Release : 3
    [[5, 128, '#000'], [-1, 128, '#001'], [-1, 256, '#01'], [4, 256, '#10'], [-1, 256, '#11']]

Buddy Release : 5
    [[-1, 512, '#0'], [4, 256, '#10'], [-1, 256, '#11']]

Buddy Release : 4
    [[-1, 1024, '#']]
```

## 扩展思考题

阅读[slab分配算法](http://en.wikipedia.org/wiki/Slab_allocation)，尝试在应用程序中实现slab分配算法，给出设计方案和测试用例。

## “连续内存分配”与视频相关的课堂练习

### 5.1 计算机体系结构和内存层次
MMU的工作机理？

- [x]  

>  http://en.wikipedia.org/wiki/Memory_management_unit

L1和L2高速缓存有什么区别？

- [x]  

>  http://superuser.com/questions/196143/where-exactly-l1-l2-and-l3-caches-located-in-computer
>  Where exactly L1, L2 and L3 Caches located in computer?

>  http://en.wikipedia.org/wiki/CPU_cache
>  CPU cache

### 5.2 地址空间和地址生成
编译、链接和加载的过程了解？

- [x]  

>  

动态链接如何使用？

- [x]  

>  


### 5.3 连续内存分配
什么是内碎片、外碎片？

- [x]  

>  答：
		内碎片：分配给进程的未被进程利用到空间
		外碎片：分配单元之间未被利用到内存

为什么最先匹配会越用越慢？

- [x]  

>  答：
		一段时间之后很可能只有高地址处有满足要求的空间可用
		由于每次都从较低的地址开始搜索，因此花费的时间会更长

为什么最差匹配会的外碎片少？

- [x]  

>  

在几种算法中分区释放后的合并处理如何做？

- [x]  

>  

### 5.4 碎片整理
一个处于等待状态的进程被对换到外存（对换等待状态）后，等待事件出现了。操作系统需要如何响应？

- [x]  

>  

### 5.5 伙伴系统
伙伴系统的空闲块如何组织？

- [x]  

>  

伙伴系统的内存分配流程？

- [x]  

>  

伙伴系统的内存回收流程？

- [x]  

>  

struct list_entry是如何把数据元素组织成链表的？

- [x]  

>  



