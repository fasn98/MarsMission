# Etapa 2.4: lançamento e DLA

Estado: **aguardando o portão do Fabio**. Resultados em `results/etapa2.4/lancamento.md` e `.yaml`,
gerados por `tools/lancamento.py` a partir de `config/lancadores.yaml`. Todos os números abaixo vêm
desses arquivos.

## 1. O que se compara

- **Duas formas de chegar à trajetória para Marte**, com orbitador e lander em lançamentos separados
  (ADR 0005):
  - **(a) Injeção direta:** o lançador entrega o veículo no C3 da janela, sem estágio de saída próprio.
  - **(b) Órbita baixa + estágio criogênico próprio:** é o modelo atual. O estágio de saída (LOX/LH2)
    é redimensionado para o C3 e a DLA de cada janela.
- **Veículos:** os do caso de base da Etapa 2.3, com órbita de encontro de 300 × 24.992 km.

| Veículo | Massa injetada na trajetória | Na órbita baixa (modelo, janela de 2028) |
| :- | -: | -: |
| Orbitador, regra (iii) | 6.027 kg | 18.294 kg |
| Orbitador, missão A | 3.548 kg | 10.770 kg |
| Lander | 3.727 kg | 11.313 kg |

As somas na órbita baixa (29.607,5 e 22.083,1 kg) diferem em 0,4 e 0,2 kg dos totais da Etapa 2.3
(29.607,1 e 22.082,9 kg). O motivo é o `config` arredondado: 442,3 kg contra os 442,27 kg da iteração.

- **Janelas verificadas** (pedido do Fabio): para o orbitador da regra (iii), cada janela do envelope
  com o seu C3 e a sua DLA; vale o caso mais restritivo. A missão A é só uma delas. O lander também
  foi verificado nas quatro janelas.

| Janela | Partida* | C3 (km²/s²) | DLA |
| :- | :- | -: | -: |
| 2028, conjunção (missão A) | 2028-11-23 | 9,10 | +29,2° |
| 2031, conjunção | 2030-12-24 | 10,70 | +14,8° |
| 2033, conjunção | 2033-04-16 | 9,11 | **−55,5°** |
| 2035, conjunção | 2035-06-28 | 10,44 | +8,7° |

\* Datas como gravadas na Etapa 1.3. Elas saem um dia antes da época real (ver seção 7).

- **Margem** = capacidade / massa − 1.

## 2. Lançadores e fontes

| Lançador | Categoria | Curva de C3 | LEO a 400 km |
| :- | :- | :- | :- |
| Falcon 9 (ASDS) | operacional | ELVPerf [F79], C3 de 0 a 10 | ELVPerf, 28,5° e 51,6° |
| Falcon Heavy (recuperação / descartável) | operacional | ELVPerf, C3 de 0 a 20 | não publicada |
| Vulcan VC2 / VC4 / VC6 | operacional | ELVPerf; em C3 = 20 difere do guia [F80] em +3,1 % / −2,0 % / +0,4 % (o guia é a configuração "S") | ELVPerf |
| Atlas V 541 / 551 | operacional | **sem curva publicada** [F27] | guia [F27], 28,5° |
| Ariane 64 | operacional | **só C3 = 6,25** ("free declination", [F81]) | só 250 km [F81] |
| New Glenn | **anunciado** ("under development", [F79]) | ELVPerf | ELVPerf |
| SLS Block 1, 5 m + iCPS | **anunciado** (não obtive fonte primária de voo desta configuração de carga) | leitura de gráfico de 2014 [F84], ±1–2 t | não usada |

- **Fora da lista:**
  - Delta IV Heavy: sem curva de C3 [F85].
  - H3, Longa Marcha 5 e Starship: sem guia público obtido.
- **O guia da SpaceX não publica desempenho** ("available upon request", [F82]). Os números do Falcon
  vêm do site de desempenho da NASA (ELVPerf), consultado em 2026-10-27.
  - As respostas brutas estão em `tests/data/elvperf/`.
  - Um teste confere que o `config` bate com elas.

## 3. DLA e centros de lançamento

- **Eastern Range:**
  - Latitude 28,45° e azimutes de 40° a 115° [F13], p. 8.
  - Latitudes das plataformas do Falcon: SLC-40 a 28,562° e LC-39A a 28,608° [F82].
- **Saída coplanar:** exige |DLA| ≤ inclinação da órbita de estacionamento. Com o azimute de 40°,
  cos i = cos φ · sen Σ dá **i_máx = 55,59° a 55,65°**, conforme a plataforma.
- **Faixa sem penalidade:** a curva do ELVPerf vale para |DLA| ≤ 28,5° [F79]. Acima disso, o
  desempenho cai [F83][F87].
  - Já houve lançamentos do Cabo nesses casos. O MRO, com DLA > 41°, usou "out-of-plane targeting" do
    Centaur [F86].
  - Para (a), a massa entregue é multiplicada pelo fator de [F83], interpolado entre 28,5° (1,0) e
    60° (0,65) (P-036).
- **Opção (b):**
  - A órbita baixa é a de 28,5° ou a de 51,6° (as inclinações com dado).
  - Quando |DLA| passa da inclinação, a assíntota precisa sair β = |DLA| − i do plano. A queima de
    saída, no perigeu, gira o plano em torno do vetor posição.
  - Como a assíntota fica a ν∞ = arccos(−1/e) ≈ 150° do perigeu, o giro necessário é
    θ = arcsin(sen β / sen ν∞), cerca de 2β (P-037). O Δv extra de cada linha está gravado nos resultados.
- **Por janela:**
  - **2028 (+29,2°):** multiplicador 0,997 em (a). Em (b), β = 0,73° e θ = 1,47° a partir de 28,5°, com
    +8 m/s.
  - **2031 (+14,8°) e 2035 (+8,7°):** dentro da faixa, sem penalidade.
  - **2033 (−55,5°): é a janela mais restritiva.**
    - É alcançável com subida coplanar, mas só 0,13° a 0,19° abaixo do limite de azimute, conforme a
      plataforma.
    - Em (a), o multiplicador é **0,764**.
    - Em (b), a partir de 51,6°: β = 3,85°, θ = 7,72° e **+211 m/s**.
    - Em (b), a partir de 28,5°: θ = 64,9° e +7,0 km/s. O estágio fica **inviável**; por isso o Atlas V
      (só com LEO a 28,5°) não serve em 2033.
    - O Falcon User's Guide põe inclinações de 55° a 65° na faixa de "dog leg" [F82].

## 4. Resultado por veículo (pior margem entre as janelas)

**Orbitador, regra (iii)** (6.027 kg injetados). Entre os lançadores com dado em todas as janelas, o
caso mais restritivo é 2033.

| Lançador | (a) injeção direta | (b) LEO + estágio próprio |
| :- | -: | -: |
| Falcon Heavy (descartável) | **+59 %** | sem dado de LEO |
| Vulcan VC6 | **+18 %** | **+26 %** |
| Vulcan VC4 | −8 % | **+6 %** |
| Vulcan VC2 | −39 % | −20 % |
| Falcon Heavy (recuperação) | −33 % | sem dado de LEO |
| Falcon 9 (ASDS) | sem dado (C3 > 10 em 2031 e 2035) | −26 % |
| Atlas V 541 / 551 | sem curva de C3 | inviável em 2033 (só LEO a 28,5°) |
| Ariane 64 | sem dado no C3 das janelas | sem dado a 400 km |
| *New Glenn (anunciado)* | −34 % | +74 % |
| *SLS Block 1 (anunciado)* | +152 % | — |

**Orbitador, missão A** (3.548 kg, só 2028). Servem todos os operacionais com dado:
- Vulcan VC2/4/6, Falcon Heavy e Atlas V 541/551.
- Falcon 9 em (b), com +44 %. Em (a) ele fica com −35 %.

**Lander** (3.727 kg). Entre os lançadores com dado em todas as janelas, o caso mais restritivo é 2033.

| Lançador | (a) | (b) |
| :- | -: | -: |
| Falcon 9 (ASDS) | sem dado (C3 > 10 em 2031 e 2035) | **+19 %** |
| Falcon Heavy (recuperação) | **+8 %** | sem dado |
| Falcon Heavy (descartável) | **+158 %** | sem dado |
| Vulcan VC2 | −1 % | **+29 %** |
| Vulcan VC4 / VC6 | **+49 % / +90 %** | **+71 % / +104 %** |
| Atlas V 541 / 551 | sem curva | inviável em 2033 |
| *New Glenn (anunciado)* | +6 % | +181 % |
| *SLS Block 1 (anunciado)* | +308 % | — |

**Lançamentos da arquitetura: 2**, um por veículo. Os dois veículos têm lançador operacional com
margem positiva em todas as janelas:
- **Orbitador (iii):** Falcon Heavy descartável (a), Vulcan VC6 (a ou b) e Vulcan VC4 (b, com só +6 %).
- **Lander:** Falcon 9 (b); Falcon Heavy (a); Vulcan VC2 (b); VC4 e VC6 (a ou b).

**Sem dado publicado:**
- Ariane 64 (escape só em C3 = 6,25).
- Atlas V (sem curva de C3).
- Falcon Heavy em LEO de 400 km.
- Falcon 9 acima de C3 = 10.

## 5. Revisão da janela de 2033

A mesma busca da Etapa 1.3 (`tools/missoes.py`), agora com |DLA| limitado. A DLA foi acrescentada à
grade do porkchop, e a busca ganhou um limite opcional de |DLA|.

| Limite de \|DLA\| | Δv total | Partida* | C3 | DLA |
| :- | -: | :- | -: | -: |
| sem limite (atual) | 5,889 km/s | 2033-04-16 | 9,11 | −55,5° |
| 50° | 5,912 km/s | 2033-04-22 | 9,60 | −49,7° |
| 40° | 6,150 km/s | 2033-05-06 | 13,59 | −39,9° |
| 28,5° | 6,442 km/s | 2033-03-01 | 12,19 | +4,7° |

- O envelope atual é 5,911 km/s (2035).
- **Com |DLA| ≤ 50°:**
  - O Δv de 2033 fica 1 m/s acima desse envelope e passaria a defini-lo.
  - A 2033 alternativa continua sendo a janela mais restritiva, agora com multiplicador de ~0,90 em (a).
    Em (b) não há giro, porque 49,7° < 51,6°.
  - O orbitador passa a ter:
    - Falcon Heavy descartável: +86 % em (a);
    - Vulcan VC6: +38 % em (a) e +34 % em (b), contra +18 % e +26 % hoje;
    - Vulcan VC4: +8 % em (a) e +13 % em (b), contra −8 % e +6 % hoje. O VC4 passa a servir também em (a).
  - O lander passa a ter o Vulcan VC2 também em (a), com +16 %.
  - O Atlas V continua sem servir em 2033: só tem LEO a 28,5°.
- **Com |DLA| ≤ 28,5°:** sem penalidade de lançamento, mas o envelope sobe 0,53 km/s.
- **A oposição de 2033 é inviável** (25,7 km/s na Etapa 1.3) e fica fora.

Pior margem com cada alternativa de 2033 está em `results/etapa2.4/lancamento.md`.

## 6. Leitura (sem decisão)

1. **A arquitetura fecha com 2 lançamentos de lançadores operacionais em todas as janelas.**
   - O orbitador da regra (iii) só cabe em Falcon Heavy descartável, Vulcan VC6 ou Vulcan VC4 (este só
     em (b), com +6 %).
   - O lander cabe em vários.
2. **A janela de 2033 é a que restringe,** pela DLA de −55,5°, quase no limite de azimute do Cabo.
   - O multiplicador de 0,764 vem de uma tabela aproximada para Atlas V e Delta IV (P-036).
   - Trocar a trajetória de 2033 por uma com |DLA| ≤ 50° custa 23 m/s e alivia todos os lançadores.
   - Em (b), elimina o giro de plano de 211 m/s.
3. **(a) × (b):**
   - (b) dá mais margem ao Vulcan, mas leva um estágio LOX/LH2 próprio, com armazenamento criogênico
     e ensaios próprios.
   - (a) dispensa esse estágio, e o Falcon Heavy descartável só aparece em (a), por falta de dado de LEO.
   - A escolha é de arquitetura.
4. **New Glenn e SLS** ficam separados como "desempenho anunciado, não demonstrado".

## 7. Achado fora do escopo: datas gravadas um dia antes

- **O defeito:** as datas das missões (Etapa 1.3 em diante) são impressas com `spice.et2utc` a partir
  de épocas à **meia-noite TDB**. Como TDB está ~69 s à frente de UTC, a data impressa é a do dia
  anterior.
  - Exemplo: a partida da missão A é 2028-11-24 00:00 TDB, impressa como "2028-11-23".
- **Alcance:** só os rótulos de data estão errados. C3, DLA e Δv estão certos para as épocas reais.
  - `tests/test_lancamento.py` documenta isso: reconstrói a época da missão A a partir da data gravada
    + 1 dia e reproduz C3 e DLA.
- **Não corrigido nesta etapa.** A correção (imprimir em TDB ou somar o dia) mexe nos relatórios da
  Fase 1 e nos ADRs. A decisão é do Fabio.

## 8. Premissas novas (NÃO VALIDADAS)

| Premissa | Conteúdo |
| :- | :- |
| P-036 | Multiplicador de DLA do Atlas V/Delta IV [F83] aplicado a todos os lançadores, com interpolação linear |
| P-037 | LEO de 400 km usada para 407 km; órbita baixa a 28,5° ou 51,6°; giro de plano no perigeu, θ = arcsin(sen β / sen ν∞) |

## 9. Limitações

- Não verificados:
  - diâmetro da coifa contra o tamanho dos veículos (não definido);
  - período de lançamento (só o dia ótimo de cada janela);
  - penalidade de janela finita ("Instantaneous launch attempt", [F79]).
- Capacidade interpolada linearmente entre os pontos publicados.
- A curva do SLS é leitura de gráfico de 2014.
- Lander: a velocidade de entrada em Marte muda com a janela, mas a razão pousada/entrada (P-018) foi
  mantida.
- Opção (b): o armazenamento de LH2 na órbita baixa antes da queima não foi modelado.
