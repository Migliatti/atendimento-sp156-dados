# Data source and license

The data is **not** covered by the MIT license of the code.

- Dataset: "Dados do SP156 - Solicitações", Prefeitura de São Paulo, Portal de Dados Abertos.
- Official page: https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156
- Resource used: "Dados do SP156 - 3º TRI 2026" (requests opened from 2026-07-01 to 2026-09-30).
- License shown on the official page: **Creative Commons CCZero (CC0)**, https://creativecommons.org/publicdomain/zero/1.0/
  (checked on 2026-11-24 through the portal's API, field `license_title`).
- Glossary: "Dicionário dados abertos - SP156 2020 em diante", published on the same page.

`data/sample/sp156_sample.csv` is a random sample of 20,000 rows of that file (fixed seed 42) with only
these columns: opening date, closing date, channel, theme, subject, service, status, organ, subprefecture,
district. Street, number, ZIP code and coordinates were removed. This project is not an official work of
the city hall and has no connection with it.
