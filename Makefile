KDIR = /Users/wuteng/gitrepo/linux
ARCH = x86
ifeq ($(ARCH), x86)
	b = b
endif

ZIMAGE = $(KDIR)/arch/$(ARCH)/boot/$(b)zImage
YOCTO_IMAGE = core-image-minimal-qemux86.ext4

QEMU_OPTS = -kernel $(ZIMAGE) \
						-device virtio-serial \
						-chardev pty,id=virtiocon0 -device virtconsole,chardev=virtiocon0 \
						-drive file=$(YOCTO_IMAGE),if=virtio,format=raw \
						--append "root=/dev/vda loglevel=15 console=ttyS0 nokaslr" \
						-nographic \
						-m 256 -s -S

qemu:
	qemu-system-x86_64 $(QEMU_OPTS)

gdb:
	gdb /Users/wuteng/gitrepo/linux/vmlinux
