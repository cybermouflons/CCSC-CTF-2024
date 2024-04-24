#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/landlock.h>
#include <linux/seccomp.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#define PAGE_SIZE 4096
#define SHELLCODE_SIZE 512

#ifndef landlock_create_ruleset
static inline int
landlock_create_ruleset(const struct landlock_ruleset_attr *const attr,
                        const size_t size, const __u32 flags) {
  return syscall(444, attr, size, flags);
}
#endif

#ifndef landlock_add_rule
static inline int landlock_add_rule(const int ruleset_fd,
                                    const enum landlock_rule_type rule_type,
                                    const void *const rule_attr,
                                    const __u32 flags) {
  return syscall(445, ruleset_fd, rule_type, rule_attr, flags);
}
#endif

#ifndef landlock_restrict_self
static inline int landlock_restrict_self(const int ruleset_fd,
                                         const __u32 flags) {
  return syscall(446, ruleset_fd, flags);
}
#endif

char flag[PAGE_SIZE] __attribute__((aligned(PAGE_SIZE))) =
    "CCSC{c0r3dumps_4r3_us3ful_4_d3bugg1ng_4nd_stuff}";

void landlock() {
  struct landlock_ruleset_attr attr = {0};
  int ruleset_fd;

  attr.handled_access_fs =
      LANDLOCK_ACCESS_FS_EXECUTE | LANDLOCK_ACCESS_FS_WRITE_FILE |
      LANDLOCK_ACCESS_FS_READ_FILE | LANDLOCK_ACCESS_FS_READ_DIR |
      LANDLOCK_ACCESS_FS_REMOVE_DIR | LANDLOCK_ACCESS_FS_REMOVE_FILE |
      LANDLOCK_ACCESS_FS_MAKE_CHAR | LANDLOCK_ACCESS_FS_MAKE_DIR |
      LANDLOCK_ACCESS_FS_MAKE_REG | LANDLOCK_ACCESS_FS_MAKE_SOCK |
      LANDLOCK_ACCESS_FS_MAKE_FIFO | LANDLOCK_ACCESS_FS_MAKE_BLOCK |
      LANDLOCK_ACCESS_FS_MAKE_SYM | LANDLOCK_ACCESS_FS_TRUNCATE;

  int abi = landlock_create_ruleset(NULL, 0, LANDLOCK_CREATE_RULESET_VERSION);
  if (abi == -1) {
    perror("ABI");
    exit(EXIT_FAILURE);
  }

  ruleset_fd = landlock_create_ruleset(&attr, sizeof(attr), 0);
  if (ruleset_fd == -1) {
    exit(EXIT_FAILURE);
  }
  struct landlock_path_beneath_attr path_beneath = {0};
  int err;

  path_beneath.allowed_access =
      LANDLOCK_ACCESS_FS_READ_FILE | LANDLOCK_ACCESS_FS_READ_DIR |
      LANDLOCK_ACCESS_FS_WRITE_FILE | LANDLOCK_ACCESS_FS_MAKE_REG;

  path_beneath.parent_fd = open("/home/user", O_PATH | O_CLOEXEC);
  if (path_beneath.parent_fd == -1) {
    close(ruleset_fd);
    exit(EXIT_FAILURE);
  }
  err = landlock_add_rule(ruleset_fd, LANDLOCK_RULE_PATH_BENEATH, &path_beneath,
                          0);
  close(path_beneath.parent_fd);
  if (err) {
    close(ruleset_fd);
    exit(EXIT_FAILURE);
  }
  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
    close(ruleset_fd);
    exit(EXIT_FAILURE);
  }
  if (landlock_restrict_self(ruleset_fd, 0)) {
    close(ruleset_fd);
    exit(EXIT_FAILURE);
  }
  close(ruleset_fd);
}

void protect() {

  size_t size = sizeof(flag);

  uintptr_t start = (uintptr_t)flag & -PAGE_SIZE;
  size_t page_length =
      ((uintptr_t)flag + size + PAGE_SIZE - 1 - start) & -PAGE_SIZE;

  if (mprotect((void *)start, page_length, PROT_NONE) == -1) {
    exit(EXIT_FAILURE);
  }
}

/* Define the BPF filter */
struct sock_filter filter[] = {
    /* Load syscall number */
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr))),

    /* Allow read (syscall number 0) */
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_read, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    /* Allow write (syscall number 1) */
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_write, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    /* Allow open (syscall number 2) */
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_open, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    /* Allow lseek (syscall number 8) */
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_lseek, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    /* Allow fork (syscall number 57) */
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_fork, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    /* Deny everything else */
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
};

/* Load the BPF filter into the kernel */
void install_seccomp_filter() {
  struct sock_fprog prog = {
      .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
      .filter = filter,
  };

  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1) {
    exit(EXIT_FAILURE);
  }

  if (syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog) == -1) {
    exit(EXIT_FAILURE);
  }
}

void setup() {

  setbuf(stdout, NULL);
  printf("Don't try anything tricky ;)\n");
  system("rm infiltration");
  system("rm infiltration.c");
  prctl(PR_SET_DUMPABLE, 1);
  protect();
  landlock();
}

void *get_shellcode() {

  char hex_input[SHELLCODE_SIZE];

  printf("Just execute whatever you want, you can't do much! hex: ");
  if (fgets(hex_input, SHELLCODE_SIZE, stdin) == NULL) {
    exit(EXIT_FAILURE);
  }

  // Remove newline character if present
  char *newline = strchr(hex_input, '\n');
  if (newline)
    *newline = '\0';

  // Calculate the length of hex string
  size_t hex_len = strlen(hex_input);
  if (hex_len % 2 != 0) {
    exit(EXIT_FAILURE);
  }

  // Convert hex string to bytes
  size_t bytes_len = hex_len / 2;
  unsigned char *bytes = (unsigned char *)malloc(bytes_len);
  if (bytes == NULL) {
    exit(EXIT_FAILURE);
  }

  for (size_t i = 0; i < bytes_len; ++i) {
    sscanf(hex_input + 2 * i, "%2hhx", &bytes[i]);
  }

  // Allocate executable memory page and copy shellcode
  void *shellcode = mmap(0, PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC,
                         MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (shellcode == MAP_FAILED) {
    exit(EXIT_FAILURE);
  }

  memcpy(shellcode, bytes, bytes_len);

  return shellcode;
}

int main() {

  setup();

  unsigned char *shellcode = get_shellcode();

  void (*exec)() = (void (*)())shellcode;

  install_seccomp_filter();
  exec();

  return 0;
}
