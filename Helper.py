def trim_comment(str):
#    print 'pre: ' + str
    (s, sep, comment) = str.partition('#')
#    s = s.strip(' \t')
#    print 'post: ' + s
    return s
