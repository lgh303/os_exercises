# Buddy System
# github : lgh303
# lcliguohao@163.com

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

