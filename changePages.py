from subprocess import call

cmd_line = "sudo rm /var/lib/lxc/s1/rootfs/root/quiz_2019/views/layout.ejs"
call(cmd_line, shell=True)

cmd_line = "sudo cp ./layout1.ejs /var/lib/lxc/s1/rootfs/root/quiz_2019/views/layout.ejs"
call(cmd_line, shell=True)


# pagina principal del servidor s2
cmd_line = "sudo rm /var/lib/lxc/s2/rootfs/root/quiz_2019/views/layout.ejs"
call(cmd_line, shell=True)

cmd_line = "sudo cp ./layout2.ejs /var/lib/lxc/s2/rootfs/root/quiz_2019/views/layout.ejs"
call(cmd_line, shell=True)


# pagina principal del servidor s3
cmd_line = "sudo rm /var/lib/lxc/s3/rootfs/root/quiz_2019/views/layout.ejs"
call(cmd_line, shell=True)

cmd_line = "sudo cp ./layout3.ejs /var/lib/lxc/s3/rootfs/root/quiz_2019/views/layout.ejs"
call(cmd_line, shell=True)