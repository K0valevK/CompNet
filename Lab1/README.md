# Небольшая сеть офиса

## Предисловие

Если честно, то эта работа шла очень туго, начиная с того, что я целых 2 дня пытался подружить mac и eve-ng, заканчивая тем, что просто установки ПО не было достаточно, и некоторые элементы требовали отдельного ручного вмешательства, чтобы хотя бы заставить их вести себя так, как это было на лекциях. Например, дефолтные настройки моего mac не позволяли мне использовать telnet для "сторонних приложений", а интернет предлагал единственное решение, включавшее в себя отключение каких-то мер безопасности в bios и исполнение некоторых команд, на что я не решился, и в итоге я костыльно через стороннюю консоль переадрессовывал себе эти запросы. И к сожалению, это лишь малая часть проблем, с которой я столкнулся. В общем, я почти на 100% уверен, что при выгрузке каких-то конфигов или даже экспорта всего zip работы из eve ng у меня что-то побилось/не сохранилось/потеряло рабочий вид, но до выгрузки система работала и пинги доходили. Поэтому кроме конфигов прикладываю также последовательность команд для каждого VPC, коммутатора и маршрутизатора, с помощью которых я настраивал сеть.

## Построение сети и конфигурация

![`placeholder`](./Scheme.jpg)

Конфигурационные файлы лежат в папке config

### Client1
```commandline
set pcname Client1
ip 10.0.10.2/24 10.0.10.1
save
```

### Client2
```commandline
set pcname Client2
ip 10.0.20.2/24 10.0.20.1
save
```

### SW1
```commandline
enable
configure terminal
hostname SW1
vlan 10
exit
vlan 20
exit
interface gi 0/0
switchport mode access
switchport access vlan 10
exit
interface range gi 1/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
exit
write memory
```

### SW2
```commandline
enable
configure terminal
hostname SW2
vlan 10
exit
vlan 20
exit
interface gi 0/0
switchport mode access
switchport access vlan 20
exit
interface range gi 1/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
exit
write memory
```

### SWCORE
```commandline
enable
configure terminal
hostname SWCORE
vlan 10
exit
vlan 20
exit
interface range gi 0/0-2
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
spanning-tree vlan 10 root primary
spanning-tree vlan 20 root primary
exit
write memory
```

### R0
```commandline
no
enable
configure terminal
hostname R0
interface gi 0/0
no shutdown
interface gi 0/0.1
encapsulation dot1q 10
ip address 10.0.10.1 255.255.255.0
exit
interface gi 0/0.2
encapsulation dot1q 20
ip address 10.0.20.1 255.255.255.0
exit
exit
write memory
```

## Консольные выводы

### Client1

```commandline
Client1> ping 10.0.10.2

10.0.10.2 icmp_seq=1 ttl=64 time=0.001 ms
10.0.10.2 icmp_seq=2 ttl=64 time=0.001 ms
10.0.10.2 icmp_seq=3 ttl=64 time=0.001 ms
10.0.10.2 icmp_seq=4 ttl=64 time=0.001 ms
10.0.10.2 icmp_seq=5 ttl=64 time=0.001 ms

Client1> ping 10.0.20.2

84 bytes from 10.0.20.2 icmp_seq=1 ttl=63 time=7.961 ms
84 bytes from 10.0.20.2 icmp_seq=2 ttl=63 time=6.635 ms
84 bytes from 10.0.20.2 icmp_seq=3 ttl=63 time=8.132 ms
84 bytes from 10.0.20.2 icmp_seq=4 ttl=63 time=8.322 ms
84 bytes from 10.0.20.2 icmp_seq=5 ttl=63 time=7.377 ms
```

### Client2

```commandline
Client2> ping 10.0.10.2

84 bytes from 10.0.10.2 icmp_seq=1 ttl=63 time=11.427 ms
84 bytes from 10.0.10.2 icmp_seq=2 ttl=63 time=11.796 ms
84 bytes from 10.0.10.2 icmp_seq=3 ttl=63 time=7.908 ms
84 bytes from 10.0.10.2 icmp_seq=4 ttl=63 time=7.105 ms
84 bytes from 10.0.10.2 icmp_seq=5 ttl=63 time=10.874 ms

Client2> ping 10.0.20.2

10.0.20.2 icmp_seq=1 ttl=64 time=0.001 ms
10.0.20.2 icmp_seq=2 ttl=64 time=0.001 ms
10.0.20.2 icmp_seq=3 ttl=64 time=0.001 ms
10.0.20.2 icmp_seq=4 ttl=64 time=0.001 ms
10.0.20.2 icmp_seq=5 ttl=64 time=0.001 ms
```
