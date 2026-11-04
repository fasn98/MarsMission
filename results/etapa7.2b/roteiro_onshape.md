# Roteiro no Onshape: veículos dentro das coifas (gerado por tools/encaixe_coifas.py)

**VERIFICAÇÃO geométrica do modelo, não validação.** O envelope do Vulcan é leitura de figura do guia, e o do Falcon é o STEP do fabricante amostrado.

**Não conferido:** os arquivos não foram compilados aqui, e as páginas de ajuda do Onshape não abriram na consulta. Os nomes de botões da Assembly vêm de memória e podem variar. Se algo não bater, anote o que apareceu.

## A. Colar os Feature Studios

1. Abra o documento "MarsMission Fase 7", ou crie um documento novo só para esta etapa.
2. Crie um Feature Studio chamado `envelope_vulcan`, apague o conteúdo e cole `results/etapa7.2b/envelope_vulcan.fs`. Clique em Commit e confira se não há erro.
3. Crie um Feature Studio chamado `envelope_falcon_heavy`, apague o conteúdo e cole `results/etapa7.2b/envelope_falcon_heavy.fs`. Clique em Commit e confira se não há erro.
4. Crie um Feature Studio chamado `lander_4_65`, apague o conteúdo e cole `results/etapa7.2b/lander_4_65.fs`. Clique em Commit e confira se não há erro.
5. Crie um Feature Studio chamado `lander_4_5`, apague o conteúdo e cole `results/etapa7.2b/lander_4_5.fs`. Clique em Commit e confira se não há erro.
6. Crie um Feature Studio chamado `orbitador`, apague o conteúdo e cole `results/etapa7.2b/orbitador.fs`. Clique em Commit e confira se não há erro.

## B. Criar os Part Studios

7. Crie um Part Studio chamado `Vulcan leitura 1` e adicione a feature "MarsMission envelope Vulcan". Em "Leitura do envelope", escolha "Contorno reto entre as cotas".
8. Crie um Part Studio chamado `Vulcan leitura 2` e adicione a feature "MarsMission envelope Vulcan". Em "Leitura do envelope", escolha "Diametro menor desde o plano da interface".
9. Crie um Part Studio chamado `Falcon Heavy` e adicione a feature "MarsMission envelope Falcon Heavy".
10. Crie um Part Studio chamado `Lander 4,65` e adicione a feature "MarsMission lander_4_65". Marque "Assign materials".
11. Crie um Part Studio chamado `Lander 4,5` e adicione a feature "MarsMission lander_4_5". Marque "Assign materials".
12. Crie um Part Studio chamado `Orbitador` e adicione a feature "MarsMission orbitador". Marque "Assign materials".
13. Em `Lander 4,65`, selecione todas as peças e abra Mass Properties. Esperado: 3 190,4 kg e CG em 0,026, −0,026, 3,003 m.
14. Em `Lander 4,5`, selecione todas as peças e abra Mass Properties. Esperado: 3 154,7 kg e CG em 0,026, −0,027, 2,099 m.
15. Em `Orbitador`, selecione todas as peças e abra Mass Properties. Esperado: 6 506,2 kg e CG em 0,000, 0,000, 1,393 m.
16. Confira se cada envelope aparece transparente. Se não aparecer, ajuste a aparência à mão; isso não muda nenhum número.

## C. Montar uma Assembly para cada configuração

| Assembly | Veículo | Envelope |
| :- | :- | :- |
| A1 | Lander 4,5 | Vulcan leitura 1 |
| A2 | Lander 4,5 | Vulcan leitura 2 |
| A3 | Lander 4,65 | Vulcan leitura 1 |
| A4 | Lander 4,65 | Vulcan leitura 2 |
| A5 | Orbitador | Falcon Heavy |

17. Crie uma Assembly para cada linha da tabela (A1, A2, A3, A4, A5). Repita os passos abaixo em cada uma.
18. Clique em Insert e insira o Part Studio do envelope. Clique com o botão direito nele e escolha Fix.
19. Insira o Part Studio do veículo, inteiro.
20. Arraste uma peça do veículo. Se ela sair sozinha, selecione todas as peças do veículo e crie um Group, para que andem juntas.
21. Escolha o mate Fastened.
22. Clique no mate connector do envelope, no plano da interface.
23. Clique no mate connector do veículo, no plano da interface.
24. Confirme. O veículo deve ficar dentro do envelope, com o topo para cima.
25. Se o veículo ficar de cabeça para baixo, use a opção de inverter o eixo no diálogo do mate.

## D. Medir as folgas (ferramenta Measure)

Selecione as duas entidades da tabela e leia a distância mínima. A leitura deve bater com o valor esperado na terceira casa.

| Assembly | Medida | Selecione no veículo | Selecione no envelope | Esperado (m) | Folga com sinal (m) |
| :- | :- | :- | :- | -: | -: |
| A1 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 2,150 m e raio 2,260 m | a face interna na mesma altura | 0,141 | +0,141 |
| A1 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,000 m | a face interna plana do topo, em z = 12,802 m | 9,802 | +9,802 |
| A2 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 2,150 m e raio 2,260 m | a face interna na mesma altura | 0,064 | +0,064 |
| A2 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,000 m | a face interna plana do topo, em z = 12,802 m | 9,802 | +9,802 |
| A3 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 3,120 m e raio 2,340 m | a face interna na mesma altura | 0,044 | +0,044 |
| A3 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,970 m | a face interna plana do topo, em z = 12,802 m | 8,832 | +8,832 |
| A4 | radial | a aresta circular de `Escudo termico (PICA)`, em z = 3,120 m e raio 2,340 m | a face interna na mesma altura | 0,016 | −0,016 |
| A4 | axial | o topo de `Nariz do escudo (PICA)`, em z = 3,970 m | a face interna plana do topo, em z = 12,802 m | 8,832 | +8,832 |
| A5 | radial | a face da peça, perto do ponto mais próximo de `Tanque insercao MON-3 1`, em z = 0,564 m e raio 1,959 m | a face interna na mesma altura | 0,361 | +0,361 |
| A5 | axial | o topo de `EES com o conteiner de amostras`, em z = 5,116 m | a face interna plana do topo, em z = 11,348 m | 6,232 | +6,232 |

O valor esperado é a menor distância entre as superfícies, um pouco menor que a folga horizontal onde o envelope é inclinado. O Measure não mostra o sinal (não conferido): uma folga negativa aparece como valor positivo, e quem diz que há interferência é a seção E.

## E. Rodar Check interference

26. Em cada Assembly, use o comando de interferência (Check interference ou o nome equivalente no menu).
27. Só importam os pares que incluem a peça Envelope. Pares entre peças do próprio veículo não são conferidos nesta etapa (P-095).

| Assembly | Esperado com a peça Envelope |
| :- | :- |
| A1 | nenhuma |
| A2 | nenhuma |
| A3 | nenhuma |
| A4 | interferência com `Escudo termico (PICA)`, no ombro |
| A5 | nenhuma |

## F. Anotar

28. Para cada Assembly, anote o valor lido no Measure e o resultado do Check interference.
29. Mande os valores para registro. O estudo compara cada um com o esperado desta página.
