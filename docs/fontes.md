# Fontes primárias

Toda constante ou dado externo usado no código cita uma entrada desta lista no comentário
(`docs/fontes.md [Fn]`). Valores sem fonte vão para `config/premissas.yaml` como NÃO VALIDADA.

| Id | Fonte | Uso no projeto | Acesso |
| :- | :- | :- | :- |
| F1 | Park, R. S.; Folkner, W. M.; Williams, J. G.; Boggs, D. H. *The JPL Planetary and Lunar Ephemerides DE440 and DE441*. The Astronomical Journal, 161:105, 2021. doi:10.3847/1538-3881/abd414 | Efemérides planetárias (`de440.bsp`) | Kernel: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp — MD5 publicado em `aa_checksums.txt` do mesmo diretório |
| F2 | NASA/JPL NAIF. Leapseconds kernel `naif0012.tls` | Conversão UTC ↔ TDB | https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls (sem checksum publicado; MD5 local em `config/kernels.yaml`) |
| F3 | NASA/JPL Solar System Dynamics Group. *Horizons On-Line Ephemeris System*, API v1.2 | Vetores de referência para verificar as efemérides locais | https://ssd.jpl.nasa.gov/api/horizons.api — respostas brutas em `tests/data/horizons/`, com a URL da consulta na 1ª linha. Consultado em 2026-10-26. |
| F4 | Acton, C. H. *Ancillary data services of NASA's Navigation and Ancillary Information Facility*. Planetary and Space Science, 44(1):65–70, 1996. doi:10.1016/0032-0633(95)00107-7 | Toolkit SPICE (CSPICE N0067) | https://naif.jpl.nasa.gov/naif/toolkit.html |
| F5 | Annex, A. M. et al. *SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit*. Journal of Open Source Software, 5(46):2050, 2020. doi:10.21105/joss.02050 | Interface Python para o SPICE (spiceypy 8.3.0) | https://github.com/AndrewAnnex/SpiceyPy |
| F6 | NASA/JPL NAIF. *NAIF Integer ID codes* e *Frames* Required Reading | Códigos de corpos (10, 399, 4) e equivalência J2000/ICRF nos SPKs DE | https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/naif_ids.html, https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/frames.html |

Referências previstas para etapas seguintes (ainda não usadas no código):
Izzo (2015), *Revisiting Lambert's problem*, Celest. Mech. Dyn. Astr. 121:1–15;
Burke, Falck, McGuire (2010), NASA/TM-2010-216764; Drake (ed.) (2009), NASA/SP-2009-566 (DRA 5.0).
