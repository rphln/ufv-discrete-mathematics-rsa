# Relatório do Trabalho 2

Nome
: Raphael Nepomuceno

Matrícula
: 89389

Chave pública
: $(n, e) = (2070279697, 23683)$

Chave privada
: $d = 1085225327$

## Geração de chaves

Os valores $p$ e $q$ são números aleatórios no intervalo $[32768,55108]$, de modo que $1\,073\,741\,824 \leq p \cdot q \leq 3\,036\,891\,664$. Utiliza-se, então, o pequeno teorema de Fermat, com todos valores $a \in [0,20)$, para checar sua primalidade. Por fim, $e$ é um valor aleatório no intervalo $[2, 65\,536]$ que obedece às condições necessárias da geração de chaves.

## Mensagens recebidas

| Remetente         |                    Decodificada                    |
| ----------------- | :------------------------------------------------: |
| Olavo/Gabriel B.  |                   `HELLOWORLDXX`                   |
| Lúcio             | `ESSAXMENSAGEMXVAIXSEXAUTOXDESTRUIRXEMXCINCOXANOS` |
| Matheus/Petterson |                   `OLARAPHAELXX`                   |

## Mensagens assinadas

A implementação da decodificação de mensagens foi reutilizada sem mudanças para checar as mensagens assinadas, trocando apenas o parâmetro $d$ por $e$.

| Remetente        | Mensagem original | Mensagem obtida | Assinada? |
| ---------------- | ----------------- | --------------- | :-------: |
| Erick/Sávio      | `OI`              | `AAOI`          |    Sim    |
| Erick/Sávio      | `SIGN`            | `SIGN`          |    Sim    |
| Erick/Sávio      | `TAASSINADA`      | `BT`            |    Não    |
| Gabriel/Matheus  | `ASSINADO`        | `ASSINADO`      |    Sim    |
| Gabriel/Matheus  | `MENSAGEM`        | `MENSAGEM`      |    Sim    |
| Gabriel/Matheus  | `AAAABBBBCCCC`    | `AAAAOZ^`       |    Não    |
| Olavo/Gabriel B. | `MATDISCRETA`     | `MATDISCRETAX`  |    Sim    |
| Olavo/Gabriel B. | `MATDISCRETA`     | `OdOdM\nOpO`    |    Não    |
| Olavo/Gabriel B. | `HELLOWORLD`      | `HELLOWORLDXX`  |    Sim    |

## Chaves privadas

Para um determinado $p$, o código testa:

1. Se $p \cdot q = n$.
2. Se $p$ é primo utilizando o pequeno teorema de Fermat.
3. Se $\mathrm{gcd}(e, \phi) = 1$.

Caso as três condições sejam válidas, a chave privada $d$ é então calculada.

O código para descobrir as chaves foi executado utilizando o [PyPy](https://www.pypy.org/). Utilizando as restrições $2 \leq p < 2^{32}$ e $q = \lfloor n \div p \rfloor$, foram necessários aproximadamente 2 segundos para obter a tabela abaixo.

| Nome                           |      n       |      e       |      d       |
| ------------------------------ | :----------: | :----------: | :----------: |
| Lucas, Mariana                 | `636367279`  | `1649410831` |  `20786871`  |
| Helvécio                       | `1015605091` |   `12689`    | `828743849`  |
| Caio/ Joao                     | `205977601`  |   `25243`    | `204598939`  |
| Lucas Vieira                   | `148773727`  |   `10667`    | `110596163`  |
| Erick, Sávio                   | `1698802277` |   `88987`    | `261315763`  |
| Gabriel Félix, Matheus Aguilar | `514449163`  | `490925531`  |  `69783971`  |
| Lucas Reis, Natan Garcias      | `232774631`  | `1000000007` | `218740247`  |
| Daniela Assis                  | `1194673973` |   `65071`    | `352258255`  |
| Raphael Nepomuceno             | `2070279697` |   `23683`    | `1085225327` |
| Gabriel Bezerra, Olavo         | `2131293569` | `517754681`  | `1312672277` |
| Lúcio                          | `1715190437` |   `35027`    | `685122299`  |
| Renan                          | `4749073919` |   `34879`    | `411458911`  |
| Lucas Campos                   | `1806430763` |   `33431`    | `966309191`  |
