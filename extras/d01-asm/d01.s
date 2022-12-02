    .global _start
    .text

/**
syscall numbers for x86_64
--------------------------
- read  = 0
- write = 1
- open  = 2
- close = 3
- exit  = 60
*/

/**
int read_int(int fd)
  - Reads a positive integer because that's all I need.
  - Return -1 on EOF
*/
read_int:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    subq $4, %rsp           # Make room for local variable
    xorl %ebx, %ebx         # Accumulated number
rloop:
                            # read arg 0 = fd (%rdi)
    leaq (%rsp), %rsi       # read arg 1 = addr of stack char
    xorq %rdx, %rdx
    inc %rdx                # read arg 2 = number of chars to read
    xorq %rax, %rax         # set syscall number to read
    syscall

    cmpq $0, %rax           
    je set_eof_flag         # if read no bytes, jump to set_eof_flag
    cmpl $0x0a, (%rsp)
    je end_rloop            # if read newline, jump to end_rloop

    imul $10, %ebx          # ebx *= 10
    addl (%rsp), %ebx       # ebx += *rsp
    subl $0x30, %ebx        # ebx -= 0x30 (aka '0')
    jmp rloop               # jump to beginning of loop (rloop)
set_eof_flag:
    movl $-1, %eax          # eax = -1
    jmp end_read_int
end_rloop:
    movl %ebx, %eax         # eax = ebx (aka eax = number read from file)
end_read_int:
    addq $4, %rsp
    popq %rbx
    leave
    ret

/**
void write_int(int x)
  - Write a single integer to stdout with a newline on the end
*/
write_int:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    pushq %r12
    
    movq $1, %r12           # r12 = 1
    dec %rsp
    movq $0xa, (%rsp)       # *rsp = '\n'

    movl %edi, %ebx         # ebx = x
    movl $10, %ecx          # ecx = 10
wloop:
    xorq %rdx, %rdx         # edx = 0
    movq %rbx, %rax         # eax = ebx
    idivq %rcx              # edx:eax /= 10
    movq %rax, %rbx         # ebx = eax
    addq $0x30, %rdx        # edx += '0'

    inc %r12
    dec %rsp
    mov %dl, (%rsp)         # *rsp = edx

    cmp $0, %rbx
    je end_wloop            # if (ebx == 0) jump to end_wloop
    jmp wloop               # jump to start of loop
end_wloop:
    movq $1, %rdi           # stdout
    leaq (%rsp), %rsi       # address of digit
    movq %r12, %rdx         # length of string
    movq $0x1, %rax         # set syscall number to write
    syscall
    
    addq %r12, %rsp
    popq %r12
    popq %rbx
    leave
    ret

/**
int get_elf(int fd)
  - Get sum of current elf calories
*/
get_elf:
    pushq %rbp
    movq %rsp, %rbp
    pushq %r12
    pushq %rbx

    movq %rdi, %r12         # r12 = fd
    xorl %ebx, %ebx         # ebx = 0
sum_loop:
    movq %r12, %rdi         # rdi = fd
    callq read_int
    cmpl $0, %eax
    jle end_sum             # if (eax <= 0) jump to end_sum
    addl %eax, %ebx         # ebx += eax
    jmp sum_loop            # jump to start of loop
end_sum:
    movl %ebx, %eax         # return ebx
    popq %rbx
    popq %r12
    leave
    ret

_start:
    subq $16, %rsp          # setup local variables
    movl $0, 8(%rsp)        # largest sum (a)
    movl $0, 4(%rsp)        # 2nd largest (b)
    movl $0, (%rsp)         # 3rd largest (c)

    leaq FILENAME, %rdi     # rdi = FILENAME
    xorq %rsi, %rsi         # rsi = 0
    movq $2, %rax           # set syscall number to open
    syscall

    cmpl $0, %eax
    jl exit_prog            # if (open_error) jump to exit_prog
    movl %eax, 12(%rsp)     # rsp+12 = eax (fd)
read_loop:
    movq 12(%rsp), %rdi     # rdi = fd
    callq get_elf
    cmpl $0, %eax
    je end                  # if (elf_sum == 0) jump to end
comp1:
    cmpl 8(%rsp), %eax
    jl comp2                # if (elf_sum < a) jump to comp2
    movl 8(%rsp), %edi      # shift a, b, and c sums down, discard old c
    movl %eax, 8(%rsp)
    movl 4(%rsp), %esi
    movl %edi, 4(%rsp)
    movl %esi, (%rsp)
    jmp read_loop           # jump to read_loop
comp2:
    cmpl 4(%rsp), %eax
    jl comp3                # if (elf_sum < b) jump to comp3
    movl %edi, 4(%rsp)      # shift b and c, discard old c
    movl 4(%rsp), %eax
    movl (%rsp), %edi
    jmp read_loop           # jump to read_loop
comp3:
    cmpl (%rsp), %eax
    jl read_loop            # if (elf_sum < c) jump to read_loop
    movl %eax, (%rsp)       # replace c
    jmp read_loop
end:
    movl 8(%rsp), %edi      # print(a)
    callq write_int
    xorl %edi, %edi         # edi = 0
    addl 8(%rsp), %edi      # edi += a
    addl 4(%rsp), %edi      # edi += b
    addl (%rsp), %edi       # edi += c
    callq write_int         # print(edi)

    movl 12(%rsp), %edi     # edi = fd
    movl $3, %eax           # set syscall number to close
    syscall
exit_prog:
    addq $16, %rsp
    xorl %edi, %edi
    movl $60, %eax
    syscall

    .data
FILENAME:
    .asciz "d01.in"
