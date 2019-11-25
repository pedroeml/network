# network-simulator
ARP - ICMP Network Simulator

# Detalhes de implementação

Foi feita uma implementação em Python cuja principal separação dos grupos de scripts são: leitura e escrita em arquivo, simulação e classes. 

## Classes

O script `network.py` contém uma classe que armazena coleções de nodos e roteadores para facilitar o acesso aos mesmos em um único objeto. Há os scripts `node.py` e `router.py` que são para as implementações de suas respectivas classes. A classe `Node` possui atributos com nome, porta, gateway e MTU e a classe `Router` também tem atributo nome, número de portas e uma coleção com portas e um atributo com a tabela de roteamento.

O script `port.py` contém a classe `Port` que tem atributos de indereço IP e MAC. A tabela roteamento do Router está implementada no script `router_table.py` e basicamente ela contém linhas (implementação na classe `TableRow` no script `tablerow.py`) com as colunas destino, próximo hop e porta.

## Principais métodos

Referente ao output da simulação, há o script `write_file.py` que armazena em um arquivo cada passo da simulação: seja reply ou request ICMP ou ARP. Este arquivo é impresso no terminal assim que a simulação termina. Em relação à própria simulação há o script `simulation.py` que inicia fazendo o encaminhamento e retorno de da simulação de ping na rede. 

# Como utilizar o simulador

Para a devida utilização do simulador, deve-se executa-lo através de um terminar que possua a linguagem Python instalada.
O programa deve receber como parametros um arquivo *.txt que apresente a descrição de topologia a ser utilizada, e um par de nodos e uma sequência de caracteres.

```bash
$ python3 main.py <topology_file> <src_node> <dest_node> <data_message>
```

Como por exemplo:

```
$ python3 main.py topologia.txt n1 n2 hello
```

# Limitações do simulador e dificuldades de implementação

Uma limitação importante de mencionar no estado atual da implementação é de que somente uma mensagem `ICMP - Time Exceeded` é impressa quando o TTL chega em 0 pois a simulação é interrompida. Foram encontradas diferenças nos resulstados da implementação atual do simulador com duas das simualações feitas manualmente em aula nas topologias dos arquivos `topologia_041119.txt` e `topologia_061119.txt`. No entanto, as diferenças notadas são que basicamente o pacote só percorre uma rota diferente apenas, o que aparentemente não indica que esteja incorreto.

# Exemplos de execução

```
$ python3 main.py topologia.txt n1 n2 hello
n1 box n1 : ETH (src=00:00:00:00:00:01 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 192.168.0.3? Tell 192.168.0.2;
n2 => n1 : ETH (src=00:00:00:00:00:02 dst=00:00:00:00:00:01) \n ARP - 192.168.0.3 is at 00:00:00:00:00:02;
n1 => n2 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:02) \n IP (src=192.168.0.2 dst=192.168.0.3 ttl=8 mf=0 off=0) \n ICMP - Echo request (data=hello);
n2 rbox n2 : Received hello;
n2 => n1 : ETH (src=00:00:00:00:00:02 dst=00:00:00:00:00:01) \n IP (src=192.168.0.3 dst=192.168.0.2 ttl=8 mf=0 off=0) \n ICMP - Echo reply (data=hello);
n1 rbox n1 : Received hello;
```

```
$ python3 main.py topologia.txt n1 n2 helloworld
n1 box n1 : ETH (src=00:00:00:00:00:01 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 192.168.0.3? Tell 192.168.0.2;
n2 => n1 : ETH (src=00:00:00:00:00:02 dst=00:00:00:00:00:01) \n ARP - 192.168.0.3 is at 00:00:00:00:00:02;
n1 => n2 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:02) \n IP (src=192.168.0.2 dst=192.168.0.3 ttl=8 mf=1 off=0) \n ICMP - Echo request (data=hello);
n1 => n2 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:02) \n IP (src=192.168.0.2 dst=192.168.0.3 ttl=8 mf=0 off=5) \n ICMP - Echo request (data=world);
n2 rbox n2 : Received helloworld;
n2 => n1 : ETH (src=00:00:00:00:00:02 dst=00:00:00:00:00:01) \n IP (src=192.168.0.3 dst=192.168.0.2 ttl=8 mf=1 off=0) \n ICMP - Echo reply (data=hello);
n2 => n1 : ETH (src=00:00:00:00:00:02 dst=00:00:00:00:00:01) \n IP (src=192.168.0.3 dst=192.168.0.2 ttl=8 mf=0 off=5) \n ICMP - Echo reply (data=world);
n1 rbox n1 : Received helloworld;
```

```
$ python3 main.py topologia.txt n1 n3 hello
n1 box n1 : ETH (src=00:00:00:00:00:01 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 192.168.0.1? Tell 192.168.0.2;
r1 => n1 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:01) \n ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n1 => r1 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:05) \n IP (src=192.168.0.2 dst=192.168.1.2 ttl=8 mf=0 off=0) \n ICMP - Echo request (data=hello);
r1 box r1 : ETH (src=00:00:00:00:00:06 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:06) \n ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ETH (src=00:00:00:00:00:06 dst=00:00:00:00:00:03) \n IP (src=192.168.0.2 dst=192.168.1.2 ttl=7 mf=0 off=0) \n ICMP - Echo request (data=hello);
n3 rbox n3 : Received hello;
n3 => r1 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:06) \n IP (src=192.168.1.2 dst=192.168.0.2 ttl=8 mf=0 off=0) \n ICMP - Echo reply (data=hello);
r1 => n1 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:01) \n IP (src=192.168.1.2 dst=192.168.0.2 ttl=7 mf=0 off=0) \n ICMP - Echo reply (data=hello);
n1 rbox n1 : Received hello;
```

```
$ python3 main.py topologia.txt n1 n3 helloworld
n1 box n1 : ETH (src=00:00:00:00:00:01 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 192.168.0.1? Tell 192.168.0.2;
r1 => n1 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:01) \n ARP - 192.168.0.1 is at 00:00:00:00:00:05;
n1 => r1 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:05) \n IP (src=192.168.0.2 dst=192.168.1.2 ttl=8 mf=1 off=0) \n ICMP - Echo request (data=hello);
n1 => r1 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:05) \n IP (src=192.168.0.2 dst=192.168.1.2 ttl=8 mf=0 off=5) \n ICMP - Echo request (data=world);
r1 box r1 : ETH (src=00:00:00:00:00:06 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 192.168.1.2? Tell 192.168.1.1;
n3 => r1 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:06) \n ARP - 192.168.1.2 is at 00:00:00:00:00:03;
r1 => n3 : ETH (src=00:00:00:00:00:06 dst=00:00:00:00:00:03) \n IP (src=192.168.0.2 dst=192.168.1.2 ttl=7 mf=1 off=0) \n ICMP - Echo request (data=hello);
r1 => n3 : ETH (src=00:00:00:00:00:06 dst=00:00:00:00:00:03) \n IP (src=192.168.0.2 dst=192.168.1.2 ttl=7 mf=0 off=5) \n ICMP - Echo request (data=world);
n3 rbox n3 : Received helloworld;
n3 => r1 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:06) \n IP (src=192.168.1.2 dst=192.168.0.2 ttl=8 mf=1 off=0) \n ICMP - Echo reply (data=hello);
n3 => r1 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:06) \n IP (src=192.168.1.2 dst=192.168.0.2 ttl=8 mf=0 off=5) \n ICMP - Echo reply (data=world);
r1 => n1 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:01) \n IP (src=192.168.1.2 dst=192.168.0.2 ttl=7 mf=1 off=0) \n ICMP - Echo reply (data=hello);
r1 => n1 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:01) \n IP (src=192.168.1.2 dst=192.168.0.2 ttl=7 mf=0 off=5) \n ICMP - Echo reply (data=world);
n1 rbox n1 : Received helloworld;
```

```
$ python3 main.py topologia_041119.txt N1 N3 helloworld
N1 box N1 : ETH (src=00:00:00:00:00:01 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 10.0.0.1? Tell 10.0.0.2;
R1 => N1 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:01) \n ARP - 10.0.0.1 is at 00:00:00:00:00:10;
N1 => R1 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:10) \n IP (src=10.0.0.2 dst=20.0.0.2 ttl=8 mf=0 off=0) \n ICMP - Echo request (data=helloworld);
R1 box R1 : ETH (src=00:00:00:00:00:10 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 100.10.20.2? Tell 10.0.0.1;
R2 => R1 : ETH (src=00:00:00:00:00:21 dst=00:00:00:00:00:10) \n ARP - 100.10.20.2 is at 00:00:00:00:00:21;
R1 => R2 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:21) \n IP (src=10.0.0.2 dst=20.0.0.2 ttl=7 mf=0 off=0) \n ICMP - Echo request (data=helloworld);
R2 box R2 : ETH (src=00:00:00:00:00:20 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 20.0.0.2? Tell 20.0.0.1;
N3 => R2 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:20) \n ARP - 20.0.0.2 is at 00:00:00:00:00:03;
R2 => N3 : ETH (src=00:00:00:00:00:20 dst=00:00:00:00:00:03) \n IP (src=10.0.0.2 dst=20.0.0.2 ttl=6 mf=0 off=0) \n ICMP - Echo request (data=helloworld);
N3 rbox N3 : Received helloworld;
N3 => R2 : ETH (src=00:00:00:00:00:03 dst=00:00:00:00:00:20) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=8 mf=0 off=0) \n ICMP - Echo reply (data=helloworld);
R2 => R3 : ETH (src=00:00:00:00:00:20 dst=00:00:00:00:00:31) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=7 mf=0 off=0) \n ICMP - Echo reply (data=helloworld);
R3 => R1 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:12) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=6 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R3 => R1 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:12) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=6 mf=1 off=3) \n ICMP - Echo reply (data=low);
R3 => R1 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:12) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=6 mf=1 off=6) \n ICMP - Echo reply (data=orl);
R3 => R1 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:12) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=6 mf=0 off=9) \n ICMP - Echo reply (data=d);
R1 => N1 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:01) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=5 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R1 => N1 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:01) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=5 mf=1 off=3) \n ICMP - Echo reply (data=low);
R1 => N1 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:01) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=5 mf=1 off=6) \n ICMP - Echo reply (data=orl);
R1 => N1 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:01) \n IP (src=20.0.0.2 dst=10.0.0.2 ttl=5 mf=0 off=9) \n ICMP - Echo reply (data=d);
N1 rbox N1 : Received helloworld;
```

```
$ python3 main.py topologia_061119.txt N1 N5 hello
N1 box N1 : ETH (src=00:00:00:00:00:01 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 10.0.0.1? Tell 10.0.0.2;
R1 => N1 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:01) \n ARP - 10.0.0.1 is at 00:00:00:00:00:10;
N1 => R1 : ETH (src=00:00:00:00:00:01 dst=00:00:00:00:00:10) \n IP (src=10.0.0.2 dst=30.0.0.2 ttl=8 mf=0 off=0) \n ICMP - Echo request (data=hello);
R1 box R1 : ETH (src=00:00:00:00:00:10 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 100.10.20.2? Tell 10.0.0.1;
R2 => R1 : ETH (src=00:00:00:00:00:21 dst=00:00:00:00:00:10) \n ARP - 100.10.20.2 is at 00:00:00:00:00:21;
R1 => R2 : ETH (src=00:00:00:00:00:10 dst=00:00:00:00:00:21) \n IP (src=10.0.0.2 dst=30.0.0.2 ttl=7 mf=0 off=0) \n ICMP - Echo request (data=hello);
R2 box R2 : ETH (src=00:00:00:00:00:21 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 100.10.30.2? Tell 100.10.20.2;
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:21) \n ARP - 100.10.30.2 is at 00:00:00:00:00:31;
R2 => R3 : ETH (src=00:00:00:00:00:21 dst=00:00:00:00:00:31) \n IP (src=10.0.0.2 dst=30.0.0.2 ttl=6 mf=0 off=0) \n ICMP - Echo request (data=hello);
R3 box R3 : ETH (src=00:00:00:00:00:30 dst=FF:FF:FF:FF:FF:FF) \n ARP - Who has 30.0.0.2? Tell 30.0.0.1;
N5 => R3 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:30) \n ARP - 30.0.0.2 is at 00:00:00:00:00:05;
R3 => N5 : ETH (src=00:00:00:00:00:30 dst=00:00:00:00:00:05) \n IP (src=10.0.0.2 dst=30.0.0.2 ttl=5 mf=0 off=0) \n ICMP - Echo request (data=hello);
N5 rbox N5 : Received hello;
N5 => R3 : ETH (src=00:00:00:00:00:05 dst=00:00:00:00:00:30) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=8 mf=0 off=0) \n ICMP - Echo reply (data=hello);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=7 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=7 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R2 => R3 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:31) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=6 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R2 => R3 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:31) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=6 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=5 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=5 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R2 => R3 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:31) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=4 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R2 => R3 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:31) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=4 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=3 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=3 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R2 => R3 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:31) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=2 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R2 => R3 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:31) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=2 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=1 mf=1 off=0) \n ICMP - Echo reply (data=hel);
R3 => R2 : ETH (src=00:00:00:00:00:31 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=1 mf=0 off=3) \n ICMP - Echo reply (data=lo);
R2 => R2 : ETH (src=00:00:00:00:00:22 dst=00:00:00:00:00:22) \n IP (src=30.0.0.2 dst=10.0.0.2 ttl=0) \n ICMP - Time Exceeded;
```
