# Etapa 1.4, Parte A: carga útil de referência (proposta)

Estado: **aguardando a escolha do Fabio.** Nada foi dimensionado.

## Escopo

Esta etapa cobre **só os trechos no espaço** da missão A:
- saída da órbita baixa da Terra (407 km);
- captura na órbita de 1 sol de Marte;
- saída de Marte;
- chegada à Terra (reentrada direta da cápsula).

**Descida, pouso, operações de superfície e subida a partir da superfície ficam para a Fase 2**,
inclusive o veículo de subida, o lander e o Δv da subida até a órbita de 1 sol (ADR 0003).

## Massas publicadas do Mars Sample Return (fontes primárias)

Todas as citações abaixo foram conferidas no texto dos documentos. Páginas e slides são os
impressos.

| Item | Valor | Fonte |
| :- | :- | :- |
| ERO, massa úmida no lançamento | ≈ 6,5 t ("Approx 6.5 Tonnes (wet mass)") | [F22] Yau (ESA), 2021, slide 7 |
| ERO, módulo principal ("Return Stage"), massa seca | 2200 kg | [F22] slide 8 |
| ERO, propulsão elétrica do módulo principal | Isp 4000 s; 1100 kg de xenônio; ΔV 10 km/s | [F22] slide 8 |
| ERO, módulo de inserção ("Drop Stage", químico, descartado em Marte) | 600 kg secos; 1900 kg de propelente | [F22] slide 8 |
| CCRS, sem sensores de encontro (2021) | ≈ 500 kg | [F22] slide 8 |
| EES (cápsula) | ≈ 100 kg | [F22] slide 8 |
| CCM (descartado em Marte) | > 200 kg | [F22] slide 8 |
| OS (contêiner de amostras) | ≈ 8 kg | [F22] slide 8 |
| CCRS (2024): captura 240 + montagem 280 + proteção contra micrometeoroides 100 | ≈ 620 kg | [F23] Sarli et al., Acta Astronautica 2024, p. 5 |
| EEV, massa de entrada (alocação) | < 92,5 kg; base de 1,25 m; entrada de 12,0 km/s | [F24] Corliss & Edquist (NASA), 2021, slide 27 |
| EEV, valor máximo esperado com COS (DAC-3A, set. 2020) | 89,9 kg (COS 26,2 kg, valor máximo admitido) | [F24] slide 30 |
| EES, artigo de teste em escala real | 98,58 kg; diâmetro de 1,273 m | [F26] Karlgaard et al. (NASA), NTRS 20240007755, Tabela 2 |
| Amostras: meta | 500 g; ~32 tubos de no máximo 15–16 g | [F25] MSR IRB-2, 2023, p. 24 |
| Amostras: requisito | 30 tubos | [F25] p. 26 |

Só para contexto, elementos de superfície e subida, fora do escopo: MAV sólido de 394 a 400 kg com
carga útil de 16 kg (30 tubos), em Jackman et al. 2019 (NTRS 20190032302, p. 4) e Yaghoubi &
Schnell 2020 (NTRS 20200002328); SRL com teto de 7150 kg no lançamento, em Martin-Mur et al.,
ISSFD 2024, p. 2.

Não confirmados e deixados de fora:
- os 7000 kg do ERO e os ~90 kg do EES que aparecem na página web da NASA (sem documento nem página,
  e sem dizer se a massa é úmida);
- o Isp do módulo químico do ERO;
- a massa do ERO na chegada a Marte.

As versões também divergem: 4 propulsores elétricos em 2021 contra 5 RIT-2X em 2024, e CCRS de
500 kg contra 620 kg.

## Opções de carga útil para a missão A

Detalhe e fontes por item em `config/carga_util.yaml`. "Carga útil" aqui é o que o veículo leva,
**sem** os estágios de propulsão e sem a estrutura do próprio veículo, que entram na Parte B pela
fração estrutural.

| Opção | Até a órbita de Marte | Descartado em Marte | Volta à Terra (cápsula + amostras) | Base |
| :- | -: | -: | -: | :- |
| **CU-1**: carga do ERO, ESA 2021 | 800 kg (CCRS 500 + EES 100 + CCM 200) | CCM 200 kg | 100 kg | [F22] |
| **CU-2**: CCRS NASA 2024 + EEV DAC-3A | 709,9 kg (CCRS 620 + EEV 89,9) | — | 89,9 kg | [F23], [F24] |
| **CU-3**: cota inferior, só a cápsula | 92,5 kg | — | 92,5 kg | [F24] |

Compromissos:

- **CU-1** reproduz a decomposição publicada do ERO, com o único conjunto coerente de massas de
  2021. O CCM entra como valor mínimo (> 200 kg), e não se sabe se as massas têm margem.
- **CU-2** usa os valores mais recentes do CCRS (2024) e a cápsula detalhada da NASA. A fonte não
  diz se os 620 kg incluem a cápsula; somar a cápsula à parte, como foi feito, é a escolha
  conservadora.
- **CU-3** não tem sistema de captura em órbita. Só se aplica se as amostras chegarem à órbita já
  dentro da cápsula, o que depende da arquitetura de subida (Fase 2). Serve de cota inferior para
  a sensibilidade.

## Pontos de atenção para a escolha

1. **Velocidade de entrada.** A cápsula do MSR foi projetada para 12,0 km/s ([F24], slide 27) e o
   teste de 2024 cita 11,6 km/s ([F26]). A missão A reentra a 12,34 km/s, dentro do limite da P-011
   (12,9 km/s) mas acima do ponto de projeto dessa cápsula. Usar as massas de CU-1 e CU-2 implica
   uma cápsula projetada para uma entrada mais rápida, ainda não quantificada.
2. **Arquitetura de chegada à Terra.** No MSR, o ERO solta a cápsula e não é capturado pela Terra. No
   modelo deste estudo, a chegada à Terra não tem Δv propulsivo. Uma manobra de desvio do orbitador
   depois de soltar a cápsula não está modelada e pode entrar como margem na Parte B.
3. **Propulsão.** O ERO usa propulsão elétrica (Isp de 4000 s) na volta. As trajetórias deste estudo
   são impulsivas (cônicas emendadas), então na Parte B só faz sentido usar propulsão química, a
   menos que se modele trajetória de baixo empuxo. Esse é um ponto a decidir na Parte B.
