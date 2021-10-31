'''
Created on Feb 14, 2020

@author: assam
'''
def main():
    total = 2000023
    def recursion(total):
        if total==0:
            return 0
        if total % 2==1:
            return 1+recursion(total-1)
        else:
            return 1+recursion(total//2)
    cnt = recursion(total)
    print(cnt)
    return cnt
main()
        