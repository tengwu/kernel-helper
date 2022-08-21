#!/bin/bash
ARCH=x86

YOCTO_URL=http://downloads.yoctoproject.org/releases/yocto/yocto-2.3/machines/qemu/qemu$ARCH/
YOCTO_IMAGE=core-image-minimal-qemu$ARCH.ext4

if [ ! -f $YOCTO_IMAGE ]
then
  wget $YOCTO_URL/$YOCTO_IMAGE
fi

size=$(stat -c%s $YOCTO_IMAGE)
if [ $size -lt 50000000 ]; then
    e2fsck -f $YOCTO_IMAGE
    resize2fs $YOCTO_IMAGE 64M
fi

TMP=$(mktemp -d)

mount -t ext4 -o loop $YOCTO_IMAGE $TMP

# add console
echo "hvc0:12345:respawn:/sbin/getty 115200 hvc0" >> $TMP/etc/inittab

# add more vty
cat >> $TMP/etc/inittab <<EOF
2:12345:respawn:/sbin/getty 38400 tty2
3:12345:respawn:/sbin/getty 38400 tty3
4:12345:respawn:/sbin/getty 38400 tty4
5:12345:respawn:/sbin/getty 38400 tty5
EOF

# enable networking
echo -e "auto eth0\niface eth0 inet dhcp" >> $TMP/etc/network/interfaces

umount $TMP
rmdir $TMP
