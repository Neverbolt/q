# Prime solver

def f(n):
    if n == 0:
        return 1
    if n == 1:
        return 3
    grandparent = 1
    parent = 3
    for i = 2 to n:
        me = 3 * parent - grandparent
        grandparent = parent
        parent = me
    return me

                 n
if               0
	push(1)        0,1
	add            1

else             n
	push(1)        n,1
	sub            (n-1)

	if             0
		push(3)      0,3
		add          3

	else           n
    push(2)      n,1
    sub          m
		push(1)      m,1
		push(3)      m,1,3

		while        m,1,3
      dup        m,1,3,3
			push(3)    m,1,3,3,3
			mul        m,1,3,9
      push(3)    m,1,3,9,3
			xlast      m,1,3,9,1
			sub        m,1,3,8
      swap       m,1,8,3
      push(2)    m,1,8,3,2
      xpush      m,3,8
      push(3)    m,3,8,3
      xlast      m,3,8,n
      push(1)    m,3,8,n,1
      sub        m,3,8,(n-i)
		endwhile     m,g,p,0
    pop          m,g,p
    swap         m,p,g
    pop          m,p
    swap         m,n
    pop          p
	endelse
endelse
