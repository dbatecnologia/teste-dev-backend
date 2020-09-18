# Instalação

Instalar os seguintes pacotes/módulos:
```text
apt install python3-pip
apt install python3-setuptools
apt install git
apt install i2c-tools
pip3 install pyserial
pip3 install smbus2
pip3 install twisted
pip3 install tornado
pip3 install -e git+https://github.com/collab-project/atcmd.git#egg=atcmd
```

# Execução

Para executar o projeto é necessário estar logado com o usuário _root_ (``sudo su``).
Depois execute o módulo de simulação dos dispositivos:
```text
cd implementacao/fake_devices/
python3 main.py
```
O módulo ``fake_devices`` irá criar as seguintes interfaces:
* ``/dev/i2c-100``: Falso barramento I2C.
* ``/dev/ttyACM100``: Porta serial do falso GPS.
* ``/dev/ttyACM200``: Porta serial do falso GPRS.

Essas interfaces são _links_ simbólicos para as interfaces de simulação dos dispositivos. Normalmente as portas mudam e para não ficar mudando o arquivo de configuração (o arquivo será detalhado mais adiante) para toda vez que as portas mudarem, são criados os _links_ simbólicos, que sempre estarão com a mesma numeração.

No barramento I2C (``/dev/i2c-100``) estão configurados três endereços: 0x10, 0x26 e 0x61, que seriam os endereços para a simulação dos sensores de luminosidade, distância e de bateria, respectivamente. Como não foi especificado nenhum modelo de sensor, na simulação apenas são realizadas leituras de dados. Não foi simulado nenhuma configuração desses sensores. Ao ler o endereço do sensor fictício de luminosidade será retornado um valor entre 0 à 100, 0 escuro e 100 claro. O sensor de distância retorna um valor entre 0 à 255 simulando valores entre 0 à 2.55 metros. E o sensor de bateria retorna um valor entre 90 à 120, ou seja, de 9V à 12V.

NOTA: Não é necessário carregar manualmente os módulos I2C para configurar os falsos sensores. Isso já é realizado pelo módulo.

Com a simulação dos dispositivos em execução é possível iniciar a aplicação. Em um outro terminal, com o usuário _root_, entre no seguinte diretório e execute:
```text
cd implementacao/src/
python3 main.py -c config.json
```
Nesse comando o módulo está carregando as configurações apartir do arquivos ``config.json``.

No mesmo diretório há um simples servidor de teste que recebe as requisições via REST:
```text
cd implementacao/src/
python3 server_rest_test.py
```

# Configuração

A configuração é realizada pelo arquivo ``implementacao/src/config.json``. O arquivo possui o seguinte conteúdo:

```text
{
    "server": {
        "send_interval": 30,
        "url": "http://localhost:5000"
    },
    "i2c_sensors": {
        "distance_sensor_addr": 38,
        "battery_sensor_addr": 97,
        "bus": 100,
        "light_sensor_addr": 16
    },
    "gprs": {
        "port": "/dev/ttyACM200",
        "apn": "tim.com.br",
        "rate": 9600
    },
    "tcp_port": 1234,
    "gps": {
        "port": "/dev/ttyACM100",
        "rate": 9600
    }
}
```
Onde:
* ``server``: Configuração do servidor.
    * ``send_interval``: Intervalo em que os dados são enviados para o servidor (Via REST).
    * ``url``: Endereço do servidor.
* ``i2c_sensors``: Configuração dos sensores I2C.
    * ``distance_sensor_addr``: Endereço do sensor de distância.
    * ``battery_sensor_addr``: Endereço do sensor de bateria.
    * ``light_sensor_addr``: Endereço do sensor de luminosidade.
    * ``bus``: Número do barramento I2C.
* ``gprs``: Configuração para a comunicação com o GPRS.
    * ``port``: Porta serial.
    * ``apn``: APN utilizada para a estabilização da comunicação.
    * ``rate``: Velocidade da porta serial.
* ``tcp_port``: Porta do servidor tcp local utilizado para configuração.
* ``gps``: Configuração para a comunicação com o GPS.
    * ``port``: Porta serial
    * ``rate``: Velocidade da porta serial.

Também é possível fazer algumas alterações com o _scritp_ ``implementacao/src/cli.py`` como mudança de servidor em que os dados serão enviados e mudança no horário local.
```text
python3 cli.py -h
Usage: cli.py <opt [arg]>
opt:
	-h: show this help
	-i: show devices informations
	-s: show url server
	-t: show current time
	-d: show current date
	-u [server]: change server
	-n [time hh:mm:ss]: change current time
	-m [date aaaa-mm-dd]: change current date
```

Além disso, foi desenvolvido um _front-end_ simples para mostrar dados dos sensores e realizar as mesmas configurações que o _script_ ``cli.py``. Em um outro terminal execute:
```
cd implementacao/web_config
python3 main.py
```
Entre no seguinte endereço no navegador _web_:
http://127.0.0.1:8888
senha: admin,
usuário: admin

# Comunicação REST

A aplicação envia um POST HTTP com as informações no formato JSON no corpo da mensagem. O caminho utilizando para o POST é ``/api/v1.0/devices/<device_id>``. O ``<device_id>`` é um número inteiro obtido pelo endereço MAC da interface de rede.

Exemplo de JSON no corpo do POST HTTP:
```text
{
   "gprs_connection":true,
   "distance":0.81,
   "gps":{
      "latitude_direction":"S",
      "latitude":27.6020821,
      "longitude":48.5769515,
      "longitude_direction":"W"
   },
   "battery":9.5,
   "light":31
}
```
* ``gprs_connection``: retorna o estado da conexão do GPRS.
* ``distance``: medida do sensor de distância em metros.
* ``battery``: medida do sensor de bateria em Volts.
* ``light``: medida do sensor de luminosidade em %.
* ``gps``: Coordenadas de localização obtida pelo GPS.

# Teste unitário

No diretório ``implementacao/tests`` estão os testes unitário do módulos das interfaces e dos dispositivos fictícios. Para executar todos os testes unitários execute o _script_ que está no diretório ``implementacao/``
```
bash test.sh
```

# Dispositívos fictícios

* ``I2C``: Para a simulação do barramento I2C foi utilizado o I2C-Stub. O módulo i2c-stub é um driver I2C falso utilizado para auxiliar no processo de desenvolvimento quando não há dispositivos com barramento I2C.
* ``Serial``: Para a simulação da porta serial foi utilizado um pseudo terminal (PTY). O PTY é um arquivo (Geralmente localizado em ``/dev/pts/``) que algum _software_ pode gravar ou ler como se fosse uma conexão serial.

* ``GPIO``: É possível simular GPIOs com o [GPIO-mockup](https://wiki.peori.space/page/gpio). Para utilizá-lo é necessário compilar o módulo e carregar no _kernel_.

NOTA: Nesse projeto não foi implementado a interface GPIO falsa, portanto, não foi implementado o acionamento da iluminação.
