WINDOW_SIZE = 2

def main():
    sequence = ['c', 'c', 'd', 'b', 'c', 'e', 'c', 'e', 'a', 'd']
    pages = set(['a', 'd', 'e'])
    last_fault = -1
    page_trace = set()
    print 'initial ==> ',
    print pages
    for i in range(len(sequence)):
        page = sequence[i]
        print 'visit',
        print page,
        if page not in pages:
            if last_fault >= 0 and i - last_fault > WINDOW_SIZE:
                new_pages = set()
                for each in pages:
                    if each in page_trace:
                        new_pages.add(each)
                pages = new_pages
            last_fault = i
            page_trace = set()
            pages.add(page)
        page_trace.add(page)
        print '==> ',
        print pages


if __name__ == '__main__':
    main()
