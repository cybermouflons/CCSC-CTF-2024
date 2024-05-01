.section .data
aa:  .space 32
ac:  .byte  0x26, 0x65, 0x36, 0x75, 0xe, 0x3a, 0x48, 0x5, 0x7c, 0x23, 0x13, 0x75, 0x2a, 0x72, 0x42, 0x30, 0x43, 0x1c, 0x4e, 0x7d, 0xb, 0x38, 0x4a, 0x7f, 0x1a, 0x5e, 0x7f, 0x5e, 0x23

sm: .asciz "Success!\n"
fm: .asciz "Try again...\n"

.section .text
.global _start

_start:
    mov x0, 0
    ldr x1, =aa
    mov x2, 32 
    mov x8, 63
    svc 0
    mov x3, x0
    sub x3, x3, #1
    mov x4, #29
    cmp x3, x4
    bne dd
    ldr x1, =aa
    mov x4, 0x65
    mov x5, 0
al:
    cmp x5, x3
    bge bd
    ldrb w6, [x1, x5]
    eor w6, w6, w4
    strb w6, [x1, x5]
    mov w4, w6
    add x5, x5, 1
    b al
bd:
    ldr x6, =ac
    mov x7, 0
    mov x8, 1
cbl:
    cmp x7, x3
    bge bb
    ldrb w9, [x1, x7]
    ldrb w10, [x6, x7]
    cmp w9, w10
    bne cbf
    add x7, x7, 1
    b cbl
cbf:
    mov x8, 0
    b bb
bb:
    cmp x8, 1
    bne dd
    ldr x1, =sm
    mov x2, #10
    b de
dd:
    ldr x1, =fm
    mov x2, #13
de:
    mov x0, 1
    mov x8, 64
    svc 0
    mov x0, 0
    mov x8, 93
    svc 0
