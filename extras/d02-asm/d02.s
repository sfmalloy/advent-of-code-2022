    .global solve
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

solve:
    pushq %rbp
    movq %rsp, %rbp
    subq $12, %rsp
    pushq %rbx              # index
    pushq %r12              # part 1 answer
    pushq %r13              # part 2 answer
    pushq %r14              # FILEBUF address
    pushq %r15              # idk

    xorq %r12, %r12
    xorq %r13, %r13

    leaq FILENAME, %rdi     # edi = FILENAME
    xorl %esi, %esi         # esi = 0
    movl $2, %eax           # set syscall number to open
    syscall

    cmpl $0, %eax
    movl $1, %edi
    jl exit_prog            # if (open_error) jump to exit_prog
    movl %eax, (%rsp)       # rsp = eax (fd)

    movl (%rsp), %edi
    leaq FILEBUF, %rsi      # if (open_error) jump to exit_prog
    movq N, %rdx
    xorl %eax, %eax
    syscall

    leaq FILEBUF, %r14
    movq %rax, 4(%rsp)

    xorq %rbx, %rbx         # rbx = 0
    xorq %rdi, %rdi
    xorq %rsi, %rsi
rps_loop:
    cmp N, %rbx
    je end_rps

    mov (%r14,%rbx,), %dil  # other (rdi)
    mov 2(%r14,%rbx,), %sil # me    (rsi)

    subq $0x40, %rdi
    subq $0x57, %rsi

    addq %rsi, %r12
    addq $0x4, %rbx
comp1_part1:
    cmpl %edi, %esi
    jne comp2_part1
    addq $0x3, %r12
    jmp comp1_part2
comp2_part1:
    cmpl WIN(,%rsi,4), %edi
    jne comp1_part2
    addq $0x6, %r12
comp1_part2:
    cmpl $1, %esi
    jne comp2_part2
    addq WIN(,%rdi,4), %r13
    jmp rps_loop
comp2_part2:
    cmpl $2, %esi
    jne comp3_part2
    addq $3, %r13
    addq %rdi, %r13
    jmp rps_loop
comp3_part2:
    addq $0x6, %r13
    addq LOSE(,%rdi,4), %r13
    jmp rps_loop
end_rps:
    movq %r12, %rdi
    callq write_int

    movq %r13, %rdi
    callq write_int

    cmpl $0, %eax
    movl $1, %edi
    jle exit_prog           # read error checking

    movl (%rsp), %edi       # edi = fd
    movl $3, %eax           # set syscall number to close
    syscall
exit_success:
    xorl %edi, %edi
exit_prog:
    popq %r15
    popq %r14
    popq %r13
    popq %r12
    popq %rbx
    addq $12, %rsp
    leave
    ret

    .data
    .align 32
N:
    .long 10000
    .align 8
FILENAME:
    .asciz "d02.in"
    .align 8
FILEBUF:
    .zero 10000
    .align 32
WIN:
    .long 0
    .long 3
    .long 1
    .long 2
    .align 32
LOSE:
    .long 0
    .long 2
    .long 3
    .long 1
